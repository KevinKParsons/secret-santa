import os
import json
import random

# Overview
# Program reads in the JSON history file with names of people and their prior match up history.
# Runs through all possible combinations of gift match ups and stops when a valid combination is found.
# Takes into account the following rules:
#   Cannot give to self
#   Cannot give to the same person again (History must be cleared to reset)
#   Each person must receive only one gift
#   Each person must give only one gift.
# User is asked if they want to save the new match up to the JSON history file.

ATTEMPTS = 100  # Number of attempts before giving up


class MainClass:
    def __init__(self):
        self.people = []

        self.readHistoryJSON()
        self.printHistoryData()
        self.findMatches()
        self.printResults()
        self.askToSaveResults()

    def findMatches(self):
        for counter in range(0, ATTEMPTS):
            resetFlag = False

            # Iterate through each person
            for person in self.people:
                if person.get('givingTo') is None:

                    # Build list of indexes matching people
                    possibleRecipientsIndexes = []
                    for i in range(0, len(self.people)):
                        possibleRecipientsIndexes.append(i)

                    # Attempt to find random valid person to give gift to
                    resetFlag = True
                    while len(possibleRecipientsIndexes) != 0:
                        randomRecipientIndex = random.choice(possibleRecipientsIndexes)  # Get random index
                        recipient = self.people[randomRecipientIndex]  # Set attempted recipient
                        possibleRecipientsIndexes.remove(randomRecipientIndex)  # Remove attempted index

                        # If attempt is valid
                        if recipient['name'] not in person['pastRecipients'] \
                                and recipient['name'] != person['name'] \
                                and recipient.get('receivingFrom') is None:
                            person['givingTo'] = recipient['name']
                            recipient['receivingFrom'] = person['name']
                            resetFlag = False
                            break

                    # Reset matches if resetFlag is thrown
                    if resetFlag:
                        if counter == ATTEMPTS - 1:
                            print('\nUnable to find a valid match up. Exiting.')
                            exit()
                        else:
                            # print('Attempt ' + str(counter) + '. Invalid match up. Restarting.')
                            self.resetMatches()
                        break

            # If iterate through all people without throwing flag then break infinite loop with successful match up
            if not resetFlag:
                break

    def readHistoryJSON(self):
        PATH = os.getcwd()
        with open(PATH + '/names.json') as f:
            data = json.load(f)
        self.people = data['people']  # A list of people dictionaries

    def printHistoryData(self):
        print('\nJSON Data')
        for person in self.people:
            print('\tName: ' + person['name'])
            print('\t\tPast Recipients: ' + str(person['pastRecipients']) + '')

    def printResults(self):
        print('\nGiving List:')
        for person in self.people:
            if person['givingTo']:
                print('\t' + person['name'] + ' giving to ' + person['givingTo'])
        print('\nReceiving List:')
        for person in self.people:
            if person['receivingFrom']:
                print('\t' + person['name'] + ' receiving from ' + person['receivingFrom'])
        print('\nEveryone is matched.')

    def askToSaveResults(self):
        print('\nEnter 1 to add these recipients to the JSON history file. '
              'Enter 2 to exit without saving new recipients to history.') # Get input from user
        userInput = input()
        print('Selected: ', userInput)
        if userInput == '1':
            print('Saved history to JSON file.')
            newData = {'people': []}
            for person in self.people:
                person['pastRecipients'].append(person['givingTo'])
                person.pop('givingTo', None)
                person.pop('receivingFrom', None)
                newData['people'].append(person)

            # Write JSON to file
            with open('names.json', 'w') as json_file:
                json.dump(newData, json_file)
            exit()
        elif userInput == '2':
            print('Exiting without saving to history.')
            exit()

    def resetMatches(self):
        for person in self.people:
            person['givingTo'] = None
            person['receivingFrom'] = None


if __name__ == "__main__":
    main = MainClass()  # Initiate app
