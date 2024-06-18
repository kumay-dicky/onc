import requests
import json
import time
from colorama import Fore, Style, init
import argparse

init(autoreset=True)



def parse_arguments():
    parser = argparse.ArgumentParser(description='Blum BOT')
    parser.add_argument('--boost', type=str, choices=['y', 'n'], help='Gunakan energi booster (y/n)')
    parser.add_argument('--rocket', type=str, choices=['y', 'n'], help='Aktifkan roket (y/n)')
    args = parser.parse_args()

    if args.boost is None:
        boost_input = input("Auto use energy refill? (y/n, default n): ").strip().lower()
        args.boost = boost_input if boost_input in ['y', 'n'] else 'n'

    if args.rocket is None:
        rocket_input = input("Auto use roket? (y/n, default n): ").strip().lower()
        args.rocket = rocket_input if rocket_input in ['y', 'n'] else 'n'

    return args

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Onchain BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/onchain")
    print(Fore.YELLOW + Style.BRIGHT + "Free Konsultasi Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE ! Ngotak dikit bang. Ngoding susah2 kau tinggal rename :)\n\n")

args = parse_arguments()
cek_boost = args.boost
cek_rocket = args.rocket
set_headers = {
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://db4.onchaincoin.io/',
        'Content-Type' : 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
}
# Function to get token using query_id from query_id.txt
def get_token(query_id):
    headers = set_headers.copy()
    url = 'https://db4.onchaincoin.io/api/validate'
    data = json.dumps({
        "hash": query_id,
    })

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        try:
            print(Fore.GREEN + f"\rBerhasil mendapatkan token               ", end="", flush=True)
            token = response.json().get('token')
            return token
        except json.JSONDecodeError:
            return {"error": "Tidak ada data JSON yang valid dalam respons"}
    else:
        return None

# Function to activate rocket using the token
def activate_rocket(token):
    url = 'https://db4.onchaincoin.io/api/rocketActivation'
    headers = set_headers.copy()
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            result = response.json()
            result['status_code'] = response.status_code  # Menambahkan status_code ke dalam JSON
            return result
        except json.JSONDecodeError:
            return {"error": "Tidak ada data JSON yang valid dalam respons", "status_code": response.status_code}
    else:
        return {"error": f"Error {response.status_code}", "status_code": response.status_code}
# Function to get user info using the token
def get_info(token):
    url = 'https://db4.onchaincoin.io/api/info'
    headers = set_headers.copy()
    headers['authorization'] = f'Bearer {token}'

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Tidak ada data JSON yang valid dalam respons", "status_code": 200}
    else:
        return {"error": f"Error {response.status_code}", "status_code": response.status_code}

# Function to send clicks with rocket boost using the token
def send_clicks_with_rocket_boost(token):
    url = 'https://db4.onchaincoin.io/api/clicksWithRocketBoost'
    headers = set_headers.copy()
    headers['authorization'] = f'Bearer {token}'
    data = json.dumps({"clicks": 100})

    response = requests.post(url, headers=headers, data=data)
    try:
        return response.json()
    except json.JSONDecodeError:
        if response.text == "":
            return {"error": "Tidak ada konten dalam respons", "status_code": response.status_code}
        else:
            return {"error": "Tidak dapat mengurai JSON", "status_code": response.status_code, "response": response.text}


def send_clicks(token, total_tap):
    url = 'https://db4.onchaincoin.io/api/klick/myself/click'
    headers = set_headers.copy()
    headers['authorization'] = f'Bearer {token}'
    data = json.dumps({"clicks": total_tap})

    response = requests.post(url, headers=headers, data=data)
    try:
        return response.json()
    except json.JSONDecodeError:
        if response.text == "":
            return {"error": "Tidak ada konten dalam respons", "status_code": response.status_code}
        else:
            return {"error": "Tidak dapat mengurai JSON", "status_code": response.status_code, "response": response.text}

def use_energy(token):
    url = 'https://db4.onchaincoin.io/api/boosts/energy'
    headers = set_headers.copy()
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "Tidak ada data JSON yang valid dalam respons", "status_code": response.status_code}
    else:
        response = {"error": f"Error {response.status_code}", "status_code": response.status_code}
        return response


# Main script

