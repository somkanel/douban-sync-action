import sys
import json
from pathlib import Path
import httpx
from datetime import datetime

class DoubanClient:
    def __init__(self, user_id: str, cookie: str):
        self.user_id = user_id
        self.cookie = cookie.strip()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.douban.com/",
            "Cookie": self.cookie
        }

    def fetch_marks(self, count: int = 30):
        url = f"https://m.douban.com/rexxar/api/v2/user/{self.user_id}/interests"
        params = {
            "type": "movie",
            "status": "done",
            "count": count,
            "sort": "ctime"
        }

        with httpx.Client(headers=self.headers, timeout=30.0, follow_redirects=True) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            
            marks = []
            for item in data.get("interests", []):
                subject = item.get("subject", {})
                mark = {
                    "comment": item.get("comment", ""),
                    "rating": item.get("rating"),
                    "create_time": item.get("create_time"),
                    "subject": {
                        "id": subject.get("id"),
                        "title": subject.get("title"),
                        "url": subject.get("url"),
                        "pic": subject.get("pic", {}),
                        "rating": subject.get("rating"),
                        "year": subject.get("year")
                    }
                }
                marks.append(mark)
            
            return marks


def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else "somkanel"
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./data")
    cookie = sys.argv[3] if len(sys.argv) > 3 else ""

    if not cookie:
        print("❌ Error: DOUBAN_COOKIE is empty!")
        sys.exit(1)

    print(f"开始同步用户 {user_id} 的观影记录...")

    client = DoubanClient(user_id, cookie)
    marks = client.fetch_marks(count=30)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "movie.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(marks, f, ensure_ascii=False, indent=2)

    print(f"✅ 同步成功！共获取 {len(marks)} 条记录")
    print(f"输出文件: {output_path}")


if __name__ == "__main__":
    main()
