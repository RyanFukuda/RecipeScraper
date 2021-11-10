# This scraper uses basic code from here:
# https://hackersandslackers.com/scrape-metadata-json-ld/ 
# which results in a the python library requests to get the raw html from a 
# given URL, then uses extruct to give only the metadata. According to the 
# article here:
# https://www.linkedin.com/pulse/scraping-recipe-websites-ben-awad/
# most recipe websites will give easy, machine-readable recipe information
# in the metadata of a URL so that search engines can produce recipe cards

import requests
import extruct
import unicodedata

def get_html(url):
    """Get raw HTML from a URL."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(url, headers=headers)
    return req.text


def scrape(url):
    """Parse structured data from a target page."""
    html = get_html(url)
    metadata = get_metadata(html, url)
    return metadata


def get_metadata(html, url):
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url='https://www.allrecipes.com/',
        syntaxes=['json-ld'],
    )['json-ld'][1]
    return metadata


def getRecipeData(url):
    meta = scrape(url)
    recipeInfo = dict()
    recipeInfo['recipe'] = dict()
    recipeInfo['recipe']['name'] = meta['name']
    recipeInfo['recipe']['recipe_url'] = url
    recipeInfo['recipe']['image_url'] = meta['image']['url']

    # Parses Vulgar Fractions
    # https://stackoverflow.com/questions/49440525/detect-single-string-fraction-ex-%C2%BD-and-change-it-to-longer-string
    recipeInfo['recipe']['recipeIngredients'] = []
    for ing in meta['recipeIngredient']:
        string_list = ing.split()
        try:
            name = unicodedata.name(string_list[0][0])
        except ValueError:
            continue
        if name.startswith('VULGAR FRACTION'):
            vulgar_to_float = unicodedata.numeric(string_list[0][0])
            temp = []
            temp.append(str(round(vulgar_to_float, 3)))
            string_list = temp + string_list[1:]
        recipeInfo['recipe']['recipeIngredients'].append(' '.join(string_list))

    # Parses recipe instructions
    recipeInfo['recipe']['recipeInstructions'] = []
    for step in meta['recipeInstructions']:
        recipeInfo['recipe']['recipeInstructions'].append({'instruction': step['text']})

    recipeInfo['recipe']['nutritionalInfo'] = dict()
    recipeInfo['recipe']['nutritionalInfo']['servings_per_recipe'] = meta['recipeYield']
    recipeInfo['recipe']['nutritionalInfo']['calories'] = meta['nutrition']['calories'].split()[0]
    recipeInfo['recipe']['nutritionalInfo']['data'] = []
    for nutrient in meta['nutrition']:
        name = nutrient
        unparsed = meta['nutrition'][name]
        if(unparsed is None):
            recipeInfo['recipe']['nutritionalInfo']['data'].append({'name': name, 'amount': 'NULL', 'unit': 'NULL'})
        # Prevents index error
        elif unparsed == 'NutritionInformation':
            pass
        # Already added to object per Adam's specification, prevents duplicate
        elif unparsed == 'calories':
            pass
        else:
            unparsed_list = unparsed.split()
            amount = unparsed_list[0]
            unit = unparsed_list[1]
            recipeInfo['recipe']['nutritionalInfo']['data'].append({'name': name, 'amount': amount, 'unit': unit})

    return recipeInfo


def main():
    obj = getRecipeData('https://www.allrecipes.com/recipe/78370/hamburger-steak-with-onions-and-gravy/')

    print("Title: " + obj['recipe']["name"])
    print()
    print("URL: " + obj['recipe']["recipe_url"])
    print()
    print("Image URL: " + obj['recipe']["image_url"])
    print()
    print("Ingredients: ")
    for ing in obj['recipe']["recipeIngredients"]:
        print(ing)
    print()
    print("Instructions: ")
    for step in obj['recipe']["recipeInstructions"]:
        print(step['instruction'])
    print()
    print("Recipe Yield: " + obj['recipe']["nutritionalInfo"]["servings_per_recipe"])
    print()
    print("Calories: " + obj['recipe']["nutritionalInfo"]["calories"])
    print()
    for nutrient in obj['recipe']["nutritionalInfo"]["data"]:
        print(nutrient['name'])
        print(nutrient['amount'])
        print(nutrient['unit'])
    print()

if __name__ == "__main__":
    main()

