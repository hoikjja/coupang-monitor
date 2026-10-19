import requests, re, time, datetime
from bs4 import BeautifulSoup

# 너가 준 옵션 7개 주소 - 그대로 감시
PRODUCTS = [
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547652&vendorItemId=87051251942",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547664&vendorItemId=91089494923",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547654&vendorItemId=91089494913",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941619&vendorItemId=91089494927",
    "https://www.coupang.com/vp/products/5197241558?itemId=24024941617&vendorItemId=91089494919",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547656&vendorItemId=87051251950",
    "https://www.coupang.com/vp/products/5197241558?itemId=7234547653&vendorItemId=87051251927",
]

# 너만의 ntfy 채널 - 앱에서 이 이름 구독하면 됨
NTFY_TOPIC = "gaintex-bori-20241019"

def check(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9"
        }
        r = requests.get(url, headers=headers, timeout=20)
        text = r.text
        
        # 핵심 감지: 다른 판매자 보기
        hijacked = "다른 판매자 보기" in text
        m = re.search(r"다른 판매자 보기\((\d+)\)", text)
        cnt = m.group(1) if m else "1"
        
        # vendorItemId 추출해서 로그용
        vid = re.search(r"vendorItemId=(\d+)", url)
        vid = vid.group(1) if vid else "unknown"
        
        return hijacked, cnt, vid
    except Exception as e:
        print(f"[에러] {e}")
        return False, "0", ""

def send_push(title, msg):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=msg.encode('utf-8'),
            headers={"Title": title, "Priority": "high", "Tags": "warning,shopping_cart"}
        )
    except Exception as e:
        print(f"푸시 에러: {e}")

print(f"=== 쿠팡 타판매자 감시 시작 ===")
print(f"채널: {NTFY_TOPIC}")
print(f"감시 상품 수: {len(PRODUCTS)}개")
print(f"간격: 10분")
print(f"핸드폰 ntfy 앱에서 '{NTFY_TOPIC}' 구독하세요!")
print("================================")

# 시작 알림 1회
send_push("쿠팡 감시 시작됨", f"7개 옵션 감시 시작. 채널: {NTFY_TOPIC}. 10분마다 체크합니다.")

while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for url in PRODUCTS:
        hijacked, cnt, vid = check(url)
        print(f"[{now}] vendorItemId={vid} -> 붙음={hijacked} ({cnt}개)")
        
        if hijacked:
            short_url = url.split('&')[0]  # 로그 간소화
            message = f"""🚨 타판매자 붙음 감지!

상품ID: {vid}
다른판매자: {cnt}개
시간: {now}

링크:
{url}

빨리 쿠팡윙 > 상품관리 > 지식재산권 신고 하세요!
"""
            send_push(f"🚨 쿠팡 타판매자 {cnt}개 붙음!", message)
            # 붙었을 때는 중복 알림 방지 위해 10분 쉬고 다시 체크하지만, 계속 알림은 가게 둠
            
    print(f"--- {now} 체크 완료, 10분 대기 ---")
    time.sleep(600)
