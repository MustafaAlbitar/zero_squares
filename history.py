from square import * 
from goal import *
import copy

class History:
    def __init__(self):
        self.history = []
    
    
    def addToHistory(self,direction, squares, goals):
        squareData = [(square.row, square.column, square.color) for square in copy.deepcopy(squares)]
        goalData = [(goal.row, goal.column, goal.color) for goal in copy.deepcopy(goals)]
        
        self.history.append({'direction':direction,'squares': squareData, 'goals': goalData})
        self.printHistory()
    
    
    def printHistory(self):
        for index, state in enumerate(self.history):
            print(f'Move {index}:Direction - {state['direction']}, Squares - {state['squares']}, Goals - {state['goals']}')
    