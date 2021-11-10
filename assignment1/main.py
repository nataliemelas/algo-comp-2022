#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = '/Users/nataliemelas-kyriazi/algo-comp-2022/assignment1/testdata.json'
# Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
# x_normalized = (x - x_min)/(x_max - x_min)
def compute_score(user1, user2):
    compat = 1
    if(user1.gender == user2.gender):
        compat = compat * (0.75)
    if(user1.grad_year > user2.grad_year + 3 or user1.grad_year < user2.grad_year - 3):
        compat = 0
    for i in range(0, min(len(user2.responses), len(user1.responses))):
        if(user1.responses[i] == user2.responses[i]):
            compat = compat * 5
    return compat


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
