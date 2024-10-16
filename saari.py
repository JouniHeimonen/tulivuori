import tkinter as tk
import random
import winsound
import time
import threading

#luodaan ikkuna
ikkuna = tk.Tk()
ikkuna.title("Tulivuori")
ikkuna.geometry("600x400")
canvas = tk.Canvas(ikkuna, width=600, height=400)
canvas.pack()
canvas.create_rectangle(0, 0, 600, 400, fill="blue")

#alustetaan kohdat saarille
osiot = [1,50,100,150,200,250,300,350,400,450]

#alustuksia
apinax = 0
apinay = 0
value = 1
stop = threading.Event()
y = 0
x = 0
aika = True
saari_id = {
     'saari id':0
}

saari_location =[]

apina_id = {
     'apina id':0
}
apina_location =[]

#nauruun ja hai syömisen todennäiköisyys
kuoleman_todennakoisyys = 0.01

#luodaan saari
def saari (random_location):
    
    global y
    global x
    global aika
    global apina_count
    apina_count = 0
    aika = True
    for _ in range(1):
        x = random_location
        saari = canvas.create_rectangle(130,130,90,90,fill="brown",tags="saari")
        saari_id["saari id"] += 1
        saari_location =(saari,x,y,saari_id)
        winsound.Beep(100,500) 
        canvas.move(saari,x,y)
        osiot.remove(x)
        apina(x,y,saari_location,apina_count,saari_id)
        y += 60
    return saari_id,saari_location,y,x

def saari2(random_location):
    
    global y
    global x
    global aika
    aika = True
    y = 100
    x = random_location
    saari = canvas.create_rectangle(130,130,90,90,fill="brown",tags="saari")
    winsound.Beep(100,500) 
    canvas.move(saari,x,y)
    osiot.remove(x)


#piirtää apinat saarille
def apina(x,y,saari_location,apina_count,saari_id):
    global apinax
    global apinay
    apinax = x
    apinay = y
    apinax += 90
    apinay += 90
    print(saari_id)
    for _ in range(10):
        apina = canvas.create_oval(4, 4, 8, 8, fill="orange",tags="apina"+str((apina_id["apina id"])))
        apina_id["apina id"] +=1
        apina_count += 1
        apina_location =(apina,apinax,apinay,apina_id,saari_location)
        time.sleep(1)
        canvas.move(apina,apinax,apinay)
        apinax += 3
        apinay += 3
        ääni = random.randint(400,2000)
        
        print(ääni)
        if apina_count == 10:
            apinat_elossa(apina_count,ääni)    
         
    return apina_count,apina_id,apina_location,apinay,apinax,ääni

#alustetaan liikkuminen  
def apina_liikkuu():
    global apinax
    global apinay
    global value
    global apina_count
    value -= 1
    
    if value == 0:
                value = 1
                liikkuu(apinax,apinay,apina_count)                                                
    else:
        pass
        

#liikuttaa apinaa ja tarkistaa jos hai syö apinan                   
def  liikkuu(apinax,apinay,apina_count):
        for _ in range(100): 
            if y >= ikkuna.winfo_height():
                winsound.Beep(1200,1000)
                break    
            if random.random() < kuoleman_todennakoisyys:
                    print("apina tuli syödyksi.")
                    winsound.Beep(1000,100)
                    canvas.delete("apina"+str(apina_count))
                    break
            else:    
                canvas.delete("apina"+str(apina_count))
                apina = canvas.create_oval(4, 4, 8, 8, fill="orange",tags="apina"+str(apina_count))
                canvas.move(apina,apinax,apinay)
                ikkuna.update()
                ikkuna.after(100)
                apinay += 10
           
       
#elossa olevat apinat päästävät ääntä ja jos ne kuolee nauruun niin pääse myös ääni
def apinat_elossa(apina_count,ääni): 
    while aika:
        if random.random() < kuoleman_todennakoisyys:
                    apina_count -= 1
                    print("apina kuoli nauruun.")
                    winsound.Beep(900,600)
                    canvas.delete("apina"+str(apina_count))                       
        if apina_count > 0:
                print( apina_count," apina elossa")
                winsound.Beep(ääni,300)
                time.sleep(10)
        else: 
            print("saarella ei ole apinoita")
            ääni = random.randint(400,2000)
            break

#aloitetaan threadi saarelle apinoiden kanssa                          
def apina_thread():
        p = threading.Thread(target=monta)
        p.start()

#aloitetaan threadi saarelle
def tulivuori():
        p = threading.Thread(target=yksi)
        p.start() 


#luodaan yksi saari apinoilla
def monta(): 
        random_location= random.choice(osiot)
        saari(random_location)
        time.sleep(1) 
        
#luodaan yksi saari 
def yksi(): 
        random_location= random.choice(osiot)
        saari2(random_location)        
        
#tuhoaa kaikki saaret ja apinat
def tuhoa():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 600, 400, fill="blue")
    global aika
    aika = False
    stop.set()
    if stop.is_set():
         stop.clear()
    osiot[:] = (1,50,100,150,200,250,300,350,400,450)
       

#tuhoaa saaret ja apinat ja aloittaa saarien teon uudestaan
def tuhoa_ja_aloit_alusta():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 600, 400, fill="blue")
    global aika
    aika = False
    osiot[:] = (1,50,100,150,200,250,300,350,400,450)
    stop.set()
    if stop.is_set():
         stop.clear()
    for _ in range(1):
        apina_thread()     


#painikkeet  
btn1 = tk.Button(ikkuna, text="tulivuori", command=tulivuori)
btn1.place(x=70,y=10)

btn1 = tk.Button(ikkuna, text="saari", command=apina_thread)
btn1.place(x=160,y=50)

btn1 = tk.Button(ikkuna, text="tuhoa ja luo uudestaan", command=tuhoa_ja_aloit_alusta)
btn1.place(x=160,y=10)

btn1 = tk.Button(ikkuna, text="tuhoa", command=tuhoa)
btn1.place(x=10,y=10)

btn1 = tk.Button(ikkuna, text="liikuta apinaa", command=apina_liikkuu)
btn1.place(x=10,y=50)


ikkuna.mainloop()