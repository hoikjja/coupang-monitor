import requests, re

PRODUCTS = [
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547652&vendorItemId=87051251942",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547664&vendorItemId=91089494923",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547654&vendorItemId=91089494913",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941619&vendorItemId=91089494927",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941617&vendorItemId=91089494919",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547656&vendorItemId=87051251950",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547653&vendorItemId=87051251927",
]

NTFY_TOPIC = "gaintex-bori-20241019"

def send_push(title, msg):
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode('utf-8'), headers={"Title": title})

def check(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        return "다른 판매자 보기" in r.text
    except:
        return False

# 실제 감시
for url in PRODUCTS:
    if check(url):
        send_push("🚨 쿠팡 타판매자 붙음!", f"붙음 감지!\n{url}")

# 테스트 알림 - 이게 오면 성공
send_push("✅ 테스트 성공!", "ntfy 연결 성공! 이제 중국셀러 붙을 때만 알림 옵니다")
