import sys
import json
import time
from pathlib import Path
import httpx

class DoubanClient:
    def __init__(self, user_id: str, cookie: str):
        self.user_id = user_id
        self.cookie = cookie.strip()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.douban.com/",
            "Cookie": self.cookie
        }

    def fetch_all_marks(self):
        """分页获取所有观影记录，保留原始完整数据格式"""
        all_marks = []
        start = 0
        count = 50  # 每次拉取 50 条，避免过于频繁
        total = None

        print(f"开始全量拉取用户 {self.user_id} 的观影记录...")

        with httpx.Client(headers=self.headers, timeout=30.0, follow_redirects=True) as client:
            while True:
                url = f"https://m.douban.com/rexxar/api/v2/user/{self.user_id}/interests"
                params = {
                    "type": "movie",
                    "status": "done",
                    "count": count,
                    "start": start,
                    "sort": "ctime"
                }

                print(f"正在拉取: start={start} ...")
                resp = client.get(url, params=params)
                
                if resp.status_code != 200:
                    print(f"❌ 请求失败: HTTP {resp.status_code}")
                    print(resp.text)
                    break

                data = resp.json()
                
                # 第一次请求时获取总数
                if total is None:
                    total = data.get("total", 0)
                    print(f"发现总记录数: {total}")

                interests = data.get("interests", [])
                if not interests:
                    break  # 没有更多数据了，退出循环

                # ⚠️ 关键：直接保存原始 item，确保格式 100% 一致
                for item in interests:
                    # 可以在这里做一些图片域名的替换，如果你之前有用到 dou.img.lithub.cc
                    subject = item.get("subject", {})
                    if "id" in subject:
                        subject["cover_url"] = f"https://dou.img.lithub.cc/movie/{subject['id']}.jpg"
                    
                    all_marks.append(item)

                start += count
                
                # 如果已经拉完，退出
                if start >= total:
                    break
                    
                # 礼貌性延迟，防止被豆瓣封禁
                time.sleep(1.5)

        return all_marks


def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else "somkanel"
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./data")
    cookie = sys.argv[3] if len(sys.argv) > 3 else ""

    if not cookie:
        print("❌ Error: DOUBAN_COOKIE is empty!")
        sys.exit(1)

    client = DoubanClient(user_id, cookie)
    all_marks = client.fetch_all_marks()

    if not all_marks:
        print("⚠️ 未获取到任何数据，请检查 Cookie 是否有效或账号设置。")
        sys.exit(1)

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "movie.json"
    
    # 写入 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_marks, f, ensure_ascii=False, indent=2)

    print(f"✅ 同步成功！共保存 {len(all_marks)} 条记录到 {output_path}")


if __name__ == "__main__":
    main()
