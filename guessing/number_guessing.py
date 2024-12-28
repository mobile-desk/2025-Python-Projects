import random
import sqlite3


# database
def setup_database():
    conn = sqlite3.connect('guessing/game_users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            points INTEGER,
            secret_word TEXT
        )
    ''')
    conn.commit()   
    return conn, cursor
    
    
def save_user_points(username, points):
    conn, cursor = setup_database()
    
    # Check if user exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    
    if user:
        secret_word = input("Enter your secret word to verify your identy: ")
        cursor.execute('SELECT secret_word FROM users WHERE username = ?', (username,))
        stored_secret = cursor.fetchone()[0]
        
        if secret_word == stored_secret:
            new_points = user[1] + points
            cursor.execute('UPDATE users SET points = ? WHERE username = ?', (new_points, username))
            print("Points Updated")
            
        else:
            print("Incorrect Secret Word")
    else:
        secret_word = input("Please create a secret word: ")
        cursor.execute('INSERT INTO users (username, points, secret_word) VALUES (?, ?, ?)', (username, points, secret_word))
        print('New user created')
        
        conn.commit()
        conn.close()
        
        
        
# game

def select_level():
    print('Please select your level')
    print('1: Easy')
    print('2: Medium')
    print('3: Hard')
    
    level = input("Make your choice: ")
    
    
    if level not in ["1", "2", "3"]:
        return "Invalid input"
    else:
        return level
    
    
    
    
def generate_value(level):
    if level == "1":
        value = random.randint(1,10)
    elif level == "2":
        value = random.randint(1, 100)
    else:
        value = random.randint(1, 1000)
        
    return value



def attempt(level, value):
    guesses = 5
    points = 0
    
    print("You have 5 guesses.")
    if level == "1":
        guessable_value = 10
    elif level == "2":
        guessable_value = 100
    else:
        guessable_value = 1000
           
    try: 
        while guesses > 0:
            guess = int(input(f"Please make a guess from 1 - {guessable_value}: "))
            if guess == value:
                print("Thats Correct !!!!")
                if guesses == 3:
                    points += 10
                elif guesses == 2:
                    points += 5
                else:
                    points += 2
                break
            else:
                print(f"Try again, you have {guesses - 1} guesses left")
                guesses -= 1

        if guesses == 0:
            print(f"You are out of guesses. The correct value was {value}")
            
    except:
        print("An error occured")
    return points



def show_leaderboard():
    conn, cursor = setup_database()
    cursor.execute('SELECT username, points FROM users ORDER BY points DESC')
    users = cursor.fetchall()
    print('\n=== LEADERBOARD ===')
    for user in users:
        print(f"{user[0]}: {user[1]} points")
    conn.close()
    
    
    
def start_game():
    print("Welcome to the Guessing Game!")
    username = input("Please enter your username: ").lower()
    level = select_level()
    value = generate_value(level)
    points = attempt(level, value)
    save_user_points(username, points)
    show_leaderboard()
    return "DONE"


start_game()