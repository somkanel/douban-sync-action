# Douban Sync Action 🎬

[**🇨🇳 简体中文**](./README_zh.md) | [**🇬🇧 English**](./README.md)

一个现代、快速且稳定的 GitHub Action，用于将你的豆瓣（Douban）标记数据同步并保存为 JSON 文件。

本项目受到 [lizheming/doumark-action](https://github.com/lizheming/doumark-action) 的启发并进行了彻底重写。它摒弃了过时的依赖，运行在现代的 Python 环境上，并且 100% 保留了原始的数据结构，确保你现有的博客或展示页面不会受到任何影响，实现零成本迁移。

## 核心特性 ✨

* **全量同步**：自动处理分页，拉取你所有的标记记录（即使有 800+ 条记录也能轻松应对）。
* **100% 向下兼容**：保留与原版 `doumark-action` 完全一致的 JSON 结构，包括冗余字段和 `color_scheme` 数据。
* **现代且快速**：基于 Python 3.12 和 `httpx` 构建，彻底抛弃过时的 Node.js 老旧代码。
**稳定策略**：内置合理的请求间隔和 HTTP 配置，实现长期、稳定的同步备份。
  
## 使用方法 🚀

在你的仓库中创建一个 workflow 文件（例如 `.github/workflows/douban.yml`），并添加以下配置：

```yaml
name: douban sync

on:
  schedule:
    - cron: "0 1 * * *" # 每天北京时间 09:00 运行
  workflow_dispatch:

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      # 同步前清理旧数据
      - name: Reset data directory
        shell: bash
        run: |
          rm -rf ./data
          mkdir -p ./data

      # 运行豆瓣同步 Action
      - name: Movie Sync
        uses: somkanel/douban-sync-action@v1.0.0
        with:
          id: sampleid               # 你的豆瓣用户 ID
          type: movie                # 数据类型（目前支持 'movie'）
          format: json               # 输出格式
          dir: ./data                # 输出目录
        env:
          DOUBAN_COOKIE: ${{ secrets.DOUBAN_COOKIE }} # 你的豆瓣 Cookie

      # 使用原生 Git 命令提交并推送数据
      - name: Commit and Push
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add ./data
          
          if ! git diff-index --quiet HEAD; then
            git commit -m "chore: sync douban movie data"
            git push
            echo "Changes pushed successfully."
          else
            echo "No changes to commit."
          fi

## 输入参数 ⚙️

| 参数 | 描述 | 是否必填 | 默认值 |
| --- | --- | --- | --- |
| `id` | 你的豆瓣用户 ID | **是** | `somkanel` |
| `type` | 要同步的数据类型 (`movie`, `book` 等) | 否 | `movie` |
| `format` | 输出格式 (目前仅支持 `json`) | 否 | `json` |
| `dir` | 保存输出文件的目录 | 否 | `./data` |

## 环境变量 🔐

你必须通过 `env` 上下文提供你的豆瓣 Cookie。

| 环境变量 | 描述 | 是否必填 |
| --- | --- | --- |
| `DOUBAN_COOKIE` | 你的豆瓣登录 Cookie (存储在 GitHub Secrets 中) | **是** |

> **如何获取 Cookie：**
> 1. 在浏览器中登录 [douban.com](https://www.douban.com)。
> 2. 打开开发者工具 (F12) -> Application（或 Storage） -> Cookies。
> 3. 复制完整的 Cookie 字符串（必须包含 `dbcl2` 字段）。
> 4. 将其保存到你仓库的 **Settings -> Secrets and variables -> Actions** 中，命名为 `DOUBAN_COOKIE`。

## 为什么重写？ 💡

原版的 [doumark-action](https://github.com/lizheming/doumark-action) 是一个非常棒的项目，但它已经好几年没有更新了。它依赖于已被弃用的 Node.js 16/20 环境，导致在现代 GitHub Actions 中运行时会抛出警告。

这次重写带来了以下改变：
* 彻底解决了 `Node.js 20 actions are deprecated` 的警告。
* 将 Cookie 转移到环境变量中传入，修复了 `Unexpected input 'cookie'` 的错误。
* 使用 Python 替代了复杂的 Shell/Docker 嵌套结构，让未来的维护变得更加简单。

## 免责声明

本工具仅用于个人数据备份用途。请合理使用，并遵守平台的相关服务条款。

## 许可证 📄

MIT License

