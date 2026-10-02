from tkinter import *
from tkinter import messagebox,Canvas,ttk
from models.dionica import Dionica
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import unicodedata
from PIL import Image, ImageTk
from matplotlib.widgets import RadioButtons, TextBox,Button
import csv
import numpy as np
import yfinance as yf
from sklearn.svm import SVR
from datetime import date, timedelta

euro = unicodedata.lookup("EURO SIGN")
connection = sqlite3.connect('dionice.db')
cursor=connection.cursor()

def create_diagonal_gradient(canvas,koji, width, height):
    if(koji==1):
        end_rgb = (4, 2, 13)
        start_rgb = (20, 0, 150)
    elif(koji==2):
        end_rgb = (4, 13, 2)
        start_rgb = (20, 150, 0)
    else:
        end_rgb = (13, 2, 4)
        start_rgb = (150, 0, 20)
    step = 2
    for i in range(0, width + height, step):
        ratio = i / (width + height)
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        canvas.create_line(i, 0, 0, i, fill=color, width=step)
        

def plotaj(ime):
    cursor.execute("SELECT POVIJEST_CIJENA.CIJENA FROM POVIJEST_CIJENA JOIN DIONICE ON POVIJEST_CIJENA.ID_DIONICE=DIONICE.ID_DIONICE WHERE DIONICE.IME_DIONICE = ?",(ime,))
    Povijest =[red[0] for red in cursor.fetchall()]
    x1=[]
    for i in range(0,len(Povijest)):
        x1.append(i)
    plt.plot(x1,Povijest, c = "green", label = ime)
    plt.xlabel("Vrijeme")
    plt.ylabel("Cijena dionice")
    plt.title(f"Cijena dionice {ime}")
    plt.show()
    


