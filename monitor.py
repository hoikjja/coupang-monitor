import requests

PRODUCTS = [
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547652&vendorItemId=87051251942",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547664&vendorItemId=91089494923",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547654&vendorItemId=91089494913",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941619&vendorItemId=91089494927",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941617&vendorItemId=91089494919",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547656&vendorItemId=87051251950",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547653&vendorItemId=87051251927",
]

TOPIC = "gaintex-bori-20241019"

def send_push(title, msg):
    # 제목은 영문만 (이모지 넣으면 에러)
    requests.post(f"https://ntfy.sh/{TOPIC}", data=msg.encode('utf-8'), headers={"Title": title, "Priority": "5", "Tags": "warning,rotating_light"})

def check(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        return "다른 판매자 보기" in r.text
    except:
        return False

for url in PRODUCTS:
    if check(url):
        send_push("Coupang Alert!", f"타판매자 붙음 감지!\n{url}")
send_push("Coupang Alert!", "소리 테스트! 크게 울리면 성공!\nhttps://www.coupang.com")
