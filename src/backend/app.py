from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from the React frontend

def parse_price(price_str):
    # Remove any non-numeric characters except for periods (in case of decimal prices)
    clean_price = ''.join(c for c in price_str if c.isdigit())
    
    if clean_price:
        return int(clean_price)
    else:
        return 0  # Return 0 if the price string cannot be parsed



# Flipkart Scraper
def get_flipkart_search_page(query):
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_flipkart_products(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    products = []

    product_blocks = soup.find_all("a", {"class": "CGtC98"})
    for product_div in product_blocks:
        title = product_div.find("div", {"class": "KzDlHZ"})
        title_text = title.text.strip() if title else 'No title available'
        link = "https://www.flipkart.com" + product_div['href']

        price_div = product_div.find("div", {"class": "Nx9bqj _4b5DiR"})
        price = price_div.text.strip() if price_div else "Price not available"

        rating_div = product_div.find("div", {"class": "XQDdHH"})
        rating = rating_div.text.strip() if rating_div else "Rating not available"

        products.append({
            "title": title_text,
            "link": link,
            "price": price,
            "rating": rating,
            "source":"flipKart",
        })

    return products

# Amazon Scraper
def get_amazon_search_page(query):
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_amazon_products(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    products = []

    for product_div in soup.find_all("div", {"data-component-type": "s-search-result"}):
        title = product_div.h2.text.strip()
        link = "https://www.amazon.in" + product_div.h2.a['href']

        # Extracting the price if available
        price = product_div.find("span", class_="a-price-whole").text.strip()

        # Extracting the rating if available
        rating_span = product_div.find("span", class_="a-icon-alt")
        rating = rating_span.text.strip() if rating_span else None

        products.append({
            "title": title,
            "link": link,
            "price": price,
            "rating": rating,
            "source":"Amazon"
        })

    return products

# API Route
@app.route('/', methods=['GET'])
def get_products():
    query = request.args.get('query', 'laptop')  # Default query is 'laptop'
    print(query)
    # Get Flipkart data
    flipkart_page_content = get_flipkart_search_page(query)
    flipkart_products = parse_flipkart_products(flipkart_page_content) if flipkart_page_content else []

    # Get Amazon data
    amazon_page_content = get_amazon_search_page(query)
    amazon_products = parse_amazon_products(amazon_page_content) if amazon_page_content else []

    # Combine results
    combined_results=[]
    combined_results.extend(flipkart_products);
    combined_results.extend(amazon_products);
    print(len(combined_results[0]['price']));
    combined_results.sort(key=lambda x: parse_price(x['price']) if x['price'] and x['price'] != "Price not available" else float('inf'))


    return jsonify(combined_results)

if __name__ == '__main__':
    app.run(debug=True)
