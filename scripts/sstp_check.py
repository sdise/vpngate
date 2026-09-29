#!/usr/bin/env python3
"""
直接对 VPNGate 公共节点做 SSTP 握手, 验证节点是否有效。

与 scripts/test_nodes.py 的区别:
  - 不需要 xray 内核, 不需要 vless 入口 (saas.sin.fan), 只用 Python 标准库;
  - 直接连节点本身 (链接 path 里的 sstp://vpn:vpn@host:port), 验证的是
    "这个 VPNGate 节点还活着", 而不是 "入口 + 节点整条链路可用"。

SSTP 建连过程(与 cf-vpngate/worker.js 的 createSstpClient/establish 完全一致):
  1) TCP 连节点 443(或 TCP_Port) 端口, 外面套一层 TLS(节点用自签证书, 故不校验证书);
  2) 在 TLS 流上发一个"永不结束"的 HTTP 请求:
         SSTP_DUPLEX_POST /sra_{BA195980-CD49-458b-9E23-C84EE0ADCD75}/ HTTP/1.1
         Content-Length: 18446744073709551615
     服务端回 200 之后, 这条 TLS 流就变成了一条全双工的 SSTP 隧道;
  3) 紧接着在同一个流里发 SSTP 控制报文 MSG_CALL_CONNECT_REQUEST(携带封装协议=PPP),
     再发 SSTP 数据报文(载荷是 PPP 帧);
  4) 隧道内跑 PPP 协商:
         LCP  Configure-Request/Ack  ->  链路参数协商 (MRU 1500)
         PAP  Authenticate-Request   ->  用户名/密码固定 vpn / vpn
         IPCP Configure-Request/Nak/Ack -> 服务端分配虚拟 IPv4
     拿到 IPCP 分配的 IP 即认为该节点可用;
  5) 可选 (--tcp): 在 PPP 之上手工构造 IPv4 + TCP 报文, 对目标发起三次握手
     (SYN -> SYN+ACK -> ACK), 证明该节点不仅能握手, 还能真的把流量送出去。

报文格式要点(照搬 worker.js):
  SSTP 头 4 字节: 0x10 | (控制 0x01 / 数据 0x00) | 长度(高 4 位保留位置 0x8)
  数据报文: 头 + FF 03 + PPP 帧 (PPP 帧 = 协议 2 字节 + code/id/长度 + 选项)
  控制报文: 头 + 消息类型 2 字节 + 属性数 2 字节 + 属性(保留 1 + id 1 + 长度 2 + 数据)

用法:
  python3 scripts/sstp_check.py --file vpngate-v2ray.txt
  python3 scripts/sstp_check.py --file vpngate-v2ray.txt --limit 20 --verbose
  python3 scripts/sstp_check.py --link 'vless://...' --tcp --verbose
  python3 scripts/sstp_check.py --csv vpngate.csv --workers 32 --out valid_nodes.txt

退出码恒为 0(统计信息打印在 stdout), 便于在 CI 里自由判断。
"""

import argparse
import csv as csvmod
import ipaddress
import os
import random
import re
import socket
import ssl
import struct
import sys
import time
import urllib.parse
import uuid
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SSTP_PATH = "/sra_{BA195980-CD49-458b-9E23-C84EE0ADCD75}/"
PPP_LCP = 0xC021
PPP_PAP = 0xC023
PPP_IPCP = 0x8021
PPP_IPV4 = 0x0021
SSTP_RE = re.compile(r"sstp://([^@\s]+)@([^:/?#\s]+):(\d+)")
IPV4_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


class SstpError(Exception):
    pass


# --------------------------------------------------------------------------
# 报文构造
# --------------------------------------------------------------------------

def checksum(data):
    """Internet 校验和(IPv4 首部 / TCP 伪首部共用)。"""
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def sstp_data(ppp):
    """SSTP 数据报文: 4 字节头 + FF 03 + PPP 帧。"""
    size = 6 + len(ppp)
    return bytes([0x10, 0x00, ((size >> 8) & 0x0F) | 0x80, size & 0xFF, 0xFF, 0x03]) + ppp


