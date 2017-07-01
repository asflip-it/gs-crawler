#!/usr/bin/env python
# coding: utf-8

import parser
import requester

from bs4 import BeautifulSoup

BASE_URL = "https://www.gamespot.com/reviews/?review_filter_type[platform]=19&sort=date&page=1"

if __name__ == '__main__':
    response = requester.capture(BASE_URL)
    print parser.parse_page(response.content)
