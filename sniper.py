"""Syntax Username Sniper"""

import itertools
import string
import queue                                                                                                             #MADE BY SYNTAX
import threading
from time import sleep, time
import traceback
import random
import os
from signal import signal, SIGINT
import requests
import json
from pathlib import Path
from urllib3.exceptions import MaxRetryError
import sys

VERSION = "1.0.0"

class Config:
    """Config class"""
    def __init__(self):
        self.config = None
        self.load_config()

    def load_config(self):
        with open('data/config.json', 'a') as f:
            if os.path.getsize("data/config.json") == 0:
                f.write("{}")
                f.close()
        

    def get(self, key):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        try:
            return self.config[key]
        except KeyError:
            return None
    
    def set(self, key, value):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        self.config[key] = value
        with open('data/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        
    def get_all(self):
        with open('data/config.json', 'r') as f:
            self.config = json.load(f)
        return self.config


###############################################################
#                      Close on ctrl+c                        #
###############################################################                                                                                                                   #MADE BY SYNTAX
@staticmethod
def handler(signal_received, frame):
    
    print('\nSIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

signal(SIGINT, handler)







confirmators =  ["y", "yes", "1", "true", "t"]
negators =      ["n", "no", "0", "false", "f"]

os.makedirs("logs", exist_ok=True)
os.makedirs("results", exist_ok=True)  
os.makedirs("data", exist_ok=True)


def create_empty_file(file_path):
    file_path = Path(file_path)
    
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding='utf-8'):
            pass

def clear_file(file_path):
    file_path = Path(file_path)
    
    if file_path.exists():
        with file_path.open("w", encoding='utf-8'):
            pass


create_empty_file("logs/log.txt")
clear_file("logs/log.txt")


create_empty_file("results/hits.txt")

create_empty_file("data/names_to_check.txt")

create_empty_file("logs/error.txt")
clear_file("logs/error.txt")

create_empty_file("data/proxies.txt")

with Path("data/proxies.txt").open("r", encoding='utf-8') as proxies_file:
    proxies = proxies_file.read().splitlines()





config = Config()
lock = threading.Lock()





if len(proxies) == 0:
    proxies = [None]
proxy_cycle = itertools.cycle(proxies)



RPS =       0
REQUESTS =  0
WORKS =     0
TAKEN =     0
DEACTIVATE = False


class Logger:
    """Logger class"""
    def __init__(self, file_name: str):
        """Initiate the class"""
        self.file_name = file_name
        self.file = open(self.file_name, "a")

    def log(self, message: str):
        """Log a message to the file"""
        self.file.write(f"{message}\n")
        self.file.flush()

    def close(self):
        """Close the file"""
        self.file.close()

 


class _Colors:
    """Menu colors"""
    @staticmethod
    def _color_code(code):
        """Static method to format color codes"""
        return f'\033[{code}m'


    ENDC: str =         _color_code(0)
    BOLD: str =         _color_code(1)
    UNDERLINE: str =    _color_code(4)
    BLACK: str =        _color_code(30)
    RED: str =          _color_code(31)
    GREEN: str =        _color_code(32)
    YELLOW: str =       _color_code(33)
    BLUE: str =         _color_code(34)
    MAGENTA: str =      _color_code(35)
    CYAN: str =         _color_code(36)
    WHITE: str =        _color_code(37)
    REDBG: str =        _color_code(41)
    GREENBG: str =      _color_code(42)
    YELLOWBG: str =     _color_code(43)
    BLUEBG: str =       _color_code(44)
    MAGENTABG: str =    _color_code(45)
    CYANBG: str =       _color_code(46)
    WHITEBG: str =      _color_code(47)
    GREY: str =         _color_code(90)


Colors = _Colors()

Logger = Logger("logs/log.txt")


Logger.log(f"CloudChecker started at {time()}")



def clear():
    """Clear the screen"""
    os.system('cls' if os.name=='nt' else 'clear')

clear()

class Pomelo:
    """Syntax"""
    def __init__(self):
        """Initiate the class"""
        self.endpoint = "https://discord.com/api/v9"
        self.headers_post = {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.proxies_not_working = []
        self.remove_proxies = config.get("remove_proxies")
        self.timeout = config.get("timeout")
        if self.timeout is None:
            self.timeout = 30

        Logger.log(f"Timeout set to {self.timeout}")
        Logger.log(f"Remove proxies set to {self.remove_proxies}")
        Logger.log(f"Headers set to {self.headers_post}")



    def proxy_err(self, name, proxy, proxy_cycle):
        name = [name, next(proxy_cycle)]
        Logger.log(f"ReadTimeout with proxy {proxy}")
        if self.remove_proxies and proxy != None:
            Logger.log(f"Removing proxy {proxy}")
            self.proxies_not_working.append(proxy)
        
        
    def  check(self, name: list):
        """Check if the name is available"""

    
        
        global RPS, REQUESTS, WORKS, TAKEN, DEACTIVATE
        while not DEACTIVATE:
            try:
                try:
                    name, proxy = name
                
                except ValueError:
                    if proxy_cycle is None:
                        proxy = None
                    else:
                        proxy = next(proxy_cycle)
                        if len(self.proxies_not_working) >= len(proxies):
                            Logger.log(f"Exiting because all proxies are not working")
                            
                            DEACTIVATE = True
                            
                            Logger.log(f"Clearing queue")
                            while queue.qsize() > 0:
                                queue.get()
                                queue.task_done()
                            Logger.log(f"Queue cleared")
                            sleep(self.timeout+1)
                            print(f"\n{Colors.RED}No proxies left{Colors.ENDC}"*3)
                            
                            
                        while proxy in self.proxies_not_working:
                            proxy = next(proxy_cycle)
                        
                if proxy is not None:
                    proxy = f"http://{str(proxy).strip()}"

                
                

                r = self.session.post(
                    url=self.endpoint + "/unique-username/username-attempt-unauthed",
                    headers = self.headers_post,
                    json={"username": name},
                    proxies={"http": proxy, "https": proxy},
                    timeout=self.timeout
                ) 
                REQUESTS += 1

                if r.status_code in [200, 201, 204]:
                    if str(r.json()) in ["", None, "{}"]:
                        Logger.log(f"Unexpected response resp = {r.text}")
                        return self.check(name)
                    

                    elif r.json()["taken"]:
                        TAKEN += 1
                        return [False, r.json(), r.status_code]

                    elif not r.json()["taken"]:
                        WORKS += 1
                        return [True, r.json(), r.status_code]

                
                elif r.status_code == 429:
                    if proxy is None or proxy == "None" or proxy == "":

                        print("PROXYLESS RATELIMITED SLEEPING")
                        sleep(r.json()["retry_after"])
                        name = [name, next(proxy_cycle)]
                        return self.check(name)
                else:
                    Logger.log(f"Unknown error with request {r.status_code}    |   {r.json()}")

            except requests.exceptions.ProxyError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)

            except requests.exceptions.ConnectionError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)
            
            except requests.exceptions.ReadTimeout:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)
            
            except MaxRetryError:
                self.proxy_err(name, proxy, proxy_cycle)
                return self.check(name)



            except:
            
                with lock:
                    try:
                        exception = traceback.format_exc()
                        Logger.log(f"Unknown error with proxy {proxy}")
                        with open("logs/error.txt", "w") as f:
                            f.write(f"{exception}\n")
                            f.close()
                        sleep(0.3) 
                    except:
                        pass
                return self.check(name)

