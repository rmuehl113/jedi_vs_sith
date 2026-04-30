# Jedi vs Sith Battle Simulator
# Author: Robert Muehleisen
# Date: 04/26/2026
# Description: A CLI-based battle simulator.
# Choose a Jedi and a Sith to duel it out. Imports CSV file with Jedi and Sith stats.
# Randomly generated fights have unpredictable outcomes. Cinematic announcing throughout.

import random
import time
import os
import csv

class ForceUser:
    """
    Sets up base class all force users inherit from
    Parameters: Name, Health, Attack, Defense, Force Power
    """
    def __init__(self, name, health, attack, defense, force_power, wins=0, losses=0, gauntlet_wins=0):
        self.name = name
        self.health = health
        self.max_health = health  # equal to health to set starting hp
        self.attack = attack
        self.defense = defense
        self.force_power = force_power
        self.wins = wins
        self.losses = losses
        self.gauntlet_wins = gauntlet_wins

    def __str__(self):
        """
        Prints name and health during fight
        """
        return f"{self.name} | HP: {self.health}/{self.max_health}"
    
    def print_info(self):
        """
        Prints full stats of chosen fighter
        """
        print("\n--------------------")
        print(f"{self.name}({self.wins}-{self.losses})".center(20))
        print("--------------------")
        print(f"Health: {self.health}".center(20))
        print(f"Attack: {self.attack}".center(20))
        print(f"Defense: {self.defense}".center(20))
        print("--------------------")
        if isinstance(self, Jedi):
            print("Special Ability:".center(20))
            print("Force Deflect 🛡️".center(20))
            print(f"Chance: {self.force_power}%".center(20))
        elif isinstance(self, Sith):
            print("Special Ability:".center(20))
            print("Rage Burst ⚠️".center(20))
            print(f"Chance: {self.force_power}%".center(20))
        print("--------------------")
        print(f"Gauntlet Wins: {self.gauntlet_wins}".center(20))
        print("--------------------")

class Jedi(ForceUser):
    """
    Sets up Jedi class with ForceUser attributes inherited
    Parameters: Name, Health, Attack, Defense, Force Power
    """
    def __init__(self, name, health, attack, defense, force_power, wins=0, losses=0, gauntlet_wins=0):
        super().__init__(name, health, attack, defense, force_power, wins, losses, gauntlet_wins)

    def deflect(self, damage):
        """
        Jedi special ability, can be called randomly by battle
        Negates incoming damage
        """
        damage = 0
        return damage

class Sith(ForceUser):
    """
    Sets up Sith class with ForceUser attributed inherited
    Parameters: Name, Health, Attack, Defense, Force Power
    """
    def __init__(self, name, health, attack, defense, force_power, wins=0, losses=0, gauntlet_wins=0):
        super().__init__(name, health, attack, defense, force_power, wins, losses, gauntlet_wins)

    def rage(self, damage):
        """
        Sith special ability, can be called randomly by battle
        Increases attack
        """
        damage = damage * 2
        return damage
    
def int_check(prompt):
    """
    Helper function to provide error handling for integer input
    Prints error message if user enters non-integer
    Loop until valid integer is entered
    """
    while True:
        try:
            user_input = input(prompt)
            user_int = int(user_input)
            break
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
    return user_int

def load_fighters(filename, fighter_class):
    """
    Loads Fighter roster from CSV file into dictionary
    Parameters: filename, fighter_class
    """
    roster = {}
    if os.path.exists(filename):
        with open(filename, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:  
                roster[row["name"]] = fighter_class(row["name"], int(row["health"]), int(row["attack"]), int(row["defense"]), 
                                                    int(row["force_power"]), int(row["wins"]), int(row["losses"]), int(row["gauntlet_wins"]))
    else:
        print(f"Error: {filename} not found.")
    return roster

def save_fighters(filename, roster):
    """
    Updates win/loss stat for fighter
    Saves updated CSV file
    """
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "health", "attack", "defense", "force_power", "wins", "losses", "gauntlet_wins"])
        writer.writeheader()
        for item in roster.values():
            writer.writerow({"name": item.name, "health": item.health, "attack": item.attack, "defense": item.defense, 
                             "force_power": item.force_power, "wins": item.wins, "losses": item.losses, "gauntlet_wins": item.gauntlet_wins})
            
