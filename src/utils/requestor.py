import os.path

import requests

from utils.DTO import World, Player


class Requestor:
    def __init__(self, api):
        self.api = api

    def getWorld(self):
        response = requests.get(os.path.join(self.api, 'world'))

        if response.status_code == 200:
            return World(response.json())
        else:
            print(f'{response.status_code} - {response.text}')

    def join(self):
        response = requests.post(os.path.join(self.api, 'world/join'), data={'name':'Loutre'})

        if response.status_code == 200:
            return Player(response.json())
        else:
            print(f'{response.status_code} - {response.text}')

    def getPlayer(self, id):
        response = requests.get(os.path.join(self.api, f'player/{id}'))
        if response.status_code == 200:
            return Player(response.json())
        else:
            print(f'{response.status_code} - {response.text}')

    def move(self, id, newX, newY):
        data = {'newX': newX, 'newY': newY}
        response = requests.put(os.path.join(self.api, f'player/{id}/move'), data)
        if response.status_code == 200:
            return Player(response.json())
        else:
            print(f'{response.status_code} - {response.text}')

    def quit(self, id):
        response = requests.delete(os.path.join(self.api, f'player/{id}'))
        if response.status_code == 200:
            return Player(response.json())
        else:
            print(f'{response.status_code} - {response.text}')

