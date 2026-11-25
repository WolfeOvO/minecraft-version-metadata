# Minecraft Version Metadata (Mojang 官方数据镜像)

每日自动同步 Mojang 官方启动器元数据。

- `version_manifest_v2.json` — 官方全量版本清单（含 latest release/snapshot）
- `versions/<id>.json` — 每个版本的官方 JSON（启动器/客户端/服务端下载 URL + SHA1 校验，资源索引、JVM 参数、规则等）

数据源：`https://launchermeta.mojang.com/mc/game/version_manifest_v2.json`（Mojang 官方公开 API）。
仅存元数据与官方下载链接，不含游戏 jar 文件本体（jar 分发受 Mojang EULA 限制）。
更新：`python sync_mojang.py`（增量，按 SHA1 幂等），或等 GitHub Actions 每日 UTC 3:00 自动跑。