def choose_fighter(roster):
    """
    Display fighter list to user
    Returns user-picked fighter
    """
    for i, name in enumerate(roster, 1):
        print(f"{i}. {name}")
    while True:    
        choice = int_check("Choose Fighter: ")
        if 1 <= choice <= len(roster):
            break
        print(f"\nInvalid input. Enter a number between 1 and {len(roster)}.")
    chosen = list(roster.values())[choice - 1]
    return chosen

def battle(fighter1, fighter2, jedi_roster, sith_roster):
    """
    Handles battle between Jedi and Sith using random number generations
    Displays cinematic text after each battle sequence
    Parameters: Jedi, Sith, both rosters
    Returns: Winning fighter
    """
    options = ["heads", "tails"]
    result = random.choice(options)
    if result == "heads":
        attacker = fighter1
        defender = fighter2
    else:
        attacker = fighter2
        defender = fighter1

    print(f"\n⚔️  {fighter1.name} vs {fighter2.name} ⚔️")
    while attacker.health > 0 and defender.health > 0:
        damage = attacker.attack + random.randint(10, 15) - defender.defense
        damage = max(1, damage)
        if isinstance(attacker, Sith):
            sith_action = random.choices(["attack", "ability"], weights=[100 - attacker.force_power, attacker.force_power])[0]
            if sith_action == "ability":
                damage = attacker.rage(damage)
                print(f"\n⚠️  {attacker.name} uses Rage Burst! Damage Increased! ⚠️")

            jedi_action = random.choices(["attack", "ability"], weights=[100 - defender.force_power, defender.force_power])[0]
            if jedi_action == "ability":
                damage = defender.deflect(damage)
                print(f"\n🛡️  {defender.name} uses Force Deflect! Damage Blocked! 🛡️")
           
        defender.health = defender.health - damage
        print(f"\n{attacker.name} attacks {defender.name} for {damage} damage! {defender}")
        time.sleep(1.5)
        attacker, defender = defender, attacker

    if fighter1.health <= 0:
        print(f"\n⚔️  {fighter2.name} has defeated {fighter1.name} ⚔️")
        fighter2.wins += 1
        fighter1.losses += 1
        winner = fighter2
    else:
        print(f"\n⚔️  {fighter1.name} has defeated {fighter2.name} ⚔️")
        fighter1.wins += 1
        fighter2.losses += 1
        winner = fighter1
    fighter1.health = fighter1.max_health
    fighter2.health = fighter2.max_health
    save_fighters("jedi.csv", jedi_roster)
    save_fighters("sith.csv", sith_roster)
    return winner

def gauntlet(jedi_roster, sith_roster):
    """
    Allows user to pick a Jedi or Sith and battle all opponents
    Random order of opposing roster to fight until chosen fighter health is depleted
    """
    while True:
        print("\n1. Jedi\n2. Sith")
        class_choice = input("Choose your Fighter: ")
        print()
        if class_choice == "1":
            for i, name in enumerate(jedi_roster, 1):
                print(f"{i}. {name}")
            roster = jedi_roster
            break
        elif class_choice == "2":
            for i, name in enumerate(sith_roster, 1):
                print(f"{i}. {name}")
            roster = sith_roster
            break
        else:
            print("\nInvalid input. Please enter 1 or 2.")

    while True:    
        choice = int_check("Choose Fighter: ")
        if 1 <= choice <= len(roster):
            break
        print(f"\nInvalid input. Enter a number between 1 and {len(roster)}.")
    fighter = list(roster.values())[choice - 1]
    
    if isinstance(fighter, Jedi):
        opponents = list(sith_roster.values())
        random.shuffle(opponents)
    elif isinstance(fighter, Sith):
        opponents = list(jedi_roster.values())
        random.shuffle(opponents)

    defeated = []
    for opponent in opponents:
        winner = battle(fighter, opponent, jedi_roster, sith_roster)
        if winner != fighter:
            break
        elif winner == fighter:
            defeated.append(opponent.name)
    if len(defeated) == len(opponents):
        fighter.gauntlet_wins += 1
        if isinstance(fighter, Jedi):
            save_fighters("jedi.csv", jedi_roster)
        elif isinstance(fighter, Sith):
            save_fighters("sith.csv", sith_roster)
        print(f"\n{fighter.name} has completed the Gauntlet, Impressive.")
    else:
        print(f"\n{fighter.name} failed the Gauntlet. Fights Won: {len(defeated)}")
    if len(defeated) > 0:
        print("Fighters Defeated:")
        for name in defeated:
            print(f"{name}")
    else:
        print("Better luck next time.")

