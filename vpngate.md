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

```
vpngate.me | {Country} | {short_hostname}
```

示例（URL 编码前）：`vpngate.me | Japan | vpn228702251`

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
  #vpngate.me%20%7C%20Japan%20%7C%20vpn228702251
```

其中 `path` 解码为 `/fdip=sstp://vpn:vpn@vpn228702251.opengw.net:1587?ed=2560`，
`#` 后解码为 `vpngate.me | Japan | vpn228702251`。

## 8. 生成流程

数据分两条线生成：

1. **`vpngate.txt`（全量列表）**：每小时任务调用
   `rebuild_v2ray_links(vpngate.csv, vpngate.txt)`，由原始库全量重建，
   未经有效性检测；同时作为每日检测任务的输入。
2. **订阅文件（有效节点）**：`scripts/test_nodes.py` 每日检测后调用
   `rebuild_subscriptions(vpngate_tested.csv)`，由有效库生成
   `vpngate-v2ray.txt`（v2rayN）与 `vpngate-clash.yaml`（Clash）。

## 9. 已知数据异常

- `_unregistered_vpn335506854.opengw.net`（China）：全表唯一非标准注册格式
  的主机名（正常为 `vpn+数字.opengw.net`），“unregistered”表示未在 VPNGate
  官方注册，来源可疑；且速度仅 0.99 Mbps，基本不可用。建议视为不可信节点。
- VPNGate 节点由全球志愿者提供，随时上下线；有效性以每日自动检测为准，
  失效节点会自动从 `vpngate.csv` 中删除。

### Clash 订阅结构（`vpngate-clash.yaml`）

由 `build_clash_proxy` 为每个有效节点生成：

```yaml
- name: "vpngate.me | Japan | vpn228702251"  # 与 VLESS 备注同格式
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
