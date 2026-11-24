import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv(
    "dataset.csv",
    encoding="latin1"
)
print(data.head())
print("Total Rows:", len(data))


vectorizer = joblib.load("vectorizer.pkl")
query_vectors = joblib.load("query_vectors.pkl")

print("Dataset Rows:", len(data))
print("Vector Rows:", query_vectors.shape[0])

def get_solution(user_query):

    user_vector = vectorizer.transform([user_query])

    similarity = cosine_similarity(
        user_vector,
        query_vectors
    )

    best_match = similarity.argmax()
    confidence = similarity.max()

    print("\n========== DEBUG ==========")
    print("User Query:", user_query)
    print("Matched Query:", data.iloc[best_match]["STUDENT_QUERY"])
    print("Confidence:", confidence)
    print("===========================\n")

    if confidence < 0.20:
        return {
            "found": False,
            "message": "No suitable solution found"
        }

    return {
        "found": True,
        "department": data.iloc[best_match]["DEPARTMENT"],
        "solution": data.iloc[best_match]["SOLUTION"],
        "priority": data.iloc[best_match]["PRIORITY"],
        "confidence": round(confidence * 100, 2)
    }

from ai_engine import get_solution
