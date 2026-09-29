# vpngate — VPNGate 节点自动采集与 VLESS 订阅

本仓库每小时自动从 **VPNGate 官方 API** 采集全球志愿者 VPN 中继节点，
并用 **xray 内核逐个实测**连通性，只把有效节点做成订阅，
保证订阅里都是可用节点。

---

## 📡 订阅链接（重点）

> 每小时自动采集 + 检测更新，直接填入客户端的"订阅"即可。
> 以下三个订阅均由**同一批有效节点**生成，按客户端/协议三选一：

| 客户端 / 协议 | 订阅链接 |
|---|---|
| **v2rayN / Shadowrocket / Streisand 等**（VLESS + WebSocket，每行一条） | `https://raw.githubusercontent.com/sdise/vpngate/main/vpngate-v2ray.txt` |
| **Clash / Clash Verge / Mihomo 等**（YAML 配置） | `https://raw.githubusercontent.com/sdise/vpngate/main/vpngate-clash.yaml` |
| **VLESS + XHTTP**（`mode=stream-one` + xPadding 混淆，每行一条） | `https://raw.githubusercontent.com/sdise/vpngate/main/vpngate-xhttp.txt` |

国内访问 GitHub raw 较慢时，可换 jsdelivr 加速镜像（内容相同）：

| 客户端 / 协议 | jsdelivr 镜像 |
|---|---|
| v2rayN 系（VLESS ws） | `https://cdn.jsdelivr.net/gh/sdise/vpngate@main/vpngate-v2ray.txt` |
| Clash 系 | `https://cdn.jsdelivr.net/gh/sdise/vpngate@main/vpngate-clash.yaml` |
| VLESS XHTTP | `https://cdn.jsdelivr.net/gh/sdise/vpngate@main/vpngate-xhttp.txt` |

---

## 📊 数据快照（自动生成）

下面两组数据由 GitHub Actions 自动写入（脚本 `scripts/gen_readme.py`），
**标记行之间请勿手工编辑**。

### 原始库（每小时抓取后更新）

<!-- BEGIN:TOTAL -->
> 更新时间：2026-09-29 09:26 UTC ｜ 原始库累计 **1058** 个节点，覆盖 **22** 个国家/地区
<!-- END:TOTAL -->

### 有效节点（每天检测后更新）

<!-- BEGIN:TESTED -->
> 检测时间：2026-09-29 09:26 UTC ｜ 实测有效 **896** 个节点，覆盖 **21** 个国家/地区，平均速度 **279 Mbps**

#### 各国有效节点数

| 国家/地区 | 有效节点 | 平均速度 | 最高速度 |
|---|---:|---:|---:|
| Japan | 425 | 376 Mbps | 3933 Mbps |
| Korea Republic of | 336 | 194 Mbps | 853 Mbps |
| Russian Federation | 55 | 113 Mbps | 607 Mbps |
| Thailand | 24 | 397 Mbps | 750 Mbps |
| Viet Nam | 19 | 247 Mbps | 725 Mbps |
| United States | 12 | 114 Mbps | 349 Mbps |
| Croatia (LOCAL Name: Hrvatska) | 7 | 143 Mbps | 226 Mbps |
| Mexico | 3 | 173 Mbps | 403 Mbps |
| Canada | 2 | 79 Mbps | 134 Mbps |
| Malaysia | 2 | 452 Mbps | 730 Mbps |
| Armenia | 1 | 25 Mbps | 25 Mbps |
| Australia | 1 | 45 Mbps | 45 Mbps |
| Chile | 1 | 47 Mbps | 47 Mbps |
| Grenada | 1 | 27 Mbps | 27 Mbps |
| Hungary | 1 | 117 Mbps | 117 Mbps |
| India | 1 | 82 Mbps | 82 Mbps |
| Latvia | 1 | 123 Mbps | 123 Mbps |
| Saudi Arabia | 1 | 41 Mbps | 41 Mbps |
| Ukraine | 1 | 6 Mbps | 6 Mbps |
| United Arab Emirates | 1 | 73 Mbps | 73 Mbps |
| United Kingdom | 1 | 127 Mbps | 127 Mbps |

#### 各国最快的链接（每国最多 5 条，不足则全部列出）