def build_canvas(main_window,canvas1, canvas2,canvas3,dionice_tab,investicije_tab,options_tab, hash_lozinka, id_korisnika,photos):
    create_diagonal_gradient(canvas1, 1, 1000, 750)
    create_diagonal_gradient(canvas2, 2, 1000, 750)
    create_diagonal_gradient(canvas3, 3, 1000, 750)
    cursor.execute("SELECT TICKER,IME_DIONICE,CIJENA FROM DIONICE")
    row1 = cursor.fetchall()
    cursor.execute("SELECT IME_KORISNIKA,PREZIME_KORISNIKA,CASH,IME_DIONICE,CIJENA,KOLIKO,PROSJECNA_CIJENA FROM KORISNICI JOIN INVESTICIJE ON KORISNICI.ID_KORISNIKA=INVESTICIJE.ID_KORISNIKA JOIN DIONICE ON INVESTICIJE.ID_DIONICE=DIONICE.ID_DIONICE  WHERE KORISNICI.ID_KORISNIKA=?",(id_korisnika,))
    row2 = cursor.fetchall()
    
    
    main_label1= Label(dionice_tab, text=f"Korisnik: {row2[0][0]}",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#2000f0",fg="#ffffff")
    main_label1.pack(expand=True,fill="both")
    main_label2= Label(investicije_tab, text=f"Korisnik: {row2[0][0]}",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#20b000",fg="#ffffff")
    main_label2.pack(expand=True,fill="both")
    main_label3= Label(investicije_tab, text=f"Cash: {row2[0][2]}",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#20b000",fg="#ffffff")
    main_label3.pack(expand=True,fill="both")
    main_label4= Label(options_tab, text=f"Korisnik: {row2[0][0]}",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#f02000",fg="#ffffff")
    main_label4.pack(expand=True,fill="both")
    main_label5= Label(options_tab, text=f"Cash: {row2[0][2]}",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#f02000",fg="#ffffff")
    main_label5.pack(expand=True,fill="both")
    
    canvas1.create_window(500,50,window=main_label1)
    canvas2.create_window(500,50,window=main_label2)
    canvas2.create_window(500,100,window=main_label3)
    canvas3.create_window(500,50,window=main_label4)
    canvas3.create_window(500,100,window=main_label5)
    
    y=150
    for dionica in row1:
        button_frame1 = Frame(main_window,bg="#2000f0",highlightbackground="white",highlightthickness=2,width=30,height=5)
        button_frame1.pack(padx=20,pady=10)
        button_frame1.bind("<Button-1>", lambda event, ime=dionica[1]: plotaj(ime))

        left_text= Label(button_frame1, height=5,text=f"{dionica[0]} {dionica[1]} ",font=('Times New Roman',15),bg="#2000f0",fg="#ffffff")
        left_text.pack(side="left",padx=10)
        left_text.bind("<Button-1>", lambda event, ime=dionica[1]: plotaj(ime))
        
        right_text= Label(button_frame1, height=5, text=f"{dionica[2]:.2f} {euro}",font=('Times New Roman',15),bg="#2000f0",fg="#ffffff")
        right_text.pack(side="right",padx=10)
        right_text.bind("<Button-1>", lambda event, ime=dionica[1]: plotaj(ime))

        canvas1.create_window(500,y,window=button_frame1)
        y+=150
    y=200
    
    for investicija in row2:
        button_frame2 = Frame(main_window,bg="#20b000",highlightbackground="white",highlightthickness=2,width=30,height=5)
        button_frame2.pack(padx=20,pady=10)
        button_frame2.bind("<Button-1>", lambda event, ime=dionica[1]: plotaj(ime))

        left_text= Label(button_frame2, height=5,text=f"{investicija[3]} {investicija[4]:.2f} {euro}",font=('Times New Roman',15),bg="#20b000",fg="#ffffff")
        left_text.pack(side="left",padx=10)
        left_text.bind("<Button-1>", lambda event, ime=dionica[1]: plotaj(ime))
        
        cursor.execute("SELECT CIJENA FROM (SELECT ID_PROMJENE,POVIJEST_CIJENA.CIJENA FROM POVIJEST_CIJENA JOIN DIONICE ON POVIJEST_CIJENA.ID_DIONICE=DIONICE.ID_DIONICE WHERE DIONICE.IME_DIONICE = ? ORDER BY ID_PROMJENE DESC LIMIT 10) AS LASTTEN ORDER BY ID_PROMJENE ASC",(investicija[3],))

        Povijest =[red[0] for red in cursor.fetchall()]

        x1=[]
        for i in range(0,len(Povijest)):
            x1.append(i)
        plt.figure(figsize=(1, 1), dpi=100,facecolor="white")
        plt.plot(x1,Povijest, c = "green")
        plt.axis('off')
        plt.savefig(f"{investicija[3]}.png",facecolor="white")
        plt.close()

        img = Image.open(f"{investicija[3]}.png").resize((80,80),Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        photos.append(photo)
        
        right_text= Label(button_frame2,image=photo, height=100, text=f"Ukupna vrijednost = {investicija[5]:.2f} x {investicija[4]:.2f} = {investicija[5]*investicija[4]:.2f} {euro}   ",font=('Times New Roman',15),compound="right",bg="#20b000",fg="#ffffff")
        right_text.pack(side="right",padx=10)
        right_text.bind("<Button-1>", lambda event, ime=investicija[3]: plotaj(ime))
        
        canvas2.create_window(500,y,window=button_frame2)
        y+=150

    #odkadentry=Entry(options_tab)
    #odkadentry.pack(expand=True,fill="both")
    #dokadentry=Entry(options_tab)
    #dokadentry.pack(expand=True,fill="both")

    #main_label6= Label(options_tab, text="Odkad",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#f02000",fg="#ffffff")
    #main_label6.pack(expand=True,fill="both")
    #main_label7= Label(options_tab, text="Dokad",font=('Times New Roman',20),highlightbackground="white",highlightthickness=2,bg="#f02000",fg="#ffffff")
    #main_label7.pack(expand=True,fill="both")

    #canvas3.create_window(400,150,window=main_label6)
    #canvas3.create_window(600,150,window=main_label7)
    #canvas3.create_window(400,200,window=odkadentry)
    #canvas3.create_window(600,200,window=dokadentry)

    

    svi_podaci=[]
    y=200
    for dionica in row1:
        dates=[]
        prices=[]
        ticker_symbol = dionica[0]
        start_date = "2026-01-01"
        end_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        df = yf.download(ticker_symbol, start=start_date, end=end_date)
        output_filename = f"{ticker_symbol}_historical_prices.csv"
        df.to_csv(output_filename)

        get_data(output_filename,dates,prices)
        podaci=[dionica[0],dates,prices]
        svi_podaci.append(podaci)
        
        button_frame3 = Frame(main_window,bg="#f02000",highlightbackground="white",highlightthickness=2,width=30,height=5)
        button_frame3.pack(padx=20,pady=10)
        button_frame3.bind("<Button-1>",lambda event, podaci=podaci: otvori_option(podaci))

        left_text= Label(button_frame3, height=5,text=f"{dionica[0]} {dionica[1]} ",font=('Times New Roman',15),bg="#f02000",fg="#ffffff")
        left_text.pack(side="left",padx=10)
        left_text.bind("<Button-1>", lambda event, podaci=podaci: otvori_option(podaci))

        right_text= Label(button_frame3, height=5, text=f"{prices[len(prices)-1]:.2f} {euro}",font=('Times New Roman',15),bg="#f02000",fg="#ffffff")
        right_text.pack(side="right",padx=10)
        right_text.bind("<Button-1>", lambda event, podaci=podaci: otvori_option(podaci))

        canvas3.create_window(500,y,window=button_frame3)

        y=y+150
        
def otvori_option(podaci):
    print("otvaram opciju")
    ticker=podaci[0]
    dates=podaci[1]
    prices=podaci[2]

    loading = Toplevel()
    loading.title("Please wait")
    loading.geometry("250x80")
    Label(loading, text="Calculating models...", font=("Arial", 11)).pack(expand=True)
    loading.update()
    
    predict_prices(ticker,dates,prices,len(dates))
    
    
def get_data(filename,dates,prices):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row[0][:4].isdigit():
                continue
            dates.append(len(dates))     
            prices.append(float(row[1]))
            
def predict_prices(ticker,dates, prices, x,loading=None):
    dates = np.reshape(dates, (len(dates), 1))

    svr_lin = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.001)

    svr_lin.fit(dates, prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)

    x_in = [[x]]
    pred_rbf = svr_rbf.predict(x_in)[0]
    pred_lin = svr_lin.predict(x_in)[0]
    pred_poly = svr_poly.predict(x_in)[0]
    latest_price = prices[-1]
    
    if loading is not None:
        loading.destroy()
        
    fig, ax = plt.subplots(figsize=(11, 5))
    fig.subplots_adjust(right=0.70)  

    ax.scatter(dates, prices, color='black', s=5, label='Data')  
    ax.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    ax.plot(dates, svr_lin.predict(dates), color='green', label='Linear model')
    ax.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')
    ax.set_xlabel('Trading day')
    ax.set_ylabel('Price')
    ax.set_title(f'{ticker} - Support Vector Regression')
    ax.legend(loc='upper left')
    
    x0=0.73
    
    fig.text(x0, 1, "Latest price:", fontsize=11, color='gray')
    fig.text(x0, 0.95, f"{latest_price:.2f}", fontsize=14, color='black', fontweight='bold')

    if(pred_rbf>latest_price):
        fig.text(x0, 0.8, f"RBF:  {pred_rbf:.2f}", fontsize=11, color='green')
    else:
        fig.text(x0, 0.8, f"RBF:  {pred_rbf:.2f}", fontsize=11, color='red')

    if(pred_lin>latest_price):
        fig.text(x0, 0.75, f"Linear:  {pred_lin:.2f}", fontsize=11, color='green')
    else:
        fig.text(x0, 0.75, f"Linear:  {pred_lin:.2f}", fontsize=11, color='red')

    if(pred_poly>latest_price):
        fig.text(x0, 0.7, f"Polynomial:  {pred_poly:.2f}", fontsize=11, color='green')
    else:
        fig.text(x0, 0.7, f"Polynomial:  {pred_poly:.2f}", fontsize=11, color='red')

    fig.text(x0,0.65, "Opcije" , fontsize=15, color='black')

    ax_box = fig.add_axes([x0+0.05, 0.55, 0.08, 0.06])
    predviđena_promjena = TextBox(ax_box, "Procjena: ", initial="0")

    
    t_result = fig.text(x0, 0.5, "", fontsize=11, color='black')
    t_profit = fig.text(x0, 0.45, "", fontsize=11, color='black')

    bx_box = fig.add_axes([x0+0.07, 0.35, 0.08, 0.06])
    kolicina = TextBox(bx_box, "Koliko opcija: ", initial="0")
    ukupna_zarada=fig.text(x0,0.30,"",fontsize=11,color='black')
    
    btn_box = fig.add_axes([x0, 0.2, 0.08, 0.06])
    btn = Button(btn_box, "Calculate")
    
    def update(_=None):
        try:
            change = float(predviđena_promjena.text.replace(',', '.'))
            koliko = float(kolicina.text.replace(',','.'))
        except ValueError:
            change = 0.0
            koliko = 0.0
        
        new_price = latest_price + change
        zarada=koliko*change
        t_result.set_text(f"{latest_price:.2f} {change:+.2f} = {new_price:.2f}")
        t_profit.set_text(f"Call: {change:+.2f}{euro}" if change >0 else f"Short: {change:-.2f}")
        ukupna_zarada.set_text(f"Zarada: {abs(change):.2f}{euro} * {koliko:.2f} = {abs(zarada):.2f}{euro}")
        

        fig.canvas.draw_idle()
    def postavi_opciju(event):
        try:
            change = float(predviđena_promjena.text.replace(',', '.'))
            koliko = float(kolicina.text.replace(',','.'))
        except ValueError:
            change = 0.0
            koliko = 0.0
        
        

    btn.on_clicked(postavi_opciju)
    predviđena_promjena.on_text_change(update)
    kolicina.on_text_change(update)
    update()

    
    plt.show()


"""
def simuliraj(main_window,canvas1, canvas2,canvas3,dionice_tab,investicije_tab,options_tab, hash_lozinka, id_korisnika,photos):

    cursor.execute("SELECT ID_DIONICE,IME_DIONICE,CIJENA FROM DIONICE")
    row = cursor.fetchall()

    lista_dionica=[]
    for dionica in row:
        lista_dionica.append(Dionica(dionica[0],dionica[1],dionica[2]))
    for dionica in lista_dionica:
        dionica.simuliraj("neutralan")
        cursor.execute("UPDATE DIONICE SET CIJENA=? WHERE ID_DIONICE=?",(dionica.cijena,dionica.id_dionice,))
        cursor.execute("INSERT INTO POVIJEST_CIJENA (ID_DIONICE, CIJENA) VALUES (?, ?)",(dionica.id_dionice,dionica.cijena,))
        connection.commit()

    for widget in canvas1.winfo_children():
        widget.destroy()
    canvas1.delete("all")

    for widget in canvas2.winfo_children():
        widget.destroy()
    canvas2.delete("all")

    photos.clear()
    
    build_canvas(main_window,canvas1, canvas2,canvas3,dionice_tab,investicije_tab,options_tab, hash_lozinka, id_korisnika,photos)
    main_window.after(6000,lambda: simuliraj(main_window,canvas1, canvas2,canvas3,dionice_tab,investicije_tab,options_tab, hash_lozinka, id_korisnika,photos))
"""
