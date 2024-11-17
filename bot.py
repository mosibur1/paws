import requests
import json
import os
from core.helper import get_headers, countdown_timer, extract_user_data, config
from colorama import *
import random
from datetime import datetime
import time
import sys
import pyfiglet
from termcolor import colored
from tqdm import tqdm


class PAWS:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {}  # Initialize headers in the constructor

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = pyfiglet.figlet_format("", font="slant")
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" JOIN TELEGRAM @savanop121")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}@savanop")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def user_auth(self, query: str, retries=5):
        url = 'https://api.paws.community/v1/user/auth'
        data = json.dumps({'data':query, 'referralCode':'qEKFjt3Y'})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    token = result['data'][0] if isinstance(result['data'][0], str) else None
                    return token
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def user_data(self, token: str, retries=5):
        url = 'https://api.paws.community/v1/user'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def quest_lists(self, token: str, retries=5):
        url = 'https://api.paws.community/v1/quests/list'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def set_proxy(self, proxy):
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }
        if '@' in proxy:
            host_port = proxy.split('@')[-1]
        else:
            host_port = proxy.split('//')[-1]
        return host_port

    def start_quests(self, token: str, quest_id: str, retries=5):
        url = 'https://api.paws.community/v1/quests/completed'
        data = json.dumps({'questId':quest_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None

    def connect_wallet(self, token: str, wallet: str):
        url = 'https://api.paws.community/v1/user/wallet'
        data = json.dumps({'wallet': wallet})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })


        try:
            response = self.session.post(url, headers=self.headers, data=data)
            response.raise_for_status()
            result = response.json()
            if result['success']:
                self.log(Fore.GREEN + f"Successfully connected to wallet")
                return
            else:
                self.log(Fore.RED + f"Failed connected to wallet")
                return
        except (requests.RequestException, ValueError) as e:
                print(
                    f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
        except Exception as e:
            print(e)

    def claim_quests(self, token: str, quest_id: str, retries=5):
        url = 'https://api.paws.community/v1/quests/claim'
        data = json.dumps({'questId':quest_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if result['success']:
                    return result['data']
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED+Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(2)
                else:
                    return None
        
    def process_query(self, query: str, wallet: str):
        
        token = self.user_auth(query)
        if not token:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Token{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if token:
            user = self.user_data(token)
            if user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['userData']['firstname']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['gameData']['balance']} $PAWS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                account_delay = config['account_delay']
                countdown_timer(random.randint(min(account_delay), max(account_delay)))

                if wallet:
                    self.connect_wallet(token, wallet)
                    countdown_timer(random.randint(min(account_delay), max(account_delay)))

                quests = self.quest_lists(token)
                if quests:
                    for quest in quests:
                        quest_id = quest['_id']
                        rewards = quest.get('rewards', [])
                        amount = rewards[0]['amount'] if rewards and 'amount' in rewards[0] else None

                        current_progress = quest['progress']['current']
                        total_progress = quest['progress']['total']
                        claimed = quest['progress']['claimed']

                        if quest and not claimed:
                            
                            if current_progress != total_progress:
                                start = self.start_quests(token, quest_id)
                                if start:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                    countdown_timer(random.randint(min(account_delay), max(account_delay)))

                                    claim = self.claim_quests(token, quest_id)
                                    if claim:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                            f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {amount} $PAWS {Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                        )
                                    else:
                                        self.log(
                                            f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                            f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                            f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                            f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                        )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                            else:
                                claim = self.claim_quests(token, quest_id)
                                if claim:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {amount} $PAWS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                
    def add_query(self):
        query = input(f"{Fore.YELLOW}Enter the query to add: {Style.RESET_ALL}")
        with open('query.txt', 'a') as file:
            file.write(query + '\n')
        print(f"{Fore.GREEN}Query added successfully!{Style.RESET_ALL}")

    def reset_query(self):
        open('query.txt', 'w').close()
        user_agents_path = os.path.join('core', 'user_agents.json')
        with open(user_agents_path, 'w') as file:
            json.dump({}, file)
        print(f"{Fore.GREEN}All queries have been reset and user_agents.json has been cleared!{Style.RESET_ALL}")

    def add_proxy(self):
        proxy = input(f"{Fore.YELLOW}Enter the proxy to add: {Style.RESET_ALL}")
        with open('proxies.txt', 'a') as file:
            file.write(proxy + '\n')
        print(f"{Fore.GREEN}Proxy added successfully!{Style.RESET_ALL}")

    def reset_proxies(self):
        open('proxies.txt', 'w').close()
        print(f"{Fore.GREEN}All proxies have been reset!{Style.RESET_ALL}")

    def add_wallet(self):
        wallet = input(f"{Fore.YELLOW}Enter the wallet to add: {Style.RESET_ALL}")
        with open('wallets.txt', 'a') as file:
            file.write(wallet + '\n')
        print(f"{Fore.GREEN}Wallet added successfully!{Style.RESET_ALL}")

    def reset_wallets(self):
        open('wallets.txt', 'w').close()
        print(f"{Fore.GREEN}All wallets have been reset!{Style.RESET_ALL}")

    def toggle_connect_wallets(self):
        config_path = 'config.json'
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        config_data['connect_wallets'] = not config_data['connect_wallets']
        
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        
        status = "ON" if config_data['connect_wallets'] else "OFF"
        print(f"{Fore.CYAN}╔══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}Connect wallets has been turned {Fore.GREEN}{status}{Fore.CYAN} ║")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝")

    def hacker_animation(self):
        chars = "/-\|"
        for _ in range(20):
            for char in chars:
                sys.stdout.write('\r' + Fore.GREEN + Style.BRIGHT + f'Initializing PAWS Bot {char}' + Style.RESET_ALL)
                sys.stdout.flush()
                time.sleep(0.1)
        print("\n")

    def main(self):
        while True:
            self.clear_terminal()
            self.welcome()
            self.hacker_animation()
            
            menu = pyfiglet.figlet_format("SAVAN", font="slant")
            print(Fore.CYAN + menu + Style.RESET_ALL)
            
            options = [
                "Start bot", "Add query", "Reset queries", "Add proxy", "Reset proxies",
                "Add wallet", "Reset wallets", "Toggle connect wallets", "Exit"
            ]
            
            for i, option in enumerate(options, 1):
                print(colored(f"{i}. {option}", 'yellow'))
            
            choice = input(f"\n{Fore.GREEN}Enter your choice: {Style.RESET_ALL}")
            
            if choice == '1':
                secret_code = input(f"{Fore.YELLOW}Enter the secret code: {Style.RESET_ALL}")
                if secret_code == "LOVE":
                    self.start_bot()
                else:
                    print(f"{Fore.RED}Invalid secret code. Access denied.{Style.RESET_ALL}")
            elif choice == '2':
                secret_code = input(f"{Fore.YELLOW}Enter the secret code: {Style.RESET_ALL}")
                if secret_code == "VAISH":
                    self.add_query()
                else:
                    print(f"{Fore.RED}Invalid secret code. Access denied.{Style.RESET_ALL}")
            elif choice == '3':
                self.reset_query()
            elif choice == '4':
                secret_code = input(f"{Fore.YELLOW}Enter the secret code: {Style.RESET_ALL}")
                if secret_code == "BREAKUP":
                    self.add_proxy()
                else:
                    print(f"{Fore.RED}Invalid secret code. Access denied.{Style.RESET_ALL}")
            elif choice == '5':
                self.reset_proxies()
            elif choice == '6':
                secret_code = input(f"{Fore.YELLOW}Enter the secret code: {Style.RESET_ALL}")
                if secret_code == "SAVAN":
                    self.add_wallet()
                else:
                    print(f"{Fore.RED}Invalid secret code. Access denied.{Style.RESET_ALL}")
            elif choice == '7':
                self.reset_wallets()
            elif choice == '8':
                self.toggle_connect_wallets()
            elif choice == '9':
                print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def start_bot(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]
            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]
            with open('wallets.txt', 'r') as file:
                wallets = [line.strip() for line in file if line.strip()]

            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Wallets's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(wallets)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i + 1} / {len(queries)}{Style.RESET_ALL}"
                        )
                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])  # Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )
                        else:
                            self.log(Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")

                        wallet = None
                        if config['connect_wallets']:
                            if len(wallets) >= len(queries):
                                wallet = wallets[i]
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}Connect wallet:{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT}{wallet}{Style.RESET_ALL}"
                                )
                            else:
                                self.log(Fore.RED + "The number of wallets is less than the number of accounts. The connection of wallets is disabled!")

                        user_info = extract_user_data(query)
                        user_id = str(user_info.get('id'))
                        self.headers = get_headers(user_id)

                        try:
                            self.process_query(query, wallet)
                        except Exception as e:
                            self.log(f"{Fore.RED + Style.BRIGHT}An error process_query: {e}{Style.RESET_ALL}")

                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        account_delay = config['account_delay']
                        countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] PAWS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = PAWS()
    bot.clear_terminal()
    bot.welcome()
    bot.main()
