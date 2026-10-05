# vpngate — VPNGate 节点自动采集与 VLESS 订阅

本仓库每 3 小时自动从 **VPNGate 官方 API** 采集全球志愿者 VPN 中继节点，
并用 **xray 内核逐个实测**连通性，只把有效节点做成订阅，
保证订阅里都是可用节点。

---

## 📡 订阅链接（重点）

> 每 3 小时自动采集 + 检测更新，直接填入客户端的"订阅"即可。
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

### 原始库（每 3 小时抓取后更新）

<!-- BEGIN:TOTAL -->
> 更新时间：2026-10-05 16:25 UTC ｜ 原始库累计 **1634** 个节点，覆盖 **38** 个国家/地区
<!-- END:TOTAL -->

### 有效节点（每 3 小时检测后更新）

<!-- BEGIN:TESTED -->
> 检测时间：2026-10-05 16:25 UTC ｜ 实测有效 **929** 个节点，覆盖 **28** 个国家/地区，平均速度 **283 Mbps**

#### 各国有效节点数

| 国家/地区 | 有效节点 | 平均速度 | 最高速度 |
|---|---:|---:|---:|
| Japan | 443 | 382 Mbps | 3731 Mbps |
| Korea Republic of | 347 | 200 Mbps | 907 Mbps |
| Russian Federation | 52 | 119 Mbps | 607 Mbps |
| Viet Nam | 25 | 243 Mbps | 733 Mbps |
| Thailand | 15 | 347 Mbps | 637 Mbps |
| United States | 14 | 153 Mbps | 349 Mbps |
| United Kingdom | 5 | 98 Mbps | 160 Mbps |
| Croatia (LOCAL Name: Hrvatska) | 4 | 159 Mbps | 226 Mbps |
| Australia | 3 | 142 Mbps | 285 Mbps |
| Hong Kong | 2 | 450 Mbps | 859 Mbps |
| United Arab Emirates | 2 | 76 Mbps | 79 Mbps |
| Armenia | 1 | 25 Mbps | 25 Mbps |
| Bangladesh | 1 | 47 Mbps | 47 Mbps |
| Belgium | 1 | 38 Mbps | 38 Mbps |
| Canada | 1 | 134 Mbps | 134 Mbps |
| Finland | 1 | 52 Mbps | 52 Mbps |
| Germany | 1 | 227 Mbps | 227 Mbps |
| Greece | 1 | 80 Mbps | 80 Mbps |
| Hungary | 1 | 90 Mbps | 90 Mbps |
| India | 1 | 109 Mbps | 109 Mbps |
| Iran (ISLAMIC Republic Of) | 1 | 11 Mbps | 11 Mbps |
| Italy | 1 | 14 Mbps | 14 Mbps |
| Lithuania | 1 | 143 Mbps | 143 Mbps |
| Mexico | 1 | 82 Mbps | 82 Mbps |
| Poland | 1 | 99 Mbps | 99 Mbps |
| Spain | 1 | 172 Mbps | 172 Mbps |
| Taiwan | 1 | 496 Mbps | 496 Mbps |
| Ukraine | 1 | 25 Mbps | 25 Mbps |

#### 各国最快的链接（每国最多 5 条，不足则全部列出）

<details>
<summary>Japan —— 443 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn517690502.opengw.net%3A1461%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A6%7CJapan%7C3730.97%7C%E8%90%BD%E5%9C%B0%3A118.156.174.68
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn315437254.opengw.net%3A1510%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A5%7CJapan%7C2580.25%7C%E8%90%BD%E5%9C%B0%3A14.132.250.59
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn595476537.opengw.net%3A1405%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A6%7CJapan%7C2489.62%7C%E8%90%BD%E5%9C%B0%3A118.106.229.134
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn193342579.opengw.net%3A1863%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A1%7CJapan%7C2426.76%7C%E8%90%BD%E5%9C%B0%3A118.156.149.7
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn129214879.opengw.net%3A1767%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A6%7CJapan%7C2293.96%7C%E8%90%BD%E5%9C%B0%3A59.138.218.10
  ```

</details>

<details>
<summary>Korea Republic of —— 347 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn532221228.opengw.net%3A1930%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A2%7CKorea%20Republic%20of%7C906.95%7C%E8%90%BD%E5%9C%B0%3A110.15.34.238
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn137307590.opengw.net%3A995%3Fed%3D2560#Korea%20Republic%20of%7C894.36
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn950308053.opengw.net%3A1865%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CKorea%20Republic%20of%7C814.11%7C%E8%90%BD%E5%9C%B0%3A220.86.144.21
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn567706863.opengw.net%3A1302%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A5%7CKorea%20Republic%20of%7C807.52%7C%E8%90%BD%E5%9C%B0%3A112.223.223.68
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn144440524.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CKorea%20Republic%20of%7C793.62%7C%E8%90%BD%E5%9C%B0%3A121.139.54.121
  ```

