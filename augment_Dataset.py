# import pandas as pd
import pandas as pd
df = pd.read_excel("Dataset.csv.xlsx")

templates = [
    "Can you help me with {}?",
    "I need information about {}",
    "Please guide me regarding {}",
    "Tell me about {}",
    "Can you explain {}?",
    "I need assistance with {}",
    "How do I resolve {}?",
    "What should I do about {}?"
]

new_rows = []

for _, row in df.iterrows():

    query = str(row["STUDENT_QUERY"]).strip()

    for temp in templates:

        new_query = temp.format(query.lower())

        new_rows.append({
            "STUDENT_QUERY": new_query,
            "DEPARTMENT": row["DEPARTMENT"],
            "SOLUTION": row["SOLUTION"],
            "PRIORITY": row["PRIORITY"]
        })

augmented = pd.concat([df, pd.DataFrame(new_rows)])

augmented.drop_duplicates(
    subset=["STUDENT_QUERY"],
    inplace=True
)

augmented.to_excel(
    "English_Augmented.xlsx",
    index=False
)

print("Rows:", len(augmented))