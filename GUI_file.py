#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:38:15 2023

@author: geza
"""

import tkinter as tk
from tkinter import filedialog as fd


class NewWindows(tk.Toplevel):
    
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("New Window")
        self.geometry("600x400")
        Label = tk.Label(self, text = "This is a new windows").pack()

    
class NewQuestions(tk.Toplevel):
    
    def __init__(self, master = None):
        super().__init__(master=master)
        
    def EntryQuestions(self):
        self.Name = Name 
        

def GeomSetup():
    master = tk.Tk()
    master.geometry("600x400") 
    Label = tk.Label(master, text = "This is the main window")
    Label.pack(pady=10)
    #Btn = tk.Button(master, text="Click to open a new window", command=lambda: OpenNewWindows(master))
    Btn = tk.Button(master, text = "Click to open a new window")
    Btn.bind("<Button>", lambda e: NewWindows(master))
    Btn.pack(pady=10)
    
    master.mainloop()
    


def OpenNewWindows(MasterWindow):
    NewWindow = tk.Toplevel(MasterWindow)
    
    NewWindow.title("Új adat")
    NewWindow.geometry("600x400")
    tk.Label(NewWindow, text = "This is a new windows").pack()
    
GeomSetup()