def display_roster(jedi_roster, sith_roster):
    """
    Displays chosen Jedi or Sith stats
    Parameters: jedi_roster, sith_roster
    """
    while True:
        print("\n1. Jedi\n2. Sith")
        class_choice = input("Choose a Class: ")
        print()
        if class_choice == "1":
            for i, name in enumerate(jedi_roster, 1):
                print(f"{i}. {name}")
            roster = jedi_roster
            break
        elif class_choice == "2":
            for i, name in enumerate(sith_roster, 1):
                print(f"{i}. {name}")
            roster = sith_roster
            break
        else:
            print("\nInvalid input. Please enter 1 or 2.")

    while True:    
        choice = int_check("Choose Fighter: ")
        if 1 <= choice <= len(roster):
            break
        print(f"\nInvalid input. Enter a number between 1 and {len(roster)}.")
    chosen = list(roster.values())[choice - 1]
    chosen.print_info()

def reset_records(jedi_roster, sith_roster):
    """
    Resets Win/Loss records
    Parameters: Jedi roster, Sith roster
    """
    confirm = input("Reset Win/Losses? (y): ")
    if confirm.lower() == "y":
        for fighter in jedi_roster.values():
            fighter.wins = 0
            fighter.losses = 0
            fighter.gauntlet_wins = 0

        for fighter in sith_roster.values():
            fighter.wins = 0
            fighter.losses = 0
            fighter.gauntlet_wins = 0

        save_fighters("jedi.csv", jedi_roster)
        save_fighters("sith.csv", sith_roster)
        print("Records reset!")
    else:
        print("Reset cancelled")

def main():
    """
    Main loop
    Processes user input
    Calls appropriate function 
    """
    jedi_roster = load_fighters("jedi.csv", Jedi)
    sith_roster = load_fighters("sith.csv", Sith)
    print("Program loaded succesfully.\nPrepare for battle!")
    while True:
        print("\nMenu Options:\n1. Battle\n2. View Stats\n3. Reset Win/Losses\n4. Quit")
        user_input = input("Select an option (1-4): ")

        if user_input == "1":
            while True:
                print("\n1. Single Fight\n2. Gauntlet")
                battle_input = input("Select Fight Type (1-2): ")
                if battle_input == "1":
                    print("\nChoose your Jedi:")
                    jedi = choose_fighter(jedi_roster)
                    print("\nChoose your Sith:")
                    sith = choose_fighter(sith_roster)
                    battle(jedi, sith, jedi_roster, sith_roster)
                    break
                elif battle_input == "2":
                    gauntlet(jedi_roster, sith_roster)
                    break
                else:
                    print("\nInvalid option. Please select 1 or 2.")

        elif user_input == "2":
            display_roster(jedi_roster, sith_roster)

        elif user_input == "3":
            reset_records(jedi_roster, sith_roster)

        elif user_input == "4":
            print("Exiting Program\nGood Fighting, Goodbye!!")
            break

        else:
            print("\nInvalid option. Please select 1-4.")

if __name__ == "__main__":
    main()