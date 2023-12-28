#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 00:15:26 2023

@author: geza
"""

from tkinter import *
from tkinter import messagebox as mb


class GUIInterface:
    
    def __init__(self):
        self.DisplayTitle()
        self.DisplayQuestions()

    
    def DisplayTitle(self):
        self.Title = Label(gui, text = "Kérlek add meg a könvy ISBN számát (13 vagy 10 karakter)")
        self.Title.grid(row=0, column=0)
        self.ISBNAnswerBox = StringVar()
        self.Box = Entry(gui, textvariable=self.ISBNAnswerBox)
        self.Box.grid(row=0, column=1)
        
    def DisplayQuestions(self):
        for i in range(len(MovieQuestions)):     
            self.MovieNameVar = StringVar()
            self.MovieNameVar.set(MovieQuestions[i])
            self.Question = Label(gui, textvariable=self.MovieNameVar)
            self.Question.grid(row=i+1, column=0)
        for i in range(len(MovieQuestions)):
            self.NameAnswer=StringVar()
            self.Box=Entry(gui,textvariable=self.NameAnswer)
            self.Box.grid(row=i+1,column=1)
            ListOfMovies.append(self.Box)
        

gui = Tk()
gui.geometry("800x450")
gui.title("Kérlek add meg a könyv ISBN számát")

global ListOfMovies
ListOfMovies = []

MovieQuestions = ["A könyv neve/Name of the book:", "A könyv szerzője/Author of the Book:", "3 betűs rövidítés/3 char abbreviation:","Tulajdonos/Owner:", "Kategória/Category:",
                  "Feltöltési dátum/LogDate", "Alá van írva/Is it dedicated?", "Leírása/Description:", "Értékelés/Rating:","Kiadó/Publisher:"]


Interface = GUIInterface()

gui.mainloop()        
    
    