g = Colors.GREY
r = Colors.RED
x = Colors.ENDC
ASCII = f"""
{r}             ⠀⠀⠀⣀⡀⠀⠀⠀⣀⣶⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠤⠤⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣰⣿⡇⠀⠀⠾⠏⠁⠀⠀⠀⠀⠀⠀⠀⢀⣠⠖⠋⠀⠀⠀⠀⠀⠉⠳⢄⣀⠀⠀⠀⠀⠀⠀⠘⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⣿⣯⣁⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠒⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⣿⣿⠇⠀⠀⠀⠀⢀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠙⠉⠉⠀⠀⠀⠀⢀⣠⠟⠀⠀⠀⠀⠀⠀⠠⣷⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠋⠀⠀⠀⠀⠀⠀⠐⠄⠀⠀⠀⠀⠙⠂⠀⠀⠀⠀⠉⠑⠦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠉⣻⠀⠀⠀⣤⣄⠀
⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣧⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⢤⡿⠀⠀⢠⠋⣼⡆
⣤⣴⣧⠀⠘⣿⣦⢀⠀⠀⣀⢠⣿⣦⣄⣀⣄⣰⣾⣶⣦⣤⣄⣄⢀⢠⣦⣿⣿⣴⣦⣄⣤⣴⣿⡟⠀⠀⠀⠀⣀⣿⠇⠀⣠⢏⠎⣰⡇
⠹⣌⢿⡇⠀⠘⠻⣿⣾⣯⣿⣿⠿⡿⣿⣿⢿⣟⣟⣿⣿⣿⣿⣯⣿⣿⣿⣯⣻⣿⣿⣿⣿⡿⣿⣷⣦⣶⠀⣰⡟⠃⢀⡴⡿⢻⣸⡟⠁
⠀⠹⣼⡇⠀⠀⠀⠀⠉⠛⠷⣯⣷⣿⡿⠿⠿⠿⢿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣷⣿⣿⡿⠿⠛⢧⣤⣖⠛⢁⣶⠾⠟⠀⠀
⠀⠀⠹⡆⠀⠀⠰⢶⣞⠳⣀⠀⠈⠀⠀⠀⠀⣠⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠋⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢻⣦⣸⠇⠀⠀⠀⠀⠐⣯⣿⣾⣯⣧⣾⣧⣾⣷⣿⣿⣼⣧⣿⠟⠀⢠⡀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣀⣀⡙⢀⣰⣿⣿⣶⣦⡳⣤⣄⣸⣿⠛⢿⣿⣿⣿⣿⠿⣿⣀⣠⣤⡶⢿⡟⠻⣿⣿⣦⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣆⢀⣾⠿⣿⡿⠋⠙⣿⡃⠄⠈⠀⠀⠙⠛⡝⢿⣶⣯⣯⠟⢶⡶⠛⠉⠀⠀⠀⠚⢃⠀⠀⠙⢿⡿⠟⠛⣇⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢹⣉⡡⠄⠉⢀⠂⠘⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠉⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠈⠃⠀⡆⠀⢻⡟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⡀⠰⢄⢠⡇⠀⠀⠀⢀⣴⣶⣷⣷⣶⣤⡀⠀⠀⠀⠀⠀⣠⣴⣶⣶⣶⣄⡀⠀⠀⠈⢀⡇⢠⠀⢀⣽⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⡇⠀⢸⢸⡇⠀⠰⣶⣿⣿⣿⣿⣿⣿⣿⣿⣀⠀⠆⢆⣾⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⡇⢸⠀⢀⡏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣇⠀⢸⢸⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢐⡇⢸⡀⣸⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⣆⠘⢸⡀⠈⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢨⡇⣿⢷⡏⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣜⡆⡇⠀⠘⣿⡿⣝⣯⣿⣿⣿⣿⠏⠈⠀⠀⠓⠻⣿⣿⣿⣿⢯⣟⣿⣿⠃⠀⠸⣠⣟⡎⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⣿⠀⠀⠈⠻⣿⣾⣿⣿⠟⠃⠀⠀⣠⣄⠀⠀⠈⠻⣿⣯⣿⣿⠟⠃⠀⠀⣸⢸⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣳⡠⠒⠀⢀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⠾⢶⣶⣆⠀⠀⠀⠀⠐⠋⠁⠈⠉⠁⠀⠀⠀⠀⢀⣶⡶⠶⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡾⢷⣶⢤⣤⡶⣤⣴⢤⣤⠾⣷⡿⢷⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⣄⣇⠀⣙⠀⢘⣂⠀⣻⠀⣸⣄⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠉⠉⠉⠉⠉⠉⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣶⡗⠢⣄⣀⣀⡀⠀⣀⠀⢺⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣤⣧⡀⣸⣇⠀⣿⣤⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

                    {r}Syntax Username Sniper{x}          
                    {r}Async Development{x}     
                    {r}https://discord.gg/5yqxjKdyy8{x}         
                    {r}Version: {VERSION}{x}               
        """