</details>

<details>
<summary>Russian Federation —— 52 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn501803801.opengw.net%3A1577%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A12%7CRussian%20Federation%7C607.26%7C%E8%90%BD%E5%9C%B0%3A77.34.16.16
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn305517077.opengw.net%3A1839%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A5%7CRussian%20Federation%7C432.21%7C%E8%90%BD%E5%9C%B0%3A178.218.156.154
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn173458867.opengw.net%3A1968%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A13%7CRussian%20Federation%7C355.25%7C%E8%90%BD%E5%9C%B0%3A87.225.107.25
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn934535809.opengw.net%3A1751%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CRussian%20Federation%7C349.45%7C%E8%90%BD%E5%9C%B0%3A77.35.50.149
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn397955876.opengw.net%3A1938%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A5%7CRussian%20Federation%7C329.47%7C%E8%90%BD%E5%9C%B0%3A77.35.136.164
  ```

</details>

<details>
<summary>Viet Nam —— 25 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn992628199.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A9%7CViet%20Nam%7C732.64%7C%E8%90%BD%E5%9C%B0%3A118.68.96.173
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn864131273.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CViet%20Nam%7C724.53%7C%E8%90%BD%E5%9C%B0%3A1.52.202.80
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn433220298.opengw.net%3A1771%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A28%7CViet%20Nam%7C534.45%7C%E8%90%BD%E5%9C%B0%3A118.68.114.82
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn242832503.opengw.net%3A1653%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CViet%20Nam%7C527.13%7C%E8%90%BD%E5%9C%B0%3A1.53.139.247
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn399301599.opengw.net%3A1482%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CViet%20Nam%7C405.45%7C%E8%90%BD%E5%9C%B0%3A42.113.89.17
  ```

</details>

<details>
<summary>Thailand —— 15 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn672097281.opengw.net%3A1820%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A13%7CThailand%7C637.14%7C%E8%90%BD%E5%9C%B0%3A134.236.89.106
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn422139168.opengw.net%3A1872%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A2%7CThailand%7C627.49%7C%E8%90%BD%E5%9C%B0%3A184.82.248.14
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn515969624.opengw.net%3A1562%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A6%7CThailand%7C596.55%7C%E8%90%BD%E5%9C%B0%3A184.82.141.67
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn605489791.opengw.net%3A1441%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A1%7CThailand%7C473.18%7C%E8%90%BD%E5%9C%B0%3A180.183.158.221
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn156765013.opengw.net%3A1801%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A8%7CThailand%7C429.09%7C%E8%90%BD%E5%9C%B0%3A171.5.5.230
  ```

</details>

<details>
<summary>United States —— 14 个有效节点（最快 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn918840683.opengw.net%3A1245%3Fed%3D2560#United%20States%7C348.58
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn852173626.opengw.net%3A1299%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CUnited%20States%7C347.91%7C%E8%90%BD%E5%9C%B0%3A47.160.201.172
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn118756292.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A8%7CUnited%20States%7C295.18%7C%E8%90%BD%E5%9C%B0%3A67.5.100.174
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn164693092.opengw.net%3A1363%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A86%7CUnited%20States%7C175.10%7C%E8%90%BD%E5%9C%B0%3A38.71.123.196
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn380700331.opengw.net%3A1252%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A84%7CUnited%20States%7C173.56%7C%E8%90%BD%E5%9C%B0%3A96.18.192.206
  ```

