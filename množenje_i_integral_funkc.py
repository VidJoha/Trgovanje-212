import numpy as np
import math
from scipy.stats import norm
from scipy.integrate import quad
import matplotlib.pyplot as plt

mu=float(input("upisi trenutnu cijenu: "))
opc=float(input("upisi cijenu opcije: "))
sigma = math.sqrt(mu)
m1, c1 = 0, -opc             
m2, c2 = 1, -mu-opc

def product(x,a,b):
    return norm.pdf(x, mu, sigma) * (a * x + b)

# (-infinity, 0]
r1, err1 = quad(product, -np.inf, mu+opc,args=(m1,c1))

# [0, infinity)
r2, err2 = quad(product, mu+opc, np.inf,args=(m2,c2))

x0 = np.linspace((-3*sigma+mu), (3*sigma+mu), 100)
y0 = 0*x0

x1 = np.linspace((-3*sigma+mu), mu, 100)
x2 = np.linspace(mu, (3*sigma+mu), 100)
y_norm = norm.pdf(x0, loc=mu, scale=sigma)
y1 = norm.pdf(x1, loc=mu, scale=sigma)
y2 = norm.pdf(x2, loc=mu, scale=sigma)
y3 = (m1*x1+c1)/(3*sigma)
y4 = (m2*x2+c2)/(3*sigma)
funkc_opcija1= y1*y3
funkc_opcija2= y2*y4

def updateaj_podatke(y3,y4,x1,x2,funkc_opcija1,funkc_opcija2):
    y3 = (m1*x1+c1)/(3*sigma)
    y4 = (m2*x2+c2)/(3*sigma)
    funkc_opcija1= y1*y3
    funkc_opcija2= y2*y4
    return y3,y4,funkc_opcija1,funkc_opcija2

updateaj_podatke(y3,y4,x1,x2,funkc_opcija1,funkc_opcija2)
fig, (plt1, plt2) = plt.subplots(1, 2, figsize=(10, 4))
def plotaj(plt1,x0,y0,y_norm,x1,x2,funkc_opcija1,funkc_opcija2):
    #Ravna crta i Gaussova krivulja
    plt1.plot(x0,y0)
    plt1.plot(x0, y_norm) 
    #Integrali opcija
    plt1.plot(x1, funkc_opcija1)
    plt1.plot(x2, funkc_opcija2)
    return plt1

print(round(r1,2),round( r2,2))
plotaj(plt1,x0,y0,y_norm,x1,x2,funkc_opcija1,funkc_opcija2)

while(abs(r2+r1)>0.1):
    if(abs(r1)<abs(r2)):
        opc=opc+abs((r1+r2))/2
    else:
        opc=opc-abs((r1+r2))/2
    m1, c1 = 0, -opc             
    m2, c2 = 1, -mu-opc
    r1, err1 = quad(product, -np.inf, mu+opc,args=(m1,c1))
    r2, err2 = quad(product, mu+opc, np.inf,args=(m2,c2))
    print("Za cijenu opcije:",round(opc,2),", integrali opcija su: ",round(r1,2)," i ",round(r2,2),"")

print("Zadnja cijena opcije ",opc)

y3,y4,funkc_opcija1,funkc_opcija2=updateaj_podatke(y3,y4,x1,x2,funkc_opcija1,funkc_opcija2)
plotaj(plt2,x0,y0,y_norm,x1,x2,funkc_opcija1,funkc_opcija2)
plt.show(block=False)
while plt.get_fignums():
    plt.pause(1)

