import json
import os

# Create a class that will allow us to call upon .json attributes in our main method
class jsonHandler:

    def __init__(self):

        # Open and load both setup.json and prefixes.json
        with open('setup.json') as config_file:
            data = json.load(config_file)
        with open('prefixes.json') as prefix_file:
            prefix_data = json.load(prefix_file)

        # Assign .json attributes to class attributes
        self.discord = data['discord-bot']['discord']
        self.reddit = data['discord-bot']['reddit']
        # Create an array of subreddits given from setup.json
        # This is needed from how MemeGenerator.py is coded
        self.subreddits=[]
        for x in data['discord-bot']['reddit']['subreddits']:
            self.subreddits.append(x)
        self.prefixes = prefix_data

    # Open our prefixes.json file and write to it
    # Used when changing our prefix from its default value
    def write_prefixes(self, data, filename='prefixes.json'):
        with open(filename, 'w') as temp:
            json.dump(data, temp, indent=4)