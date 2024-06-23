#!/usr/bin/env python3

import sys
import json
from amazon_page_parser.parsers import DetailParser
from amazon_page_parser.parsers import OfferListingParser


def escape_control_characters(s):
    return s.encode('unicode_escape').decode()


def parse_page(page_path):

    with open(page_path, 'r') as f:
        c = f.read()

    parser = DetailParser(c)
    parser2 = OfferListingParser(c)

    offer_listing = parser2.parse()

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

    print(json.dumps(data, indent=4, ensure_ascii=True))


parse_page(sys.argv[1])