def sstp_control(message_type, attributes=()):
    """SSTP 控制报文: 4 字节头 + 消息类型 + 属性数 + 属性列表。"""
    body = b""
    for attr_id, data in attributes:
        body += bytes([0, attr_id]) + struct.pack(">H", 4 + len(data)) + data
    size = 8 + len(body)
    return (
        bytes([0x10, 0x01])
        + struct.pack(">H", size | 0x8000)
        + struct.pack(">HH", message_type, len(attributes))
        + body
    )


def ppp_frame(protocol, code, ident, options=()):
    """PPP 控制帧(带 code/id/长度的标准 PPP 头)。"""
    body = b""
    for opt_type, data in options:
        body += bytes([opt_type, 2 + len(data)]) + data
    return (
        struct.pack(">H", protocol)
        + bytes([code, ident])
        + struct.pack(">H", 4 + len(body))
        + body
    )


def pap_frame(ident, user, password):
    """PPP PAP Authenticate-Request。"""
    u = user.encode()
    p = password.encode()
    return (
        struct.pack(">H", PPP_PAP)
        + bytes([1, ident])
        + struct.pack(">H", 6 + len(u) + len(p))
        + bytes([len(u)])
        + u
        + bytes([len(p)])
        + p
    )


def find_option(payload, opt_type):
    """在 PPP 选项区里找指定类型的选项, 返回其数据。"""
    i = 0
    while i + 2 <= len(payload):
        t, length = payload[i], payload[i + 1]
        if length < 2 or i + length > len(payload):
            return None
        if t == opt_type:
            return payload[i + 2 : i + length]
        i += length
    return None


# --------------------------------------------------------------------------
# SSTP 客户端
# --------------------------------------------------------------------------

