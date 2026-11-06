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