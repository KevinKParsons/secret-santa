# secret-santa
Secret Santa Match Up Solver

Program reads in the JSON history file with names of people and their prior match up history.
Runs through all possible combinations of gift match ups and stops when a valid combination is found.

Takes into account the following rules:
- Cannot give to self
- Cannot give to the same person again (History must be cleared to reset)
- Each person must receive only one gift
- Each person must give only one gift.

User is asked if they want to save the new match up to the JSON history file.
