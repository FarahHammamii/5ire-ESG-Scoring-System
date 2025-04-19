import requests
from textblob import TextBlob
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Load or initialize JSON data safely
try:
    with open("web3_data.json", "r", encoding="utf-8") as f:
        web3_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    web3_data = {}

# Ensure all required keys are initialized
if "governance" not in web3_data:
    web3_data["governance"] = {}
if "proposals" not in web3_data["governance"]:
    web3_data["governance"]["proposals"] = []
if "web3_page" not in web3_data:
    web3_data["web3_page"] = {}
if "community_engagement" not in web3_data:
    web3_data["community_engagement"] = []

# --- Snapshot API request (Governance Data) ---
snapshot_url = "https://hub.snapshot.org/graphql"
snapshot_headers = {"Content-Type": "application/json"}
snapshot_query = {
    "query": """
    {
      proposals(
        first: 5
        where: { space: "valnine.eth" }
        orderBy: "created"
        orderDirection: desc
      ) {
        id
        title
        votes
        author
        body 
      }
    }
    """
}

response = requests.post(snapshot_url, json=snapshot_query, headers=snapshot_headers)
data = response.json()

total_votes = 0
num_proposals = 0

if "data" in data and "proposals" in data["data"]:
    for proposal in data["data"]["proposals"]:
        total_votes += proposal["votes"]
        num_proposals += 1
        sentiment_score = TextBlob(proposal["body"]).sentiment.polarity

        web3_data["governance"]["proposals"].append({
            "title": proposal["title"],
            "sentiment_score": round(sentiment_score, 2)
        })

    avg_votes = total_votes / num_proposals if num_proposals > 0 else 0
    web3_data["governance"]["total_votes"] = total_votes
    web3_data["governance"]["average_votes"] = round(avg_votes, 2)

# --- GitHub API request (Engagement Data) ---
org = "5ire-tech"
github_url = f"https://api.github.com/orgs/{org}/repos"
github_headers = {"Accept": "application/vnd.github.v3+json"}

response = requests.get(github_url, headers=github_headers)

total_engagement = 0
repo_count = 0

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        repo_count += 1
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        watchers = repo.get("watchers_count", 0)
        open_issues = repo.get("open_issues_count", 0)

        contributors_url = f"https://api.github.com/repos/{org}/{repo['name']}/contributors"
        contributors_response = requests.get(contributors_url, headers=github_headers)
        contributors_count = len(contributors_response.json()) if contributors_response.status_code == 200 else 0

        engagement_score = (stars + forks + watchers + contributors_count) / (1 + open_issues)
        total_engagement += engagement_score

    avg_engagement = total_engagement / repo_count if repo_count > 0 else 0
    web3_data["average_engagement_score"] = round(avg_engagement, 2)

# --- Community scraping via Selenium ---
options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
url = "https://5ire.org/community"
driver.get(url)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
community_content = soup.find_all("main", class_="w-full min-h-[calc(100vh-423px)]")

for content in community_content:
    web3_data["community_engagement"].append(content.get_text(strip=True))

driver.quit()

# --- Save the final JSON ---
with open("web3_data.json", "w", encoding="utf-8") as json_file:
    json.dump(web3_data, json_file, indent=4, ensure_ascii=False)

print("✅ JSON file 'web3_data.json' created/updated successfully!")
