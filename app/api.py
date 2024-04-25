import csv
import numpy as np
import os
from sentence_transformers import SentenceTransformer
import openai

# Initialize OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load the sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load CSV data

# Get the absolute path to the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the CSV file
csv_file = os.path.join(current_dir, 'database', 'vaping_refs.csv')

# csv_file = 'database/vaping_refs.csv'
messages = []
refs = []

with open(csv_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        messages.append(row[0])
        refs.append(row[1])

def compute_similarity(sentence1, sentence2):
    embeddings = model.encode([sentence1, sentence2])
    similarity = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    return similarity

def compare_message(message):
    for i in range(len(messages)):
        text = messages[i]
        similarity = compute_similarity(text, message)
        if similarity > 0.8:
            return refs[i]
    return None

def paraphrase_by_avatar(original_message):
    prompt = f"Please paraphrase this message: '{original_message}'"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.5,
    )
    if response.choices:
        return response.choices[0].message.content.strip()
    else:
        return None