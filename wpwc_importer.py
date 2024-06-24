import json
import os
import subprocess


def parse_product_data(input_string):
    # Load the JSON string into a Python dictionary
    product_data = json.loads(input_string)

    return product_data


input_string = """
{
    "title": "Nature Valley Crunchy Oats 'n Honey Granola Bars, 60 Bars, 44.7 OZ (30 Pouches)",
    "authors": [
        "Visit the Nature Valley Store"
    ],
    "feature_bullets": [
        "CRUNCHY GRANOLA BARS: Nature Valley Crunchy Oats 'n Honey Granola Bars combine delicious whole-grain oats with real honey for a breakfast snack or on-the-go treat",
        "BREAKFAST SNACK: Wholesome snacks with 22g of whole grain per serving (at least 48g recommended daily)",
        "PERFECTLY PORTABLE: Easy bars for snack time or an on-the-go invigorating treat; Perfect as a part of breakfast, for the pantry, lunch box, and hiking trail",
        "QUALITY INGREDIENTS: Hearty whole grain oats with no artificial flavors, artificial colors, or high fructose corn syrup",
        "CONTAINS: One 44.7 oz box of Nature Valley Crunchy Oats 'n Honey Granola Bars; 30 two-bar pouches; 60 bars total"
    ],
    "book_description": "",
    "product_description": "The Original Crunch. Nature Valley Oats 'n Honey Crunchy Granola Bars are a tasty snack made with whole-grain oats and a touch of honey. A portable snack perfect for the pantry, lunch box, and hiking trail. There are no artificial flavors, colors or high fructose corn syrup, and these snack bars contain 22g of whole grain per serving (at least 48g recommended daily). It's a breakfast snack bar, an office snack or an on-the-go treat everyone in your household can enjoy. At Nature Valley, we believe that what you put in is what you get out. So wherever the moment takes you and your family, you can rely on our great-tasting snacks to help keep you going. Includes 15 two-bar pouches, 30 bars total.",
    "images": [
        "https://m.media-amazon.com/images/I/51L7HYBOQzL.jpg",
        "https://m.media-amazon.com/images/I/51hTJHrT0iL.jpg",
        "https://m.media-amazon.com/images/I/51XDvsg0DaL.jpg",
        "https://m.media-amazon.com/images/I/61qQqpL5ifL.jpg",
        "https://m.media-amazon.com/images/I/51JEGYPzAJL.jpg",
        "https://m.media-amazon.com/images/I/51tnYzhCwTL.jpg",
        "https://m.media-amazon.com/images/I/519mrqw3ABL.jpg"
    ],
    "rating": 4.6,
    "reviews": 9938,
    "rank": 0,
    "cats": "",
    "price": 12.49
}
"""

product_data = parse_product_data(input_string)

# Initialize an empty list for image IDs
image_ids = []

# Download and import all images
for image in product_data['images']:
    # Generate a title for the image
    title = 'image_' + product_data['title'].replace(' ', '_')

    # Download the image
    if os.getenv('ENV') == 'dev':
        subprocess.run(['wget', '-P', './', image], check=True)
    else:
        subprocess.run(
            ['wget', '-P', '/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images', image], check=True)

    # Get the filename of the image
    filename = image.split('/')[-1]

    # Import the image into WordPress
    if os.getenv('ENV') == 'dev':
        result = """
        --2024-06-23 14:59:13--  https://m.media-amazon.com/images/I/81Kb5TVBQvL._SX425_.jpg
        Resolving m.media-amazon.com (m.media-amazon.com)... 2600:9000:2368:9400:1d:d7f6:39d3:d9e1, 2600:9000:2368:dc00:1d:d7f6:39d3:d9e1, 2600:9000:2368:b400:1d:d7f6:39d3:d9e1, ...
        Connecting to m.media-amazon.com (m.media-amazon.com)|2600:9000:2368:9400:1d:d7f6:39d3:d9e1|:443... connected.
        HTTP request sent, awaiting response... 200 OK
        Length: 37158 (36K) [image/jpeg]
        Saving to: ‘/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images/81Kb5TVBQvL._SX425_.jpg’

        81Kb5TVBQvL._SX425_.jpg                 100%[=============================================================================>]  36.29K  --.-KB/s    in 0.001s

        2024-06-23 14:59:13 (46.0 MB/s) - ‘/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images/81Kb5TVBQvL._SX425_.jpg’ saved [37158/37158]

        Imported file '/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images/81Kb5TVBQvL._SX425_.jpg' as attachment ID 97.
        """
        # Split the result into lines, remove empty lines, and get the last line
        id_line = [line for line in result.split('\n') if line.strip()][-1]
        print(f'id line: {id_line}')
    else:
        result = subprocess.run(
            ['wp', 'media', 'import', f'/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images/{filename}', '--title=' + title, '--featured_image'], check=True, text=True, capture_output=True)
        # Print the entire output
        print(f'Output: {result.stdout}')

        # Split the result into lines, remove empty lines, and get the last line
        id_line = [line for line in result.stdout.split(
            '\n') if line.strip()][-1]
        print(f'id line: {id_line}')

    # Get the ID of the imported image
    image_id = id_line.split(' ')[-1]
    image_ids.append(image_id)

# Now you can use the image IDs to create a product in WooCommerce
# Here's an example of how you might do this:
product_data = {
    'name': product_data['title'],
    'type': 'simple',
    # Use the parsed price
    'regular_price': product_data['price'],
    # Use the product description
    'description': product_data['product_description'],
    'short_description': '',
    'categories': [
            {
                'id': 22,  # You'll need to get the ID of the category you want to use
                'name': 'Products'  # Use the category name "Products"
            }
    ],
    'images': [{'id': id} for id in image_ids]
}
# Create the wp wc command
wp_wc_command = ['wp', 'wc', 'product', 'create', '--user=admin', '--name=' + product_data['name'], '--type=' + product_data['type'], '--regular_price=' +
                 str(product_data['regular_price']), '--description=' + product_data['description'], '--short_description=' + product_data['short_description'], '--categories=' + json.dumps(product_data['categories'])]

# Print the command for manual execution
print(' '.join(wp_wc_command))

# Optionally run the command
if os.getenv('ENV') == 'prod' and os.getenv('RUN_WP_WC_COMMAND', 'false') == 'true':
    subprocess.run(wp_wc_command, check=True)
