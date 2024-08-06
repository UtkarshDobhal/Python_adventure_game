import time
import random
import threading
import keyboard  


chosen_weapon = None
pirate_gear = None
health = 100  
current_environment = None  

puzzles = [
    {"question": "What has keys but can't open locks?", "answer": "piano", "hint": "It's a musical instrument."},
    {"question": "What can travel around the world while staying in a corner?", "answer": "stamp", "hint": "It's something you find on letters."},
    {"question": "What has a face and two hands but no arms or legs?", "answer": "clock", "hint": "It's used to tell time."},
    {"question": "What has many teeth but cannot bite?", "answer": "comb", "hint": "You use it on your hair."}
]


current_puzzle = None
wrong_attempts = 0

def print_pause(message, delay=1):
    print(message)
    time.sleep(delay)

def intro():
    global treasure_door, fake_treasure_door, maze_door, key_door, health, current_environment
    health = 100  
    current_environment = random.choice(["sunny", "rainy", "stormy"])  
    treasure_door = random.choice(['1', '2', '3', '4', '5'])
    fake_treasure_door = random.choice([door for door in ['1', '2', '3', '4', '5'] if door != treasure_door])
    remaining_doors = [door for door in ['1', '2', '3', '4', '5'] if door != treasure_door and door != fake_treasure_door]
    maze_door = random.choice(remaining_doors)
    key_door = random.choice([door for door in remaining_doors if door != maze_door])
    
    print_pause(f"You find yourself standing on the deck of a pirate ship. It's a {current_environment} day.")
    print_pause("In front of you, there are five doors.")
    print_pause("Behind one of these doors lies the hidden treasure.")
    print_pause("Behind another door lies a fake treasure.")
    print_pause("But beware, some doors may hide dangerous pirates.")
    print_pause(f"Your current health is: {health}")

def choose_door():
    print_pause("Choose a door to open: 1, 2, 3, 4, or 5?")
    door = input("Enter the number of the door you want to open: ")
    if door in ['1', '2', '3', '4', '5']:
        check_door(door)
    else:
        print_pause("Invalid choice. Please choose 1, 2, 3, 4, or 5.")
        choose_door()

def check_door(door):
    if door == treasure_door:
        find_treasure()
    elif door == fake_treasure_door:
        find_fake_treasure()
    elif door == maze_door:
        navigate_maze()
    elif door == key_door:
        find_key()
    else:
        encounter_pirates()

def encounter_pirates():
    print_pause("You open the door and find... a room full of pirates!")
    pirate_leader_conversation()

def pirate_leader_conversation():
    print_pause("Pirate Leader: Ahoy! What do ye think ye be doin' here?")
    print_pause("You: I've come for the treasure, and I won't leave without it!")
    print_pause("Pirate Leader: Brave words, landlubber. How about a fight? If ye win, ye leave unharmed.")
    choose_weapon()

def choose_weapon():
    global chosen_weapon
    print_pause("Pirate Leader: Choose your weapon: sword, axe, or dagger.")
    weapon = input("Enter your weapon of choice: sword/axe/dagger ")
    if weapon.lower() in ['sword', 'axe', 'dagger']:
        chosen_weapon = weapon.capitalize()
        print_pause(f"You have chosen a {chosen_weapon}.")
        fight_or_flee()
    else:
        print_pause("Invalid choice. Please choose sword, axe, or dagger.")
        choose_weapon()

def fight_or_flee():
    response = input("Do you want to fight or flee? (fight/flee) ")
    if response.lower() == 'fight':
        combat()
    elif response.lower() == 'flee':
        print_pause("You flee back to the deck and must choose another door.")
        choose_door()
    else:
        print_pause("Invalid choice. Please choose 'fight' or 'flee'.")
        fight_or_flee()

