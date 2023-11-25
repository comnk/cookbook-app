from functions import random_recipe

while True:
    initial_input = input("Welcome back! What would you like to do? ")

    match initial_input:
        case "random recipe":
            random_recipe()
        case "exit":
            print("Thanks for using the app! Have a good day!")
            break
        case _:
            print("Invalid input! Try again!")