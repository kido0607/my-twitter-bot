import os, requests, feedparser

# 스텔라이브 공식 트위터 RSS (무료 브리지 이용)
RSS_URL = "https://rsshub.app/twitter/user/stellive_kr"
WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
LAST_FILE = "last_tweet.txt"

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries: return
    
    latest_id = feed.entries[0].id
    last_id = open(LAST_FILE).read().strip() if os.path.exists(LAST_FILE) else ""

    if latest_id != last_id:
        # vxtwitter로 변환하여 사진/영상 잘 보이게 전송
        link = feed.entries[0].link.replace("x.com", "vxtwitter.com")
        requests.post(WEBHOOK_URL, json={"content": f"📢 **스텔라이브 새 소식!**\n{link}"})
        with open(LAST_FILE, "w") as f: f.write(latest_id)

if __name__ == "__main__":
    main()
