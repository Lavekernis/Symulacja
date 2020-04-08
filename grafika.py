import  matplotlib
matplotlib.use('Qt5Agg')

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from symulacja import Populacja

pop = Populacja(40)

fig, ax = plt.subplots()

wykresy = {'zdrowy' : plt.plot([],[],'go')[0],
            'chory' : plt.plot([],[],'ro')[0],
            'nosiciel' : plt.plot([],[],'yo')[0],
            'martwy' : plt.plot([],[],'ko')[0],
            'odporny' : plt.plot([],[],'mo')[0]}

fig2, ax2 = plt.subplots()

statystyki = {'zdrowy' : plt.plot([],[],'g')[0],
                'chory' : plt.plot([],[],'r')[0],
                'nosiciel' : plt.plot([],[],'y')[0],
                'martwy' : plt.plot([],[],'k')[0],
                'odporny' : plt.plot([],[],'m')[0]}

ilosc = {'zdrowy' : [],
         'chory' : [],
         'nosiciel' : [],
         'martwy' : [],
         'odporny' : []}

fig3, ax3 = plt.subplots()

kolowy = {'zdrowy' : 0,
          'chory' : 0,
          'nosiciel':0,
          'martwy':0,
          'odporny':0}

kolory = {'zdrowy' : 'g',
          'chory' : 'r',
          'nosiciel' : 'y',
          'martwy' : 'k',
          'odporny' : 'm'}

def init():
    ax.set_xlim(0, pop.szerokosc)
    ax.set_ylim(0, pop.wysokosc)
    return wykresy.values()

def init2():
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0, 30)
    return statystyki.values()


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

def update3(frame):
    ax3.clear()
    ax3.axis('equal')
    for status,wykres in statystyki.items():
        i = 0
        for p in pop._pacjenci:
            if p.status == status:
                 i = i + 1
        kolowy[str(status)] = i
    ax3.pie(kolowy.values(), labels = kolowy.keys(), colors = kolory.values())
    return kolowy.values()


ani = FuncAnimation(fig, update, frames = None,
                     init_func=init, blit = True)
ani2 = FuncAnimation(fig2, update2, frames = None,
                     init_func=init2, blit = True)
ani3 = FuncAnimation(fig3, update3, frames = None,
                     blit = False)

plt.show(block = True)
