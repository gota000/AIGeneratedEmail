import smtplib 
from email.mime.text import MIMEText 
import google.generativeai as genai
import os

EMAIL_ADDRESS = "vickski8@gmail.com"

# I had to do "$env:EMAIL_PASSWORD = 'key'"
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')  

# I had to do "$env:GEMINI_API_KEY = 'key'"
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

RECIPIENT_EMAIL = "email"
NAME = "user name"

def generate_email_content():
    """Generate both subject and message together so they match"""
    prompt = """
    You are an engineering company HR representative sending an email to a candidate who has gotten a summer internship position.
    
    Generate a complete email with THREE parts:
    1. Company name (just the company name, no extra text)
    2. A subject line (short, professional, under 10 words)
    3. The email body (2-3 paragraphs, professional tone)
    
    Format your response EXACTLY like this:
    COMPANY: [company name]
    
    SUBJECT: [your subject line here]
    
    BODY:
    [your email body here]
    
    Requirements:
    - Choose a unique random real engineering company name that is located in michigan
    - Use the SAME company name in all three parts (COMPANY, SUBJECT, and BODY)
    - Choose a random name for yourself (the HR representative)
    - The email should be concise and professional
    - The email should congratulate the recipient on getting the internship but it should not overly praise them
    - Request the recipient to reply and schedule a Zoom meeting
    - Do not use filler brackets like [Company Name] - use actual company names
    - The recipient's name is: """ + NAME + """
    
    Remember: Use COMPANY:, SUBJECT:, and BODY: labels exactly as shown above.
    """

    response = model.generate_content(prompt)
    
    # Parse the response
    text = response.text.strip()
    
    # Split 
    if "COMPANY:" in text and "SUBJECT:" in text and "BODY:" in text:
        company_part = text.split("SUBJECT:")[0].replace("COMPANY:", "").strip()
        
        subject_part = text.split("SUBJECT:")[1].split("BODY:")[0].strip()
        
        body_part = text.split("BODY:")[1].strip()
        
        return company_part, subject_part, body_part
    else:
        raise ValueError("Generated content is not in the expected format")
    
# sends the emails
def send_email_alerts():
    company_name, subject, message_body = generate_email_content()

    # MIMEText is the format for email messages
    msg = MIMEText(message_body)
    msg["Subject"] = subject
    # Set the sender display name to the company name with "HR Team" or "Recruiting"
    msg["From"] = f"{company_name} HR Team <{EMAIL_ADDRESS}>"
    msg["To"] = RECIPIENT_EMAIL

    # Send the email, it connects to the gmails SMTP server to send the emails
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string()) # you need to send the message as a string

    print(f"Email sent from '{company_name} HR Team' with subject: '{subject}'")

# main method that sends stuff
if __name__ == "__main__":
    print("Starting the Email Spammer")

    send_email_alerts()

    print("The Email Spam has completed")

