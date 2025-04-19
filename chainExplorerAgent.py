import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://5irescan.io/tokens"
driver.get(url)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.w-full.table-auto.undefined")))

soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find("table", class_="w-full table-auto undefined")

token_data = []

if table:
    rows = table.find("tbody").find_all("tr")

    for row in rows:
        columns = row.find_all("td")
        if columns:
            try:
                token_info = {
                    "name": columns[0].text.strip(),
                    "contract_address": columns[1].text.strip(),
                    "holders": columns[3].text.strip(),
                }

                total_supply_div = columns[2].find("div", class_="whitespace-nowrap")
                if total_supply_div:
                    total_supply_text = total_supply_div.text.strip().replace("\u202f", "").replace(" ", "")
                    token_info["total_supply"] = int(total_supply_text) if total_supply_text.isdigit() else 0
                else:
                    token_info["total_supply"] = 0  
                
                token_data.append(token_info)
            except Exception as e:
                print(f"Error processing row: {e}")

else:
    print("Table not found.")

driver.quit()

cleaned_data = [token for token in token_data if token["total_supply"] > 0]

unique_tokens = []
seen = set()
for token in cleaned_data:
    token_key = (token["name"], token["contract_address"])
    if token_key not in seen:
        seen.add(token_key)
        unique_tokens.append(token)

total_supplies = [token["total_supply"] for token in unique_tokens]

def gini_coefficient(data):
    if len(data) < 2:  
        return 0
    
    data = np.array(data, dtype=np.float64)  
    data_sorted = np.sort(data)
    n = len(data_sorted)
    
    cumulative_sum = np.cumsum(data_sorted)
    sum_of_values = cumulative_sum[-1]
    
    if sum_of_values == 0: 
        return 0

    gini_index = (2 * np.sum((np.arange(1, n + 1) * data_sorted))) / (n * sum_of_values) - (n + 1) / n
    return max(0, min(gini_index, 1))

gini_score = gini_coefficient(total_supplies[:10]) 
try:
            with open("web3_data.json", "r", encoding="utf-8") as f:
                web3_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
            web3_data = {}
web3_data["gini_score"] = gini_score
with open("web3_data.json", "w", encoding="utf-8") as f:
            json.dump(web3_data, f, indent=4, ensure_ascii=False)


print(f"Gini Coefficient for the first 10 tokens: {gini_score:.5f}")