<details>
<summary>Japan —— 425 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn315836095.opengw.net%3A1378%3Fed%3D2560#vpngate.me%20%7C%20Japan%20%7C%20vpn315836095
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn949760217.opengw.net%3A1697%3Fed%3D2560#vpngate.me%20%7C%20Japan%20%7C%20vpn949760217
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn774927062.opengw.net%3A1776%3Fed%3D2560#vpngate.me%20%7C%20Japan%20%7C%20vpn774927062
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn594251655.opengw.net%3A1354%3Fed%3D2560#vpngate.me%20%7C%20Japan%20%7C%20vpn594251655
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40public-vpn-95.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Japan%20%7C%20public-vpn-95
  ```

</details>

<details>
<summary>Korea Republic of —— 336 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn720886103.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Korea%20Republic%20of%20%7C%20vpn720886103
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn830655314.opengw.net%3A1674%3Fed%3D2560#vpngate.me%20%7C%20Korea%20Republic%20of%20%7C%20vpn830655314
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn960496987.opengw.net%3A1342%3Fed%3D2560#vpngate.me%20%7C%20Korea%20Republic%20of%20%7C%20vpn960496987
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn165692380.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Korea%20Republic%20of%20%7C%20vpn165692380
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn144440524.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Korea%20Republic%20of%20%7C%20vpn144440524
  ```

</details>

<details>
<summary>Russian Federation —— 55 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn501803801.opengw.net%3A1577%3Fed%3D2560#vpngate.me%20%7C%20Russian%20Federation%20%7C%20vpn501803801
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn305517077.opengw.net%3A1839%3Fed%3D2560#vpngate.me%20%7C%20Russian%20Federation%20%7C%20vpn305517077
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn173458867.opengw.net%3A1968%3Fed%3D2560#vpngate.me%20%7C%20Russian%20Federation%20%7C%20vpn173458867
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn520583431.opengw.net%3A1425%3Fed%3D2560#vpngate.me%20%7C%20Russian%20Federation%20%7C%20vpn520583431
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn353146232.opengw.net%3A1995%3Fed%3D2560#vpngate.me%20%7C%20Russian%20Federation%20%7C%20vpn353146232
  ```

</details>

<details>
<summary>Thailand —— 24 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn558150618.opengw.net%3A1703%3Fed%3D2560#vpngate.me%20%7C%20Thailand%20%7C%20vpn558150618
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn583038823.opengw.net%3A1249%3Fed%3D2560#vpngate.me%20%7C%20Thailand%20%7C%20vpn583038823
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn672097281.opengw.net%3A1820%3Fed%3D2560#vpngate.me%20%7C%20Thailand%20%7C%20vpn672097281
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn515969624.opengw.net%3A1562%3Fed%3D2560#vpngate.me%20%7C%20Thailand%20%7C%20vpn515969624
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn113281460.opengw.net%3A1589%3Fed%3D2560#vpngate.me%20%7C%20Thailand%20%7C%20vpn113281460
  ```

</details>

<details>
<summary>Viet Nam —— 19 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn864131273.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Viet%20Nam%20%7C%20vpn864131273
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn225862051.opengw.net%3A1958%3Fed%3D2560#vpngate.me%20%7C%20Viet%20Nam%20%7C%20vpn225862051
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn922312929.opengw.net%3A1997%3Fed%3D2560#vpngate.me%20%7C%20Viet%20Nam%20%7C%20vpn922312929
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn198374908.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Viet%20Nam%20%7C%20vpn198374908
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn350891291.opengw.net%3A1671%3Fed%3D2560#vpngate.me%20%7C%20Viet%20Nam%20%7C%20vpn350891291
  ```

</details>

<details>
<summary>United States —— 12 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn918840683.opengw.net%3A1245%3Fed%3D2560#vpngate.me%20%7C%20United%20States%20%7C%20vpn918840683
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn785793258.opengw.net%3A1761%3Fed%3D2560#vpngate.me%20%7C%20United%20States%20%7C%20vpn785793258
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn164693092.opengw.net%3A1363%3Fed%3D2560#vpngate.me%20%7C%20United%20States%20%7C%20vpn164693092
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn907569351.opengw.net%3A1881%3Fed%3D2560#vpngate.me%20%7C%20United%20States%20%7C%20vpn907569351
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn115726570.opengw.net%3A1583%3Fed%3D2560#vpngate.me%20%7C%20United%20States%20%7C%20vpn115726570
  ```

