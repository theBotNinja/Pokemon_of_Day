from random import randint
import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import requests
import threading
from io import BytesIO
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from tkinter import messagebox

class App:
    def __init__(self,root):
        self.root = root
        self.ATTACK = -1
        self.HP = -1
        self.DEFENCE = -1
        self.SPEED = -1
        self.TrainModel()
        tk.Label(self.root,text="Pokemon of Day", font=("asdfsd",20,"bold")).pack()

    def Gui(self):
        self.mainFrame = tk.Frame(self.root,background="#f4f1de")
        f1 = tk.Frame(self.mainFrame)
        f2 = tk.Frame(self.mainFrame)
        f3 = tk.Frame(self.mainFrame)
        f4 = tk.Frame(self.mainFrame)
        self.Hp_bnt = tk.Button(f1,text=self.HP,font=("Helvetica",20,"bold"),background="#81b29a",activebackground="#f4f1de",command=self.setHP)
        self.Att_bnt = tk.Button(f2,text=self.ATTACK,font=("Helvetica",20,"bold"),background="#e07a5f",activebackground="#f4f1de",command=self.setAttack)
        self.Def_bnt = tk.Button(f3,text=self.DEFENCE,font=("Helvetica",20,"bold"),background="#3d405b",activebackground="#f4f1de",command=self.setDefence)
        self.Speed_bnt = tk.Button(f4,text=self.SPEED,font=("Helvetica",20,"bold"),background="#f2cc8f",activebackground="#f4f1de",command=self.setSpeed)
        tk.Label(f1,text= "HP",font=("somefont",12,"bold"),background="#81b29a").pack(side=tk.TOP,fill=tk.X)
        self.Hp_bnt.pack(fill=tk.BOTH,expand=tk.TRUE)
        tk.Label(f1,text= "click to set hp",font=("somefont",8,"normal"),background="#81b29a").pack(side=tk.BOTTOM,fill=tk.X)
        tk.Label(f2,text= "Attack",font=("somefont",12,"bold"),background="#e07a5f").pack(side=tk.TOP,fill=tk.X)
        self.Att_bnt.pack(fill=tk.BOTH,expand=tk.TRUE)
        tk.Label(f2,text= "click to set Attack",font=("somefont",8,"normal"),background="#e07a5f").pack(side=tk.BOTTOM,fill=tk.X)
        tk.Label(f3,text= "DEFENCE",font=("somefont",12,"bold"),background="#3d405b").pack(side=tk.TOP,fill=tk.X)
        self.Def_bnt.pack(fill=tk.BOTH,expand=tk.TRUE)
        tk.Label(f3,text= "click to set Defence",font=("somefont",8,"normal"),background="#3d405b").pack(side=tk.BOTTOM,fill=tk.X)
        tk.Label(f4,text= "SPEEd",font=("somefont",12,"bold"),background="#f2cc8f").pack(side=tk.TOP,fill=tk.X)
        self.Speed_bnt.pack(fill=tk.BOTH,expand=tk.TRUE)
        tk.Label(f4,text= "click to set Speed",font=("somefont",8,"normal"),background="#f2cc8f").pack(side=tk.BOTTOM,fill=tk.X)
        f1.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=10,expand=tk.TRUE)
        f2.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=10,expand=tk.TRUE)
        f3.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=10,expand=tk.TRUE)
        f4.pack(side=tk.LEFT,fill=tk.BOTH,padx=10,pady=10,expand=tk.TRUE)
        self.mainFrame.pack(fill=tk.BOTH,expand=tk.TRUE,padx=10,pady=10)
        self.start_btn = tk.Button(self.root,text="Start",background="#d6ccc2",font=("somefont",15,"bold"),command=self.makeGuess)
        self.start_btn.pack(fill=tk.X)
    
    def setHP(self):
        self.HP = randint(1,255)
        self.Hp_bnt.config(text = self.HP)
    
    def setAttack(self):
        self.ATTACK = randint(5,180)
        self.Att_bnt.config(text = self.ATTACK)
    
    def setDefence(self):
        self.DEFENCE = randint(5,230)
        self.Def_bnt.config(text = self.DEFENCE)
    
    def setSpeed(self):
        self.SPEED = randint(5,180)
        self.Speed_bnt.config(text = self.SPEED)
    
    def parallelcall(self):
        self.pokemon_got = self.classifier.predict(self.sc.transform([[self.HP,self.ATTACK,self.DEFENCE,self.SPEED]]))[0]
        try:
            URL = "https://pokeapi.co/api/v2/pokemon/"+self.pokemon_got
            res = requests.get(URL)
            if res.status_code == 200:
                data = res.json()
                img_URL = data["sprites"]["front_default"]
                response = requests.get(img_URL)
                if response.status_code == 200:
                    img_data = response.content
                    image = Image.open(BytesIO(img_data))
                    self.photo = ImageTk.PhotoImage(image)
                    self.imglable.config(image=self.photo)
                else:
                    raise
            else:
                raise 
        except:
            self.imglable.config(text="Notfound")


    def makeGuess(self):
        if self.HP>0 and self.ATTACK > 0 and self.DEFENCE>0 and self.SPEED>0:
            threading.Thread(target=self.parallelcall).start()
            self.mainFrame.destroy()
            self.mainFrame = self.mainFrame = tk.Frame(self.root,background="#f4f1de")
            self.mainFrame.pack(fill=tk.BOTH,expand=tk.TRUE,padx=10,pady=10)
            tk.Label(self.mainFrame,text = self.pokemon_got,font=("somefont",25,"bold"),background="#f4f1de").pack()
            tk.Frame(self.mainFrame, bg="black", height=2).pack(fill=tk.X)
            self.imglable = tk.Label(self.mainFrame,text="Loading ...")
            self.imglable.pack(pady=15,expand=tk.TRUE,fill=tk.BOTH)
            tk.Frame(self.mainFrame, bg="black", height=2).pack(fill=tk.X)
            tempframe = tk.Frame(self.mainFrame,background="#f4f1de")
            tk.Label(tempframe,text = "HP : " + str(self.HP),font=("somefont",12,"normal"),background="#f4f1de").pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
            tk.Label(tempframe,text ="ATTACK : " +str(self.ATTACK),font=("somefont",12,"normal"),background="#f4f1de").pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
            tk.Label(tempframe,text = "DEFENCE : " +str(self.DEFENCE),font=("somefont",12,"normal"),background="#f4f1de").pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
            tk.Label(tempframe,text = "SPEED : " +str(self.SPEED),font=("somefont",12,"normal"),background="#f4f1de").pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
            tempframe.pack(expand=True,fill=tk.BOTH)
            self.start_btn.config(text="Restart",command=self.resetForNew)
        else:
            messagebox.showerror("Invaild values","Click the buttons to set the random value!")

    def resetForNew(self):
        self.mainFrame.destroy()
        self.start_btn.destroy()
        self.Gui()

    def TrainModel(self):
        #import Dataset
        dataset = pd.read_csv('Pokemon.csv')
        X = dataset.iloc[:, 2:].values
        y = dataset.iloc[:, 0].values
        
        #Scale Date
        
        sc = StandardScaler()
        X = sc.fit_transform(X)
        self.sc = sc

        #Train model
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        classifier.fit(X, y)
        self.classifier = classifier


if __name__=="__main__":
    root = tk.Tk()
    root.title("Pokemon finder")
    root.geometry("1000x450")
    app = App(root)
    app.Gui()
    root.mainloop()