import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_csv(
    "dataset.csv",
    encoding="latin1"
)

# Load trained model
vectorizer = joblib.load("vectorizer.pkl")
query_vectors = joblib.load("query_vectors.pkl")

print("\n=== SMIU AI Student Help Desk ===\n")

while True:

    query = input("Ask your question (type exit to quit): ")

    if query.lower() == "exit":
        break

    user_vector = vectorizer.transform([query])

    similarity = cosine_similarity(
        user_vector,
        query_vectors
    )

    best_match = similarity.argmax()

    confidence = similarity.max()

    print("\n--------------------------------")

    if confidence < 0.20:

        print("❌ No suitable solution found.")
        print("🎫 Ticket should be generated.")

    else:

        print("🏢 Department:",
              data.iloc[best_match]["DEPARTMENT"])

        print("\n💡 Solution:")
        print(data.iloc[best_match]["SOLUTION"])

        print("\n⚡ Priority:",
              data.iloc[best_match]["PRIORITY"])

        print("\n🎯 Confidence:",
              round(confidence * 100, 2), "%")

    print("--------------------------------\n")