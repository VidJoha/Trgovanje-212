import sqlite3
import bcrypt
connection = sqlite3.connect('dionice.db')

cursor=connection.cursor()

command1="""CREATE TABLE IF NOT EXISTS
DIONICE(
    ID_DIONICE INTEGER PRIMARY KEY,
    IME_DIONICE CHAR(25),
    TICKER CHAR(4),
    CIJENA REAL)"""

cursor.execute(command1)

command2="""CREATE TABLE IF NOT EXISTS
KORISNICI(
    ID_KORISNIKA INTEGER PRIMARY KEY,
    IME_KORISNIKA CHAR(25),
    PREZIME_KORISNIKA CHAR(25),
    PASSWORD_HASH BLOB,
    CASH REAL)"""

cursor.execute(command2)

command3="""CREATE TABLE IF NOT EXISTS
INVESTICIJE(
    ID_INVESTICIJE INTEGER PRIMARY KEY,
    ID_KORISNIKA INTEGER,
    ID_DIONICE INTEGER,
    KOLIKO REAL,
    PROSJECNA_CIJENA REAL,
    FOREIGN KEY(ID_KORISNIKA) REFERENCES KORISNICI(ID_KORISNIKA),
    FOREIGN KEY(ID_DIONICE) REFERENCES DIONICE(ID_DIONICE))"""

cursor.execute(command3)

command4="""CREATE TABLE IF NOT EXISTS
POVIJEST_CIJENA(
    ID_PROMJENE INTEGER PRIMARY KEY AUTOINCREMENT,
    DATUM_PROMJENE DATE,
    ID_DIONICE INTEGER,
    CIJENA REAL,
    FOREIGN KEY(ID_DIONICE) REFERENCES DIONICE(ID_DIONICE))"""

cursor.execute(command4)

cursor.execute("""INSERT INTO DIONICE VALUES (1,"Nvidia","NVDA",209)""")
cursor.execute("""INSERT INTO DIONICE VALUES (2,"Apple","AAPL",165)""")
cursor.execute("""INSERT INTO DIONICE VALUES (3,"Microsoft","MSFT",420)""")

lozinka1 = "ajmonakavicu"
lozinka_bytes1 = lozinka1.encode('utf-8')
hashed1 = bcrypt.hashpw(lozinka_bytes1,bcrypt.gensalt())

lozinka2 = "temperatura"
lozinka_bytes2 = lozinka2.encode('utf-8')
hashed2 = bcrypt.hashpw(lozinka_bytes2,bcrypt.gensalt())

lozinka3 = "pivaizkafica"
lozinka_bytes3 = lozinka3.encode('utf-8')
hashed3 = bcrypt.hashpw(lozinka_bytes3,bcrypt.gensalt())

cursor.execute("INSERT INTO KORISNICI VALUES (?,?,?,?,?)",(1,"Vid","Joha",hashed1,1000))
cursor.execute("INSERT INTO KORISNICI VALUES (?,?,?,?,?)",(2,"Luka","Čizmin",hashed2,4300))
cursor.execute("INSERT INTO KORISNICI VALUES (?,?,?,?,?)",(3,"Luka","Radenić",hashed3,12500))

cursor.execute("""INSERT INTO INVESTICIJE VALUES (1,1,1,2,200)""")
cursor.execute("""INSERT INTO INVESTICIJE VALUES (2,1,2,5,150)""")
cursor.execute("""INSERT INTO INVESTICIJE VALUES (3,1,3,1,400)""")
cursor.execute("""INSERT INTO INVESTICIJE VALUES (4,2,2,10,150)""")
cursor.execute("""INSERT INTO INVESTICIJE VALUES (5,2,3,2,400)""")
cursor.execute("""INSERT INTO INVESTICIJE VALUES (6,3,1,8,200)""")

cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (1,2026-01-05,1,200)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (2,2026-01-06,1,210)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (3,2026-01-07,1,215)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (4,2026-01-08,1,202)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (5,2026-01-09,1,209)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (6,2026-01-05,2,150)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (7,2026-01-06,2,160)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (8,2026-01-07,2,155)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (9,2026-01-08,2,158)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (10,2026-01-09,2,165)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (11,2026-01-05,3,400)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (12,2026-01-06,3,404)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (13,2026-01-07,3,440)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (14,2026-01-08,3,433)""")
cursor.execute("""INSERT INTO POVIJEST_CIJENA VALUES (15,2026-01-09,3,420)""")

cursor.execute("""SELECT KORISNICI.IME_KORISNIKA,KORISNICI.PREZIME_KORISNIKA,
DIONICE.IME_DIONICE,INVESTICIJE.KOLIKO,INVESTICIJE.PROSJECNA_CIJENA,
INVESTICIJE.KOLIKO*INVESTICIJE.PROSJECNA_CIJENA
FROM INVESTICIJE JOIN KORISNICI ON
INVESTICIJE.ID_KORISNIKA=KORISNICI.ID_KORISNIKA JOIN DIONICE ON
INVESTICIJE.ID_DIONICE=DIONICE.ID_DIONICE WHERE KORISNICI.IME_KORISNIKA="Luka" """)

results = cursor.fetchall()

for i in results:
    print(i)
connection.commit()
connection.close()
