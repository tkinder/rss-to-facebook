import os, time, feedparser, requests

RSS_URL = os.environ["RSS_URL"]
PAGE_ID = os.environ["PAGE_ID"]
PAGE_TOKEN = os.environ["PAGE_TOKEN"]
SEEN_FILE = "seen.txt"

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE) as f:
        return set(l.strip() for l in f if l.strip())

def save_seen(ids):
    with open(SEEN_FILE, "w") as f:
        for i in ids:
            f.write(i + "\n")

def post_to_fb(message):
    url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
    data = {"message": message, "access_token": PAGE_TOKEN}
    r = requests.post(url, data=data, timeout=10)
    r.raise_for_status()

def run_once():
    seen = load_seen()
    feed = feedparser.parse(RSS_URL)
    new_seen = set(seen)
    for entry in feed.entries[:10]:
        eid = getattr(entry, "id", entry.link)
        if eid in seen:
            continue
        msg = f"{entry.title}\n{entry.link}"
        post_to_fb(msg)
        new_seen.add(eid)
    save_seen(new_seen)

if __name__ == "__main__":
    while True:
        run_once()
        time.sleep(300)  # 5 minutes
