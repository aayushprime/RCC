def process_state(user_input, state, commands):
    """
    Function that takes in the current state, user input and commands and returns the new state and commands.
    All state machine logic can be entered in this function. this function will control how the state transitions happen.
    """
    # use if else to find which command the user has entered
    if user_input.lower().strip() == "look out window":
        # for this state (accessed via state variable), for this command, we can display whatever,
        # change state to anything and add/remove commands
        # the function returns the new commands list and the new state
        print(
            "You look out the window and see a beautiful landscape. You see a forest, a river and a mountain."
            "But the window wont budge. Its jammed. Years of being closed has made it stuck."
            "The window glass is broken, but the frame is too small for you to get through."
        )
        return commands, state
    elif user_input.lower().strip() == "look at table":
        if "key" in state and state["key"]:
            print("You look at the table again, you have the key from before.")
        else:
            print(
                "The table is very dusty. You can see a few coins on the table. You can also see a key."
                "The table has no drawers or compartments."
            )
            commands.append("take the key")
        return commands, state
    elif user_input.lower().strip() == "go through window":
        print("The opening is too small. You won't fit through the window.")
        return commands, state
    elif user_input.lower().strip() == "take the key":
        print("You now have a key." "You wonder what lock it will open.")
        state["key"] = True
        commands.remove("take the key")
        return commands, state
    elif user_input.lower().strip() == "go up ladder":
        print(
            "You climb the ladder only to be stuck at the top. The top of the ceiling has a iron trapdoor. It won't open easily."
            "There is a keyhole. Maybe a key could help."
        )
        state["key"] = True
        commands.append("open trapdoor with key")
        return commands, state
    elif user_input.lower().strip() == "open trapdoor with key":
        print(
            "You try to insert the key to the keyhole. It doesn't fit. You try again and again. It still doesn't fit."
            "It seems this is not the key for the trapdoor."
        )
        return commands, state
    elif user_input.lower().strip() == "look at cupboard":
        print(
            "The cupboard has two doors that cover the entire front. There are no places to see through inside."
            "There is a keyhole. The cupboard is locked."
        )
        commands.append("open cupboard with key")
        return commands, state
    elif user_input.lower().strip() == "open cupboard with key":
        if "key" in state and state["key"]:
            print(
                "You insert the key into the keyhole. It fits! You turn the key and the door opens."
                "You open the door and its dissapointing, there is nothing inside."
                "You close the door and the key falls out. You pick it up."
            )
            commands.remove("open cupboard with key")
        else:
            print("You will need a key to open the cupboard.")
        return commands, state
    elif user_input.lower().strip() == "look at fireplace":
        print(
            "The fireplace is empty. There is no fire."
            "The chimney is quite big. You could fit through it."
        )
        commands.append("climb through chimney")
        return commands, state
    elif user_input.lower().strip() == "climb through chimney":
        print(
            "You climb through the chimney. You are covered in soot. You get to the top detach the chimney cover and climb out."
        )
        state["exit"] = True
        return commands, state


def escape_room():
    # print the introduction message
    print(
        "While travelling on a not often used path you fall down a hole and find yourself in a strange room."
        "You are trapped in a room and you need to find the exit. You fell from the top and you cannot climb out that way, its too high."
        "The room has a fireplace, a table, a cupboard, a window. Quite a strange place, there are no doors in the room."
        "You can also see a ladder on the corner of the room. It seems to go into the ceiling."
    )

    # initial commands that can be entered by the user
    commands = [
        "look out window",
        "look at table",
        "go up ladder",
        "look at cupboard",
        "look at fireplace",
    ]
    # special variables that can be used to control the game (game state)
    state = {}
    while True:
        # ask user what they want to do
        user_input = input("What do you want to do? ")
        # if the user enters "list commands" show them the commands they can enter
        if user_input.lower().strip() == "list commands":
            for k in commands:
                print(k)
        else:
            # invalid command
            if user_input.lower().strip() not in [k.lower().strip() for k in commands]:
                print("That doesn't make much sense!")
                print("You must try something else!")
            # user has entered a valid command
            else:
                # send current state and user input to the process_state function
                commands, state = process_state(user_input, state, commands)
                # if the user has found the exit, end the game
                if "exit" in state and state["exit"]:
                    break

    # print the end message
    print("You make it out. That was quite the adventure.")
    print("Congratulations, you have escaped the room!")


if __name__ == "__main__":
    escape_room()
