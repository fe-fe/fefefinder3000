from os import system
system('cls')
del system

from time import sleep
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from win10toast import ToastNotifier
from sys import exit
from multiprocessing import Process

bell = ToastNotifier()

ID = "0T4"
URL = f"https://steamcommunity.com/id/{ID}/friends/"
TARGETS = 'targets.txt'


process = Process(name="fefefinder3000")


def get_targets():
    with open(TARGETS, 'r') as file:
        targets = file.read().split("\n")
        if targets[0] in ['end', 'kill', 'stop', 'exit']:
            raise SystemExit
    return targets


def notify(qtd, bell):
    bell.show_toast(
        title="FF3000",
         msg=f"{qtd} target(s) online",
         icon_path="icon.ico"
         )
    

rounds = 0
while True:

    with HTMLSession() as session:

        # get targets every round, so it can be updated fastly
        targets = get_targets()

        # resets the session every 50 rounds
        while rounds < 51:
            targets_online = 0
            rounds += 1
            content = session.get(URL).content
            soup = bs(content, 'html.parser')
            friends = soup.find_all('div', {"data-panel": '{"flow-children":"row"}'}) 
            for friend in friends[1:]:
                
                # steam id
                steamid = friend['data-steamid']

                if steamid not in targets:
                    pass
                else:
                    # status
                    status = friend.attrs.get('class')
                    if "offline" in status:
                        pass
                    else:
                        targets_online += 1
            
            if targets_online > 0:
                notify(targets_online, bell)
            del targets_online, content, soup, friends
                        
            sleep(60)


