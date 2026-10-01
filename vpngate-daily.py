#!/usr/bin/env python3
"""
VPNGate 每小时增量抓取脚本
==========================
复现 /home/hatch/vpsgate.md 的数据流程,每小时执行一次:

1. 获取: 从 http://www.vpngate.net/api/iphone/ (VPNGate 官方 CSV 接口,
   与 vpsgate.md 提到的页面底部 CSV 下载入口同源) 拉取实时中继列表。
2. 提取: HostName / IP / Speed(bps) / CountryLong, 并从 OpenVPN 配置
   (base64 解码) 中解析 `proto tcp` 对应的 `remote <ip> <port>` TCP 端口。
3. 处理: 只保留带 TCP 端口的中继(与 vpsgate.md 的"只保留 TCP"一致);
   Speed(bps)/1e6 转为 Mbps 并保留两位小数;
   Hostname 统一为 `<HostName>.opengw.net` 的 DDNS 形式。
4. 增量写入: 以 Hostname 为键与 vpngate.csv 比对,
   只追加新节点,已存在的直接忽略。

数据分层:
- vpngate.csv: 原始累计库,只增不减(每周由有效库覆盖清理一次)。
- vpngate.txt: 原始库的全量 VLESS 链接列表(每行一条),每小时重建; 每日检测的输入。
- vpngate_tested.csv: 有效节点库,由 scripts/test_nodes.py 每日实测后重写;
  比原始库多三列 IsResidential / FraudScore / ExitIP(经节点请求
  https://my.ippure.com/v1/info 得到, 见 IPINFO_FIELDS)。
- vpngate-v2ray.txt / vpngate-clash.yaml: 订阅文件,始终由有效库生成。

备注(客户端里显示的节点名)规则见 remark():
- 有效库行且 ippure 三个字段齐全: `家宽|纯净度:{fraudScore}|{Country}|{Speed_Mbps}|落地:{ip}`
- 其余情况(无返回 / 返回异常 / 关键参数缺失): `{Country}|{Speed_Mbps}`

仅使用标准库,无第三方依赖,容器重置后可直接运行。
日志: vpngate-fetch.log
"""

import base64
import csv
import datetime
import os
import re
import sys
from urllib.parse import quote

API_URL = "http://www.vpngate.net/api/iphone/"
HEADER = ["Country", "Hostname", "IP", "Speed_Mbps", "TCP_Port"]
TIMEOUT = 60


def _default_in_csv_dir(name):
    base = os.path.dirname(os.environ.get("VPNGATE_CSV", "/home/hatch/vpngate.csv")) or "."
    return os.path.join(base, name)


# 路径支持环境变量覆盖(供 GitHub Actions 在仓库目录内运行时使用)
CSV_PATH = os.environ.get("VPNGATE_CSV", "/home/hatch/vpngate.csv")
TESTED_CSV_PATH = os.environ.get("VPNGATE_TESTED_CSV", _default_in_csv_dir("vpngate_tested.csv"))
LOG_PATH = os.environ.get("VPNGATE_LOG", _default_in_csv_dir("vpngate-fetch.log"))
V2RAY_PATH = os.environ.get("VPNGATE_V2RAY", _default_in_csv_dir("vpngate-v2ray.txt"))
CLASH_PATH = os.environ.get("VPNGATE_CLASH", _default_in_csv_dir("vpngate-clash.yaml"))
TXT_PATH = os.environ.get("VPNGATE_TXT", _default_in_csv_dir("vpngate.txt"))

# v2rayN 分享链接模板(见用户 2026-09-26 提供的模板链接;
# 2026-09-27 起入口地址由 61.172.182.19 改为 saas.sin.fan)
VLESS_UUID = "495c7195-85b8-498a-bf20-2ea9ce9175b5"
VLESS_SERVER = "saas.sin.fan:443"
VLESS_BASE = (
    f"vless://{VLESS_UUID}@{VLESS_SERVER}"
    "?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd"
    "&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path="
)

# Clash 订阅固定参数(与 VLESS 模板同源)
CLASH_SNI = "snip.edgeoneai.cc.cd"


