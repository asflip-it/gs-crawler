#!/usr/bin/env python
# coding: utf-8

import time
import parser
import requester

from bs4 import BeautifulSoup

BASE_URL = "https://www.gamespot.com/reviews/?review_filter_type[platform]=19&sort=date&page={}"

if __name__ == '__main__':
    response = []
    for page in range(1, 6):
        page_url = BASE_URL.format(page)
        page_response = requester.capture(page_url)
        print 'Requested page {} sucessfull'.format(page_url)
        time.sleep(3)
        page_response = parser.parse_page(page_response.content)
        response.append(page_response)

    print response
