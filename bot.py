

import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote
import requests
from datetime import datetime, timedelta

from ether import Ether

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('ether_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File ether_query.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]


def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("\nWaiting Done, Starting....\n")
       
def main():
    while True:
        start_time = time.time()
        delay = 8*3600
        clear_terminal()
        queries = load_query()
        sum = len(queries)
        ether = Ether()
        for index, query in enumerate(queries, start=1):
            print_(f"SxG========= Account {index}/{sum} =========SxG")
            token = ether.get_token(query)
            if token is not None:
                user_info = ether.get_user_info(token)
                print_(f"TGID : {user_info.get('tgId','')} | Username : {user_info.get('tgUsername','None')} | Balance : {user_info.get('balance',0)}")
                ether.daily_bonus(token)
                ether.check_tasks(token)
        end_time = time.time()
        total = delay - (end_time-start_time)
        print_delay(total)
if __name__ == "__main__":
     main()