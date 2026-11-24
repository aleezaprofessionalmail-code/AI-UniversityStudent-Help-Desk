import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading dataset...")

# Load dataset
data = pd.read_csv(
    "dataset.csv",
    encoding="latin1"
)

# Remove empty rows
data = data.dropna()

# Queries
queries = data["STUDENT_QUERY"]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

# Convert text into vectors
# query_vectors = vectorizer.fit_transform(queries)
query_vectors = vectorizer.fit_transform(data["STUDENT_QUERY"])

# Save model files
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(query_vectors, "query_vectors.pkl")

print("\nModel Trained Successfully!")
print("Total Records:", len(data))
print("Vocabulary Size:", len(vectorizer.vocabulary_))

email_rows = data[
    data["STUDENT_QUERY"]
    .str.contains("email", case=False, na=False)
]

print("\nEMAIL RELATED QUERIES:")
print(email_rows["STUDENT_QUERY"].head(20))
print("Total Email Queries:", len(email_rows))