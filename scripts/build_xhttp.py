#!/usr/bin/env python3
"""
由有效库(vpngate_tested.csv)生成 vpngate-xhttp.txt —— VLESS + XHTTP 分享链接。

与 vpngate-v2ray.txt 的区别仅在传输层:
  - vpngate-v2ray.txt : VLESS + WebSocket (type=ws)
  - vpngate-xhttp.txt : VLESS + XHTTP, mode=stream-one, 附带 xPadding 混淆 extra

链接模板(除 type/mode/extra 外与 ws 版本一致):
  vless://<uuid>@saas.sin.fan:443?encryption=none&security=tls
    &sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3,h2
    &type=xhttp&host=snip.edgeoneai.cc.cd
    &path=<fdip path>&mode=stream-one&extra=<urlencoded json>
    #vpngate.me | 国家 | 短主机名

环境变量:
  VPNGATE_TESTED_CSV  有效库路径 (默认: 仓库根 vpngate_tested.csv)
  VPNGATE_XHTTP       输出路径   (默认: 仓库根 vpngate-xhttp.txt)

仅使用标准库; 模板常量复用 vpngate-daily.py, 保证与其它订阅同源。
"""

import csv
import importlib.util
import json
import os
import sys
from urllib.parse import quote

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTED_CSV_PATH = os.environ.get("VPNGATE_TESTED_CSV", os.path.join(REPO_ROOT, "vpngate_tested.csv"))
XHTTP_PATH = os.environ.get("VPNGATE_XHTTP", os.path.join(REPO_ROOT, "vpngate-xhttp.txt"))

# XHTTP 传输模式与 extra 混淆参数(用户指定)
XHTTP_MODE = "stream-one"
XHTTP_EXTRA = {
    "xPaddingBytes": "100-500",
    "xPaddingObfsMode": True,
    "xPaddingMethod": "tokenish",
    "xPaddingPlacement": "queryInHeader",
    "xPaddingHeader": "X-Cache",
    "xPaddingKey": "_dc",
}


def load_daily_module():
    path = os.path.join(REPO_ROOT, "vpngate-daily.py")
    spec = importlib.util.spec_from_file_location("vpngate_daily", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_xhttp_link(daily, country, hostname, tcp_port):
    """由 CSV 行字段拼出一条 VLESS+XHTTP 分享链接; 字段缺失返回 None。"""
    country = (country or "").strip()
    hostname = (hostname or "").strip()
    tcp_port = (tcp_port or "").strip()
    if not (country and hostname and tcp_port):
        return None
    path = quote(daily.fdip_path(hostname, tcp_port), safe="")
    name = quote(daily.remark(country, hostname), safe="")
    extra = quote(json.dumps(XHTTP_EXTRA, separators=(",", ":"), ensure_ascii=False), safe="")
    sni = daily.CLASH_SNI
    return (
        f"vless://{daily.VLESS_UUID}@{daily.VLESS_SERVER}"
        "?encryption=none&security=tls"
        f"&sni={sni}&fp=chrome&alpn=h3%2Ch2"
        f"&type=xhttp&host={sni}"
        f"&path={path}&mode={XHTTP_MODE}&extra={extra}"
        f"#{name}"
    )


def main():
    daily = load_daily_module()
    if not os.path.exists(TESTED_CSV_PATH):
        print(f"有效库不存在: {TESTED_CSV_PATH}")
        return 1
    with open(TESTED_CSV_PATH, encoding="utf-8", errors="replace", newline="") as f:
        rows = list(csv.DictReader(f))
    links = []
    for r in rows:
        link = build_xhttp_link(daily, r.get("Country"), r.get("Hostname"), r.get("TCP_Port"))
        if link:
            links.append(link)
    with open(XHTTP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(links) + "\n")
    print(f"vpngate-xhttp.txt 已生成: {len(links)} 条 -> {XHTTP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
