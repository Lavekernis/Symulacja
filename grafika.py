import  matplotlib
matplotlib.use('Qt5Agg')

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from symulacja import Populacja

pop = Populacja(30)

fig, ax = plt.subplots()

wykresy = {'zdrowy'   : plt.plot([],[],'go')[0],
            'chory'   : plt.plot([],[],'ro')[0],
            'nosiciel': plt.plot([],[],'yo')[0]}

fig2, ax2 = plt.subplots()

statystyki = {'zdrowy' :plt.plot([],[],'g')[0],
                'chory':plt.plot([],[],'r')[0],
                'nosiciel':plt.plot([],[],'y')[0]}

ilosc = {'zdrowy' :[0],
         'chory':[0],
         'nosiciel':[0]}


def init2():
    ax2.set_xlim(0, 200)
    ax2.set_ylim(0, 30)
    return statystyki.values()

def init():
    ax.set_xlim(0, pop.szerokosc)
    ax.set_ylim(0, pop.wysokosc)
    return wykresy.values()

def update(frame):
    pop.ruch()
    for status,wykres in wykresy.items():
        xdata = [p.x for p in pop._pacjenci if p.status == status]
        ydata = [p.y for p in pop._pacjenci if p.status == status]
        wykres.set_data(xdata,ydata)
    return wykresy.values()

def update2(frame):
    for status,wykres in statystyki.items():
        i = 0
        for p in pop._pacjenci:
            if p.status == status:
                 i = i + 1   
        ilosc[str(status)].append(i)
        wykres.set_data(range(len(ilosc[status])),ilosc[status])
    return statystyki.values()   
       

ani = FuncAnimation(fig, update, frames=None,
                     init_func=init, blit=True)
ani2 = FuncAnimation(fig2, update2, frames=None,
                     init_func=init2, blit=True)
plt.show(block=True)
