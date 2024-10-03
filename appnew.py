from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_amazon_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting product name
        product_name = soup.find('span', {'id': 'productTitle'})
        product_name = product_name.text.strip()

        # Extracting product price
        product_price = soup.find('span', {'class': 'a-price-whole'})
        if product_price:
            product_price = product_price.text.strip()
        else:
            product_price = 'Price not found.'

        return f'Amazon - Product Name: {product_name}<br>Price: {product_price}'
    else:
        return f'Failed to retrieve the page from Amazon. Status Code: {response.status_code}'

def get_flipkart_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting product name from Flipkart
        product_name = soup.find('span', {'class': 'B_NuCI'})
        product_name = product_name.text.strip()

        # Extracting product price from Flipkart
        product_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
        if product_price:
            product_price = product_price.text.strip()
        else:
            product_price = 'Price not found on Flipkart.'

        return f'Flipkart - Product Name: {product_name}<br>Price: {product_price}'
    else:
        return f'Failed to retrieve the page from Flipkart. Status Code: {response.status_code}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/amazon')
def amazon():
    product_url = request.args.get('product_url')
    result = get_amazon_data(product_url)
    return result

@app.route('/flipkart')
def flipkart():
    product_url = request.args.get('product_url')
    result = get_flipkart_data(product_url)
    return result

if __name__ == "__main__":
    app.run(debug=True)
