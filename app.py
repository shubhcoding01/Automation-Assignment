from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import openai
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# print("-----Shubh Coding-----")
load_dotenv()
app = Flask(__name__)

# Set up API keys here  
CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")
APOLLO_API_KEY = os.getenv("Apollo_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("CSE_ID")
UBERSUGGEST_API_KEY = os.getenv("YOUR_UBERSUGGEST_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY
# MySQL Database Connection
# def create_db_connection():
    # try:
db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="radheradhe",
        database="ShubhAutomation"
        )
    #     return db
    # except Error as e:
    #     print(f"Error connecting to database: {e}")
    #     return None

#Close database connection properly
# def close_db_connection(db, cursor):
#         cursor.close()
#         db.close()

cursor = db.cursor()

# Function to insert data into MySQL database (using parameterized queries)
# def insert_data_into_db(name, email, website, gpt_suggestions):
#     db = create_db_connection()
#     if db is None:
#         print("Failed to connect to the database.")
#         return

#     cursor = db.cursor()
#     try:
#         cursor.execute("""
#             INSERT INTO leads (name, email, website, gpt_suggestions) 
#             VALUES (%s, %s, %s, %s)
#         """, (name, email, website, gpt_suggestions))
#         db.commit()
#     except mysql.connector.Error as e:
#         print(f"Error inserting data into database: {e}")
#     finally:
#         close_db_connection(db, cursor)

# Function to scrape crunchbase data
# def scrape_crunchbase(company_name):
#     url = f'https://api.crunchbase.com/v4/organizations/{company_name}?user_key={CRUNCHBASE_API_KEY}'
#     try:
    
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#         businesses = data.get('data', {}).get('items',[])
#         return businesses
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching Crunchbase data: {e}")
#         return []

def scrape_apollo(domain):
    url = f'https://api.apollo.io/v1/organizations/search?domain={domain}'
    headers = {
        'Authorization': f'Bearer {"APOLLO_API_KEY"}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Apollo data: {e}")
        return {}

# Function to scrape google search results using Google custom Search API
def scrape_google(query):
    url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={CSE_ID}&q={query}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        search_results = data.get('items', [])
        return search_results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Google search data: {e}")
        return []

# Function to scrape emails from a website
def scrape_emails_from_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = []
        for a in soup.find_all('a', href=True):
            if 'mailto:' in a['href']:
                emails.append(a['href'].replace('mailto:', ''))
        return emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emails from website {url}: {e}")
        return []
    
# Function to enrich data using Ubersuggest API
# def enrich_with_ubersuggest(website):
#     url = f'https://ubersuggestapi.com/keyword_ideas?keyword={website}&country=us&source=web'
#     headers = {
#         'apikey': UBERSUGGEST_API_KEY
#     }
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         return data
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching Ubersuggest data: {e}")
#         return {}

# Function to use GPT for business analysis
def analyze_with_gpt(website):
    prompt = f"Review the website: {website} and suggest improvement for SEO and online presence."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a business consultant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
  
    except Exception as e:
        print(f"Error analyzing with GPT {website}: {e}")
        return "No suggestions found."

# Function to send Telegram messages (if needed)
def send_telegram_message(token, chat_id, message):
    url = f'https://api.telegram.org/bot7552533865:AAHj0otW3T2BqXiURwI7nFB8Z1SgjdVXtbA/sendMessage'
    data = {
        'chat_id': 7025151815,
        'text': message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")    

# Function to insert data into MySQL database
def insert_data_into_db(name, email, website, gpt_suggestions): #seo_score
    try:
        cursor.execute("""
                   INSERT INTO leads (name, email, website, gpt_suggestions) 
                   VALUES (%s, %s, %s, %s)
                   """, (name, email, website,  gpt_suggestions))
        db.commit()
    except mysql.connector.Error as e:
        print(f"Error inserting data into database: {e}")

def fetch_data_from_db():
    cursor.execute("SELECT * FROM leads")
    results = cursor.fetchall()
    return results

# Main function to orchestrate the scraping, enrichment and storing of data
# def main():
    #Scrap Crunchbase for businesses 
    # companies = ['apple', 'google', 'microsoft']
    # for company_name in companies:
    #     businesses = scrape_crunchbase(company_name)
    #     for business in businesses:
    #         name = business.get('name', 'Unknown')
    #         website = business.get('website', '')

    # query = "businesses in the tech industry"
    # search_results = scrape_google(query)

    # for result in search_results:
    #         name = result.get('title', 'Unknown')
    #         website = result.get('link', '')

            #Scrape emails from website
            # emails = scrape_emails_from_website(website)

            #Enrich business data with SEO insights
            # seo_data = enrich_with_ubersuggest(website)
            # seo_score = seo_data.get('seo_score', 0)

            # Use GPT for analysis and suggestions
            # gpt_suggestions = analyze_with_gpt(website)

            # Store the enriched data in MySQL database
#             for email in emails:
#                 insert_data_into_db(name, email, website,  gpt_suggestions)

# print(f"Data enrichment completed at {datetime.now()}")

#schedule the script to run every 4 hours

# if __name__ == "__main__":
#     while True:
#         main()
#         print("Sleeping for 4 hours...")
#         time.sleep(4 * 3600) # Sleep for 4 hours

# Function to handle the entire process (scraping, enriching, inserting into DB)
# def process_business_data(query):
#     # Step 1: Scrape Google for business data
#     search_results = scrape_google(query)
#     for result in search_results:
#         name = result.get('title', 'Unknown')
#         website = result.get('link', '')

        # Step 2: Scrape emails from the business website
        # emails = scrape_emails_from_website(website)

        # Step 3: Use GPT to analyze the website and suggest improvements
        # gpt_suggestions = analyze_with_gpt(website)

        # Step 4: Insert the data into the MySQL database for each email found
        # for email in emails:
        #     insert_data_into_db(name, email, website, gpt_suggestions)

# Orchestrating data collection from multiple sources
def collect_data_from_sources(website, domain):
    # Step 1: Scrape Apollo API for Business Data (using example.com as domain)
    apollo_data = scrape_apollo(domain)
    print("Apollo Data:", apollo_data)

    # Step 2: Scrape Google API for Business Search (using example.com as website)
    google_data = scrape_google(website)  # You can also pass a query here, such as company name
    print("Google Search Results:", google_data)

    # Step 3: Scrape Emails from Website (using https://www.example.com as website)
    emails = scrape_emails_from_website(website)
    print("Emails from Website:", emails)

    # Step 4: Analyze website using GPT for SEO suggestions (using https://www.example.com as website)
    gpt_suggestions = analyze_with_gpt(website)
    print("GPT Suggestions:", gpt_suggestions)

    # Step 5: Store the data in the DB
    for email in emails:
        insert_data_into_db(name="Business Name", email=email, website=website, gpt_suggestions=gpt_suggestions)


# @app.route('/process')
# def process_data():
#     # Example query to search for businesses in tech industry
#     query = "businesses in the tech industry"
    
#     # Example call to process business data
#     process_business_data(query)
    
#     # Send a message to Telegram after processing
#     bot_token = "7552533865:AAHj0otW3T2BqXiURwI7nFB8Z1SgjdVXtbA"  # Replace with your bot's token
#     chat_id = 7025151815  # Replace with your chat ID
#     message = "Business data processing has been completed successfully!"
    
#     send_telegram_message(bot_token, chat_id, message)
    
#     return "Business data processed and message sent to Telegram successfully!"

# Flask route for home page
@app.route('/')
def home():
    # Fetch data from the database
    # data = fetch_data_from_db()
    # db = create_db_connection()
    if db is None:
        return "Error connecting to the database."
    cursor = db.cursor()
    cursor.execute("SELECT * FROM leads")
    data = cursor.fetchall()
    # close_db_connection(db, cursor)

    # You can pass data from Python to the HTML template
    return render_template('index.html', data=data)

# Flask route to trigger the business data processing
@app.route('/process')
def process_data():
    # Example query to search for businesses in tech industry
    query = "About DevDisplay"
    # process_business_data(query)
    search_results = scrape_google(query)
    for result in search_results:
        name = result.get('title', 'Unknown')
        website = result.get('link', '')
        emails = scrape_emails_from_website(website)
        gpt_suggestions = analyze_with_gpt(website)
        for email in emails:
            insert_data_into_db(name, email, website, gpt_suggestions)

    # Send a message to Telegram after processing
    bot_token = "7552533865:AAHj0otW3T2BqXiURwI7nFB8Z1SgjdVXtbA"  # Replace with your bot's token
    chat_id = 7025151815  # Replace with your chat ID
    message = "Business data processing has been completed successfully!"
    
    send_telegram_message(bot_token, chat_id, message)
    return "Business data processed successfully!"

if __name__ == "__main__":
    domain = "devdisplay.org"  # Example domain for Apollo API
    website = "https://www.devdisplay.org"  # Example website URL to scrape and analyze
    collect_data_from_sources(website, domain)  # Collect and store data
    app.run(debug=True)


# print("-----shubh coding-----")