</details>

<details>
<summary>Croatia (LOCAL Name: Hrvatska) —— 7 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn499585881.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Croatia%20%28LOCAL%20Name%3A%20Hrvatska%29%20%7C%20vpn499585881
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn962496160.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Croatia%20%28LOCAL%20Name%3A%20Hrvatska%29%20%7C%20vpn962496160
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn132328711.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Croatia%20%28LOCAL%20Name%3A%20Hrvatska%29%20%7C%20vpn132328711
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn178522347.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Croatia%20%28LOCAL%20Name%3A%20Hrvatska%29%20%7C%20vpn178522347
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn981204829.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Croatia%20%28LOCAL%20Name%3A%20Hrvatska%29%20%7C%20vpn981204829
  ```

</details>

<details>
<summary>Mexico —— 3 个有效节点（全部 3 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn158297266.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Mexico%20%7C%20vpn158297266
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40cetsssa.opengw.net%3A992%3Fed%3D2560#vpngate.me%20%7C%20Mexico%20%7C%20cetsssa
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn764449825.opengw.net%3A1412%3Fed%3D2560#vpngate.me%20%7C%20Mexico%20%7C%20vpn764449825
  ```

</details>

<details>
<summary>Canada —— 2 个有效节点（全部 2 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn421416087.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Canada%20%7C%20vpn421416087
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn491348575.opengw.net%3A1697%3Fed%3D2560#vpngate.me%20%7C%20Canada%20%7C%20vpn491348575
  ```

</details>

<details>
<summary>Malaysia —— 2 个有效节点（全部 2 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn919050053.opengw.net%3A1998%3Fed%3D2560#vpngate.me%20%7C%20Malaysia%20%7C%20vpn919050053
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn667888734.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Malaysia%20%7C%20vpn667888734
  ```

</details>

<details>
<summary>Armenia —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn763562980.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Armenia%20%7C%20vpn763562980
  ```

</details>

<details>
<summary>Australia —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn289936273.opengw.net%3A1763%3Fed%3D2560#vpngate.me%20%7C%20Australia%20%7C%20vpn289936273
  ```

</details>

<details>
<summary>Chile —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn548414740.opengw.net%3A1992%3Fed%3D2560#vpngate.me%20%7C%20Chile%20%7C%20vpn548414740
  ```

</details>

<details>
<summary>Grenada —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40diamondgnd.opengw.net%3A443%3Fed%3D2560#vpngate.me%20%7C%20Grenada%20%7C%20diamondgnd
  ```

</details>

<details>
<summary>Hungary —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn273160004.opengw.net%3A1707%3Fed%3D2560#vpngate.me%20%7C%20Hungary%20%7C%20vpn273160004
  ```

</details>

<details>
<summary>India —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn368881682.opengw.net%3A1531%3Fed%3D2560#vpngate.me%20%7C%20India%20%7C%20vpn368881682
  ```

</details>

<details>
<summary>Latvia —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn860205220.opengw.net%3A995%3Fed%3D2560#vpngate.me%20%7C%20Latvia%20%7C%20vpn860205220
  ```

</details>

<details>
<summary>Saudi Arabia —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40fing.opengw.net%3A992%3Fed%3D2560#vpngate.me%20%7C%20Saudi%20Arabia%20%7C%20fing
  ```

</details>

<details>
<summary>Ukraine —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn313985146.opengw.net%3A5555%3Fed%3D2560#vpngate.me%20%7C%20Ukraine%20%7C%20vpn313985146
  ```

</details>

<details>
<summary>United Arab Emirates —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn765941161.opengw.net%3A1271%3Fed%3D2560#vpngate.me%20%7C%20United%20Arab%20Emirates%20%7C%20vpn765941161
  ```

</details>

