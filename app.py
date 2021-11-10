from flask import Flask, request
import os
import allrecipes_scraper as scraper

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/', methods=["POST"])
def recipeScraper():
    req = request.get_json()
    url = req['URL']
    payload = scraper.getRecipeData(url)
    
    return payload

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9546)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 