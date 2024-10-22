

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
    input_coin = input("random choice coin y/n (BTC default)  : ").strip().lower()
    input_order = input("open order l(long), s(short), r(random)  : ").strip().lower()
    while True:
        start_time = time.time()
        delay = 2*3700
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
                ether.claim_ref(token)
                data_order = ether.get_order(token)
                if data_order is not None:
                    totalScore = data_order.get('totalScore',0)
                    results = data_order.get('results',{})
                    print_(f"Result Game : {results.get('orders',0)} Order | {results.get('wins',0)} Wins | {results.get('loses',0)} Loses | {results.get('winRate',0.0)} Winrate")
                    list_periods = data_order.get('periods',[])
                    detail_coin = ether.get_coins(token, input_order)
                    for list in list_periods:
                        period = list.get('period',{})
                        unlockThreshold = period.get('unlockThreshold',0)
                        detail_order = list.get('order',{})
                        id = period.get('id',1)
                        if detail_order is not None:
                            statusss = detail_order.get('status','')
                            if statusss == "CLAIM_AVAILABLE":
                                data_claim = ether.claim_order(token=token, order=detail_order)
                                if data_claim is not None:
                                    status = [True, False]
                                    if input_coin =='y':
                                        coins = random.choice(detail_coin)
                                    else:
                                        coins = detail_coin[0]
                                    if input_order == 'l':
                                        status_order = status[1]
                                    elif input_order == 's':
                                        status_order = status[0]
                                    else:
                                        status_order = random.choice(status)
                                        coin_id = coins.get('id')
                                        payload = {'coinId': coin_id, 'short': status_order, 'periodId': id}
                                        ether.post_order(token=token, payload=payload)
                            elif statusss == "NOT_WIN":
                                data_check = ether.mark_checked(token=token, order=detail_order)
                                if data_check is not None:
                                    status = [True, False]
                                    if input_coin =='y':
                                        coins = random.choice(detail_coin)
                                    else:
                                        coins = detail_coin[0]
                                    if input_order == 'l':
                                        status_order = status[1]
                                    elif input_order == 's':
                                        status_order = status[0]
                                    else:
                                        status_order = random.choice(status)
                                        coin_id = coins.get('id')
                                        payload = {'coinId': coin_id, 'short': status_order, 'periodId': id}
                                        ether.post_order(token=token, payload=payload)
                        
                        if totalScore >= unlockThreshold:
                            status = [True, False]
                            if input_coin =='y':
                                coins = random.choice(detail_coin)
                            else:
                                coins = detail_coin[0]
                            if input_order == 'l':
                                status_order = status[1]
                            elif input_order == 's':
                                status_order = status[0]
                            else:
                                status_order = random.choice(status)
                            if detail_order is None:
                                coin_id = coins.get('id')
                                payload = {'coinId': coin_id, 'short': status_order, 'periodId': id}
                                ether.post_order(token=token, payload=payload)
                        
                ether.check_tasks(token)                




        end_time = time.time()
        total = delay - (end_time-start_time)
        print_delay(total)
if __name__ == "__main__":
     main()