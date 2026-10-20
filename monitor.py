import requests, time, urllib.parse

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
    try:
        requests.post(f"https://ntfy.sh/{TOPIC}", data=msg.encode('utf-8'), headers={"Title": title, "Priority": "5", "Tags": "warning,rotating_light"}, timeout=10)
        print(f"[PUSH] {msg[:50]}")
    except Exception as e:
        print(f"PUSH 실패 {e}")

def fetch_via_proxy(url):
    # 우회 서버 2개 시도
    proxies = [
        f"https://api.allorigins.win/raw?url={urllib.parse.quote(url, safe='')}",
        f"https://corsproxy.io/?{urllib.parse.quote(url, safe='')}"
    ]
    for p_url in proxies:
        try:
            r = requests.get(p_url, timeout=20)
            print(f"  우회시도 {p_url[:30]}.. -> 상태 {r.status_code} 길이 {len(r.text)}")
            if r.status_code == 200 and len(r.text) > 1000:
                return r.text
        except Exception as e:
            print(f"  우회 실패 {e}")
    return None

print("=== 쿠팡 감시 시작 (우회버전) ===")
for url in PRODUCTS:
    print(f"-> 체크중 {url[-25:]}")
    html = fetch_via_proxy(url)
    if not html:
        print("  가져오기 실패 - 둘다 차단")
        continue

    if "다른 판매자 보기" in html:
        print("  >>> 발견! 타판매자 있음!")
        send_push("Coupang Alert!!", f"타판매자 붙음 감지!\n{url}")
    else:
        print("  정상 - 다른판매자 없음")
    
    time.sleep(4)

print("=== 체크 끝 ===")
