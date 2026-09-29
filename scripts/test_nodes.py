#!/usr/bin/env python3
"""
用 xray 逐个测试 vpngate.csv 中节点的 VLESS 链接有效性。

流程:
1. 从 vpngate.txt 读取待测 VLESS 链接(该文件由每小时任务从原始库生成)。
2. 解析每条链接,取出 uuid / 入口地址端口 / tls 与 ws 参数;
   为每条链接生成一份最小 xray 配置 (socks 入站 + vless 出站),
   启动 xray 后经 SOCKS5 请求检测 URL, 返回 2xx/3xx 即判定有效。
3. 有效节点对应行写入 vpngate_tested.csv(全量重写);
   **不修改 vpngate.csv** —— 防止因网络波动误删原始数据。
4. 由 vpngate_tested.csv 重建订阅文件:
   vpngate-v2ray.txt (v2rayN) 与 vpngate-clash.yaml (Clash)。

安全护栏:
- 先 TCP 探测入口地址 (saas.sin.fan:443); 不可达则直接中止, 不写任何文件。
- 若有效链接比例低于 MIN_VALID_RATIO (默认 20%), 判定为系统性故障
  (入口异常而非节点失效), 中止, 不写任何文件。

环境变量:
  VPNGATE_CSV         原始库路径 (默认: 仓库根目录 vpngate.csv)
  VPNGATE_TXT         待测链接列表 (默认: 仓库根目录 vpngate.txt)
  VPNGATE_TESTED_CSV  有效库路径 (默认: 仓库根目录 vpngate_tested.csv)
  VPNGATE_V2RAY       v2rayN 订阅路径 (默认: 仓库根目录 vpngate-v2ray.txt)
  VPNGATE_CLASH       Clash 订阅路径 (默认: 仓库根目录 vpngate-clash.yaml)
  XRAY_BIN            xray 可执行文件 (默认: xray)
  CURL_BIN            curl 可执行文件 (默认: curl)
  TEST_URL            检测目标 (默认: https://www.google.com/generate_204)
  TEST_TIMEOUT        单次检测超时秒数 (默认 15)
  TEST_WORKERS        并发数 (默认 24)
  MIN_VALID_RATIO     最低有效比例阈值 (默认 0.2)
  FORCE_GLOBAL        是否在 path 后追加 global=1 强制入口走 sstp 落地 (默认 1, 必须开启)

仅使用 Python 标准库; xray 与 curl 由运行环境提供。
"""

import csv
import importlib.util
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.environ.get("VPNGATE_CSV", os.path.join(REPO_ROOT, "vpngate.csv"))
TXT_PATH = os.environ.get("VPNGATE_TXT", os.path.join(REPO_ROOT, "vpngate.txt"))
TESTED_CSV_PATH = os.environ.get("VPNGATE_TESTED_CSV", os.path.join(REPO_ROOT, "vpngate_tested.csv"))
V2RAY_PATH = os.environ.get("VPNGATE_V2RAY", os.path.join(REPO_ROOT, "vpngate-v2ray.txt"))
CLASH_PATH = os.environ.get("VPNGATE_CLASH", os.path.join(REPO_ROOT, "vpngate-clash.yaml"))
XRAY_BIN = os.environ.get("XRAY_BIN", "xray")
CURL_BIN = os.environ.get("CURL_BIN", "curl")
TEST_URL = os.environ.get("TEST_URL", "https://www.google.com/generate_204")
TIMEOUT = int(os.environ.get("TEST_TIMEOUT", "15"))
WORKERS = int(os.environ.get("TEST_WORKERS", "24"))
MIN_VALID_RATIO = float(os.environ.get("MIN_VALID_RATIO", "0.2"))
# 强制入口走 sstp 落地(不加的话入口会直连目标, 测不到节点)
FORCE_GLOBAL = os.environ.get("FORCE_GLOBAL", "1") not in ("0", "", "false", "False")


def parse_link(link):
    """解析 vless 链接, 返回 dict; 解析失败返回 None。"""
    try:
        u = urllib.parse.urlparse(link.strip())
    except Exception:
        return None
    if u.scheme != "vless" or not u.username or not u.hostname:
        return None
    q = urllib.parse.parse_qs(u.query)

    def one(k, d=""):
        v = q.get(k)
        return v[0] if v else d

    path = one("path")
    m = re.search(r"sstp://[^@\s]+@([^:/?#\s]+):(\d+)", path)
    if not m:
        return None
    alpn_raw = one("alpn", "h2,http/1.1")
    return {
        "uuid": u.username,
        "address": u.hostname,
        "port": u.port or 443,
        "security": one("security", "none"),
        "sni": one("sni") or u.hostname,
        "fp": one("fp", "chrome"),
        "alpn": [a for a in alpn_raw.split(",") if a],
        "net": one("type", "ws"),
        "host": one("host") or one("sni") or u.hostname,
        "path": path,
        "node_host": m.group(1),
        "node_port": int(m.group(2)),
    }


