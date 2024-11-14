import numpy as np 
from square import *
from goal import *
from gui import *
from prediction import *

class Grid():
    def __init__(self):
        print('Welcome to Zero Squares')
    
    def level(self):
        gui = Gui()
        gui.choseLevel(self)
    
    def levelOne(self,canvas):
        board = np.array([
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','W','W','B','W','W','W','B','B'],
            ['B','B','W','W','W','W','W','W','B','B'],
            ['B','B','W','W','W','W','W','W','B','B'],
            ['B','B','B','B','B','W','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(1, 2, 'green')]
        goals = [Goal(4, 5, 'green')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals
    
    
    def levelTwo(self,canvas):
        board = np.array([
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','W','B','B','B','B','B','B'],
            ['B','B','W','W','W','W','W','W','B','B'],
            ['B','B','W','B','W','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(3, 2, 'yellow'), Square(3, 3, 'red'), Square(3, 4, 'blue')]
        goals = [Goal(2, 3, 'yellow'), Goal(4, 4, 'red'), Goal(4, 2, 'blue')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals
    
    
    
    def levelThree(self,canvas):
        board = np.array([
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','W','W','W','W','W','W','F','B'],
            ['B','B','W','B','B','B','B','W','B','B'],
            ['B','B','W','B','B','B','B','W','B','B'],
            ['B','B','W','W','W','W','W','W','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(1,2,'green')]
        goals = [Goal(4,7,'green')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals
    
    
    
    def levelFour(self,canvas):
        board = np.array([
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','W','W','B','B','B','B'],
            ['B','W','W','W','W','W','W','W','B','B'],
            ['B','W','W','B','W','W','B','W','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(2,4,'red'),Square(3,2,'pink'),Square(3,3,'blue'),Square(4,2,'green'),Square(4,7,'yellow')]
        goals = [Goal(3,1,'blue'),Goal(2,5,'yellow'),Goal(4,2,'pink'),Goal(4,4,'red'),Goal(4,7,'green')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        
        return board,squares,goals
    
    
    def levelFive(self,canvas):
        board = np.array([
            ['B','B','B','F','B','B','B','B','B','B'],
            ['B','B','F','W','W','W','W','B','B','B'],
            ['B','F','W','W','W','W','W','B','B','B'],
            ['B','B','W','W','W','B','W','B','B','B'],
            ['B','B','W','W','W','B','W','B','B','B'],
            ['B','B','W','W','W','W','W','B','B','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(4,2,'green'),Square(5,2,'blue')]
        goals = [Goal(2,2,'green'),Goal(1,4,'blue')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals
    
    
    def levelSix(self,canvas):
        board = np.array([
            ['B','B','B','B','B','B','B','B','B','B'],
            ['B','B','W','W','W','W','W','W','B','B'],
            ['F','W','W','W','W','W','W','W','W','B'],
            ['F','W','W','B','B','B','B','B','W','B'],
            ['B','W','W','W','W','W','W','B','W','B'],
            ['B','B','W','W','W','W','W','W','W','B'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(4,1,'green'),Square(2,3,'yellow'),Square(2,5,'blue')]
        goals = [Goal(2,1,'green'),Goal(1,2,'yellow'),Square(4,6,'blue')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals
    
    
    def levelSeven(swlf,canvas):
        board = np.array([
            ['B','F','B','B','B','F','B','B','F','B'],
            ['B','W','W','W','W','W','W','W','W','B'],
            ['B','W','W','W','W','W','W','W','W','B'],
            ['B','B','W','B','B','W','B','B','W','B'],
            ['B','B','B','B','B','W','B','B','W','B'],
            ['B','B','B','B','B','W','W','W','W','F'],
            ['B','B','B','B','B','B','B','B','B','B'],
        ])
        squares = [Square(1,3,'green'),Square(1,5,'blue'),Square(1,7,'yellow')]
        goals = [Goal(2,7,'green'),Goal(1,1,'gray'),Goal(5,7,'yellow')]
        gui = Gui()
        gui.drawGrid(canvas,board)
        gui.drawGoals(canvas,goals)
        gui.drawSquares(canvas,squares)
        
        predictions = Predictions(squares, goals,board)
        predictions.BFS()
        predictions.DFS()
        
        return board,squares,goals