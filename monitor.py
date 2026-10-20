import requests
import time

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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.coupang.com/",
    "Cache-Control": "no-cache",
}

def send_push(title, msg):
    try:
        # 제목 영문만 (이모지 넣으면 에러)
        requests.post(f"https://ntfy.sh/{TOPIC}", data=msg.encode('utf-8'), headers={"Title": title, "Priority": "5", "Tags": "warning,rotating_light"}, timeout=10)
        print(f"[PUSH 전송] {title} - {msg}")
    except Exception as e:
        print(f"[PUSH 실패] {e}")

def check(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        print(f"-> 체크중: {url[-20:]} | 상태: {r.status_code} | 길이: {len(r.text)}")
        
        if r.status_code != 200:
            print(f"  차단 의심 상태코드 {r.status_code}")
            return False

        # 쿠팡이 봇 차단 페이지 띄우면 길이가 짧고 특정 문구가 있음
        if "Access Denied" in r.text or "차단" in r.text and len(r.text) < 5000:
            print("  봇 차단 페이지로 보임")
            send_push("Coupang Check 차단", f"차단된것 같아요 확인필요\n{url}")
            return False

        if "다른 판매자 보기" in r.text:
            print("  >>> 발견! '다른 판매자 보기'")
            return True
        else:
            print("  없음 - 정상")
            return False
            
    except Exception as e:
        print(f"  에러: {e}")
        return False

print("=== 쿠팡 감시 시작 ===")
for url in PRODUCTS:
    if check(url):
        send_push("Coupang Alert!!", f"타판매자 붙음 감지!\n{url}")
    time.sleep(3)

print("=== 체크 끝 ===")
