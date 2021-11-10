import math
import random
import numpy as np
from typing import List, Tuple

import numpy

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Mssale, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    #number of people
    N = len(scores[0])
    ints_to_N = [i for i in range(0,N)]

    #creates two random groups
    proposers = random.sample(ints_to_N, math.ceil(N/2))
    receivers = list(set(ints_to_N) - set(proposers))

    #WHERE TO INCLUDE NON-BINARY???
    #make sure incompatible people have score 0. 
    #Cases:
    for i in range(0,N):
        for j in range(0, N):
            #gay woman
            if(gender_id[i] == "Female" and gender_pref == "Female"):
                if(i != j):
                    if(gender_id[j] != "Female" or gender_pref == "Male"):
                        scores[i][j] = 0
                        scores[j][i] = 0

            #straight woman
            elif(gender_id[i] == "Female" and gender_pref == "Male"):
                if(i != j):
                    if(gender_id[j] != "Male" or gender_pref == "Female"):
                        scores[i][j] = 0
                        scores[j][i] = 0

            #gay man
            elif(gender_id[i] == "Male" and gender_pref == "Male"):
                if(i != j):
                    if(gender_id[j] != "Male" or gender_pref == "Female"):
                        scores[i][j] = 0
                        scores[j][i] = 0
        
            #straight man
            elif(gender_id[i] == "Male" and gender_pref == "Female"):
                if(i != j):
                    if(gender_id[j] != "Female" or gender_pref == "Male"):
                        scores[i][j] = 0
                        scores[j][i] = 0
        
            #non-binary prefers man
            elif(gender_id[i] == "Non-binary" and gender_pref == "Male"):
                if(i != j):
                    if(gender_id[j] != "Male" or gender_pref != "Bisexual"):
                        scores[i][j] = 0
                        scores[j][i] = 0
        
            #non-binary prefers woman
            elif(gender_id[i] == "Non-binary" and gender_pref == "Female"):
                if(i != j):
                    if(gender_id[j] != "Female" or gender_pref == "Bisexual"):
                        scores[i][j] = 0
                        scores[j][i] = 0

            #non-binary is bi
            elif(gender_id[i] == "Non-binary" and gender_pref == "Bisexual"):
                if(i != j):
                    if(gender_pref != "Bisexual"):
                        scores[i][j] = 0
                        scores[j][i] = 0

    #create preference lists
    prop_prefs = {}
    for j in range(0, len(proposers)):
        prop_prefs[proposers[j]] = scores[proposers[j]]
    rec_pref_list = {}
    for k in range(0, len(receivers)):
        rec_pref_list[receivers[k]] = scores[receivers[k]]

    #initialize everyone unmatched
    matches = [None for i in range(0,N)]

    #allows us to make sure there are no free men
    free_men = [False for j in range(0,N)]
    for i in range(0, N):
        if i in proposers:
            free_men[i] = True
    
    free_men_id = [i for i in proposers]
    print("free men", free_men_id)

    #some man free => not all proposers matched
    #proposed to every woman => tried all combinations

    while(any(free_men)):
        #picks the next free man out of the list of proposers
        m=free_men_id[0]
            
        #gets the preference list for that man
        m_prefs = numpy.argsort(prop_prefs.get(m))[::-1]
        print("m:", m, "preferences", m_prefs)

        #going through the man's preference list
        for w in m_prefs:
            #proposer cannot match with proposer
            if w in proposers:
                continue

            if matches[w] is not None:
                print(scores[w][m], "vs", scores[w][matches[w]])  

            #if no match, then set match
            if matches[w] == None:
                matches[w] = m
                matches[m] = w
                free_men[m] = False
                print(m)
                print(free_men_id)
                free_men_id.remove(m)
                print(free_men_id)
                print(matches[m])
                print(matches[w])
                break
             

            #if more compatible match, then change woman's match
            elif scores[w][m] > scores[w][matches[w]]:
                #free old match
                matches[matches[w]] = None
                free_men[matches[w]] = True
                free_men_id.append(matches[w])
                #set new match
                matches[w] = m
                matches[m] = w
                free_men[m] = False
                free_men_id.remove(m)
                break
            
            #gets rejected
            else:
                if w == m_prefs[-1]:
                    free_men[m] = False

    match_pairs = []
    for index in matches:
        if (index, matches[index]) not in match_pairs and (matches[index], index) not in match_pairs:
            match_pairs.append((index, matches[index]))
    print(match_pairs)
    return match_pairs


if __name__ == "__main__":
    raw_scores = np.loadtxt('/Users/nataliemelas-kyriazi/algo-comp-2022/assignment2/raw_scores.txt').tolist()
    genders = []
    with open('/Users/nataliemelas-kyriazi/algo-comp-2022/assignment2/genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('/Users/nataliemelas-kyriazi/algo-comp-2022/assignment2/gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
