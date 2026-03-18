# Douban Sync Action 🎬

[**🇨🇳 简体中文**](./README_zh.md) | [**🇬🇧 English**](./README.md)

A modern, fast, and stable GitHub Action to sync your Douban (豆瓣) marked data to JSON files. 

This project is inspired by and rewritten from [lizheming/doumark-action](https://github.com/lizheming/doumark-action). It drops legacy dependencies, runs on a modern Python environment, and preserves 100% of the original data structure, ensuring zero downstream breakage for your blogs or display pages.

## Features ✨

- **Full Synchronization**: Automatically paginates and fetches all your marked records (even 800+ items).
- **100% Backward Compatible**: Preserves the exact same JSON structure as the original `doumark-action`, including redundant fields and color schemes.
- **Built-in Image Proxy**: Automatically injects `cover_url` using `dou.img.lithub.cc` to bypass Douban's image anti-hotlinking.
- **Modern & Fast**: Built with Python 3.12 and `httpx`, abandoning outdated Node.js legacy code.
- **Anti-Ban Protection**: Implements polite request delays and proper headers to prevent account bans.

## Usage 🚀

Create a workflow file in your repository (e.g., `.github/workflows/douban.yml`) and add the following configuration:

```yaml
name: douban sync

on:
  schedule:
    - cron: "0 1 * * *" # Runs every day at 09:00 (UTC+8)
  workflow_dispatch:

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      # Clean up old data before syncing
      - name: Reset data directory
        shell: bash
        run: |
          rm -rf ./data
          mkdir -p ./data

      # Run Douban Sync Action
      - name: Movie Sync
        uses: somkanel/douban-sync-action@main
        with:
          id: sampleid               # Your Douban user ID
          type: movie                # Currently supports 'movie'
          format: json               # Output format
          dir: ./data                # Output directory
        env:
          DOUBAN_COOKIE: ${{ secrets.DOUBAN_COOKIE }} # Your Douban Cookie

      # Commit the synced data back to your repo
      - name: Commit and Push
        uses: EndBug/add-and-commit@v9
        with:
          message: "chore: sync douban movie data"
          add: "./data"
          default_author: github_actions
```



## Inputs ⚙️

| Input | Description | Required | Default |
| --- | --- | --- | --- |
| `id` | Your Douban user ID | **Yes** | `somkanel` |
| `type` | Type of data (`movie`, `book`, etc.) | No | `movie` |
| `format` | Output format (currently only `json`) | No | `json` |
| `dir` | Directory to save the output file | No | `./data` |

## Environment Variables 🔐

You must provide your Douban Cookie via the `env` context.

| Env Variable | Description | Required |
| --- | --- | --- |
| `DOUBAN_COOKIE` | Your Douban login cookie (stored in GitHub Secrets) | **Yes** |

> **How to get the cookie:**
> 1. Log in to [douban.com](https://www.douban.com) in your browser.
> 2. Open Developer Tools (F12) -> Application/Storage -> Cookies.
> 3. Copy the entire cookie string (must include `dbcl2`).
> 4. Save it to your repository's **Settings -> Secrets and variables -> Actions** as `DOUBAN_COOKIE`.

## Why Rewrite? 💡

The original [doumark-action](https://github.com/lizheming/doumark-action) is a great project, but it hasn't been updated for years. It relies on deprecated Node.js 16/20 environments, throwing warnings in modern GitHub Actions. 

This rewrite:
* Solves the `Node.js 20 actions are deprecated` warning.
* Fixes the `Unexpected input 'cookie'` error by moving cookies to environment variables.
* Uses Python instead of Shell/Docker nesting for easier future maintenance.

## License 📄

MIT License

