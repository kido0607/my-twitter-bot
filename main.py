import os, requests, feedparser

# 설정
RSS_URL = "https://rsshub.app/twitter/user/stellive_kr"
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
LAST_FILE = "last_tweet.txt"

def main():
    # 웹훅 주소 체크
    if not WEBHOOK_URL:
        print("에러: DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    # 피드 가져오기
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("새 글이 없거나 RSS 서버 응답이 없습니다.")
        return
    
    latest_id = feed.entries[0].id
    
    # 파일이 없으면 만들고 시작 (에러 방지 핵심!)
    if not os.path.exists(LAST_FILE):
        with open(LAST_FILE, "w") as f:
            f.write("")

    with open(LAST_FILE, "r") as f:
        last_id = f.read().strip()

    if latest_id != last_id:
        link = feed.entries[0].link.replace("x.com", "vxtwitter.com")
        payload = {"content": f"📢 **새 소식이 올라왔습니다!**\n{link}"}
        
        # 전송 시도
        res = requests.post(WEBHOOK_URL, json=payload)
        if res.status_code in [200, 204]:
            with open(LAST_FILE, "w") as f:
                f.write(latest_id)
            print("전송 완료!")
        else:
            print(f"전송 실패 코드: {res.status_code}")
    else:
        print("새로운 글이 없습니다.")

if __name__ == "__main__":
    main()
