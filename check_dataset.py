import pandas as pd

# Load file
df = pd.read_excel("English_Augmented.xlsx")

# Step 1: Duplicate Check
print("Total Rows:", len(df))

duplicates = df.duplicated(
    subset=["STUDENT_QUERY"]
).sum()

print("Duplicate Queries:", duplicates)

# Step 2: Length Check
df["length"] = df["STUDENT_QUERY"].astype(str).str.len()

df = df[df["length"] > 10]

print("Rows after cleaning:", len(df))

# Save cleaned file
df.drop(columns=["length"], inplace=True)

df.to_excel(
    "English_Cleaned.xlsx",
    index=False
)

print("Cleaned file saved.")