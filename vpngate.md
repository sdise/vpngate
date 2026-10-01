# vpngate.md — VPNGate 数据获取与 VLESS 链接转换详解

> 本文档详细说明 `vpngate.csv` 的数据来源、过滤规则，以及如何将其转换为
> `vpngate-v2ray.txt` 中的 v2rayN 分享链接（含 `saas.sin.fan` 入口替换与
> `fdip` 路径方案的完整拆解）。

---

## 1. 数据来源：VPNGate 官方 API

- 接口：`http://www.vpngate.net/api/iphone/`（VPNGate 官网页面底部的 CSV 下载入口同源）
- 返回：CSV 文本，第一行为 `*vpn_servers` 标记行、`#` 开头注释行，之后每行一个中继
- 关键列（按顺序）：
  | 列号 | 字段 | 说明 |
  |---|---|---|
  | 0 | HostName | 短主机名，如 `vpn228702251` |
  | 1 | IP | 中继公网 IP |
  | 4 | Speed | 速度，单位 bps |
  | 5 | CountryLong | 国家/地区全称，如 `Japan` |
  | 14 | OpenVPN_Config | base64 编码的 OpenVPN 客户端配置 |

## 2. 过滤与处理规则（`vpngate-daily.py :: parse_rows`）

1. 跳过 `*` / `#` 开头的非数据行，以及列数不足 15 的脏行。
2. base64 解码第 14 列，得到 OpenVPN 配置文本。
3. 用正则提取配置中的协议与远端：
   - `^proto\s+(\S+)` → 协议集合
   - `^remote\s+\S+\s+(\d+)` → 远端口列表
4. **只保留同时满足以下两条的中继**（与 `vpsgate.md` 的“只保留 TCP”规则一致）：
   - 协议集合包含 `tcp`
   - 存在至少一个 `remote` 端口
5. 速度换算：`Speed(bps) / 1_000_000` → Mbps，保留 2 位小数。
6. 主机名统一为 DDNS 形式：`<HostName>.opengw.net`（如 `vpn228702251.opengw.net`）。
7. 同一 Hostname 去重；排序：Country 升序、Speed 降序。
8. **增量写入**：以 Hostname 为键与现有 `vpngate.csv` 比对，只追加新节点，已存在的整行忽略（节点下线不会自动删除，删除由每日有效性检测负责）。

## 3. `vpngate.csv` 文件格式

表头：`Country,Hostname,IP,Speed_Mbps,TCP_Port`

示例行：

```csv
Japan,vpn228702251.opengw.net,219.100.37.214,523.10,1587
```

## 4. VLESS 链接模板（`vpngate-daily.py :: VLESS_BASE`）

每条分享链接由“固定模板 + 节点相关 path + 备注”拼接而成。模板取自用户提供的自有 VLESS 链接：

```
vless://<UUID>@<SERVER>?encryption=none&security=tls&sni=snip.edgeoneai.cc.cd
  &fp=chrome&alpn=h3%2Ch2&type=ws&host=snip.edgeoneai.cc.cd&path=<PATH>#<NAME>
```

固定参数说明：

| 参数 | 值 | 说明 |
|---|---|---|
| UUID | `495c7195-85b8-498a-bf20-2ea9ce9175b5` | 用户自有 VLESS 账号的 UUID |
| SERVER | `saas.sin.fan:443` | **入口地址（2026-09-27 起由 `61.172.182.19:443` 替换）** |
| encryption | `none` | VLESS 无内层加密（外层靠 TLS） |
| security | `tls` | 传输层 TLS |
| sni | `snip.edgeoneai.cc.cd` | TLS SNI |
| fp | `chrome` | TLS 指纹伪装 |
| alpn | `h3,h2` | ALPN（URL 编码为 `h3%2Ch2`） |
| type | `ws` | WebSocket 传输 |
| host | `snip.edgeoneai.cc.cd` | WebSocket Host 头 |

## 5. `path` 的构成：fdip 方案（核心）

`path` 参数 = URL 编码后的以下字符串：

```
/fdip=sstp://vpn:vpn@{hostname}:{tcp_port}?ed=2560
```

以日本节点 `vpn228702251.opengw.net:1587` 为例，解码后：

```
/fdip=sstp://vpn:vpn@vpn228702251.opengw.net:1587?ed=2560
```

