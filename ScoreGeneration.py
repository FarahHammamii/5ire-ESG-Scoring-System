import json
from fpdf import FPDF
from datetime import datetime
from textblob import TextBlob

# Load classification and original data
with open('classification.json', 'r') as file:
    classification_data = json.load(file)

with open('web3_data.json', 'r') as file:
    web3_data = json.load(file)

# ESG category weights
CATEGORY_WEIGHTS = {
    'environmental': 0.4,
    'social': 0.3,
    'governance': 0.3
}

# Sentiment scoring (simple approximation)
def get_sentiment_score(sentence):
    return TextBlob(sentence).sentiment.polarity

# Score per category based on sentiment
def calculate_category_score(sentences):
    total_score = 0
    for sentence in sentences:
        sentiment_score = get_sentiment_score(sentence)
        if abs(sentiment_score) > 0.1:
            total_score += sentiment_score
    category_score = total_score / len(sentences) if sentences else 0
    category_score = max(0, category_score)
    return (category_score + 1) * 50  # Scale to 0-100

# Calculate ESG score
def calculate_esg_score(data):
    scores = {}
    for category_data in data['categories']:
        category = category_data['category']
        sentences = category_data['sentences']
        score = calculate_category_score(sentences)
        scores[category] = score

    final_score = sum(scores.get(cat, 0) * weight for cat, weight in CATEGORY_WEIGHTS.items())
    return round(final_score, 2), scores

# Extract ESG features
def extract_features(web3_data):
    features = {
        'Gini Score': round(web3_data.get('gini_score', 0), 2),
        'Avg Proposal Sentiment': 0.0,
        'Governance Participation (Avg Votes)': web3_data.get('governance', {}).get('average_votes', 0),
        'Avg Engagement Score': web3_data.get('average_engagement_score', 0),
        'Negative Articles Count': web3_data.get('Negative_Articles_Count', 0)
    }

    proposals = web3_data.get('governance', {}).get('proposals', [])
    if proposals:
        features['Avg Proposal Sentiment'] = round(
            sum(p['sentiment_score'] for p in proposals) / len(proposals), 2
        )

    return features

# Create PDF Report
def generate_pdf_report(esg_score, category_scores, features):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "ESG Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Final ESG Score: {esg_score}", ln=True)

    pdf.ln(5)
    for category, score in category_scores.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{category.capitalize()} Score: {round(score, 2)}", ln=True)
        pdf.set_font("Arial", "", 11)
        if category == "environmental":
            pdf.cell(0, 8, f"- Gini Score: {features['Gini Score']}", ln=True)
        elif category == "social":
            pdf.cell(0, 8, f"- Avg Engagement Score: {features['Avg Engagement Score']}", ln=True)
            pdf.cell(0, 8, f"- Negative Articles Count: {features['Negative Articles Count']}", ln=True)
        elif category == "governance":
            pdf.cell(0, 8, f"- Avg Proposal Sentiment: {features['Avg Proposal Sentiment']}", ln=True)
            pdf.cell(0, 8, f"- Governance Participation: {features['Governance Participation (Avg Votes)']}", ln=True)
        pdf.ln(5)

    # Save the PDF
    pdf.output("esg_report.pdf")
    print("PDF report generated successfully as esg_report.pdf")

# Run pipeline
final_score, category_scores = calculate_esg_score(classification_data)
features = extract_features(web3_data)
generate_pdf_report(final_score, category_scores, features)
