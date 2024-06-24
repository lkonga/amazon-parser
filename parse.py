#!/usr/bin/env python3

import sys
import json
import os
from amazon_page_parser.parsers import DetailParser
from amazon_page_parser.parsers import OfferListingParser


def escape_control_characters(s):
    return s.encode('unicode_escape').decode()


def parse_page(page_path):

    with open(page_path, 'r') as f:
        c = f.read()
    try:
        parser = DetailParser(c)
        parser2 = OfferListingParser(c)

        offer_listing = parser2.parse()
    except Exception as e:
        print(f"Error parsing file {file}: {str(e)}")
        return None  # or however you want to handle this case

    data = dict(
        title=parser.parse_title(),
        authors=parser.parse_author(),
        feature_bullets=parser.parse_feature_bullets(),
        book_description=parser.parse_book_description(),
        product_description=parser.parse_product_description(),
        images=parser.parse_images(),
        rating=parser.parse_star(),
        reviews=parser.parse_reviews(),
        rank=parser.parse_rank(),
        cats=parser.parse_categories(),
        # details=parser.parse_details(),
        price=offer_listing['offers'][0]['price'] if offer_listing['offers'] else None
    )

    # Apply the escape function to your strings
    data = {k: escape_control_characters(v) if isinstance(
        v, str) else v for k, v in data.items()}

    return data


# Get a list of all files in the directory
files = os.listdir('pages_html_output')

# Loop over each file
for file in files:
    # Parse the page and get the data
    data = parse_page(f'pages_html_output/{file}')
    if data is not None and data['price'] is not None and data['price'] != 0:
        # Write the data to a JSON file
        with open(f'pages_html_output/{os.path.splitext(file)[0]}.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=True)
    else:
        print(f"Skipping file {file} due to missing or null price.")
