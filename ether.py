import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "https://api.miniapp.dropstab.com/api"

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

def make_request(method, url, headers, json=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, json=json)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=json, data=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=json, data=data)
        else:
            raise ValueError("Invalid method.")
        
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            retry_count += 1
            return None
        elif response.status_code >= 400:
            print_(f"Status Code: {response.status_code} | {response.text}")
            return None
        elif response.status_code >= 200:
            return response

class Ether:

    def __init__(self):
        self.header = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": '"Microsoft Edge;v=129, Not=A?Brand;v=8, Chromium;v=129, Microsoft Edge WebView2;v=129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://mdkefjwsfepf.dropstab.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    def get_token(self, query):
        url = "https://api.miniapp.dropstab.com/api/auth/login"
        #https://api.miniapp.dropstab.com/api/auth/refresh
        headers = self.header
        payload = {"webAppData": query}
        print_("Generate Token....")
        try:
            response = make_request('post', url, headers=headers, json=payload)
            if response is not None:
                data = response.json()
                token = data["jwt"]["access"]["token"]
                return token
        except Exception as e:
            print_(f"Error Detail : {e}")

    def get_user_info(self, token):
        url = "https://api.miniapp.dropstab.com/api/user/current"
        headers = {
            **self.header,
            'authorization': f"Bearer {token}"
        }
        try:
            response = make_request('get', url, headers=headers)
            if response is not None:
                data = response.json()
                return data
        except Exception as e:
            print_(f"Error Detail : {e}")

    def daily_bonus(self, token):
        url = "https://api.miniapp.dropstab.com/api/bonus/dailyBonus"
        headers = {
            **self.header,
            'authorization': f"Bearer {token}"
        }
        try:
            response = make_request('post',url, headers=headers)
            if response is not None:
                data = response.json()
                result = data.get('result',False)
                if result:
                    print_(f"Daily login Done. Streaks: {data['streaks']}")
                else:
                    print_("Daily Bonus Claimed")
        except Exception as e:
            print_(f"Error Detail : {e}")

    def check_tasks(self, token):
        url = "https://api.miniapp.dropstab.com/api/quest"
        headers = {
            **self.header,
            'authorization': f"Bearer {token}"
        }
        try:
            response = make_request('get',url, headers=headers)
            if response is not None:
                tasks = response.json()
                for task in tasks:
                    name = task.get('name','')
                    quests = task.get('quests',[])
                    print_(f"== Title Task : {name} ==")
                    for quest in quests:
                        claimAllowed = quest.get('claimAllowed',False)
                        name = quest.get('name','')
                        reward = quest.get('reward',0)
                        print_(f"Checking task {name} | Reward {reward}")
                        if claimAllowed:
                            self.claim_task(token, quest["id"], name)
                        else:
                            self.verify_task(token, quest["id"], name)
        except Exception as e:
            print_(f"Error Detail : {e}")

    def verify_task(self, token, task_id, name):
        url = f'https://api.miniapp.dropstab.com/api/quest/{task_id}/verify'
        headers = {
            **self.header,
            'authorization': f"Bearer {token}"
        }
        response = make_request('put',url, headers=headers)
        if response is not None:
            data = response.json()
            print_(f"Verification Task {name} : {data.get('status','')}")

    def claim_task(self, token, task_id, name):
        url = f"https://api.miniapp.dropstab.com/api/quest/{task_id}/claim"
        headers = {
            **self.header,
            'authorization': f"Bearer {token}"
        }
        response = make_request('put',url, headers=headers)
        if response is not None:
            data = response.json()
            print_(f"Claim Task {name} : {data.get('status','')}")

    
