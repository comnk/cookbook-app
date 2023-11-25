from dotenv import load_dotenv
import requests
import pdfkit
import os

load_dotenv()
api_key = os.getenv("API_KEY")

def random_recipe():
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
                print("Ok! Saving pdf to your computer")

                file_title = title.lower().replace(" ", "")
                path = "../recipe-docs/" + file_title + '.html'
                with open(path, 'w') as f:
                    f.write(f"<h1>{title}</h1>\n")
                    f.write("<ul>")
                    for ingredient in ingredients:
                        f.write(f"<li>{ingredient['original']}</li>\n")

                    f.write("</ul>")
                    f.write(instructions)
                    f.close()
                
                pdfkit.from_file(path, "../recipe-docs/" + file_title + '.pdf') 
                print("PDF saved!")

                os.remove(path)

            elif (save_input == "no"):
                print("Ok! Heading back to home page!")
            else:
                print("Invalid input!")
        
        except IndexError:
            print(f"Sorry no {type_meal} of {cuisine} exists! Please try again!")

    else:
        print(f"Failed to retrieve a recipe. Status code: {response.status_code}")