clear()
print(ASCII)





with open("data/names_to_check.txt", "r", encoding='utf-8') as f:
    combos = f.read().splitlines()

with open("data/config.json", "r") as f:
    config_str = f.read()

if len(config_str) == 2 or os.path.getsize("data/config.json") == 0 or config.get("remove_proxies") is None:
    if config.get("webhook") is None:
        ask_webhook = input(f"Send hits to webhook [y/n] ")
        if ask_webhook.lower() in confirmators:
            webhook = input(f"Webhook url ")
            config.set("webhook", webhook)
            print(f"Use <name> to send the name of the hit \nuse <@userid> to mention the user (replace user id with actual id)\n<time> to send timestamp of the hit\nUse <RPS> to send requests per second\nUse <elapsed> to send elapsed time")
            message = input(f"Message to send ")
            config.set("message", message)
        else:
            config.set("webhook", None)
    if config.get("remove_proxies") is None:
        ask_proxy = input(f"Use proxies [y/n] ")
        ask_timeout = input(f"Timeout in seconds (Default: 30) ")
        config.set("timeout", int(ask_timeout))
        if ask_proxy.lower() in confirmators:
            ask_proxy = input(f"Rotating proxies ? (login:pass@host:port) [y/n] ")
            if ask_proxy.lower() in confirmators:
                proxy = input(f"Proxy ")
                with open(proxy, "r", encoding='utf-8') as f:
                    proxies = f.read().splitlines()
                config.set("remove_proxies", False)

            elif ask_proxy.lower() in negators:
                print(f"Please input proxies to data/proxies.txt")
                input("Press enter to continue")
                with open("data/proxies.txt", "r", encoding='utf-8') as proxies:
                    proxies = proxies.read().splitlines()
                if len(proxies) == 0:
                    proxies = [None]
                    print(f"No proxies loaded switching to proxyless")
                else:
                    print(f"Loaded {len(proxies)} proxies")
                proxy_cycle = itertools.cycle(proxies)
                ask_remove_bad_proxies = input(f"Remove bad proxies [y/n] ")
                if ask_remove_bad_proxies.lower() in confirmators:
                    config.set("remove_proxies", False)
        elif ask_proxy.lower() in negators:
            print(f" It is recommended to use proxies\nHowever you can use proxyless mode but i recommend turning off discord client while using proxyless mode")
            config.set("remove_proxies", False)
            input("Press enter to continue")
