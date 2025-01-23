import requests
import random
import string
import threading
from termcolor import colored  
import time
url = "https://auth.roblox.com/v1/usernames/validate"
birthday = "1979-03-03T22:00:00.000Z"
context = "Signup"
OUTPUT_FILE = "hits.txt"
def generate_username(length=4):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
def get_csrf_token():
    try:
        response = requests.post(url, json={"username": "testuser"})
        if response.status_code == 403:  
            csrf_token = response.headers.get("x-csrf-token")
            if csrf_token:
                return csrf_token
            else:
                return None
        else:
            return None
    except Exception as e:
        return None
def check_username(csrf_token):
    username = generate_username()
    payload = {
        "birthday": birthday,
        "context": context,
        "username": username
    }
    headers = {
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Origin": "https://www.roblox.com",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json; charset=utf-8",
        "Origin": "https://www.roblox.com",
        "Referer": "https://www.roblox.com/",
        "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-CSRF-Token": csrf_token
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                print(colored(f"Username: {username} - [+] {data}", 'green'))  
                with open(OUTPUT_FILE, "a") as file:
                    file.write(f"{username}\n")
            elif data.get("code") == 1:
                print(colored(f"[-] {username} ", 'red'))  
            else:
                print(colored(f"[-] {username} ", 'red'))  
        else:
            csrf_token = get_csrf_token()
    except Exception as e:
        print(f"Exception occurred: {e}")
def run_loop():
    csrf_token = get_csrf_token()  
    if csrf_token:
        while True:
            check_username(csrf_token)  
    else:
        print("Unable to start the username validation process without a CSRF token.")

if __name__ == "__main__":
    run_loop()