<details>
<summary>United Kingdom —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn175717635.opengw.net%3A1287%3Fed%3D2560#vpngate.me%20%7C%20United%20Kingdom%20%7C%20vpn175717635
  ```

</details>
<!-- END:TESTED -->

---

## ⭐ 重点速览

| 项目 | 说明 |
|---|---|
| 数据来源 | `http://www.vpngate.net/api/iphone/`（VPNGate 官方实时接口） |
| 原始库 | `vpngate.csv` —— 全部采集节点（只增不减，每周用有效库覆盖清理一次） |
| 全量列表 | `vpngate.txt` —— 原始库全部节点的 VLESS 链接（未经检测），检测的输入 |
| 有效库 | `vpngate_tested.csv` —— xray 实测有效的节点 |
| 订阅文件 | `vpngate-v2ray.txt`（VLESS ws）/ `vpngate-clash.yaml`（Clash）/ `vpngate-xhttp.txt`（VLESS XHTTP），均由有效库生成 |
| 入口地址 | `saas.sin.fan:443`（VLESS 链接中的 `@` 后地址） |
| 更新频率 | **每小时**：抓取增量 + 检测有效性 + 重建订阅（外部定时器触发 `sync.yml`） |
| 每周清理 | **每 7 天**用有效库覆盖原始库，防止无效节点越积越多 |
| 转换原理 | 见 [`vpngate.md`](vpngate.md)（模板拆解、fdip 路径方案详解） |

---

## 📁 文件说明

| 文件 | 说明 |
|---|---|
| `vpngate.csv` | 原始库：全部采集节点，`Country,Hostname,IP,Speed_Mbps,TCP_Port`，只增不减 |
| `vpngate.txt` | 原始库全量链接列表：VLESS 链接每行一条（未经检测），每日检测的输入 |
| `vpngate_tested.csv` | 有效库：xray 实测有效的节点（全量重写） |
| `vpngate-v2ray.txt` | v2rayN 系订阅：VLESS + WebSocket 分享链接，每行一条（由有效库生成） |
| `vpngate-clash.yaml` | Clash 系订阅：完整 YAML 配置，可直接作为订阅链接（由有效库生成） |
| `vpngate-xhttp.txt` | VLESS + XHTTP 订阅：`mode=stream-one` + xPadding 混淆，每行一条（由有效库生成） |
| `vpngate-daily.py` | 主脚本：抓取 API → 过滤 TCP 中继 → 增量写原始库；内含订阅生成函数 |
| `vpngate.md` | **转换原理详解**：API 字段、过滤规则、VLESS 模板、`fdip=sstp://…` 路径方案、备注格式 |
| `scripts/test_nodes.py` | 有效性检测脚本：xray 实测每条链接 → 写有效库 → 重建订阅（不碰原始库） |
| `scripts/build_xhttp.py` | 由有效库生成 `vpngate-xhttp.txt`（VLESS + XHTTP） |
| `scripts/sstp_check.py` | 轻量节点探测：直接对节点做 SSTP 握手（纯标准库，无需 xray），用于体检/排查 |
| `scripts/gen_readme.py` | 统计脚本：把总节点、有效节点与各国最快链接写回本文件的自动区块 |
| `.github/workflows/sync.yml` | 主工作流：每 2 小时「抓取 + 检测 + 重建订阅 + 提交」（外部定时器触发） |
| `.github/workflows/prune.yml` | 每周用有效库覆盖清理原始库工作流 |
| `vpngate-fetch.log` | 抓取运行日志 |

---

## 🔗 VLESS 链接结构（核心原理）

每条链接形如（已解码示意）：

```text
vless://<UUID>@saas.sin.fan:443?encryption=none&security=tls
  &sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3,h2&type=ws
  &host=snip.edgeoneai.cc.cd
  &path=/fdip=sstp://vpn:vpn@vpn228702251.opengw.net:1587?ed=2560
  #vpngate.me | Japan | vpn228702251
```

**两段式设计**，重点理解：

1. **入口（固定）**：`saas.sin.fan:443` —— VLESS + TLS + WebSocket 接入点；
   SNI/Host 为 `snip.edgeoneai.cc.cd`，TLS 指纹伪装 chrome。
2. **出口（每行不同）**：`path` 中的
   `/fdip=sstp://vpn:vpn@{hostname}:{tcp_port}?ed=2560` —— 入口收到连接后，
   用 **SSTP 协议**（账号 `vpn`/`vpn`）拨号到对应的 VPNGate 志愿者节点，
   再把流量桥接回去。

备注格式为 `vpngate.me | 国家 | 短主机名`，方便在客户端中识别。

> 完整拆解见 [`vpngate.md`](vpngate.md)。

## 📲 使用方法