else:
    Logger.log(f"Loaded config {config.get_all()}")



if len(combos) == 0:
    length = int(input("Length of username: "))
    chars = 'abcdefghijklmnopqrstuvwxyz'
    combos = [''.join(combo) for combo in itertools.product(chars, repeat=length)]
    with open("data/names_to_check.txt", "w", encoding='utf-8') as f:
        for combo in combos:
            f.write(combo)
            f.write("\n")
    with open("data/names_to_check.txt", "r", encoding='utf-8') as f:
        combos = f.read().splitlines()
Logger.log(f"Loaded {len(combos)} combos")
longest_name = max([len(name) for name in combos])
Logger.log(f"Longest name is {longest_name} characters long")
queue = queue.Queue()
try:
    combos = random.sample(combos, 50000)
except ValueError:
    pass
for name in combos:
    print(f"[+] Adding username = {name}", end="\r")
    name = [name.strip(), next(proxy_cycle)]
    queue.put(name)


Syntax = Pomelo()
Logger.log("Syntax Username Sniper successfully initiated")


def worker():
    """Thread worker function"""
    while queue.qsize() > 0:
        
        name = queue.get()
        try:
            x = Syntax.check(name)
            available, json, status_code = x
        except:
            with lock:
                exception = traceback.format_exc()
                with open("logs/error.txt", "a", encoding='utf-8') as f:
                    f.write(f"{exception}\nreturned={x}")
                    f.close()
            available, json, status_code = "ERROR", None, None
        name, proxy = name

        proxy_formated = str(proxy[:10]+'*'*10) if proxy else 'Proxyless'

        with lock:

            if available is True:
                print(f"[{Colors.GREEN}+{Colors.ENDC}] Available  : {Colors.GREEN}{name}{Colors.ENDC}, {' '*(longest_name-len(name))}RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC}, proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
                
                with open("results/hits.txt", "a", encoding='utf-8') as f:
                    f.write(name)
                    f.write("\n")
                    f.close()

            elif available == "RATELIMITED":
                
                print(f"[{Colors.YELLOW}?{Colors.ENDC}] TIMEOUT    : {Colors.CYAN}{json}{Colors.ENDC}, {' '*(20-int(len(str(json))))}RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC},{' '*(18-int(len(str(json)))-1)}proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
            
            elif available == "ERROR":
               
                with open("logs/error.txt", "a", encoding='utf-8') as f:
                    f.write(f"{name, json, status_code}\n")
            
            else:
                print(f"[{Colors.RED}-{Colors.ENDC}]   Taken    : {Colors.RED}{name}{Colors.ENDC}, {' '*(longest_name-len(name))}RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC},  proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
       
        queue.task_done()                



def RPS_CALCULATOR():
    """Calculate RPS (Requests per second)"""
    global RPS
    Logger.log("Started RPS calculator thread")
    while True:
        RPS_BEFORE = REQUESTS
        sleep(1)
        RPS = REQUESTS - RPS_BEFORE

start_time = time()        

def TITLE_SPINNER():
    Logger.log("Started title spinner thread")
    """Fix for windows 11 console"""
    TITLE = ["CloudChecker", "Avaible : {WORKS}", "Taken : {TAKEN}", "Requests : {REQUESTS}", "RPS : {RPS}", "Elapsed : {ELAPSED}s"]
    while True:
        for i in TITLE:
            edited = i          
            for _ in range(50):
                edited = i.format(WORKS=WORKS, TAKEN=TAKEN, REQUESTS=REQUESTS, RPS=RPS, ELAPSED=round(time()-start_time))
                os.system(f'title {edited}')
                sleep(0.01)
            sleep(1)

def WEBHOOK_PROCESSOR():
    Logger.log("Started webhook processor thread")
    """Process webhook
    Note: this function is terrible and needs to be rewritten but it works so i dont care"""
    webhook = config.get("webhook")
    message = config.get("message")
    start_time = time()  

    def return_diff(old, new):
        """Return the difference between two lists"""
        return list(set(new) - set(old))

    names = []
    last_send_time = time()  

    with open("results/hits.txt", "r", encoding='utf-8') as f:
            names = f.read().splitlines()
    
    while True:
        old_names = names
        last_send_time = 0
        with open("results/hits.txt", "r", encoding='utf-8') as f:
            names = f.read().splitlines()
        
        names_diff = return_diff(old_names, names)
        

        if len(names_diff) > 1 and last_send_time-time() < 5: 
            
            old_names = names
            old_diff = names_diff
            inloop_start = time()
            
            new_names = []

            while len(names_diff) < 10 - len(names_diff):
                
                with open("results/hits.txt", "r", encoding='utf-8') as f:
                    names = f.read().splitlines()

                names_diff = return_diff(old_names, names)

                for name in names_diff:
                    
                    if name not in str(new_names):
                        
                        new_name = name + ":!#:!#" + str(round(time()))
                        new_names.append(new_name)

                if time() - inloop_start > 10:
                    break

                sleep(0.3)

            
          
            names_diff.extend(new_names)


            payload = []
            
            for name in names_diff[::-1]:
                current_time = time()
                hittime = round(current_time)
                
                if ":!#:!#" in name:
                    name, hittime = name.split(":!#:!#")
                    
                hittime = f'<t:{hittime}:T>'

                msg = message.replace("<name>", name).replace("<time>", str(hittime)).replace("<elapsed>", str(round(current_time - start_time))).replace("<RPS>", str(RPS))
                payload.append(
                    msg
                )
            
            json = {"content": "\n".join(payload), 'username': 'Syntax Username Sniper', 'avatar_url': 'https://media.discordapp.net/attachments/1330498539499028490/1331617101827538984/pfp_old.png?ex=67924491&is=6790f311&hm=a4391070470e8929f8d31af4f74474692ccc5946691dea1097694541935dcfd8&=&format=webp&quality=lossless'}
            
            x = Syntax.session.post(
                url=webhook,
                json=json
            )
            
            
            if x.status_code == 429:
                sleep(x.json()["retry_after"])

           
            last_send_time = time()
            sleep(0.5)  
        elif len(names_diff) == 1:
            name = names_diff[0]
            current_time = time()
            hittime = f'<t:{round(current_time)}:T>'
            json = {"content": message.replace("<name>", name).replace("<time>", str(hittime)).replace("<elapsed>", str(round(current_time - start_time))).replace("<RPS>", str(RPS)), 'username': 'Syntax Username Sniper', 'avatar_url': 'https://media.discordapp.net/attachments/1330498539499028490/1331617101827538984/pfp_old.png?ex=67924491&is=6790f311&hm=a4391070470e8929f8d31af4f74474692ccc5946691dea1097694541935dcfd8&=&format=webp&quality=lossless'}
            x = Syntax.session.post(
                url=webhook,
                json=json
            )
            if x.status_code == 429:
                sleep(x.json()["retry_after"])


        sleep(1)

threading.Thread(target=RPS_CALCULATOR, daemon=True).start()


if os.name == "nt":
    threading.Thread(target=TITLE_SPINNER, daemon=True).start()

if config.get("webhook") is not None:
    threading.Thread(target=WEBHOOK_PROCESSOR, daemon=True).start()

clear()
print(ASCII)

print(f"[{Colors.YELLOW}+{Colors.ENDC}] Loaded {Colors.CYAN}{len(combos)}{Colors.ENDC} combos")
ask = input(f"How many threads {Colors.YELLOW}>>>{Colors.ENDC} ")
for _ in range(5):
    print(f"Starting in {5-_}s. with {ask} threads (Ctrl+c Abort)", end="\r")
    sleep(1)
print(f"Starting in 0s. with {ask} threads (Ctrl+c Abort)", end="\r")
ths = []

for i in range(int(ask)):
    t = threading.Thread(target=worker)
    t.daemon = True   
    t.start()
    ths.append(t)
    
Logger.log(f"Started {ask} threads")

queue.join()

print(f"[{Colors.GREEN}+{Colors.ENDC}] Done")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total requests = {Colors.CYAN}{REQUESTS}{Colors.ENDC} Note: requests wont equal to hits + taken because of sometimes requests are rate limited")                                                                                                                                       #MADE BY SYNTAX
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total valid names = {Colors.CYAN}{WORKS}{Colors.ENDC}")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total invalid names = {Colors.CYAN}{TAKEN}{Colors.ENDC}")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total time = {Colors.CYAN}{round(time()-start_time)}{Colors.ENDC} seconds")
# MADE BY SYNTAX 
