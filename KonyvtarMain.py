#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 12:21:40 2023

@author: geza
"""

import pandas as pd
import sqlite3
import sys
import os
import tkinter as tk
from tkinter import filedialog as fd
from GUI_better import RunGUI

def main():
    
    # Az adatbázis nevének beálltása
    File = "Konyvtar.db"
    Connection = CreateDatabase(File)
    SQLAuthorTableCreation = """CREATE TABLE IF NOT EXISTS AuthorTable (
        ID integer PRIMARY KEY,
        AuthorName text Not Null
        );"""
    
    SQLPublisherTable = """ CREATE TABLE IF NOT EXISTS PublisherTable (
        ID integer PRIMARY KEY,
        PublisherName text Not Null
        );"""
    
    SQLBooksTableCreation = """CREATE TABLE IF NOT EXISTS BOOKSTable (
        ID integer PRIMARY KEY,
        BookTitle text Not Null,
        AuthorID integer Not Null,
        PublisherID integer Not Null,
        PublicationaDate text,
        Category text,
        Language text,
        PageCount int,
        Description text,
        Type text,
        ISBN text,
        SpecialID text Not Null,
        Owner text Not Null,
        LogDate text,
        Dedicated text,
        DedicateDescription text,
        Ratings integer,
        FOREIGN KEY (AuthorID) REFERENCES AuthorTable (ID),
        FOREIGN KEY (PublisherID) REFERENCES PublisherTable (ID)
        );"""
    
    CreateTables(Connection, SQLAuthorTableCreation)
    CreateTables(Connection, SQLPublisherTable)
    CreateTables(Connection, SQLBooksTableCreation)
    
    
    ListOfMovies = RunGUI()

 
       
    #Itt felvisszük a dolgokat
    Author = [ListOfMovies.pop(1)]
    Publisher = [ListOfMovies.pop(1)]   
   
    AuthorID = AddAuthor(Connection, Author)
    PublisherID = AddPublisher(Connection, Publisher)
    
    ListOfMovies.insert(len(ListOfMovies), int(AuthorID))
    ListOfMovies.insert(len(ListOfMovies), int(PublisherID))
    print(ListOfMovies)

    Book = ListOfMovies
    AddBook(Connection, Book)
    
    SQL = """SELECT * FROM BOOKSTable"""
    df = pd.read_sql(SQL,Connection)
    print(df)


def AddAuthor(conn, Value):
    """
    
    
    Parameters
    ----------
    conn : Kapcsolódás/Connection
    Value : String
        Szerző neve, Name of Author
        
    Return
    ----------
    Visszaadja az index számát
    Returns the index number

    """
    
    SQLTest = f"""SELECT * FROM AuthorTable WHERE AuthorName = '{Value[0].upper()}';"""
    df = pd.read_sql(SQLTest,conn)
    
    if len(df) >= 1:
        None
    else:
        Value = [x.upper() for x in Value]
        SQLInsert = """INSERT INTO AuthorTable(AuthorName) VALUES (?)"""
        Cursor = conn.cursor()
        Cursor.execute(SQLInsert, Value)
        conn.commit()
    df = pd.read_sql(SQLTest,conn)
    return df['ID'].iloc[0]
    
def AddPublisher(conn, Value):
    """
    Parameters
    ----------
    conn : Kapcsolódás/Connection
    Value : String
        Kiadó neve, Name of Publisher
    
    Return
    ----------
    Visszaadja az index számát
    Returns the index number

    """
    
    SQLTest = f"""SELECT * FROM PublisherTable WHERE PublisherName = '{Value[0].upper()}';"""
    df = pd.read_sql(SQLTest,conn)
    
    if len(df) >= 1:
        None
    else:
        Value = [x.upper() for x in Value]
        SQLInsert = """INSERT INTO PublisherTable(PublisherName) VALUES (?)"""
        Cursor = conn.cursor()
        Cursor.execute(SQLInsert, Value)
        conn.commit()   
    df = pd.read_sql(SQLTest,conn)
    return df['ID'].iloc[0]
    

def AddBook(conn, Values: list):
    """
    

    Parameters
    ----------
    conn : Kapcsolódás az adatbázishoz/Connection to Database
        DESCRIPTION.
    Values :  Az értékek, amiket fel kell töltenie.
        Values which will be uploaded

    """

    SQL_row = f"SELECT * FROM BOOKSTable WHERE Owner = '{Values[-7].upper()}'"
    DfMeglevo = pd.read_sql(SQL_row, conn)
    Cursor = conn.cursor()
    Cursor.execute(SQL_row)
    conn.commit()
    NumberOfOwnerBook = len(DfMeglevo) + 1

    #Speciális ID értéke / Special ID
    Values[-8] = f"{Values[-8].upper()}{NumberOfOwnerBook}"
    
    #A könyv címe / Title of the Book
    Values[0] = Values[0].upper()

    #A könyv tulajdonosa / Owner of the book
    Values[2] = Values[2].upper()

    
    SQLInsert = """INSERT INTO BooksTable(BookTitle, PublicationaDate, Category, Language, 
    PageCount, Description, Type, ISBN, SpecialID, Owner,  
    LogDate, Dedicated, DedicateDescription, Ratings, AuthorID, PublisherID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    
    
    SQLNewBookTest = f"""SELECT BookTitle FROM BooksTable WHERE BookTitle = '{Values[0]}'"""
    df = pd.read_sql(SQLNewBookTest,conn)
    if len(df) >= 1:
        print("Van már ilyen könyv")
    else:    
        Cursor.execute(SQLInsert, Values)
        conn.commit()
    
    
    
    

def CreateDatabase(path):
    """
    

    Parameters
    ----------
    path : String
        Ahova menteni akarjuk az adatbázist.

    Returns
    -------
    conn : Kapcsolódás az adatbázishoz/Connection to Database
        

    """
    try: 
        conn = sqlite3.connect(path) 
        print("Megcsináltam az Adatbázist./Database has been created.") 
        return conn
    except: 
        print("Az Adatbázist nem sikerült megcsinálni. Most kilépek / Database was not formed. I am quitting.")
        sys.exit()
    
def CreateTables(conn, CreateTableSQL):
    """

    Parameters
    ----------
    conn : Kapcsolódás az adatbázishoz/Connection to Database
    CreateTableSQL : String
        Adatbázis Tábla SQL stringje
        Database Table creation string

    """
    
    try:
        Connection = conn.cursor()
        Connection.execute(CreateTableSQL)
    except Exception as e:
        print(e)
    
    
    
if __name__ == "__main__":
    main()