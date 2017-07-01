#!/usr/bin/env python
# coding: utf-8

import datetime

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


def pipeline(data, *funcs):
    allowed_dtypes = [NavigableString, unicode, str]
    for f in funcs:
        if type(data) is list:
            data = map(f, data)
        elif type(data) in allowed_dtypes:
            data = f(data)
        else:
            raise Exception('Unexpected data structure. Exiting.')

    return data

def extract_articles_from_page(html):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.select('#js-sort-filter-results > section.editorial.river > article')
    return articles

def extract_title(element):
    s = element.find('a', class_='js-event-tracking')
    title = s.attrs.get('data-event-title').split()[:-1]  # striping the " Review" part
    return ' '.join(title)  # rebuilding the former title

def extract_review_url(element):
    s = element.find('a', class_='js-event-tracking')
    return s.attrs.get('href')

def extract_score(element):
    s = element.find('span', class_='content').string
    if s.isdigit():
        return pipeline(s, int)
    return None

def extract_classified_as(element):
    s = element.find('span', class_='score-word')
    return pipeline(s.string, NavigableString.lower, NavigableString.capitalize)

def extract_reviewer_platform(element):
    s = element.select('li.system.label + li')[0]
    return pipeline(s.string, NavigableString.upper)

def extract_reviewed_on(element):
    s = element.footer.time.attrs.get('datetime')
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

def extract_single_phrase_review(element):
    s = element.find('p', class_='media-deck')
    return pipeline(s.string, NavigableString.strip)

def extract_metadata_from_article(article):
    title = extract_title(article)
    review_url = extract_review_url(article)
    score = extract_score(article)
    classified_as = extract_classified_as(article)
    reviewer_platform = extract_reviewer_platform(article) 
    reviewed_on = extract_reviewed_on(article)
    single_phrase_review = extract_single_phrase_review(article) 

    metadata = {
        'title': title,
        'review_url': review_url,
        'score': score,
        'classified_as': classified_as,
        'reviewer_platform': reviewer_platform,
        'reviewed_on': reviewed_on,
        'single_phrase_review': single_phrase_review
    }

    return metadata

def parse_page(content):
    articles = extract_articles_from_page(content)
    return pipeline(articles, extract_metadata_from_article)
