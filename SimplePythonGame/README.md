# Present the solution and explain the purpose of each line/block of lines in this code.
There are comments in the source code, it should be clear what each block is doing.

# How you tested your solution?
Q1. tested by manually going through every possible option in the menu.
Q2. tested against the examples given in the assignment instructions and a few manually crafted examples.

# Highlight a more difficult part in the code and explain in more detail how you tackled it. 
Designing the operation of state machine in Q1 was challenging. The state could change in various ways(The game requires it). Controlling state changes so that the changes were accounted for was difficult.

This problem was tackled using a uniform method of mutating state. There are no haphazard changes to variables. 


# Include possible mistakes that one could make, and indicate for each mistake how it would cause the program to fail to work and why.
When adding more "levels" to the game, all old states and conventions have to be understood. Otherwise, the game will behave in unexpected way and it will be hard to trace the issue.

Only change "state" inside an "if" of the "process_state" function.
Use `if "exit" in state and state["exit"]:` instead of direct `state["exit"]` to avoid errors. (uniform patterns everywhere)

In Q2, the assumptions of each functions are not thorougly checked. They will result in unexpected behavior if the input assumptions are not met. The functions can be modified to raise error if input if of a bad form.

The functions are designed to adhere to the assignment instructions as much as possible. 