def build_xray_config(info, socks_port):
    # 入口默认会先尝试直连目标, 只有直连失败才回落到 sstp 节点(见 cf-vpngate/worker.js
    # 的 dialOutbound)。google.com:443 从入口处必然直连成功, 那样测出来的是入口而不是
    # 节点, 会出现"100% 有效"的假象。在 path 后追加 global=1 强制入口走落地,
    # 才能真正检验节点本身。
    path = info["path"]
    if FORCE_GLOBAL:
        path += ("&" if "?" in path else "?") + "global=1"
    stream = {"network": info["net"]}
    if info["security"] == "tls":
        stream["security"] = "tls"
        stream["tlsSettings"] = {
            "serverName": info["sni"],
            "fingerprint": info["fp"],
            "alpn": info["alpn"],
        }
    if info["net"] == "ws":
        stream["wsSettings"] = {"path": path, "headers": {"Host": info["host"]}}
    return {
        "log": {"loglevel": "warning"},
        "inbounds": [
            {
                "port": socks_port,
                "listen": "127.0.0.1",
                "protocol": "socks",
                "settings": {"udp": False},
            }
        ],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": info["address"],
                            "port": info["port"],
                            "users": [{"id": info["uuid"], "encryption": "none"}],
                        }
                    ]
                },
                "streamSettings": stream,
            }
        ],
    }


def free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def wait_port(host, port, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def test_one(link):
    info = parse_link(link)
    if not info:
        return (link, False, "link-parse-fail")
    port = free_port()
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(build_xray_config(info, port), tmp)
    tmp.close()
    proc = subprocess.Popen(
        [XRAY_BIN, "-c", tmp.name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        if not wait_port("127.0.0.1", port):
            return (link, False, "xray-not-ready")
        r = subprocess.run(
            [
                CURL_BIN, "-s", "-o", "/dev/null", "-w", "%{http_code}",
                "--socks5-hostname", f"127.0.0.1:{port}",
                "--max-time", str(TIMEOUT), TEST_URL,
            ],
            capture_output=True, text=True, timeout=TIMEOUT + 15,
        )
        code = (r.stdout or "").strip()
        ok = r.returncode == 0 and len(code) == 3 and code[0] in "23"
        return (link, ok, code if code else f"curl-rc={r.returncode}")
    except Exception as e:  # noqa: BLE001
        return (link, False, f"error:{e}")
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            proc.kill()
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


def load_daily_module():
    path = os.path.join(REPO_ROOT, "vpngate-daily.py")
    spec = importlib.util.spec_from_file_location("vpngate_daily", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    daily = load_daily_module()

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    print(f"原始库共 {len(rows)} 行", flush=True)
    host_to_row = {}
    for r in rows:
        h = (r.get("Hostname") or "").strip()
        if h:
            host_to_row[h] = r

    # 检测链接从 vpngate.txt 读取(由每小时任务从原始库生成)
    with open(TXT_PATH, encoding="utf-8") as f:
        links = [ln.strip() for ln in f if ln.strip().startswith("vless://")]
    print(f"待测链接: {len(links)} (来源 {TXT_PATH})", flush=True)
    if not links:
        print("无可测链接, 退出", flush=True)
        return 0

    # 安全护栏 1: 先确认入口地址可达, 入口故障时直接中止, 不写任何文件
    first = parse_link(links[0])
    if not first:
        print("SAFETY ABORT: 首条链接解析失败, 中止检测", flush=True)
        return 0
    try:
        with socket.create_connection((first["address"], first["port"]), timeout=10):
            print(f"入口可达: {first['address']}:{first['port']}", flush=True)
    except OSError as e:
        print(
            f"SAFETY ABORT: 入口 {first['address']}:{first['port']} 不可达 ({e}), "
            "疑似入口故障, 中止检测, 不写任何文件",
            flush=True,
        )
        return 0

    valid, invalid = [], []
    done = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(test_one, ln): ln for ln in links}
        for fut in as_completed(futs):
            link, ok, detail = fut.result()
            (valid if ok else invalid).append((link, detail))
            done += 1
            if done % 100 == 0 or done == len(links):
                print(
                    f"进度 {done}/{len(links)}: 有效 {len(valid)}, 无效 {len(invalid)}",
                    flush=True,
                )

    # 安全护栏 2: 有效比例过低视为系统性故障, 中止, 不写任何文件
    ratio = len(valid) / len(links)
    print(f"有效: {len(valid)}, 无效: {len(invalid)}, 有效比例: {ratio:.1%}", flush=True)
    if ratio < MIN_VALID_RATIO:
        print(
            f"SAFETY ABORT: 有效比例 {ratio:.1%} 低于阈值 {MIN_VALID_RATIO:.0%}, "
            "疑似系统性故障, 中止, 不写任何文件",
            flush=True,
        )
        return 0

    # 写入有效库(全量重写); 原始库 vpngate.csv 不做任何修改
    kept, missing = [], 0
    for link, _ in valid:
        info = parse_link(link)
        row = host_to_row.get(info["node_host"]) if info else None
        if row is None:
            missing += 1
            continue
        kept.append(row)
    if missing:
        print(f"警告: {missing} 条有效链接在原始库中找不到对应行, 已跳过", flush=True)
    with open(TESTED_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(kept)
    print(f"有效库已写入: {TESTED_CSV_PATH} ({len(kept)} 行)", flush=True)

    # 由有效库重建订阅文件
    n_v2ray, n_clash = daily.rebuild_subscriptions(TESTED_CSV_PATH)
    print(f"订阅已重建: v2rayN {n_v2ray} 条 -> {V2RAY_PATH}", flush=True)
    print(f"订阅已重建: Clash {n_clash} 个 -> {CLASH_PATH}", flush=True)
    for link, detail in invalid[:20]:
        info = parse_link(link)
        host = info["node_host"] if info else "?"
        print(f"  - 无效 {host} ({detail})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