def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def fetch_api():
    import urllib.request

    req = urllib.request.Request(
        API_URL, headers={"User-Agent": "Mozilla/5.0 (vpngate-daily/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_rows(text):
    """解析 API CSV, 返回 [(Country, Hostname, IP, Speed_Mbps, TCP_Port)]."""
    nodes = []
    reader = csv.reader(text.splitlines())
    for r in reader:
        if not r or r[0].startswith("*") or r[0].startswith("#"):
            continue
        if len(r) < 15:
            continue
        short_host, ip, _score, _ping, speed_raw, country = r[0], r[1], r[2], r[3], r[4], r[5]
        try:
            cfg = base64.b64decode(r[14]).decode("utf-8", errors="replace")
        except Exception:
            continue
        protos = set(re.findall(r"^proto\s+(\S+)", cfg, re.M))
        ports = re.findall(r"^remote\s+\S+\s+(\d+)", cfg, re.M)
        if "tcp" not in protos or not ports:
            continue  # 无 TCP 入口: 与 vpsgate.md 过滤规则一致,丢弃
        try:
            mbps = f"{int(speed_raw) / 1_000_000:.2f}"
        except ValueError:
            continue
        hostname = f"{short_host}.opengw.net"
        nodes.append((country.strip(), hostname, ip.strip(), mbps, ports[0]))
    # 去重(同一 Hostname 只保留一次) + 排序: Country 升序, Speed 降序
    seen = set()
    uniq = []
    for n in nodes:
        if n[1] not in seen:
            seen.add(n[1])
            uniq.append(n)
    uniq.sort(key=lambda n: (n[0].lower(), -float(n[3])))
    return uniq


def load_existing():
    """读取现有 CSV 的 Hostname 集合;文件不存在则创建并写入表头."""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(HEADER)
        return set()
    hostnames = set()
    with open(CSV_PATH, encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            h = (row.get("Hostname") or "").strip()
            if h:
                hostnames.add(h)
    return hostnames


def short_hostname(hostname):
    return hostname[: -len(".opengw.net")] if hostname.endswith(".opengw.net") else hostname


def fdip_path(hostname, tcp_port):
    """/fdip=sstp://vpn:vpn@{hostname}:{tcp_port}?ed=2560 (URL 编码前原文)."""
    return f"/fdip=sstp://vpn:vpn@{hostname}:{tcp_port}?ed=2560"


# ---------------------------------------------------------------------------
# 备注(客户端里显示的节点名)
# ---------------------------------------------------------------------------
# 有效库(vpngate_tested.csv)里额外保存由 scripts/test_nodes.py 经节点请求
# https://my.ippure.com/v1/info 得到的三个字段; 原始库(vpngate.csv)没有这些列。
IPINFO_FIELDS = ["IsResidential", "FraudScore", "ExitIP"]


def residential_kind(value):
    """IsResidential 单元格 -> 家宽 / 机房; 无法判定时返回空串。"""
    v = str(value if value is not None else "").strip().lower()
    if v in ("true", "1", "yes", "y"):
        return "家宽"
    if v in ("false", "0", "no", "n"):
        return "机房"
    return ""


def _as_row(row_or_country, hostname=None, tcp_port=None):
    """兼容两种调用方式:

    - ``build_xxx(row)`` —— 推荐, row 为 csv.DictReader 的一行;
    - ``build_xxx(country, hostname, tcp_port)`` —— 旧签名, 继续支持。
    """
    if isinstance(row_or_country, dict):
        return row_or_country
    return {"Country": row_or_country, "Hostname": hostname, "TCP_Port": tcp_port}


def remark(row, hostname=None, tcp_port=None):
    """生成节点备注。

    有 ippure 检测数据(家宽/机房、纯净度、落地 IP 齐全)时:
        ``家宽|纯净度:7|Japan|241.51|落地:219.100.37.15``
    否则(无返回 / 返回异常 / 关键参数缺失, 例如触发人机验证时)回退为:
        ``Japan|241.51``
    """
    r = _as_row(row, hostname, tcp_port)
    country = (r.get("Country") or "").strip()
    host = (r.get("Hostname") or "").strip()
    speed = (r.get("Speed_Mbps") or "").strip()
    kind = residential_kind(r.get("IsResidential"))
    score = str(r.get("FraudScore") if r.get("FraudScore") is not None else "").strip()
    exit_ip = (r.get("ExitIP") or "").strip()

    if kind and score and exit_ip and country and speed:
        return f"{kind}|纯净度:{score}|{country}|{speed}|落地:{exit_ip}"
    if country and speed:
        return f"{country}|{speed}"
    # 极端兜底: 关键字段缺失时也不要生成空备注
    return country or short_hostname(host) or host or "vpngate"


def build_vless_link(row, hostname=None, tcp_port=None):
    """由 CSV 行字段拼出一条 v2rayN 分享链接;字段缺失返回 None。"""
    r = _as_row(row, hostname, tcp_port)
    country = (r.get("Country") or "").strip()
    host = (r.get("Hostname") or "").strip()
    port = str(r.get("TCP_Port") if r.get("TCP_Port") is not None else "").strip()
    if not (country and host and port):
        return None
    path = quote(fdip_path(host, port), safe="")
    name = quote(remark(r), safe="")
    return f"{VLESS_BASE}{path}#{name}"


def build_clash_proxy(row, hostname=None, tcp_port=None):
    """由 CSV 行字段拼出一个 Clash proxy 节点 dict;字段缺失返回 None。"""
    r = _as_row(row, hostname, tcp_port)
    country = (r.get("Country") or "").strip()
    host = (r.get("Hostname") or "").strip()
    port = str(r.get("TCP_Port") if r.get("TCP_Port") is not None else "").strip()
    if not (country and host and port):
        return None
    return {
        "name": remark(r),
        "type": "vless",
        "server": VLESS_SERVER.split(":")[0],
        "port": int(VLESS_SERVER.split(":")[1]),
        "uuid": VLESS_UUID,
        "network": "ws",
        "tls": True,
        "udp": False,
        "sni": CLASH_SNI,
        "fingerprint": "chrome",
        "alpn": ["h3", "h2"],
        "ws-opts": {
            "path": fdip_path(host, port),
            "headers": {"Host": CLASH_SNI},
        },
    }


def read_rows(csv_path):
    with open(csv_path, encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def rebuild_v2ray_links(csv_path=None, out_path=None):
    """根据指定 CSV 全量重建 v2rayN 分享链接文件(每行一条)."""
    csv_path = csv_path or CSV_PATH
    out_path = out_path or V2RAY_PATH
    links = []
    for r in read_rows(csv_path):
        link = build_vless_link(r)
        if link:
            links.append(link)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(links) + "\n")
    return len(links)


def rebuild_clash_subscription(csv_path=None, out_path=None):
    """根据指定 CSV 全量重建 Clash 订阅文件(YAML,可直接作为订阅链接)."""
    import yaml  # 延迟导入: 每小时抓取任务保持零第三方依赖

    csv_path = csv_path or CSV_PATH
    out_path = out_path or CLASH_PATH
    proxies = []
    used_names = set()
    for r in read_rows(csv_path):
        p = build_clash_proxy(r)
        if not p:
            continue
        # Clash 要求 proxy 名字唯一; 新备注格式只含 国家+速度+落地 IP,
        # 同一出口 IP 的多个 Hostname 可能撞名, 这里按需补短主机名 / 序号。
        if p["name"] in used_names:
            short = short_hostname((r.get("Hostname") or "").strip())
            base = f"{p['name']}|{short}" if short else p["name"]
            candidate = base
            i = 2
            while candidate in used_names:
                candidate = f"{base}#{i}"
                i += 1
            p["name"] = candidate
        used_names.add(p["name"])
        proxies.append(p)
    names = [p["name"] for p in proxies]
    config = {
        "proxies": proxies,
        "proxy-groups": [
            {"name": "vpngate-手动选择", "type": "select", "proxies": names},
        ],
        "rules": ["MATCH,vpngate-手动选择"],
    }
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = (
        "# vpngate Clash 订阅,由 vpngate-daily.py 自动生成\n"
        f"# 更新时间: {ts}\n"
        f"# 有效节点数: {len(proxies)}\n"
        "# 项目: https://github.com/sdise/vpngate\n"
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)
    return len(proxies)


def rebuild_subscriptions(csv_path=None):
    """由指定 CSV 重建全部订阅文件(v2rayN txt + Clash),返回 (v2ray数, clash数)."""
    return rebuild_v2ray_links(csv_path), rebuild_clash_subscription(csv_path)


def main():
    log("开始抓取 VPNGate 数据")
    try:
        text = fetch_api()
    except Exception as e:
        log(f"抓取失败: {e}")
        return 1
    nodes = parse_rows(text)
    log(f"API 返回 {len(nodes)} 个 TCP 中继")
    if not nodes:
        log("解析结果为空,跳过写入")
        return 1

    existing = load_existing()
    log(f"vpngate.csv 现有 {len(existing)} 个 Hostname")
    new_nodes = [n for n in nodes if n[1] not in existing]
    skipped = len(nodes) - len(new_nodes)

    if new_nodes:
        with open(CSV_PATH, "a", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(new_nodes)
        log(f"新增 {len(new_nodes)} 个节点,忽略已存在 {skipped} 个")
        for n in new_nodes[:10]:
            log(f"  + {n[1]} ({n[0]}, {n[3]} Mbps, TCP:{n[4]})")
        if len(new_nodes) > 10:
            log(f"  ... 另有 {len(new_nodes) - 10} 个未列出")
    else:
        log(f"无新节点,忽略已存在 {skipped} 个")

    n_txt = rebuild_v2ray_links(CSV_PATH, TXT_PATH)
    log(f"vpngate.txt 已重建: {n_txt} 条")

    log("完成")
    return 0


if __name__ == "__main__":
    sys.exit(main())
