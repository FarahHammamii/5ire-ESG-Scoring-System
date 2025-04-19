import json
import requests
from bs4 import BeautifulSoup
import pdfplumber
import json
import requests
import pdfplumber

url = "https://hashlock.com/audits/5ire"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


audit_link = soup.find("a", href=True, string="View Report")
pdf_url = audit_link["href"]


if pdf_url:
    pdf_response = requests.get(pdf_url)
    with open("5ire_L1_Audit_Report.pdf", "wb") as pdf_file:
        pdf_file.write(pdf_response.content)

    extracted_text = ""
    with pdfplumber.open("5ire_L1_Audit_Report.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and "Secure" in text:
                start_index = text.find("Secure")
                relevant_section = text[start_index:start_index + 500]  
                relevant_section = relevant_section.replace("\n", " ") 
                relevant_section = relevant_section.replace("\u2019", "'") 
                relevant_section = relevant_section.replace("\u201c", '"').replace("\u201d", '"')
                
                print(relevant_section)
                extracted_text = relevant_section
                break  

try:
            with open("web3_data.json", "r", encoding="utf-8") as f:
                web3_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
            web3_data = {"web3_page": {}}
web3_data["Security"] = extracted_text
with open("web3_data.json", "w", encoding="utf-8") as f:
            json.dump(web3_data, f, indent=4, ensure_ascii=False)
