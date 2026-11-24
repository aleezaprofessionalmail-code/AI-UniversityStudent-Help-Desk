import requests

response = requests.post(
    "http://127.0.0.1:5000/chat",
    json={
        "query":"forgot my lms password"
    }
)

print(response.json())