if __name__ == "__main__":
    prev_coin_balance = None

    while True:
            print_welcome_message()
        # try:
            with open('query.txt', 'r') as file:
                queries = file.readlines()
            for query_data in queries:
                query_data = query_data.strip()
                print("\rGetting access token....", end="", flush=True)
                token = get_token(query_data)
                time.sleep(3)
                if token is None:
                    print(Fore.RED + Style.BRIGHT + f"\rInvalid Query ID", flush=True)
                    continue
                # Dapatkan informasi pengguna sebelum aktivasi roket
                print(Fore.GREEN + Style.BRIGHT + f"\rGetting user info...              ", end="", flush=True)
                # print(token)
                info_response = get_info(token)
                time.sleep(3)
                if 'error' in info_response:
                    if info_response['status_code'] == 429:
                        print(Fore.RED + Style.BRIGHT + f"\rError. too many request!", end="", flush=True)
                        continue
                    else:
                        print(Fore.RED + Style.BRIGHT + f"\rError getting user info. {info_response['error']}", end="", flush=True)
                        continue
                user_info = info_response.get('user', {})
                coin_balance_before_rocket = user_info.get('coins', 0)
                fullName = user_info.get('fullName', 'Tidak ada user name') 
                clicklevel = user_info.get('clickLevel', 0)
                print(Fore.CYAN + Style.BRIGHT + f"\r==== [ {fullName} ] =====                  ", flush=True)
                print(Fore.YELLOW + Style.BRIGHT + f"[ Balance ] : {coin_balance_before_rocket}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Daily Energy ] : {user_info.get('dailyEnergyRefill', 0)}")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Energy ] : {int(user_info.get('energy', 0))} - {user_info.get('maxEnergy', 0)} Max")
                print(Fore.BLUE + Style.BRIGHT + f"[ Energy Level ] : {user_info.get('energyLevel', 0)}")
                print(Fore.BLUE + Style.BRIGHT + f"[ Click Level ] : {clicklevel}")

                print(Fore.GREEN  + f"\r[ Tap ] : Tapping...", end="", flush=True)
                time.sleep(3)
                energy_save = user_info['energy']
                if energy_save < 50:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Tap ] : Low energy {int(energy_save)}")
                else:
                    energy_used = int(energy_save) - 30
                    total_tap = energy_used // clicklevel
                    time.sleep(3)
                    sent_tap = send_clicks(token,total_tap)
                    print(Fore.GREEN  + f"\r[ Tap ] : Taping...", end="", flush=True)
                    # print(sent_tap)
                    if 'error' not in sent_tap:
                        print(Fore.GREEN + Style.BRIGHT + "\r[ Tap ] : Tapped                                      ", flush=True)
                    else:
                        error_message = sent_tap.get('error', 'Terjadi kesalahan')
                        print(Fore.RED + f"\r[ Tap ] {error_message}", flush=True)
                if cek_boost == 'y':
                    if user_info.get('dailyEnergyRefill', 0) > 0:
                        print(Fore.YELLOW + Style.BRIGHT + f"[ Boost ] : Activating Energy Boost ...", end="", flush=True)  
                        time.sleep(3)
                        response = use_energy(token)
                        if response['status_code'] == 400:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Boost ] : Energy Boost Kosong             ", flush=True)
                        elif response['status_code'] == 429:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Boost ] : Too many request                ", flush=True)
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Boost ] : Energy Boost Aktif            ", flush=True)
                else:
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Boost ] : Energy boost disable", flush=True)
                if cek_rocket == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Rocket ] : Checking...", end="", flush=True)
                    time.sleep(3)
                    response = activate_rocket(token)
                    if response['status_code'] == 400:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Rocket ] : Roket Sudah Aktif             ", flush=True)
                    elif response['status_code'] == 429:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Rocket ] : Too many request                ", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Rocket ] : Roket Aktif            ", flush=True)

                        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Rocket ] : Tapping...", end="", flush=True)
                        clicks_response = send_clicks_with_rocket_boost(token)
                        time.sleep(3)
                        info_response_after = get_info(token)
                        user_info_after = info_response_after.get('user', {})
                        coin_balance_after_rocket = user_info_after.get('coins', 0)
                        total_coin = coin_balance_after_rocket - coin_balance_before_rocket
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Rocket ] : {clicks_response}        ", end="", flush=True)
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Rocket ] : You got {total_coin}         ", end="", flush=True)
                        prev_coin_balance = coin_balance_after_rocket
                else:
                    print(Fore.YELLOW + Style.BRIGHT + f"[ Rocket ] : Rocket disable", flush=True)
     
            # prev_coin_balance = coin_balance_after_rocket
        # except Exception as e:
        #     print(f"An error occurred: {str(e)}")
  
     