def combat():
    print_pause("You engage in combat with the pirate leader!")
    rounds = random.randint(1, 3)  
    for round_num in range(1, rounds + 1):
        print_pause(f"Round {round_num} of combat!")
        success = combat_interaction()
        if not success:
            global health
            health -= random.randint(10, 30)  
            print_pause(f"Your current health is: {health}")
            if health <= 0:
                print_pause("You have been defeated by the pirate leader.")
                print_pause("Game Over!")
                play_again()
                return
        else:
            print_pause("You won this round of combat!")
    print_pause("You have defeated the pirate leader!")
    print_pause("The other pirates step aside and let you leave unharmed.")
    choose_final_door()

def combat_interaction():
    required_presses = random.randint(5, 12)  
    print_pause(f"Press 'f' {required_presses} times within 3 seconds to win the fight!")

    f_presses = 0
    start_time = time.time()

    def count_f_presses():
        nonlocal f_presses
        while time.time() - start_time < 3:
            if keyboard.read_event().name == 'f':
                f_presses += 1
                print(f'Pressed f {f_presses}/{required_presses}')

    thread = threading.Thread(target=count_f_presses)
    thread.start()
    thread.join()

    if f_presses >= required_presses:
        return True
    else:
        return False

def navigate_maze():
    print_pause("You find yourself in a maze. You need to find your way out.")
    
    correct_path = random.choice(["left", "right", "straight"])
    print_pause("Choose a direction: left, right, or straight.")
    direction = input("Enter your choice: ")
    if direction == correct_path:
        print_pause("You successfully navigate the maze and find the treasure!")
        solve_puzzle()
    else:
        print_pause("You hit a dead end and must find your way back.")
        global health
        health -= 10
        print_pause(f"Your current health is: {health}")
        if health <= 0:
            print_pause("You have lost all your health in the maze.")
            print_pause("Game Over!")
            play_again()
        else:
            navigate_maze()

def find_key():
    print_pause("You enter a room filled with hidden keys.")
    correct_key = random.choice(["gold", "silver", "bronze"])
    print_pause("Choose a key: gold, silver, or bronze.")
    key = input("Enter your choice: ")
    if key == correct_key:
        print_pause("You found the correct key and unlock the next door to find the treasure!")
        solve_puzzle()
    else:
        print_pause("The key doesn't fit. You need to find another key.")
        global health
        health -= 10
        print_pause(f"Your current health is: {health}")
        if health <= 0:
            print_pause("You have lost all your health while searching for the key.")
            print_pause("Game Over!")
            play_again()
        else:
            find_key()

def find_treasure():
    print_pause("You open the door and find... the hidden treasure!")
    solve_puzzle()

def find_fake_treasure():
    print_pause("You open the door and find... what looks like the treasure!")
    print_pause("But wait, it might be a fake treasure.")
    solve_puzzle()

def solve_puzzle():
    global wrong_attempts
    wrong_attempts = 0
    puzzle = random.choice(puzzles)
    global current_puzzle
    current_puzzle = puzzle

    while wrong_attempts < 2:
        answer = input(f"{puzzle['question']} ")
        if answer.lower() == puzzle['answer']:
            print_pause("Correct! The treasure is real!")
            print_pause("Congratulations! You have found the real treasure and won the game!")
            play_again()
            return
        else:
            wrong_attempts += 1
            if wrong_attempts == 1:
                print_pause(f"Hint: {puzzle['hint']}")
            else:
                print_pause("Wrong! The treasure is fake.")
                print_pause("Game Over!")
                play_again()
                return

def choose_final_door():
    print_pause("After defeating the pirates, you see two more doors: 1 and 2.")
    print_pause("One leads to freedom, and the other leads to a deadly trap.")
    door = input("Choose a door to open: 1 or 2? ")
    if door in ['1', '2']:
        final_choice(door)
    else:
        print_pause("Invalid choice. Please choose 1 or 2.")
        choose_final_door()

def final_choice(door):
    if door == '1':
        print_pause("You open the door and find a path to safety. Congratulations!")
    else:
        print_pause("You open the door and fall into a trap. Game Over!")
    play_again()

def play_again():
    response = input("Do you want to play again? (yes/no) ")
    if response.lower() == 'yes':
        intro()
        choose_door()
    else:
        print_pause("Thank you for playing!")

if __name__ == "__main__":
    intro()
    choose_door()