class SstpProbe:
    """最小化 SSTP 客户端: 建链 + PPP 协商 + 可选 TCP 三次握手。"""

    def __init__(self, host, port=443, user="vpn", password="vpn", timeout=15, sni=None):
        self.host = host
        self.port = port
        self.user = user or "vpn"
        self.password = password or "vpn"
        self.timeout = timeout
        self.sni = sni or host
        self.sock = None
        self.buf = b""
        self._id = 0
        self.my_ip = None

    # ---- 基础 IO ----

    def _recv_exact(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise SstpError("eof")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _read_line(self):
        while True:
            index = self.buf.find(b"\n")
            if index >= 0:
                line, self.buf = self.buf[:index], self.buf[index + 1 :]
                return line.decode("latin-1").rstrip("\r")
            chunk = self.sock.recv(65536)
            if not chunk:
                raise SstpError("eof")
            self.buf += chunk

    def next_id(self):
        self._id = (self._id + 1) & 0xFF
        return self._id

    @staticmethod
    def _context(legacy):
        """legacy=True 时放宽到 TLS1.0 + 低安全级别, 兼容老版本 SoftEther。"""
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False          # VPNGate 节点用自签证书
        ctx.verify_mode = ssl.CERT_NONE
        if not legacy:
            return ctx
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                ctx.minimum_version = ssl.TLSVersion.TLSv1
            except Exception:
                pass
            try:
                ctx.set_ciphers("DEFAULT:@SECLEVEL=1")
            except Exception:
                pass
        return ctx

    def connect(self):
        last = None
        for legacy in (False, True):
            raw = socket.create_connection((self.host, self.port), timeout=self.timeout)
            raw.settimeout(self.timeout)
            try:
                self.sock = self._context(legacy).wrap_socket(raw, server_hostname=self.sni)
                return
            except Exception as exc:
                last = exc
                try:
                    raw.close()
                except Exception:
                    pass
                if "timed out" in str(exc) or isinstance(exc, socket.timeout):
                    break                    # 网络不通, 换套件重试没有意义
        raise SstpError("tls: %s" % last)

    def send(self, data):
        self.sock.sendall(data)

    def read_packet(self):
        """读一个 SSTP 报文, 返回 (是否控制报文, 载荷)。"""
        header = self._recv_exact(4)
        length = struct.unpack(">H", header[2:4])[0] & 0x0FFF
        body = self._recv_exact(length - 4) if length > 4 else b""
        return (header[1] & 1) == 1, body

    @staticmethod
    def parse_ppp(data):
        """去掉 FF 03 前缀, 解析 PPP 帧。"""
        offset = 2 if len(data) >= 2 and data[0] == 0xFF and data[1] == 0x03 else 0
        if len(data) - offset < 4:
            return None
        protocol = struct.unpack(">H", data[offset : offset + 2])[0]
        if protocol == PPP_IPV4:
            return {"protocol": protocol, "ip": data[offset + 2 :], "raw": data[offset:]}
        if len(data) - offset < 6:
            return None
        return {
            "protocol": protocol,
            "code": data[offset + 2],
            "id": data[offset + 3],
            "payload": data[offset + 6 :],
            "raw": data[offset:],
        }

    # ---- 建链 ----

    def establish(self):
        request = (
            "SSTP_DUPLEX_POST %s HTTP/1.1\r\n"
            "Host: %s\r\n"
            "Content-Length: 18446744073709551615\r\n"
            "SSTPCORRELATIONID: {%s}\r\n\r\n" % (SSTP_PATH, self.host, uuid.uuid4())
        ).encode()
        mru = struct.pack(">H", 1500)
        self.send(
            request
            + sstp_control(0x0001, [(1, struct.pack(">H", 1))])      # 封装协议 = PPP
            + sstp_data(ppp_frame(PPP_LCP, 1, self.next_id(), [(1, mru)]))
        )

        status = self._read_line()
        while self._read_line():
            pass
        if "200" not in status:
            raise SstpError("http %s" % status.strip())

        lcp_opened = False
        authenticated = False
        my_ip = None

        for _ in range(40):
            ctrl, body = self.read_packet()
            if ctrl:
                continue                       # 控制报文(CONNECT_ACK 等)无需回应
            ppp = self.parse_ppp(body)
            if not ppp:
                continue

            if ppp["protocol"] == PPP_LCP:
                if ppp["code"] == 1:           # Configure-Request -> Configure-Ack
                    ack = bytearray(ppp["raw"])
                    ack[2] = 2
                    if lcp_opened and not authenticated:
                        self.send(sstp_data(bytes(ack)) + sstp_data(pap_frame(self.next_id(), self.user, self.password)))
                        authenticated = True
                    else:
                        self.send(sstp_data(bytes(ack)))
                elif ppp["code"] == 2:         # 链路已开 -> 发 PAP 认证
                    lcp_opened = True
                    if not authenticated:
                        self.send(sstp_data(pap_frame(self.next_id(), self.user, self.password)))
                        authenticated = True

            elif ppp["protocol"] == PPP_PAP:
                if ppp["code"] == 2:           # 认证通过 -> 申请 IPCP 地址
                    self.send(sstp_data(ppp_frame(PPP_IPCP, 1, self.next_id(), [(3, b"\x00\x00\x00\x00")])))
                elif ppp["code"] == 3:
                    raise SstpError("pap rejected")

            elif ppp["protocol"] == PPP_IPCP:
                if ppp["code"] == 1:           # 对方也要地址 -> Ack
                    ack = bytearray(ppp["raw"])
                    ack[2] = 2
                    self.send(sstp_data(bytes(ack)))
                elif ppp["code"] == 3:         # Nak: 采纳对方给的 IP 再请求一次
                    option = find_option(ppp["payload"], 3)
                    if option:
                        self.send(sstp_data(ppp_frame(PPP_IPCP, 1, self.next_id(), [(3, option)])))
                elif ppp["code"] == 2:         # Ack: 拿到虚拟 IP
                    option = find_option(ppp["payload"], 3)
                    if option:
                        my_ip = ".".join(str(b) for b in option)
                        break

        if not my_ip:
            raise SstpError("no ip from ipcp")
        self.my_ip = my_ip
        return my_ip

    # ---- PPP 之上手搓 IPv4/TCP ----

    def _tcp_frame(self, src, dst, sport, dport, seq, ack, flags, payload=b""):
        tcp = (
            struct.pack(">HHIIBBHHH", sport, dport, seq, ack, 0x50, flags, 65535, 0, 0) + payload
        )
        ip_len = 20 + len(tcp)
        ip = (
            struct.pack(">BBHHHBBH", 0x45, 0, ip_len, random.randint(0, 65535), 0x4000, 64, 6, 0)
            + src
            + dst
        )
        ip = ip[:10] + struct.pack(">H", checksum(ip)) + ip[12:]
        pseudo = src + dst + bytes([0, 6]) + struct.pack(">H", len(tcp))
        tcp = tcp[:16] + struct.pack(">H", checksum(pseudo + tcp)) + tcp[18:]
        return sstp_data(struct.pack(">H", PPP_IPV4) + ip + tcp)

    def tcp_handshake(self, target_ip, target_port, rounds=40):
        """经 SSTP/PPP 隧道对 target_ip:target_port 完成三次握手。"""
        src = socket.inet_aton(self.my_ip)
        dst = socket.inet_aton(target_ip)
        sport = random.randint(10000, 60000)
        seq = random.randint(0, 0xFFFFFFFF)

        self.send(self._tcp_frame(src, dst, sport, target_port, seq, 0, 0x02))  # SYN
        seq = (seq + 1) & 0xFFFFFFFF

        for _ in range(rounds):
            ctrl, body = self.read_packet()
            if ctrl:
                continue
            ppp = self.parse_ppp(body)
            if not ppp or ppp["protocol"] != PPP_IPV4:
                continue
            ip = ppp["ip"]
            if len(ip) < 40 or ip[9] != 6:
                continue
            ihl = (ip[0] & 0x0F) * 4
            if struct.unpack(">H", ip[ihl : ihl + 2])[0] != target_port:
                continue
            if struct.unpack(">H", ip[ihl + 2 : ihl + 4])[0] != sport:
                continue
            flags = ip[ihl + 13]
            if flags & 0x12 != 0x12:           # 只要 SYN+ACK
                continue
            their_seq = struct.unpack(">I", ip[ihl + 4 : ihl + 8])[0]
            ack = (their_seq + 1) & 0xFFFFFFFF
            self.send(self._tcp_frame(src, dst, sport, target_port, seq, ack, 0x10))  # ACK
            return True
        return False

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


# --------------------------------------------------------------------------
# 目标解析
# --------------------------------------------------------------------------

class Node:
    __slots__ = ("host", "port", "user", "password", "label", "link")

    def __init__(self, host, port, user="vpn", password="vpn", label="", link=""):
        self.host = host
        self.port = int(port)
        self.user = user or "vpn"
        self.password = password or "vpn"
        self.label = label or "%s:%s" % (host, port)
        self.link = link

    def __repr__(self):
        return "<Node %s>" % self.label


def node_from_sstp(value):
    """从 sstp://user:pass@host:port 解析。"""
    m = SSTP_RE.search(value)
    if not m:
        return None
    user, _, password = m.group(1).partition(":")
    return Node(m.group(2), m.group(3), user, password or "vpn", label="%s:%s" % (m.group(2), m.group(3)))


def nodes_from_lines(lines):
    """支持 vless:// 链接 / sstp:// / host:port 三种输入。"""
    nodes = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("vless://"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(line).query)
            path = (query.get("path") or [""])[0]
            m = SSTP_RE.search(path)
            if not m:
                continue
            node = node_from_sstp(m.group(0))
            fragment = urllib.parse.unquote(urllib.parse.urlparse(line).fragment or "")
            node.label = fragment or node.label
            node.link = line
            nodes.append(node)
        elif line.startswith("sstp://"):
            node = node_from_sstp(line)
            if node:
                node.link = line
                nodes.append(node)
        elif re.match(r"^[\w.\-]+:\d+$", line):
            host, port = line.rsplit(":", 1)
            nodes.append(Node(host, port))
    return nodes


def nodes_from_csv(path, limit=None):
    """: 从 vpngate.csv 读取 (列: Country,Hostname,IP,Speed_Mbps,TCP_Port)。"""
    nodes = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csvmod.DictReader(f):
            host = (row.get("Hostname") or row.get("IP") or "").strip()
            port = (row.get("TCP_Port") or "").strip()
            if not host or not port.isdigit():
                continue
            node = Node(host, port)
            node.label = "%s (%s)" % (host, (row.get("Country") or "").strip())
            nodes.append(node)
            if limit and len(nodes) >= limit:
                break
    return nodes


# --------------------------------------------------------------------------
# 检测
# --------------------------------------------------------------------------

def check_node(node, timeout, tcp_target=None, sni=None):
    probe = SstpProbe(node.host, node.port, node.user, node.password, timeout, sni)
    started = time.time()
    try:
        probe.connect()
        ip = probe.establish()
        detail = "ip=%s" % ip
        if tcp_target:
            host, port = tcp_target
            target_ip = host if IPV4_RE.match(host) else socket.gethostbyname(host)
            if not probe.tcp_handshake(target_ip, port):
                raise SstpError("tcp handshake timeout (%s:%s)" % (host, port))
            detail += " tcp=ok"
        return node, True, "%s %.1fs" % (detail, time.time() - started)
    except Exception as exc:
        return node, False, "%s: %s" % (type(exc).__name__, exc)
    finally:
        probe.close()


def main():
    parser = argparse.ArgumentParser(description="用 SSTP 握手验证 VPNGate 节点有效性(无需 xray)")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--file", help="链接文件 (vpngate-v2ray.txt / vpngate.txt / sstp:// 列表)")
    src.add_argument("--link", help="单条 vless:// 或 sstp:// 链接")
    src.add_argument("--csv", help="vpngate.csv (用 Hostname + TCP_Port)")
    parser.add_argument("--workers", type=int, default=16, help="并发数 (默认 16)")
    parser.add_argument("--timeout", type=int, default=15, help="单节点超时秒数 (默认 15)")
    parser.add_argument("--limit", type=int, help="只测前 N 个")
    parser.add_argument("--tcp", metavar="HOST:PORT", help="额外验证: 经隧道对 HOST:PORT 完成 TCP 三次握手")
    parser.add_argument("--user", default="vpn", help="PAP 用户名 (默认 vpn)")
    parser.add_argument("--password", default="vpn", help="PAP 密码 (默认 vpn)")
    parser.add_argument("--sni", help="TLS SNI (默认用节点域名)")
    parser.add_argument("--out", help="把有效节点写入该文件(原链接, 无链接则写 sstp://)")
    parser.add_argument("--verbose", action="store_true", help="逐条打印结果")
    args = parser.parse_args()

    if args.csv:
        nodes = nodes_from_csv(args.csv, args.limit)
        source = args.csv
    elif args.link:
        nodes = nodes_from_lines([args.link])
        source = "命令行链接"
    elif args.file:
        with open(args.file, encoding="utf-8") as f:
            nodes = nodes_from_lines(f.readlines())
        if args.limit:
            nodes = nodes[: args.limit]
        source = args.file
    else:
        parser.error("需要 --file / --link / --csv 之一")
        return 2

    if not nodes:
        print("没有解析到任何节点")
        return 0

    tcp_target = None
    if args.tcp:
        host, _, port = args.tcp.rpartition(":")
        tcp_target = (host, int(port or 80))

    print("待测节点: %d (来源 %s)%s" % (len(nodes), source, ", 含 TCP 出网验证" if tcp_target else ""))

    valid, invalid = [], []
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(check_node, n, args.timeout, tcp_target, args.sni): n for n in nodes}
        for fut in as_completed(futures):
            node, ok, detail = fut.result()
            (valid if ok else invalid).append((node, detail))
            done += 1
            if args.verbose:
                print("[%s] %-46s %s" % ("OK " if ok else "BAD", node.label, detail), flush=True)
            elif done % 50 == 0 or done == len(nodes):
                print("进度 %d/%d: 有效 %d, 无效 %d" % (done, len(nodes), len(valid), len(invalid)), flush=True)

    ratio = len(valid) / len(nodes)
    print("有效: %d, 无效: %d, 有效比例: %.1f%%" % (len(valid), len(invalid), ratio * 100))
    for node, detail in invalid[:20]:
        print("  - 无效 %s (%s)" % (node.label, detail))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for node, _ in valid:
                f.write((node.link or "sstp://%s:%s@%s:%d" % (node.user, node.password, node.host, node.port)) + "\n")
        print("有效节点已写入: %s (%d 条)" % (args.out, len(valid)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
