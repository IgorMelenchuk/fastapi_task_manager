import requests
from base64 import urlsafe_b64encode

API_KEY = ""
API_URL = "https://www.virustotal.com/api/v3/urls"


def check_url_safety(url_to_check):

    url_id = urlsafe_b64encode(url_to_check.encode()).decode().strip("=")


    headers = {
        "x-apikey": API_KEY
    }
    response = requests.get(f"{API_URL}/{url_id}", headers=headers)


    print("Request URL:", f"{API_URL}/{url_id}")
    print("Headers:", headers)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)


    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("message", f"HTTP Error {response.status_code}")}

# Проверка работы функции
result = check_url_safety("google.com")
print(result)
