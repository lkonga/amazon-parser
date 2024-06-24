import json
import os
import random
import subprocess

# Get the value of the 'ENV' environment variable
ENV = os.getenv('ENV')


def parse_product_data(input_string):
    # Load the JSON string into a Python dictionary
    product_data = json.loads(input_string)

    return product_data


# Ask the user to enter the debug mode
debug_mode = input("Enter debug mode? (yes/no): ").lower() == "yes"

# Ask the user to run the wp wc command
run_wp_wc_command = input("Run wp wc command? (yes/no): ").lower() == "yes"

# Get a list of all JSON files in the directory
files = [f for f in os.listdir('pages_html_output') if f.endswith('.json')]

# Loop over each file
for file in files:
    # Open the file and read its contents
    with open(f'pages_html_output/{file}', 'r') as f:
        input_string = f.read()

    product_data = parse_product_data(input_string)

    # Initialize an empty list for image IDs
    image_ids = []

    # Download and import all images
    for image in product_data['images']:
        # Generate a title for the image
        title = 'image_' + product_data['title'].replace(' ', '_')

        # Download the image
        if debug_mode:
            subprocess.run(['wget', '-P', './', image], check=True)
        else:
            subprocess.run(
                ['wget', '-P', '/home/hestia/web/newgiftonlineindia.store/public_html/amazon_images', image], check=True)

        # Get the filename of the image
        filename = image.split('/')[-1]

        # Import the image into WordPress
        if ENV == 'dev':
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

            # If debug mode is on, print the entire output and ID line
            if debug_mode:
                print(f'Output: {result.stdout}')
            id_line = [line for line in result.stdout.split(
                '\n') if line.strip()][-2]
            if debug_mode:
                print(f'id line: {id_line}')

            # Extract the ID from the id_line
            image_id = id_line.split(' ')[-1]

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

    # Generate a random factor between 8.5 and 9.5
    factor = random.uniform(8.5, 9.5)
    # Multiply the price by the factor and round the result
    product_data['regular_price'] = round(
        product_data['regular_price'] * factor)

    # Create the wp wc command
    wp_wc_command = ['wp', 'wc', 'product', 'create', '--user=admin', '--name="' + product_data['name'] + '"', '--type=' + product_data['type'], '--regular_price=' +
                     str(product_data['regular_price']), '--description="' + product_data['description'] + '"', '--short_description="' + product_data['short_description'] + '"', '--categories=' + json.dumps(product_data['categories']), '--images=' + json.dumps(product_data['images'])]
    # If debug mode is on, print the command for manual execution
    if debug_mode:
        print(' '.join(wp_wc_command))

    # If ENV is 'dev', ask for confirmation before running the command
    if ENV == 'dev':
        confirm = input(
            "Do you want to run this command? (yes/no): ").lower() == "yes"
        if not confirm:
            continue

    # Run the command if ENV is 'prod'
    if ENV == 'prod':
        subprocess.run(wp_wc_command, check=True)
    else:
        print("Not running the command, not in prod ENV")
