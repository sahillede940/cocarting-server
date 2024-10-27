import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


async def fetch_selectors(website_name):
    try:
        response = requests.post(
            'https://cron-job-9njv.onrender.com/selector',
            headers={
                'Content-Type': 'application/json'
            },
            json={'website_name': website_name}
        )

        if response.status_code != 200:
            raise Exception(f"Failed to fetch: {response.status_code}")

        data = response.json()
        return data
    except Exception as error:
        print(f"Error fetching selectors: {error}")
        return None


def get_valid_data(selector, attr=None):
    if selector:
        if attr:
            return selector.get(attr, None)
        return selector.text.strip()
    return None


async def scrape_product_data(page_html, url):
    try:
        soup = BeautifulSoup(page_html, 'html.parser')
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return None

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    product_title = ''
    product_price = ''
    mrp_price = ''
    rating = ''
    image_url = ''

    if "amazon" in hostname:
        product_title = soup.select_one('#productTitle').get_text(
            strip=True) if soup.select_one('#productTitle') else 'Title not available'

        price_whole = soup.select_one('.a-price .a-price-whole').get_text(
            strip=True) if soup.select_one('.a-price .a-price-whole') else ''
        price_fraction = soup.select_one('.a-price .a-price-fraction').get_text(
            strip=True) if soup.select_one('.a-price .a-price-fraction') else '00'

        if price_whole:
            product_price = f"₹{price_whole}"
        else:
            product_price = 'Price not available'

        mrp_price = soup.select_one('.a-price.a-text-price .a-offscreen').get_text(strip=True) or \
            soup.select_one('.basisPrice .a-price .a-offscreen').get_text(strip=True) if soup.select_one(
                '.basisPrice .a-price .a-offscreen') else 'MRP not available'

        rating_text = soup.select_one('#acrPopover').get('title', '').strip(
        ) if soup.select_one('#acrPopover') else 'Rating not available'
        rating = rating_text.split(
            ' ')[0] if 'out of' in rating_text else 'Rating not available'

        # Fix for image URL extraction to handle multiple potential sources
        image_element = soup.select_one('.a-dynamic-image.a-stretch-vertical')
        if image_element:
            image_url = image_element.get(
                'data-old-hires') or image_element.get('src')
        else:
            image_element = soup.select_one(
                'span.a-declarative[data-action="main-image-click"] img')
            if image_element:
                image_url = image_element.get(
                    'data-old-hires') or image_element.get('src')
            else:
                image_url = 'Image not available'

    elif "flipkart" in hostname:
        product_title = soup.select_one(
            '.VU-ZEz').get_text(strip=True) if soup.select_one('.VU-ZEz') else 'Title not available'
        product_price = soup.select_one('.Nx9bqj').get_text(
            strip=True) if soup.select_one('.Nx9bqj') else 'Price not available'
        mrp_price = soup.select_one('.yRaY8j').get_text(
            strip=True) if soup.select_one('.yRaY8j') else 'MRP not available'
        rating = soup.select_one('.XQDdHH').get_text(
            strip=True) if soup.select_one('.XQDdHH') else 'Rating not available'
        image_url = soup.select_one('.DByuf4').get(
            'src') if soup.select_one('.DByuf4') else 'Image not available'

    else:
        selectors = await fetch_selectors(hostname)
        if not selectors:
            print('No selectors found for this website')
            return

        product_title = get_valid_data(soup.select_one(
            selectors.get('title'))) or "Title N/A"
        product_price = get_valid_data(soup.select_one(
            selectors.get('current'))) or "Price N/A"
        mrp_price = get_valid_data(soup.select_one(
            selectors.get('mrp'))) or "MRP N/A"
        rating = get_valid_data(soup.select_one(
            selectors.get('rating'))) or "Rating N/A"
        image_url = get_valid_data(soup.select_one(
            selectors.get('image')), 'src') or "Image N/A"

    product_url = url
    website_name = "Amazon" if "amazon" in hostname else "Flipkart" if "flipkart" in hostname else "Unknown Website"

    return {
        "name": product_title,
        "original_price": mrp_price,
        "customer_rating": rating,
        "price": product_price,
        "product_tracking_url": product_url,
        "slug": product_url,
        "image": image_url}