</details>

<details>
<summary>United Kingdom —— 5 个有效节点（全部 5 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn501386584.opengw.net%3A1266%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A0%7CUnited%20Kingdom%7C159.75%7C%E8%90%BD%E5%9C%B0%3A80.3.208.251
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn175717635.opengw.net%3A1287%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A68%7CUnited%20Kingdom%7C127.45%7C%E8%90%BD%E5%9C%B0%3A149.13.213.68
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40neko69.opengw.net%3A443%3Fed%3D2560#United%20Kingdom%7C97.89
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn777297866.opengw.net%3A1958%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CUnited%20Kingdom%7C77.58%7C%E8%90%BD%E5%9C%B0%3A86.31.10.118
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40patito.opengw.net%3A1750%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CUnited%20Kingdom%7C28.25%7C%E8%90%BD%E5%9C%B0%3A92.16.99.146
  ```

</details>

<details>
<summary>Croatia (LOCAL Name: Hrvatska) —— 4 个有效节点（全部 4 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn499585881.opengw.net%3A443%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A85%7CCroatia%20%28LOCAL%20Name%3A%20Hrvatska%29%7C226.46%7C%E8%90%BD%E5%9C%B0%3A150.40.105.4
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn962496160.opengw.net%3A443%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A27%7CCroatia%20%28LOCAL%20Name%3A%20Hrvatska%29%7C210.11%7C%E8%90%BD%E5%9C%B0%3A150.40.105.24
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn981204829.opengw.net%3A443%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A33%7CCroatia%20%28LOCAL%20Name%3A%20Hrvatska%29%7C100.09%7C%E8%90%BD%E5%9C%B0%3A150.40.105.12
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn232859084.opengw.net%3A443%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A35%7CCroatia%20%28LOCAL%20Name%3A%20Hrvatska%29%7C98.73%7C%E8%90%BD%E5%9C%B0%3A150.40.105.21
  ```

</details>

<details>
<summary>Australia —— 3 个有效节点（全部 3 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn103948172.opengw.net%3A1785%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CAustralia%7C285.27%7C%E8%90%BD%E5%9C%B0%3A120.147.155.231
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn759761201.opengw.net%3A1521%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A58%7CAustralia%7C95.93%7C%E8%90%BD%E5%9C%B0%3A125.253.56.120
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn911912049.opengw.net%3A1446%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A2%7CAustralia%7C44.65%7C%E8%90%BD%E5%9C%B0%3A1.159.52.103
  ```

</details>

<details>
<summary>Hong Kong —— 2 个有效节点（全部 2 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn187430919.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A10%7CHong%20Kong%7C859.25%7C%E8%90%BD%E5%9C%B0%3A58.153.159.195
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn986755484.opengw.net%3A1852%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A11%7CHong%20Kong%7C40.51%7C%E8%90%BD%E5%9C%B0%3A58.152.29.26
  ```

</details>

<details>
<summary>United Arab Emirates —— 2 个有效节点（全部 2 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn490466648.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A1%7CUnited%20Arab%20Emirates%7C79.32%7C%E8%90%BD%E5%9C%B0%3A109.177.50.40
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn765941161.opengw.net%3A1271%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A9%7CUnited%20Arab%20Emirates%7C73.42%7C%E8%90%BD%E5%9C%B0%3A92.96.63.169
  ```

</details>

<details>
<summary>Armenia —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn763562980.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A14%7CArmenia%7C24.94%7C%E8%90%BD%E5%9C%B0%3A37.252.65.108
  ```

</details>

<details>
<summary>Bangladesh —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn342499472.opengw.net%3A1220%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A10%7CBangladesh%7C47.49%7C%E8%90%BD%E5%9C%B0%3A103.30.31.82
  ```

</details>

<details>
<summary>Belgium —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn316776003.opengw.net%3A1517%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CBelgium%7C38.47%7C%E8%90%BD%E5%9C%B0%3A91.177.40.240
  ```