1. 复制上方"📡 订阅链接"中对应客户端的链接，填入客户端的订阅设置并更新；
   或打开 `vpngate-v2ray.txt` 复制单条链接粘贴导入（v2rayN 支持从剪贴板导入）；
2. 连接即可。建议在客户端中按延迟排序，优先选择速度快、延迟低的节点。

## 🔄 自动更新机制

数据分三层流转：**原始库 → 有效库 → 订阅文件**。

**主流水线 `.github/workflows/sync.yml`（每 2 小时）** —— 由**外部定时器**触发
（服务器 crontab 调用 GitHub API 的 `workflow_dispatch`），不使用 GitHub 原生 `schedule`
（后者是 best-effort，高负载时会延迟数十分钟甚至丢点）。单次运行依次执行：

1. **抓取更新**：拉取官方 API，只追加新出现的 Hostname 到 `vpngate.csv`（原始库），
   并重建 `vpngate.txt`（全量 VLESS 链接列表）；
2. **检测有效性**：安装最新 xray 内核，逐个实测 `vpngate.txt` 中的链接
   （为每条生成最小配置：socks 入站 + vless 出站），经 SOCKS5 请求
   `https://www.google.com/generate_204`，2xx/3xx 视为有效；
   有效节点写入 `vpngate_tested.csv`（有效库，全量重写），并由有效库重建
   `vpngate-v2ray.txt`、`vpngate-clash.yaml` 与 `vpngate-xhttp.txt`；
   **全程不修改 `vpngate.csv`**，防止网络波动误删原始数据；
   **安全护栏**：检测前先确认入口可达，有效比例低于 20% 视为系统性故障，自动中止且不写文件；
3. **更新 README**：把原始库摘要、有效节点统计与各国最快链接写回本文件「数据快照」区块；
4. **提交并推送**：一次性提交全部产物。
- **检测强制走落地**：入口（Cloudflare Worker）默认会先尝试**直连**目标，
  只有直连失败才回落到 SSTP 节点；而 `google.com:443` 从入口必然直连成功，
  那样测出来的是入口而不是节点（会出现"100% 有效"的假象）。
  因此检测时会在链接的 `path` 后追加 `global=1` 强制入口走 SSTP 落地
  （见 `scripts/test_nodes.py` 的 `FORCE_GLOBAL`），实测有效比例约 45%~55%。
- **每周清理**（`prune.yml`，每周日 04:00 UTC）：用 `vpngate_tested.csv`
  覆盖 `vpngate.csv`，清除累积的下线节点，防止原始库无限膨胀。
- 公开仓库的计划任务在 **60 天无提交时会被 GitHub 自动暂停**，
  本仓库每小时都有提交，因此不会触发该限制。

## ✅ 合规说明（GitHub 使用政策评估）

- 本仓库的 Actions 用途：① 定时读取**公开 API** 并提交数据文件；
  ② 以 xray 作**客户端**进行连通性测试（等价于 CI 集成测试）。
- 不挖矿、不发送垃圾流量、不对外提供代理服务、不做端口扫描，
  单次检测约十几分钟、并发适度，符合 GitHub 可接受使用政策与
  Actions 使用条款。
- 若未来 GitHub 调整政策或仓库收到警告，应优先降级检测频率
  （如改为纯 TCP 连通性检测），必要时暂停 `sync.yml`。

## ⚠️ 风险提示

1. **入口依赖 Cloudflare Workers**：`saas.sin.fan` 背后为 Cloudflare 网络。
   Cloudflare 服务条款 2.2.1(j) 明确禁止未经书面许可“提供 VPN 或类似代理服务”，
   相关账号存在被封禁风险，请自行评估。
2. **节点为志愿者提供**：VPNGate 中继由全球志愿者运行，随时上下线，
   且流量经过第三方节点，**不要传输敏感信息**。
3. **异常节点**：`_unregistered_vpn335506854.opengw.net` 为全表唯一非标准注册
   格式主机名，来源可疑、速度极低（0.99 Mbps），建议不要使用。
4. 各国家/地区对 VPN 的法律规定不同，请遵守当地法律法规。

---

*数据来源：[VPNGate](https://www.vpngate.net/)（筑波大学 SoftEther VPN 项目）。
本仓库仅做公开数据的自动化整理与格式转换。*
