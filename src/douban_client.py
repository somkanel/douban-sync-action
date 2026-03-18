import sys
import json
from pathlib import Path
import httpx
from datetime import datetime
from .models import MovieMark, Subject, Rating

class DoubanClient:
    def __init__(self, user_id: str, cookie: str):
        self.user_id = user_id
        self.cookie = cookie
        self.base_url = "https://m.douban.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.douban.com/",
            "Cookie": cookie
        }

    def fetch_latest_marks(self, count: int = 30) -> list:
        """获取最新标记的电影"""
        url = f"{self.base_url}/rexxar/api/v2/user/{self.user_id}/interests"
        params = {
            "type": "movie",
            "status": "done",
            "count": count,
            "sort": "ctime"
        }

        with httpx.Client(headers=self.headers, timeout=30.0) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            
            marks = []
            for item in data.get("interests", []):
                subject = item.get("subject", {})
                mark = MovieMark(
                    subject=Subject(
                        id=subject.get("id"),
                        title=subject.get("title"),
                        url=subject.get("url"),
                        pic=subject.get("pic", {}),
                        year=subject.get("year")
                    ),
                    rating=Rating(value=item.get("rating", {}).get("value")),
                    comment=item.get("comment"),
                    create_time=item.get("create_time"),
                    status=item.get("status", "done")
                )
                marks.append(mark)
            
            return marks


def main():
    user_id = sys.argv[1] if len(sys.argv) > 1 else "somkanel"
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./data")
    cookie = sys.argv[3] if len(sys.argv) > 3 else ""

    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = DoubanClient(user_id, cookie)
    marks = client.fetch_latest_marks(count=30)
    
    output_path = output_dir / "movie.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([mark.dict() for mark in marks], f, ensure_ascii=False, indent=2)
    
    print(f"成功同步 {len(marks)} 条观影记录 → {output_path}")


if __name__ == "__main__":
    main()
