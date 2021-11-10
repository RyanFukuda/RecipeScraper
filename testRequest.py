import requests
import json

# raw = requests.post('http://flip3.engr.oregonstate.edu:9546/scrape', json={'URL': 'https://www.allrecipes.com/recipe/78370/hamburger-steak-with-onions-and-gravy/'})
raw = requests.post('https://cs361recipescraper.herokuapp.com/', json={'URL': 'https://www.allrecipes.com/recipe/78370/hamburger-steak-with-onions-and-gravy/'})
r = raw.json()

with open('recipe.json', 'w') as f:
    json.dump(r, f)

print(json.dumps(r, indent=4, sort_keys=True))

# print("Title: " + r['recipe']["name"])
# print()
# print("URL: " + r['recipe']["recipe_url"])
# print()
# print("Image URL: " + r['recipe']["image_url"])
# print()
# print("Ingredients: ")
# for ing in r['recipe']["recipeIngredients"]:
#     print(ing)
# print()
# print("Instructions: ")
# for step in r['recipe']["recipeInstructions"]:
#     print(step['instruction'])
# print()
# print("Recipe Yield: " + r['recipe']["nutritionalInfo"]["servings_per_recipe"])
# print()
# print("Calories: " + r['recipe']["nutritionalInfo"]["calories"])
# print()
# for nutrient in r['recipe']["nutritionalInfo"]["data"]:
#     print(nutrient['name'])
#     print(nutrient['amount'])
#     print(nutrient['unit'])
# print()