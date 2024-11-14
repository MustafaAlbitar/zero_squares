import customtkinter as ctk
from grid import * 
from square import *
from goal import *
from move import *


class Gui():
    def __init__(self):
        pass
    
    ctk.set_appearance_mode('system')
    ctk.set_default_color_theme('green')
    
    def choseLevel(self,grid):
        app = ctk.CTk()
        app.title('Zero Squares Gaame')
        app.geometry('720x720')
        
        self.selectedLevel = ctk.CTkComboBox(app, values=[f'level {i+1}' for i in range(7)])
        self.selectedLevel.pack(pady = 20)
        
        self.gameCanvas = ctk.CTkCanvas(app , width = 820 , height = 580 )
        self.gameCanvas.pack(pady=20)
        
        self.startLevel = ctk.CTkButton(app , text='Start Game' , command = lambda:self.startSelectedLevel(grid))
        self.startLevel.pack(pady = 20)
        
        app.mainloop()
    
    
    def startSelectedLevel(self,grid):
        selectedLevel = self.selectedLevel.get()
        for widget in self.gameCanvas.winfo_children():
            widget.destroy()
        
        
        if selectedLevel == 'level 1':
            board , squares , goals = grid.levelOne(self.gameCanvas)
        elif selectedLevel == 'level 2':
            board , squares , goals = grid.levelTwo(self.gameCanvas)
        elif selectedLevel == 'level 3':
            board , squares , goals = grid.levelThree(self.gameCanvas)
        elif selectedLevel == 'level 4':
            board , squares , goals = grid.levelFour(self.gameCanvas)
        elif selectedLevel == 'level 5':
            board , squares , goals = grid.levelFive(self.gameCanvas)
        elif selectedLevel == 'level 6':
            board , squares , goals = grid.levelSix(self.gameCanvas)
        elif selectedLevel == 'level 7':
            board , squares , goals = grid.levelSeven(self.gameCanvas)
        else:
            print('Invalid level')
        
        self.move = Moving(board,squares,goals)
        direction = 'none'
        self.move.history.addToHistory(direction,squares,goals)
        self.gameCanvas.focus_set()
        self.gameCanvas.bind('<Right>',lambda e: self.moveRight())
        self.gameCanvas.bind('<Left>' ,lambda e: self.moveLeft())
        self.gameCanvas.bind('<Up>' ,lambda e: self.moveUp())
        self.gameCanvas.bind('<Down>' ,lambda e: self.moveDown())
        #self.gameCanvas.bind('<space>', lambda e: self.move.predictMove())
        
        
    
    def moveRight(self):
        oldSquares = self.move.squares.copy()
        for square in oldSquares:
            self.deleteSquare(self.gameCanvas,square)
        
        newSquares , reachedGoals = self.move.move('right')
        
        for goal in reachedGoals:
            self.deleteGoal(self.gameCanvas,goal)
        
        self.drawGoals(self.gameCanvas,self.move.goals)
        
        self.drawSquares(self.gameCanvas,newSquares)
        
        if self.move.isGameEnd() == 'gameOver':
            self.gameOver(self.gameCanvas)
        if self.move.isGameEnd() == 'win':
            self.win(self.gameCanvas)
    
    
    def moveLeft(self):
        oldSquares = self.move.squares.copy()
        for square in oldSquares:
            self.deleteSquare(self.gameCanvas,square)
        
        newSquares , reachedGoals = self.move.move('left')
        
        for goal in reachedGoals:
            self.deleteGoal(self.gameCanvas,goal)
        
        self.drawGoals(self.gameCanvas,self.move.goals)
        
        self.drawSquares(self.gameCanvas,newSquares)
        
        if self.move.isGameEnd() == 'gameOver':
            self.gameOver(self.gameCanvas)
        if self.move.isGameEnd() == 'win':
            self.win(self.gameCanvas)
    
    
    def moveUp(self):
        oldSquares = self.move.squares.copy()
        for square in oldSquares:
            self.deleteSquare(self.gameCanvas ,square)
        
        newSquares , reachedGoals = self.move.move('up')
        
        for goal in reachedGoals:
            self.deleteGoal(self.gameCanvas,goal)
        
        self.drawGoals(self.gameCanvas,self.move.goals)
        
        self.drawSquares(self.gameCanvas,newSquares)
        
        if self.move.isGameEnd() == 'gameOver':
            self.gameOver(self.gameCanvas)
        if self.move.isGameEnd() == 'win':
            self.win(self.gameCanvas)
    
    def moveDown(self):
        oldSquares = self.move.squares.copy()
        for square in oldSquares:
            self.deleteSquare(self.gameCanvas ,square)
        
        newSquares , reachedGoals = self.move.move('down')
        
        for goal in reachedGoals:
            self.deleteGoal(self.gameCanvas,goal)
        
        self.drawGoals(self.gameCanvas,self.move.goals)
        
        self.drawSquares(self.gameCanvas,newSquares)
        
        if self.move.isGameEnd() == 'gameOver':
            self.gameOver(self.gameCanvas)
        if self.move.isGameEnd() == 'win':
            self.win(self.gameCanvas)
    
    
    def drawGrid(self,canvas,board):
        cellWidth = 55 
        cellHeight = 55
        paddingWiith = 65
        paddingHeight = 65
        
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col] == 'B':
                    color = 'black'
                    paddingColor = 'lightgray'
                if board[row][col] == 'W':
                    color = 'white'
                    paddingColor = 'white'
                if board[row][col] == 'F':
                    color = 'white'
                    paddingColor = 'black'
                else:
                    color == 'red'
                
                paddingFrame = ctk.CTkFrame(canvas , width=paddingWiith, height= paddingHeight, fg_color=paddingColor)
                paddingFrame.grid(row = row , column = col ,padx=1,pady=1)
                
                cellFrame = ctk.CTkFrame(paddingFrame,width= cellWidth, height= cellHeight, fg_color=color)
                cellFrame.pack(padx=5,pady=5)
                
    
    
    def drawSquares(self,canvas,squares):
        for square in squares:
            self.drawSquare(canvas,square)
    
    
    def drawSquare(self,canvas,square):
        
        paddingFrame = ctk.CTkFrame(canvas, width=50, height=50, fg_color=square.color)
        paddingFrame.grid(row=square.row, column=square.column, padx=1, pady=1)
        
        # cellFrame = ctk.CTkFrame(paddingFrame, width=squareWidth, height=squareHeight, fg_color=square.color)
        # cellFrame.pack(padx=5, pady=5)
    
    
    def drawGoals(self,canvas,goals):
        for goal in goals:
            self.drawGoal(canvas,goal)
    
    
    def drawGoal(self,canvas,goal):
        goalWidth = 55
        goalHeight = 55
        paddingWidth = 65
        paddingHeight = 65
        
        paddingFrame = ctk.CTkFrame(canvas, width=paddingWidth, height=paddingHeight, fg_color=goal.color)
        paddingFrame.grid(row=goal.row, column=goal.column, padx=1, pady=1)
        
        cellFrame = ctk.CTkFrame(paddingFrame, width=goalWidth, height=goalHeight, fg_color='white')
        cellFrame.pack(padx=5, pady=5)
    
    
    def deleteSquare(self, canvas, square):
        for widget in canvas.winfo_children():
            gridInfo = widget.grid_info()
            if gridInfo.get('row') == square.row and gridInfo.get('column') == square.column:
                widget.destroy()

    def deleteGoal(self, canvas, goal):
        for widget in canvas.winfo_children():
            gridInfo = widget.grid_info()
            if gridInfo.get('row') == goal.row and gridInfo.get('column') == goal.column:
                widget.destroy()
    
    def gameOver(self, canvas):
        for widget in canvas.winfo_children():
            widget.destroy()

        messageFrame = ctk.CTkFrame(canvas, width=400, height=200, fg_color='darkred', corner_radius=20)
        messageFrame.place(relx=0.5, rely=0.5, anchor='center')

        gameOverLabel = ctk.CTkLabel(
            messageFrame,
            text='Game Over',
            font=('Arial', 50, 'bold'),
            text_color='white'
        )
        gameOverLabel.pack(padx=20, pady=20)
    
    def win(self, canvas):
        for widget in canvas.winfo_children():
            widget.destroy()

        messageFrame = ctk.CTkFrame(canvas, width=400, height=200, fg_color='darkgreen', corner_radius=20)
        messageFrame.place(relx=0.5, rely=0.5, anchor='center')

        winLabel = ctk.CTkLabel(
            messageFrame,
            text='You Win!',
            font=('Arial', 50, 'bold'),
            text_color='white'
        )
        winLabel.pack(padx=20, pady=20)
