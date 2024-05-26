import random

import secrets
import string
import hashlib
from getpass import getpass

def generate_username(name_of_user):
	# Constraints 
	minimum_capital_letter = 2
	minimum_specia_char = 2
	minimum_digits = 2
	min_len_of_username = 8
	special_chars = ['@','#','$','&']

	# variable to store generated username
	username = ""

	# remove space from name of user
	name_of_user = "".join(name_of_user.split())

	# convert whole name in lowercase 
	name_of_user = name_of_user.lower()

	# calculate minimum characters that we need to take from name of user 
	minimum_char_from_name = min_len_of_username-minimum_digits-minimum_specia_char

	# take required part from name 
	temp = 0
	for i in range(random.randint(minimum_char_from_name,len(name_of_user))):
		if temp < minimum_capital_letter:
			username += name_of_user[i].upper()
			temp += 1
		else:
			username += name_of_user[i]

	# temp_list to store digits and special_chars so that they can be shuffled before adding to username 
	temp_list = []
	# add required digits 
	for i in range(minimum_digits):
		temp_list.append(str(random.randint(0,9)))

	# append special characters 
	for i in range(minimum_specia_char):
		temp_list.append(special_chars[random.randint(0,len(special_chars)-1)])

	# shuffle list 
	random.shuffle(temp_list)

	username += "".join(temp_list)

    



USER_DETAILS = ""

PUNCTUATIONS = "@#$%&"

DEFAULT_PASSWORD_LENGTH = 12

INVALID_LENGTH_MESSAGE = f'''
Password length must be between 8 and 16. 
Password length must be a number.
Generating password with default length of {DEFAULT_PASSWORD_LENGTH} characters.
'''


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + PUNCTUATIONS
    pwd = ''.join(secrets.choice(characters) for _ in range(length))
    return pwd


def hash_password(pwd):
    """Hash a password using SHA-256 algorithm"""
    pwd_bytes = pwd.encode('utf-8')
    hashed_pwd = hashlib.sha256(pwd_bytes).hexdigest()
    return hashed_pwd

def save_user(username, hashed_pwd):
    """Save user-details to the users detail file"""
    pass

def user_exists(username):
    try:
        for line in USER_DETAILS:
            parts = line.split()
            if parts[0] == username:
                return True
    except FileNotFoundError as fl_err:
        print(f"{fl_err.args[-1]}: {USER_DETAILS}")
        print(f"System will create file: {USER_DETAILS}")
    return False

def authenticate_user(username, password):
    for line in USER_DETAILS:
        parts = line.split()
        if parts[0] == username:
            hashed_password = parts[1]
            if hashed_password == hash_password(password):
                return True
            else:
                return False
    return False






password = "password123"
salt = "randomsaltvalue"
hashed_password = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

def validate_input(password_length):
    try:
        password_length = int(password_length)
        if password_length < 8 or password_length > 16:
            raise ValueError("Password length must be between 8 and 16")
        return password_length
    except ValueError:
        print(INVALID_LENGTH_MESSAGE)
        return DEFAULT_PASSWORD_LENGTH


def register():
    username = input("Enter username: ")
    if user_exists(username):
        print("User already exists.")
        return
    length = input("Enter Auto Generated Password Length (Number 8-16): ")
    length = validate_input(length)
    password = generate_password(length)

    hashed_password = hash_password(password)
    save_user(username, hashed_password)
    print("User created successfully.")
    print("Your password is:", password)


def login():
    username = input("Enter username: ")
    if not user_exists(username):
        print("User does not exist.")
        return

    password = getpass("Password: ")
    if not authenticate_user(username, password):
        print("Incorrect password.")
        return
    print("Login successful.")




def main():
    while True:
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")



