from flask import Flask, request
import os
import allrecipes_scraper as scraper

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/', methods=['GET', 'POST'])
def root():
    return "Welcome to the Allrecipes.com recipe scraper. Please send POST requests to /scrape as a JSON with the url as \'URL\' "

@app.route('/scrape', methods=["POST"])
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