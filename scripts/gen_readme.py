#!/usr/bin/env python3
"""
把节点统计写回 README.md 的自动区块。

区块(用 HTML 注释标记, 手工编辑时不要改动标记行):
  <!-- BEGIN:TOTAL  --> ... <!-- END:TOTAL  -->   原始库总节点统计(update.yml 更新)
  <!-- BEGIN:TESTED --> ... <!-- END:TESTED -->   有效节点统计 + 各国最快链接(test.yml 更新)

用法:
  python scripts/gen_readme.py --mode total    # 更新总节点区块
  python scripts/gen_readme.py --mode tested   # 更新有效节点区块
  python scripts/gen_readme.py --mode both     # 两个都更新(默认)

环境变量:
  VPNGATE_CSV         原始库路径 (默认: 仓库根 vpngate.csv)
  VPNGATE_TESTED_CSV  有效库路径 (默认: 仓库根 vpngate_tested.csv)
  README_PATH         README 路径 (默认: 仓库根 README.md)
  TOP_PER_COUNTRY     每个国家展示的链接数 (默认 5, 有效数 <= 该值时全部展示)

仅使用标准库; 链接生成复用 vpngate-daily.py 的 build_vless_link, 保证与订阅一致。
"""

import argparse
import csv
import datetime
import importlib.util
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.environ.get("VPNGATE_CSV", os.path.join(REPO_ROOT, "vpngate.csv"))
TESTED_CSV_PATH = os.environ.get("VPNGATE_TESTED_CSV", os.path.join(REPO_ROOT, "vpngate_tested.csv"))
README_PATH = os.environ.get("README_PATH", os.path.join(REPO_ROOT, "README.md"))
TOP_PER_COUNTRY = int(os.environ.get("TOP_PER_COUNTRY", "5"))

TOTAL_BEGIN, TOTAL_END = "<!-- BEGIN:TOTAL -->", "<!-- END:TOTAL -->"
TESTED_BEGIN, TESTED_END = "<!-- BEGIN:TESTED -->", "<!-- END:TESTED -->"


def load_daily_module():
    path = os.path.join(REPO_ROOT, "vpngate-daily.py")
    spec = importlib.util.spec_from_file_location("vpngate_daily", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def read_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        return [r for r in csv.DictReader(f) if (r.get("Hostname") or "").strip()]


def speed_of(row):
    try:
        return float((row.get("Speed_Mbps") or "0").strip())
    except ValueError:
        return 0.0


def country_of(row):
    return (row.get("Country") or "").strip() or "Unknown"


def anchor(country):
    return re.sub(r"[^a-z0-9]+", "-", country.lower()).strip("-") or "unknown"


def build_total_block():
    """原始库总节点统计(仅摘要: 更新时间 / 累计节点数 / 覆盖国家数, 不含明细表)。"""
    rows = read_rows(CSV_PATH)
    if not rows:
        return None
    countries = {country_of(r) for r in rows}
    return (
        f"> 更新时间：{utcnow()} ｜ 原始库累计 **{len(rows)}** 个节点，"
        f"覆盖 **{len(countries)}** 个国家/地区"
    )


def build_tested_block(daily):
    """有效节点统计 + 各国最快的 TOP 链接。"""
    rows = read_rows(TESTED_CSV_PATH)
    if not rows:
        return None
    groups = {}
    for r in rows:
        groups.setdefault(country_of(r), []).append(r)
    order = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))
    avg = sum(speed_of(r) for r in rows) / len(rows)

    lines = [
        f"> 检测时间：{utcnow()} ｜ 实测有效 **{len(rows)}** 个节点，"
        f"覆盖 **{len(groups)}** 个国家/地区，平均速度 **{avg:.0f} Mbps**",
        "",
        "#### 各国有效节点数",
        "",
        "| 国家/地区 | 有效节点 | 平均速度 | 最高速度 |",
        "|---|---:|---:|---:|",
    ]
    for country, rs in order:
        speeds = [speed_of(r) for r in rs]
        lines.append(
            "| %s | %d | %.0f Mbps | %.0f Mbps |" % (country, len(rs), sum(speeds) / len(speeds), max(speeds))
        )

    lines += ["", "#### 各国最快的链接（每国最多 %d 条，不足则全部列出）" % TOP_PER_COUNTRY, ""]
    for country, rs in order:
        rs = sorted(rs, key=lambda r: -speed_of(r))
        top = rs if len(rs) <= TOP_PER_COUNTRY else rs[:TOP_PER_COUNTRY]
        note = "全部 %d 条" % len(rs) if len(rs) <= TOP_PER_COUNTRY else "最快 %d 条" % TOP_PER_COUNTRY
        lines.append("<details>")
        lines.append("<summary>%s —— %d 个有效节点（%s）</summary>" % (country, len(rs), note))
        lines.append("")
        lines.append("  ```text")
        for r in top:
            link = daily.build_vless_link(r.get("Country"), r.get("Hostname"), r.get("TCP_Port"))
            if link:
                lines.append("  " + link)
        lines.append("  ```")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    return "\n".join(lines).rstrip()


def replace_block(text, begin, end, body):
    if begin in text and end in text:
        pre, _, rest = text.partition(begin)
        _, _, post = rest.partition(end)
        return pre + begin + "\n" + body + "\n" + end + post
    return text.rstrip() + "\n\n" + begin + "\n" + body + "\n" + end + "\n"


def main():
    parser = argparse.ArgumentParser(description="更新 README.md 的统计区块")
    parser.add_argument("--mode", choices=("total", "tested", "both"), default="both")
    args = parser.parse_args()

    if not os.path.exists(README_PATH):
        print("README 不存在: %s" % README_PATH)
        return 1

    with open(README_PATH, encoding="utf-8") as f:
        text = f.read()

    if args.mode in ("total", "both"):
        body = build_total_block()
        if body is None:
            print("跳过总节点区块: %s 无数据" % CSV_PATH)
        else:
            text = replace_block(text, TOTAL_BEGIN, TOTAL_END, body)
            print("已更新总节点区块")

    if args.mode in ("tested", "both"):
        body = build_tested_block(load_daily_module())
        if body is None:
            print("跳过有效节点区块: %s 无数据" % TESTED_CSV_PATH)
        else:
            text = replace_block(text, TESTED_BEGIN, TESTED_END, body)
            print("已更新有效节点区块")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("README 已写入: %s" % README_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