</details>

<details>
<summary>Canada —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn421416087.opengw.net%3A995%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CCanada%7C134.10%7C%E8%90%BD%E5%9C%B0%3A70.79.238.90
  ```

</details>

<details>
<summary>Finland —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn950979828.opengw.net%3A1418%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A18%7CFinland%7C52.19%7C%E8%90%BD%E5%9C%B0%3A84.251.61.191
  ```

</details>

<details>
<summary>Germany —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn695737487.opengw.net%3A110%3Fed%3D2560#Germany%7C226.84
  ```

</details>

<details>
<summary>Greece —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn295596292.opengw.net%3A1414%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CGreece%7C80.22%7C%E8%90%BD%E5%9C%B0%3A46.176.74.138
  ```

</details>

<details>
<summary>Hungary —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn273160004.opengw.net%3A1707%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CHungary%7C90.29%7C%E8%90%BD%E5%9C%B0%3A46.139.25.117
  ```

</details>

<details>
<summary>India —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn359610091.opengw.net%3A995%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A87%7CIndia%7C109.04%7C%E8%90%BD%E5%9C%B0%3A103.78.12.208
  ```

</details>

<details>
<summary>Iran (ISLAMIC Republic Of) —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn371998765.opengw.net%3A1873%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A28%7CIran%20%28ISLAMIC%20Republic%20Of%29%7C10.59%7C%E8%90%BD%E5%9C%B0%3A94.139.167.134
  ```

</details>

<details>
<summary>Italy —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn398736484.opengw.net%3A1723%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A53%7CItaly%7C14.30%7C%E8%90%BD%E5%9C%B0%3A45.89.183.66
  ```

</details>

<details>
<summary>Lithuania —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn539804093.opengw.net%3A1974%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A3%7CLithuania%7C143.17%7C%E8%90%BD%E5%9C%B0%3A77.79.18.229
  ```

</details>

<details>
<summary>Mexico —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40cetsssa.opengw.net%3A992%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A6%7CMexico%7C81.92%7C%E8%90%BD%E5%9C%B0%3A189.186.2.74
  ```

</details>

<details>
<summary>Poland —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn951109898.opengw.net%3A1345%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CPoland%7C99.06%7C%E8%90%BD%E5%9C%B0%3A83.9.97.234
  ```

</details>

<details>
<summary>Spain —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn610588987.opengw.net%3A1253%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A2%7CSpain%7C172.42%7C%E8%90%BD%E5%9C%B0%3A37.15.147.52
  ```

</details>

<details>
<summary>Taiwan —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn713264157.opengw.net%3A992%3Fed%3D2560#%E6%9C%BA%E6%88%BF%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A30%7CTaiwan%7C495.76%7C%E8%90%BD%E5%9C%B0%3A140.111.148.186
  ```

</details>

<details>
<summary>Ukraine —— 1 个有效节点（全部 1 条）</summary>

  ```text
  vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd&fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn455074928.opengw.net%3A1880%3Fed%3D2560#%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A4%7CUkraine%7C24.90%7C%E8%90%BD%E5%9C%B0%3A178.165.55.84
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
| 更新频率 | **每 3 小时**：抓取增量 + 检测有效性 + 重建订阅（外部定时器触发 `sync.yml`） |
| 每周清理 | **每 7 天**用有效库覆盖原始库，防止无效节点越积越多 |
| 转换原理 | 见 [`vpngate.md`](vpngate.md)（模板拆解、fdip 路径方案详解） |

---

## 📁 文件说明

