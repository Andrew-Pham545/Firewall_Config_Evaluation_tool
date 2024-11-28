# ai_evaluation.py
import google.generativeai as genai
import key


genai.configure(api_key=key.API_KEY)

def evaluate_scan_result(scan_results):

    prompt = f"""
   
    giờ tôi sẽ đưa bạn 1 file kết quả đánh giá tường lừa bằng theo định dạng json. đây là đánh giá được custom lại từ SANS firewall checklist để phù hợp với đánh giá cấu hình cho firewall của cơ sở hạ tầng mạng nhỏ (như start up, công ty nhỏ chưa tới 100 host), tôi sẽ đưa bạn bộ tiêu chí, bộ chuẩn 5 bullet point và output yêu cầu bạn in ra
   
   tiêu chí: "Review the rulesets order (in the following order)	Check anti-spoofing filter
	Check user permit rules
	Check noise drops
	Check deny and alert rules
	Check deny and log rules
Stateful inspection	Check state tables
	Ensure harmful scripts like ActiveX, Java are blocked.
	If using a URL filtering server, ensure definitions are correct.
	Check MAC address filtering if used.
Logging	Ensure logging is enabled.
	Periodically check logs for attack patterns.
Patches and updates	Ensure the firewall is updated to the latest patches.
	Check download sources (reliable websites or emails with digital signatures).
Vulnerability assessments/Testing	Ensure that the network have procedure to check for open ports using tools like nmap.
	Ensure unnecessary ports are closed.
	Check rulesets to prevent denial of service or vulnerabilities.
Compliance with security policy	Match ruleset with organizational security policies.
Block spoofed, private, and illegal IPs	Block Standard unroutables (255.255.255.255, 127.0.0.0).
	Block Private RFC1918 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
	Block Reserved addresses (240.0.0.0).
	Block Illegal addresses (0.0.0.0).
	Block UDP echo, ICMP broadcast (RFC 2644).
Port restrictions	Block unnecessary ports (e.g., TFTP - 69, RPC - 111, X Windows - 6000-6255, FTP - 21, Telnet - 23, etc.).
	Verify the port list matches organizational requirements.
Remote access	Ensure SSH (port 22) is used instead of Telnet.
File transfers	Ensure the server supporting FTP is placed on a separate subnet from the internal network.
ICMP	ICMP echo requests and replies.
Egress filtering	Ensure only traffic originating from internal IPs is allowed out.
	Log all traffic not originating from internal IPs.
Firewall redundancy	Ensure hot standby for firewall in order to lower the firewall's downtime.
"
   chuẩn 5 bulletpoint: "Công thức 5 Bullet Point Đánh Giá Cấu Hình Mạng Nhỏ
Bảo mật các quy tắc tường lửa (Firewall Rules Security)

Đánh giá khả năng thiết lập, ưu tiên và thực thi các quy tắc tường lửa. Tập trung vào các tiêu chí như chống giả mạo (spoofing), chặn các địa chỉ không hợp lệ, và kiểm soát luồng dữ liệu.

Quản lý cổng và giao thức (Port and Protocol Management)

Đánh giá cách quản lý cổng mở và giao thức được phép. Hệ thống cần đảm bảo rằng chỉ các cổng và giao thức cần thiết cho mạng nhỏ được mở, trong khi các cổng không sử dụng được chặn để giảm nguy cơ tấn công.

Giám sát và logging (Monitoring and Logging)

Đánh giá hiệu quả của việc kích hoạt logging và khả năng giám sát mạng. Logging nên được cấu hình để lưu trữ các sự kiện quan trọng và hỗ trợ phát hiện cũng như xử lý sự cố kịp thời.

Cập nhật và kiểm tra bảo mật (Patch Management and Security Testing)

Đánh giá mức độ cập nhật phần mềm và thực hiện các kiểm tra bảo mật định kỳ. Bao gồm cập nhật bản vá, đánh giá lỗ hổng, và thử nghiệm các quy tắc tường lửa để đảm bảo khả năng bảo vệ trước các mối đe dọa mới nhất.

Tính sẵn sàng và dự phòng (Availability and Redundancy)

Đánh giá các biện pháp đảm bảo tính sẵn sàng và dự phòng của hệ thống. Ví dụ: dự phòng cấu hình firewall, backup định kỳ, hoặc cơ chế hot standby để đảm bảo hoạt động liên tục ngay cả khi xảy ra sự cố."

    đây là scan esult: {scan_results}
    
    output bằng tiếng anh, không cần in đậm, ngôn từ đơn giản hơn,
    
    output tôi muốn: là 5 bullet point, mỗi bulletpoint không quá 1 câu.
    ví dụ: "•....
    •....
    •...
    •...
    •..."
   
    """
    

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text
