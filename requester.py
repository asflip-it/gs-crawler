#!/usr/bin/env python
# coding: utf-8

import requests

CUSTOM_HEADERS = {'User-Agent': 'Some humble dude/1.0'}

def capture(page_url):
    return requests.get(page_url, headers=CUSTOM_HEADERS)
