from pygooglenews import GoogleNews
from textblob import TextBlob
import json


gn = GoogleNews()

search_query = '5ire blockchain'
results = gn.search(search_query)

def is_negative_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity 
    return sentiment < 0  


negative_count = 0
negative_articles = []

for entry in results['entries']:
    title = entry['title']
    if is_negative_sentiment(title): 
        negative_count += 1
        negative_articles.append({
            "Title": title,
            "Link": entry['link'],
            "Published": entry['published']
        })

try:
    with open("web3_data.json", "r", encoding="utf-8") as file:
        web3_data = json.load(file)
except FileNotFoundError:
    web3_data = {}

web3_data["Negative_Articles_Count"] = negative_count
web3_data["Negative_Articles"] = negative_articles


with open("web3_data.json", "w", encoding="utf-8") as file:
    json.dump(web3_data, file, indent=4, ensure_ascii=False)

print(f"Number of negative articles: {negative_count}")
