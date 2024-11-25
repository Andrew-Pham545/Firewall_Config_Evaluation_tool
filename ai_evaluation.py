# ai_evaluation.py
import google.generativeai as genai
import key


genai.configure(api_key=key.API_KEY)

def evaluate_scan_result(scan_results):

    prompt = f"""
   
   Bạn là 1 chuyên gia bảo mật mạng. Tôi dùng sơ đồ mạng như thế này (tôi scan sơ đồ mạng bằng Nmap). Bạn có thể đánh giá sơ đồ mạng của tôi được không. Bạn hãy in theo cấu trúc này bằng tiếng Anh và không in đậm.

   1. Evaluate Firewall Configuration:
   - Đánh giá một cách tổng quan nhất bằng 3-4 câu.
   
   2. Risks of Firewall Configuration:
   - Những cổng đang mở có những lỗ hổng gì và sẽ bị tấn công theo kiểu gì? Đồng thời cung cấp các CVE về nó (nếu không có CVE thì không cần ghi, nếu có vẫn cứ ghi). Không cần giải thích.

   3. Solutions:
   - Hãy cho những biện pháp phù hợp nằm trong phạm vi cấu hình Firewall (không IDS, IPS) dựa theo những CVE đã cung cấp.

   Các ý trên được viết theo cấu trúc như sau:
   1. .....
   - ...
   - ...
   2. ....
   - ...
   - ...
   3. ....
   - ...
   - ...

    Firewall Scan Results:
    {scan_results}
    """


    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text
