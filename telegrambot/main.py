import requests
import pprint
import random


def get_recipe(recipe):
    try:
        # write here your api_url and api_key instead of "XXX"
        api_url = 'XXXquery={}'.format(recipe)
        api_key = 'XXX'
        r = requests.get(
            api_url, headers={'X-Api-Key': api_key}
        )
        print(r.url)
        random_number0 = random.randint(1, 15)
        data = r.json()[random_number0]
        # pprint.pprint(data)
        recipe = data["title"]
        ingredients = data["ingredients"]
        instructions = data["instructions"]
        servings = data["servings"]
        print(f"Name of the dish: {recipe}")
        print(f"\nIngredients: {ingredients}")
        print(f"\nInstructions: {instructions}")
        print(f"\nServings: {servings}")
        data1 = r.json()[4]
        # pprint.pprint(data1)
        recipe1 = data1["title"]
        ingredients1 = data1["ingredients"]
        instructions1 = data1["instructions"]
        servings1 = data1["servings"]
        print(f"\nName of the dish: {recipe1}")
        print(f"\nIngredients: {ingredients1}")
        print(f"\nInstructions: {instructions1}")
        print(f"\nServings: {servings1}")
        data2 = r.json()[9]
        # pprint.pprint(data2)
        recipe2 = data2["title"]
        ingredients2 = data2["ingredients"]
        instructions2 = data2["instructions"]
        servings2 = data2["servings"]
        print(f"\nName of the dish: {recipe2}")
        print(f"\nIngredients: {ingredients2}")
        print(f"\nInstructions: {instructions2}")
        print(f"\nServings: {servings2}")
    except Exception as ex:
        print(ex)
        print("Error:", r.status_code, r.text)


def main():
    recipe = input("What recipe do you need? ")
    get_recipe(recipe)


if __name__ == '__main__':
    main()
