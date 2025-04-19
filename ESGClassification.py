import json
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

# Load JSON file
with open('web3_data.json', 'r') as file:
    data = json.load(file)

# Extract text content
text_content = data.get("web3_page", "")


# Tokenize text into sentences
nltk.download()
sentences = sent_tokenize(text_content)

# Define ESG models
models = {
    "environmental": "ESGBERT/EnvironmentalBERT-environmental",
    "social": "ESGBERT/SocialBERT-social",
    "governance": "ESGBERT/GovernanceBERT-governance"
}

# Load models and tokenizers
def load_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

# Load all ESG models
tokenizers_models = {key: load_model(model) for key, model in models.items()}

# Function to classify a sentence
def classify_sentence(sentence):
    scores = {}
    for category, (tokenizer, model) in tokenizers_models.items():
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            scores[category] = torch.softmax(outputs.logits, dim=1)[0][1].item()  # Probability of relevance
    return max(scores, key=scores.get)  # Category with highest score

# Classify sentences
classified_sentences = {"environmental": [], "social": [], "governance": []}

for sentence in sentences:
    category = classify_sentence(sentence)
    classified_sentences[category].append(sentence)
output_data = {
    "categories": []
}
# Print categorized sentences
for category, sentences in classified_sentences.items():
    category_data = {
        "category": category,
        "sentences": sentences
    }
    output_data["categories"].append(category_data)

with open('classification.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)
