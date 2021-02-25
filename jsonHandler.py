import json
import os

class jsonHandler:

    def __init__(self):

        with open('setup.json') as config_file:
            data = json.load(config_file)
        with open('prefixes.json') as prefix_file:
            prefix_data = json.load(prefix_file)

        self.discord = data['discord-bot']['discord']
        self.reddit = data['discord-bot']['reddit']
        self.subreddits=[]
        for x in data['discord-bot']['reddit']['subreddits']:
            self.subreddits.append(x)
        self.prefixes = prefix_data

    def write_prefixes(self, data, filename='prefixes.json'):
        with open(filename, 'w') as temp:
            json.dump(data, temp, indent=4)