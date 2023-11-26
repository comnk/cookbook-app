from functions import *

while True:
    initial_input = input("Welcome back! What would you like to do? ")

    match initial_input:
        case "clear history":
            clear_history()
        case "extract recipe":
            extract_recipe()
        case "random recipe":
            random_recipe()
        case "generate cookbook":
            generate_cookbook()
        case "exit":
            print("Thanks for using the app! Have a good day!")
            break
        case _:
            print("Invalid input! Try again!")