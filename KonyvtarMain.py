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
        SpecialID text Not Null,
        AuthorID integer Not Null,
        Owner text Not Null,
        Category text,
        LogDate text,
        Dedicated text,
        Description text,
        Ratings integer,
        PDFFile text,
        PublisherID integer Not Null,
        FOREIGN KEY (AuthorID) REFERENCES AuthorTable (ID),
        FOREIGN KEY (PublisherID) REFERENCES PublisherTable (ID)
        );"""
    
    CreateTables(Connection, SQLAuthorTableCreation)
    CreateTables(Connection, SQLPublisherTable)
    CreateTables(Connection, SQLBooksTableCreation)
    
    
    #Create GUI for adding data to data database
    global ListOfMovies
    ListOfMovies = []
    Window = tk.Tk()
    Window.wm_title("Tölts fel adatot az Adatbázisba/Upload data to Database.")
    
    #Film neve - kérdés / Name of the movies - question
    MovieQuestions = ["A könyv neve/Name of the book:", "A könyv szerzője/Author of the Book:", "3 betűs rövidítés/3 char abbreviation:","Tulajdonos/Owner:", "Kategória/Category:",
                      "Feltöltési dátum/LogDate", "Alá van írva/Is it dedicated?", "Leírása/Description:", "Értékelés/Rating:","Kiadó/Publisher:", "Elérési útja/Location Path:"]
    
    for i in range(len(MovieQuestions)):     
        MovieNameVar = tk.StringVar()
        MovieNameVar.set(MovieQuestions[i])
        Label = tk.Label(Window, textvariable=MovieNameVar, height = 2)
        Label.grid(row=i,column=0)
    
    

    #Film neve - válasz / Name of the Movie - answer
    for i in range(len(MovieQuestions)):
        NameAnswer=tk.StringVar()
        Box=tk.Entry(Window,bd=4,textvariable=NameAnswer)
        Box.insert(0, "alma")
        Box.grid(row=i,column=1)
        ListOfMovies.append(Box)
    
    ButtonBrowseFile = tk.Button(Window,text="Browse File",command=lambda: browsefunc(Box))
    ButtonBrowseFile.grid(row = i, column=2)
    

    ButtonAccept = tk.Button(Window, text = "Feltöltés/Upload", command=GetData)
    ButtonAccept.grid(row=0,column=2)
    
    Window.mainloop()
       
    #Itt felvisszük a dolgokat
    Author = [ListOfMovies.pop(1)]
    Publisher = [ListOfMovies.pop(-2)]   
   
    AuthorID = AddAuthor(Connection, Author)
    PublisherID = AddPublisher(Connection, Publisher)
    
    ListOfMovies.insert(len(ListOfMovies), int(AuthorID))
    ListOfMovies.insert(len(ListOfMovies), int(PublisherID))


    Book = ListOfMovies
    AddBook(Connection, Book)
    
    SQL = """SELECT * FROM BOOKSTable"""
    df = pd.read_sql(SQL,Connection)
    print(df)
 
def browsefunc(ent1):
    """
    

    Parameters
    ----------
    ent1 : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    filename =fd.askopenfilename(filetypes=(("pdf files","*.pdf"),("All files","*.*")))
    ent1.insert(tk.END, filename) # add this
    
 
def GetData():
    """
    

    Returns
    -------
    None.

    """
    for i in range(len(ListOfMovies)):
        ListOfMovies[i] = ListOfMovies[i].get()
    print("Elvégeztem a szükséges műveletet")
    #l.append(box.get())
    #print(l)    


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

    SQL_row = f"SELECT * FROM BOOKSTable WHERE Owner = '{Values[2].upper()}'"
    DfMeglevo = pd.read_sql(SQL_row, conn)
    Cursor = conn.cursor()
    Cursor.execute(SQL_row)
    conn.commit()
    NumberOfOwnerBook = len(DfMeglevo) + 1

    
    Values[1] = f"{Values[1].upper()}{NumberOfOwnerBook}"
    Values[0] = Values[0].upper()
    Values[2] = Values[2].upper()

    
    SQLInsert = """INSERT INTO BooksTable(BookTitle, SpecialID,
     Owner, Category, LogDate, Dedicated, Description, Ratings, PDFFile, AuthorID, PublisherID)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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