含义：入口 Worker（`saas.sin.fan:443`）收到 WebSocket 连接后，读取 `fdip`
参数，使用 **SSTP 协议**、以用户名/密码 `vpn`/`vpn` 拨号到对应的 VPNGate
志愿者节点（`ed=2560` 为 SSTP 加密参数），再把流量桥接回去。也就是说：

- **入口**（固定）：`saas.sin.fan:443` —— 用户自己的 Cloudflare Workers
- **出口**（每行不同）：`{hostname}:{tcp_port}` —— VPNGate 志愿者 SSTP 节点

## 6. 备注（`#` 后面的名字）构成

由 `vpngate-daily.py :: remark()` 生成，分两种：

**A. 有 IP 画像数据**（有效库 `vpngate_tested.csv` 的 `IsResidential` / `FraudScore` / `ExitIP` 三列齐全）：

```
{家宽|机房}|纯净度:{fraudScore}|{Country}|{Speed_Mbps}|落地:{ip}
```

示例（URL 编码前）：`家宽|纯净度:7|Japan|241.51|落地:219.100.37.15`

**B. 无画像数据**（原始库 `vpngate.csv`，或采集失败 / 返回非 JSON / 关键字段缺失）：

```
{Country}|{Speed_Mbps}
```

示例：`Japan|241.51`

字段来源：

| 字段 | 来源 | 说明 |
|---|---|---|
| 家宽 / 机房 | ippure `isResidential` | `true` → 家宽，`false` → 机房 |
| 纯净度 | ippure `fraudScore` | 越低越干净；`0` 是合法值，不会被当成缺失 |
| Country | `vpngate.csv` | 国家名 |
| Speed_Mbps | `vpngate.csv` | 采集时的测速值 |
| 落地 | ippure `ip` | 经该节点出口查到的公网 IP，可能是 IPv4 或 IPv6 |

> 备注里的 `|`、中文等字符会由 `urllib.parse.quote` 做 URL 编码，
> 例如 `家宽|纯净度:7|Japan|241.51|落地:1.2.3.4` →
> `%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CJapan%7C241.51%7C%E8%90%BD%E5%9C%B0%3A1.2.3.4`。

## 7. 完整链接示例（拆解）

```text
vless://495c7195-85b8-498a-bf20-2ea9ce9175b5@saas.sin.fan:443
  ?encryption=none
  &security=tls
  &sni=snip.edgeoneai.cc.cd
  &fp=chrome
  &alpn=h3%2Ch2
  &type=ws
  &host=snip.edgeoneai.cc.cd
  &path=%2Ffdip%3Dsstp%3A%2F%2Fvpn%3Avpn%40vpn228702251.opengw.net%3A1587%3Fed%3D2560
  #%E5%AE%B6%E5%AE%BD%7C%E7%BA%AF%E5%87%80%E5%BA%A6%3A7%7CJapan%7C241.51%7C%E8%90%BD%E5%9C%B0%3A219.100.37.15
```

其中 `path` 解码为 `/fdip=sstp://vpn:vpn@vpn228702251.opengw.net:1587?ed=2560`，
`#` 后解码为 `家宽|纯净度:7|Japan|241.51|落地:219.100.37.15`（无画像数据时为 `Japan|241.51`）。

## 8. 生成流程

数据分两条线生成：

1. **`vpngate.txt`（全量列表）**：每小时任务调用
   `rebuild_v2ray_links(vpngate.csv, vpngate.txt)`，由原始库全量重建，
   未经有效性检测；同时作为每日检测任务的输入。
2. **订阅文件（有效节点）**：`scripts/test_nodes.py` 每日检测后调用
   `rebuild_subscriptions(vpngate_tested.csv)`，由有效库生成
   `vpngate-v2ray.txt`（v2rayN）与 `vpngate-clash.yaml`（Clash）。

### IP 画像采集（新增）

对**检测有效**的节点，检测脚本会**复用同一条 SOCKS 出口**再请求一次：

```
GET https://my.ippure.com/v1/info
```

该接口返回**请求方出口 IP** 的画像，所以必须经节点发起请求才能拿到该节点自己的数据。
取其中三个字段写入有效库：

