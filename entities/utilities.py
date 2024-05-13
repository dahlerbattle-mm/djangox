import tldextract
import random

# Ensure your `generate_random_number` function is correctly generating a unique number as needed.
def generate_random_number():
    return random.randint(100000, 999999)

def get_domain(url):
    extracted = tldextract.extract(url)
    return "{}.{}".format(extracted.domain, extracted.suffix)

def currency_to_country(currency_name):
    # Dictionary mapping currencies to their respective countries
    currencies_to_countries = {
        "United States Dollar": "United States",
        "Hong Kong Dollar": "Hong Kong", 
        "Japanese Yen": "Japan", 
        "Euro": "Europe", 
        "Canadian Dollar": "Canada",
        "British Pound": "Great Britian",
        "Swiss Franc": "Switzerland",
        "Australian Dollar": "Austrailia", 
        "Chinese Renminbi": "China", 
        "Chinese Yuan": "China",
        "New Zealand Dollar": "New Zealand", 
    }

    # Return the country if the currency is found, otherwise return 'Unknown'
    return currencies_to_countries.get(currency_name, "Unknown")
