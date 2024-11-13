# ai_evaluation.py
import google.generativeai as genai
import key

# Configure the API key for Google Gemini
genai.configure(api_key=key.API_KEY)

def evaluate_scan_result(scan_results):
    # Define a prompt to guide Gemini in explaining results to non-technical users
    prompt = f"""
    Imagine you are a cybersecurity expert. Please evaluate the following firewall configuration data and explain it as if you were teaching someone without technical knowledge. Make the explanation clear, straightforward, and easy to follow. Avoid technical jargon and use relatable examples where possible.

    Evaluation Structure:

    1. Internal Firewall Setup:
       - Describe what the internal firewall is doing in simple terms, such as "allowing" or "blocking" types of connections.
       - Explain why these settings might be used to protect the network inside the organization.

    2. External Firewall Setup:
       - Summarize the external firewall's role, focusing on which services or applications are accessible to the outside world.
       - Describe how this setup helps in keeping certain parts of the network secure.

    3. Vulnerabilities:
       - For each open service or application, mention any risks found.
       - Explain the risks in simple terms, such as "this could allow unauthorized access" or "this could expose sensitive data."

    4. Recommendations:
       - Provide clear, simple recommendations that focus on making firewall settings more secure.
       - Suggest specific changes to firewall rules that would be easy to understand, like "close access to this service from outside" or "only allow trusted users to access."

    5. Summary:
       - Give a final overview of the firewall’s strengths and any urgent areas for improvement.

    Firewall Scan Results:
    {scan_results}
    """

    # Generate response from Gemini using provided prompt
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text
