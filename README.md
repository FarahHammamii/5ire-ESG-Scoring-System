# 🌿 ESG Scoring System for Ethereum-based 5ire Blockchain

This project automates the **ESG (Environmental, Social, and Governance) scoring** for the 5ire blockchain — an Ethereum-based Layer 1 platform committed to sustainability and decentralization.

---

## 📊 What It Does

✅ Scrapes and processes structured and unstructured ESG-related data 
✅Integrates  DAO governance activity  
✅ Classifies this data into ESG categories using language models  
✅ Performs **sentiment analysis** to score each category  
✅ Extracts key features from structured JSON datasets (like Gini score, governance votes, engagement)  
✅ Computes a **final ESG score** based on weighted category scores  
✅ Generates a clean and professional **PDF report**  



---

## 🧠 How the Score is Computed

The ESG score is calculated using a hybrid approach:

### 🟢 1. Classification Using LLMs
We use large language models (LLMs) to classify ESG-related text into the following categories:
- **Environmental**
- **Social**
- **Governance**

This ensures that complex and nuanced ESG data is properly categorized, even when phrased informally or embedded in long paragraphs.

### 💬 2. Sentiment Analysis
Each sentence within these categories is scored using **TextBlob** to assess:
- Positive and negative sentiment
- Magnitude and context of each opinion

This quantifies the attitude of public and organizational discourse in ESG topics.

### ⚖️ 3. Feature Extraction
We extract objective, structured features directly from JSON data:
- `gini_score`: A proxy for wealth inequality
- `average_votes`: Participatory governance metric
- `average_engagement_score`: Proxy for social activity
- `Negative_Articles_Count`: Reputational risk signal
- `avg_proposal_sentiment`: Sentiment towards governance proposals

These are then combined with LLM-based classification scores to generate a final ESG score.

### 🧮 4. Final Score Formula
A weighted average is applied:
- 40% Environmental
- 30% Social
- 30% Governance

---

## 🧰 Tech Stack

- **Python**
  - TextBlob (Sentiment Analysis)
  - FPDF (PDF Report Generation)
- **Markdown → PDF Converter**
- **Web Scraping Tools**
- **GraphQL GitHub API** for real-time developer activity
- **LLMs** for ESG sentence classification (offline)

---

## 📥 Output

- `esg_report.pdf`: A professional, timestamped ESG report
- `classification.json`, `web3_data.json`: Input data structures

---

## 🛠️ Getting Started

1. Clone this repo  
2. Run the Python script to generate ESG results   
3. Share or archive the generated PDF report  

---

## 💡 Future Enhancements

- Real-time ESG dashboard  
- On-chain reputation tracking  
- AI-powered sustainability alerts  

---

## 🤝 Contributions

PRs, feedback, and improvements are always welcome!

