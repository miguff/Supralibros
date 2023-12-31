#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:17:39 2023

@author: geza
"""

#Python's built-in module for encoding and decoding JSON data
import json
# Python's built-in module for opening and reading URLs
from urllib.request import urlopen
# sample ISBN for testing: 1593276036

#test number: 9781617294433

def ISBNLookUp(ISBNNumber):
    # create getting started variables
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    isbn = str(ISBNNumber)
    
    # send a request and get a JSON response
    resp = urlopen(api + isbn)
    # parse JSON into Python as a dictionary
    book_data = json.load(resp)

    # create additional variables for easy querying
    try:
        volume_info = book_data["items"][0]["volumeInfo"]
    except:
        return "Nem található ilyen elem az adatbázisban"
    author = volume_info["authors"]
    # practice with conditional expressions!
    prettify_author = author if len(author) > 1 else author[0]

    # display title, author, page count, publication date
    # fstrings require Python 3.6 or higher
    # \n adds a new line for easier reading

    Title = volume_info['title']
    Author = prettify_author
    Publisher = volume_info['publisher']
    PublishedDate = volume_info['publishedDate']
    Language = volume_info['language']
    Category = volume_info['categories'][0]
    Description = volume_info['description']
    PageCount = volume_info['pageCount']
    Type = volume_info['printType']
    ISBNNumber = volume_info['industryIdentifiers'][0]['identifier']

    ReturnLista = [Title, Author, Publisher, PublishedDate, Category, Language, PageCount, Description, Type, ISBNNumber]
    
    return ReturnLista
