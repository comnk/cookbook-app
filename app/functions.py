from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join
from pypdf import PdfWriter
import glob, os, pdfkit, requests, random, string

load_dotenv()
api_key = os.getenv("API_KEY")

# GENERAL FEATURES

def clear_history():
    history_input = input("Which history would you like to clear? ")

    match history_input:
        case "recipe":
            files = glob.glob('../recipe-docs/recipes/*.pdf')

            if (len(files) == 0):
                print("No files to clear!")

            for f in files:
                os.remove(f)
            
            print("All recipe files removed")

        case "cookbook":
            files = glob.glob('../recipe-docs/cookbooks/*.pdf')

            if (len(files) == 0):
                print("No files to clear!")

            for f in files:
                os.remove(f)
            
            print("All cookbook files removed")

        case "_":
            print("Invalid input! Please try again!")

def save_pdf(title, image, ingredients, instructions):
    print("Ok! Saving pdf to your computer")

    file_title = title.lower().replace(" ", "")
    path = "../recipe-docs/recipes/" + file_title + '.html'
    
    with open(path, 'w') as f:
        f.write(f"<h1>{title}</h1>\n")
        f.write(f"<img src={image} width='300' height='300'>\n")
        f.write("<ul>")

        for ingredient in ingredients:
            f.write(f"<li>{ingredient['original']}</li>\n")

        f.write("</ul>")
        f.write(instructions)
        f.close()
                
    pdfkit.from_file(path, "../recipe-docs/recipes/" + file_title + '.pdf') 
    print("PDF saved!")

    os.remove(path)

# FOOD FEATURES FOR CHATBOT

def extract_recipe():

    """
    
    """

    get_website = input("Insert website url here: ")

    endpoint = "https://api.spoonacular.com/recipes/extract"
    params = {"apiKey": api_key, "url": get_website}
    response = requests.get(endpoint, params=params)

    # Check the status code of the response
    if response.status_code == 200:
        # Parse the JSON response
        recipe = response.json()
        # Extract information about the random recipe
        try:
            title = recipe["title"]
            ingredients = recipe["extendedIngredients"]
            instructions = recipe["instructions"]

            # Display information
            print(f"Title: {title}")
            print("Ingredients:")
            for ingredient in ingredients:
                print(f"  - {ingredient['original']}")
            print("Instructions:")
            print(instructions)

            save_input = input("Do you want to save this recipe? ").lower()

            if (save_input == "yes"):
                save_pdf(title, recipe["image"], ingredients, instructions)

            elif (save_input == "no"):
                print("Ok! Heading back to home page!")
            else:
                print("Invalid input!")

        except IndexError:
            print(f"Sorry that url does not exists! Please try again!")

    else:
        print(f"Failed to retrieve a recipe. Status code: {response.status_code}")

def generate_cookbook():

    """
    
    """

    recipe_files = [f for f in listdir("../recipe-docs/recipes/") if isfile(join("../recipe-docs/recipes/", f))]

    if (len(recipe_files) == 0):
        print("No files to merge! Please upload recipes!")
    else:
        print("Merging...")
        merge = PdfWriter()

        for pdf in recipe_files:
            merge.append("../recipe-docs/recipes/" + pdf)

        all_char = string.ascii_letters + string.punctuation + string.digits
        password = "".join(random.choice(all_char) for x in range(random.randint(1, 10)))

        merge.write("../recipe-docs/cookbooks/cookbook" + password + ".pdf")
        merge.close()

        print("Merge successful!")

def random_recipe():

    """
    
    """

    cuisine = input("What cuisine are you feeling today? ")
    type_meal = input("What type of meal do you want? ")
    endpoint = "https://api.spoonacular.com/recipes/random"
    params = {"apiKey": api_key, "tags": cuisine + "," + type_meal, "number": 1}
    response = requests.get(endpoint, params=params)

    # Check the status code of the response
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract information about the random recipe
        try:
            recipe = data["recipes"][0]
            title = recipe["title"]
            ingredients = recipe["extendedIngredients"]
            instructions = recipe["instructions"]

            # Display information
            print(f"Title: {title}")
            print("Ingredients:")
            for ingredient in ingredients:
                print(f"  - {ingredient['original']}")
            print("Instructions:")
            print(instructions)

            save_input = input("Do you want to save this recipe? ").lower()

            if (save_input == "yes"):
                save_pdf(title, recipe["image"], ingredients, instructions)

            elif (save_input == "no"):
                print("Ok! Heading back to home page!")
            else:
                print("Invalid input!")
        
        except IndexError:
            print(f"Sorry no {type_meal} of {cuisine} exists! Please try again!")

    else:
        print(f"Failed to retrieve a recipe. Status code: {response.status_code}")