| 文件 | 说明 |
|---|---|
| `vpngate.csv` | 原始库：全部采集节点，`Country,Hostname,IP,Speed_Mbps,TCP_Port`，只增不减 |
| `vpngate.txt` | 原始库全量链接列表：VLESS 链接每行一条（未经检测），每次检测的输入 |
| `vpngate_tested.csv` | 有效库：xray 实测有效的节点（全量重写）；比原始库多 `IsResidential` / `FraudScore` / `ExitIP` 三列（经节点请求 `my.ippure.com/v1/info` 采集的画像） |
| `vpngate-v2ray.txt` | v2rayN 系订阅：VLESS + WebSocket 分享链接，每行一条（由有效库生成） |
| `vpngate-clash.yaml` | Clash 系订阅：完整 YAML 配置 —— **含国内外分流**（私有网段 + `GEOIP,CN` 直连，其余走代理）、**两个代理组**（手动选择，含 `DIRECT`；`url-test` 自动测速）、**DNS 段**（fake-ip + 国内优先解析）；由有效库生成，可直接作为订阅链接 |
| `vpngate-xhttp.txt` | VLESS + XHTTP 订阅：`mode=stream-one` + xPadding 混淆，每行一条（由有效库生成） |
| `vpngate-daily.py` | 主脚本：抓取 API → 过滤 TCP 中继 → 增量写原始库；内含订阅生成函数 |
| `vpngate.md` | **转换原理详解**：API 字段、过滤规则、VLESS 模板、`fdip=sstp://…` 路径方案、备注格式 |
| `scripts/test_nodes.py` | 有效性检测脚本：xray 实测每条链接 → 经节点采集 IP 画像（家宽/机房、纯净度、落地 IP）→ 写有效库 → 重建订阅（不碰原始库） |
| `scripts/build_xhttp.py` | 由有效库生成 `vpngate-xhttp.txt`（VLESS + XHTTP） |
| `scripts/sstp_check.py` | 轻量节点探测：直接对节点做 SSTP 握手（纯标准库，无需 xray），用于体检/排查 |
| `scripts/gen_readme.py` | 统计脚本：把总节点、有效节点与各国最快链接写回本文件的自动区块 |
| `.github/workflows/sync.yml` | 主工作流：每 3 小时「抓取 + 检测 + 重建订阅 + 提交」（外部定时器触发） |
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
  #家宽|纯净度:7|Japan|241.51|落地:219.100.37.15
```

**两段式设计**，重点理解：

1. **入口（固定）**：`saas.sin.fan:443` —— VLESS + TLS + WebSocket 接入点；
   SNI/Host 为 `snip.edgeoneai.cc.cd`，TLS 指纹伪装 chrome。
2. **出口（每行不同）**：`path` 中的
   `/fdip=sstp://vpn:vpn@{hostname}:{tcp_port}?ed=2560` —— 入口收到连接后，
   用 **SSTP 协议**（账号 `vpn`/`vpn`）拨号到对应的 VPNGate 志愿者节点，
   再把流量桥接回去。

**备注（客户端里显示的节点名）**分两种：

| 情况 | 格式 | 示例 |
|---|---|---|
| 有效节点且画像数据齐全 | `{家宽\|机房}\|纯净度:{fraudScore}\|{国家}\|{速度}\|落地:{ip}` | `家宽\|纯净度:7\|Japan\|241.51\|落地:219.100.37.15` |
| 无画像数据（原始库，或采集失败/触发人机验证） | `{国家}\|{速度}` | `Japan\|241.51` |

- `家宽` / `机房` 由 `isResidential` 决定（`true` = 家宽，`false` = 机房）；
- `纯净度` 取接口返回的 `fraudScore`（越低越干净）；
- `落地` 是经该节点出口查到的公网 IP，可能是 IPv4 或 IPv6；
- `速度` 取 `vpngate.csv` 的 `Speed_Mbps`。

> 完整拆解见 [`vpngate.md`](vpngate.md)。

## 📲 使用方法

1. 复制上方"📡 订阅链接"中对应客户端的链接，填入客户端的订阅设置并更新；
   或打开 `vpngate-v2ray.txt` 复制单条链接粘贴导入（v2rayN 支持从剪贴板导入）；
2. 连接即可。建议在客户端中按延迟排序，优先选择速度快、延迟低的节点。

## 🔄 自动更新机制

数据分三层流转：**原始库 → 有效库 → 订阅文件**。

**主流水线 `.github/workflows/sync.yml`（每 3 小时）** —— 由**外部定时器**触发
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
  本仓库每 3 小时都有提交，因此不会触发该限制。

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
