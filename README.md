first at all the state is not the full grid it is a list of squares (x position , y position , and color) and a list of goals (x position , y position , and color ) 

we have eight classes lets start 
the first class is Square it has no methods just an initializer to set the attributes (x position , y position , square color)

the next class is Goal and it has the same built of the Square class 

Grid class 
in this class the initializer has no attributes

there are eight methods
a function to choose the level wich create an object from Gui class and call a method from the Gui class we will talke about it later

and the other seven methods represents seven different levels in each method we declare an array of character witch represent the board ( 'w' for white cell , 'B' for black cell and 'f' for the fragile square) 

and then create a list of square objects and another list of goals object
then we call some methods from Gui class to sett up  the game and finally return the board ,squares list and goals list

Main class 
it just create an object from Grid class then call level method to start the program

Gui class 
in this class we have separated the 'player' from the 'game' and create the game interfaces 

now the last three classes it can't be fully explained here it needs a face-to-face conversation but i will try to clarify the general idea

Move class 
it has a method to story the move to the move history list 
a method to check the possibility of movement relative to board

a method to check the possibility of movement relative to other squares

method to sort the squares based on the moving direction to ensure that the squares will pass through as far as possible

a method to color the transparent goal with the color of the square witch pass on it 

* i make the transparent goal gray to recognize it 

a method to move the square 
a method to check if game has end (win or lose)

and finally a method to predict next states


History Class 

it has a method to make a deepcopy from each state happend (every move) and store it in the history list 

a method to print the history list 

and a method to to compare the history list with the prediction states and get the unique predictions (states that have never happened before) 

Graph class 

this class has one method to create a nodes contains the unique predictions states and connect them to the state wich the come from  
we did this to create a graph represents all possible moves in the game without repetition so when we add the solution algorithm we have a stable structure to apply search algorithms .