| 有效库列 | 接口字段 | 类型 |
|---|---|---|
| `IsResidential` | `isResidential` | `true` / `false`（布尔） |
| `FraudScore` | `fraudScore` | 整数 |
| `ExitIP` | `ip` | 字符串（IPv4 或 IPv6） |

以下情况三列留空，备注自动回退为 `{Country}|{Speed_Mbps}`：

- 请求失败 / 超时 / 返回体为空；
- 返回的不是 JSON（**常见于触发人机验证**，拿到的是 HTML 验证页）；
- 缺少 `isResidential` / `fraudScore` / `ip` 中的任意一个。

可通过环境变量控制：`IPINFO_ENABLE`（置 `0` 整体关闭）、`IPINFO_URL`、`IPINFO_TIMEOUT`、`IPINFO_UA`。

## 9. 已知数据异常

- `_unregistered_vpn335506854.opengw.net`（China）：全表唯一非标准注册格式
  的主机名（正常为 `vpn+数字.opengw.net`），“unregistered”表示未在 VPNGate
  官方注册，来源可疑；且速度仅 0.99 Mbps，基本不可用。建议视为不可信节点。
- VPNGate 节点由全球志愿者提供，随时上下线；有效性以每日自动检测为准，
  失效节点会自动从 `vpngate.csv` 中删除。

### Clash 订阅结构（`vpngate-clash.yaml`）

由 `build_clash_proxy` 为每个有效节点生成：

```yaml
- name: "家宽|纯净度:7|Japan|241.51|落地:219.100.37.15"  # 与 VLESS 备注同格式
  type: vless
  server: saas.sin.fan
  port: 443
  uuid: 495c7195-85b8-498a-bf20-2ea9ce9175b5
  network: ws
  tls: true
  udp: false
  sni: snip.edgeoneai.cc.cd
  fingerprint: chrome
  alpn: [h3, h2]
  ws-opts:
    path: /fdip=sstp://vpn:vpn@vpn228702251.opengw.net:1587?ed=2560
    headers:
      Host: snip.edgeoneai.cc.cd
```

文件尾部附带一个 `select` 类型的 `proxy-groups`（`vpngate-手动选择`，
含全部节点）与 `rules: [MATCH, vpngate-手动选择]`，因此整个文件就是一份
开箱即用的 Clash 配置，可直接填入客户端订阅。

> **名字唯一性**：Clash 要求每个 proxy 的 `name` 唯一。新备注只含
> `国家 + 速度 + 落地 IP`，同一出口 IP 上挂多个 `Hostname` 时可能撞名，
> 因此 `rebuild_clash_subscription()` 在检测到重名时会按需补上短主机名
> （仍重复则再加 `#序号`），例如
> `家宽|纯净度:7|Japan|241.51|落地:219.100.37.15|public-vpn-50`。

## 10. 数据分层与文件总览

| 层 | 文件 | 更新方式 |
|---|---|---|
| 原始库 | `vpngate.csv` | 每小时抓取增量追加；每周被有效库覆盖清理一次 |
| 全量列表 | `vpngate.txt` | 每小时由原始库重建；每日检测的输入 |
| 有效库 | `vpngate_tested.csv` | 每日 xray 实测后全量重写 |
| 订阅 | `vpngate-v2ray.txt`（v2rayN） | 由有效库生成 |
| 订阅 | `vpngate-clash.yaml`（Clash YAML） | 由有效库生成 |

| 文件 | 说明 |
|---|---|
| `vpngate-daily.py` | 抓取 + 增量写入原始库 + 重建全量列表的主脚本；内含订阅生成函数 |
| `vpngate.csv` | 原始累计库（只增不减） |
| `vpngate.txt` | 原始库全量 VLESS 链接列表（未经检测） |
| `vpngate_tested.csv` | 有效节点库 |
| `vpngate-v2ray.txt` | v2rayN 分享链接（每行一条） |
| `vpngate-clash.yaml` | Clash 订阅（YAML） |
| `scripts/test_nodes.py` | 每日有效性检测：读取 vpngate.txt 实测 → 写有效库 → 重建订阅（不碰原始库） |
| `.github/workflows/update.yml` | 每小时自动抓取更新 |
| `.github/workflows/test.yml` | 每天自动检测有效性并重建订阅 |
| `.github/workflows/prune.yml` | 每周用有效库覆盖清理原始库 |
