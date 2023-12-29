#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 00:15:26 2023

@author: geza
"""

from tkinter import *
from ISBN_database import ISBNLookUp

class NewWindows(Toplevel):
    
    def __init__(self, master=None, NewData = None, List = []):
        super().__init__(master=master)
        self.title("Kérlek Töltsd fel az adatokat")
        self.geometry("600x400")
        self.NewData = NewData
        self.ListData = List
        self.DisplayQuestions(self.ListData)
    
    def DisplayQuestions(self, ListValue=[]):
        for i in range(len(MovieQuestions)):     
            self.MovieNameVar = StringVar()
            self.MovieNameVar.set(MovieQuestions[i])
            self.Question = Label(self, textvariable=self.MovieNameVar)
            self.Question.grid(row=i+1, column=0)
        for i in range(len(MovieQuestions)):
            self.NameAnswer=StringVar(self)
            
            
            if MovieQuestions[i] == "Aláírt vagy Dedikált?/Is it Signed or Dedicated?":
                self.NameAnswer.set("Nincs/No")
                w = OptionMenu(self, self.NameAnswer, "Nincs/No", "Aláírt/Signed", "Dedikált/Dedicated")
                w.grid(row=i+1,column=1)
                ListOfMovies.append(self.NameAnswer)
            
            elif i < len(ListValue):
                self.Box=Entry(self,textvariable=self.NameAnswer)
                self.Box.insert(0, ListValue[i])
                self.Box.grid(row=i+1,column=1)
                ListOfMovies.append(self.Box) 
            
            else:
                self.Box=Entry(self,textvariable=self.NameAnswer)
                self.Box.grid(row=i+1,column=1)
                ListOfMovies.append(self.Box)
            
            
        self.ExitButton = Button(self, text="Kilépés a programból", command=self.Exit)
        self.ExitButton.grid(row=i+1, column=2)

        ButtonAccept = Button(self, text = "Feltöltés/Upload", command=self.GetData)
        ButtonAccept.grid(row=1,column=2)


    def Exit(self):
        self.destroy()
    
    def GetData(self):
        """

        Returns
        -------
        None.

        """
        for i in range(len(ListOfMovies)):
            ListOfMovies[i] = ListOfMovies[i].get()
        print("Elvégeztem a szükséges műveletet")

class GUIInterface:
    
    def __init__(self, gui):
        self.gui = gui
        self.ISBNData = []
        self.DisplayTitle()
        self.Answer = IntVar()
        
        #self.DisplayQuestions()
        
    
    def DisplayTitle(self):
        self.Title = Label(self.gui, text = "Kérlek add meg a könvy ISBN számát (13 vagy 10 karakter)")
        self.Title.grid(row=0, column=0)
        self.ISBNAnswerBox = StringVar()
        self.Box = Entry(self.gui, textvariable=self.ISBNAnswerBox)
        #Ez csak tesztelés miatt van itt, hogy ne kelljen mindig beírni a ISBN-t
        self.Box.insert(0, 1617294438)

        self.Box.grid(row=0, column=1)
        self.ButtonSearch = Button(self.gui, text="Ellenőrzés, hogy van-e az adatbázisban", command=self.ISBNAnswer)
        self.ButtonSearch.grid(row=0, column=2)
        self.ExitButton = Button(self.gui, text="Kilépés a programból", command=self.Exit)
        self.ExitButton.grid(row=1, column=2)


    def ISBNAnswer(self):
        Valtozo = self.Box.get()
        self.ISBNData = ISBNLookUp(Valtozo)
        if isinstance(self.ISBNData, list):
            NewWindows(self.gui, List=self.ISBNData)
        else:
            NewWindows(self.gui)
    
    def Exit(self):
        self.gui.destroy()

        

def RunGUI():

    gui = Tk()
    gui.geometry("800x450")
    gui.title("Kérlek add meg a könyv ISBN számát")

    global ListOfMovies
    ListOfMovies = []

    global MovieQuestions 
    MovieQuestions = ["A könyv neve/Name of the book:", "A könyv szerzője/Author of the Book:", "Kiadó/Publisher:", "Kiadás ideje/Publication Date","Kategória/Category:",
                  "Nyelv/Language", "Oldalszám/Page Count", "Leírása/Description:", "Típus/Type", "ISBN azanosító/ISBN identifie:",
                  "3 betűs rövidítés/3 char abbreviation:","Tulajdonos/Owner:","Feltöltési dátum/LogDate", "Aláírt vagy Dedikált?/Is it Signed or Dedicated?", "Dedikáció leírása/Description of Dedication:", "Értékelés/Rating:"]
    Interface = GUIInterface(gui)
    gui.mainloop()   

    return ListOfMovies     
