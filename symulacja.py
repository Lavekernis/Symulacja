# -*- coding: utf-8 -*-
"""Program do symulacji rozprzestrzeniania choroby w populacji

Kod do wykorzystania na zajęciach 01.04.2020
"""
import math
import random

def d(p1,p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def dv_rand(v_max):
    
    dvx = random.uniform(-v_max, v_max)
    dvy_max =  math.sqrt(v_max**2 - dvx**2)
    dvy = random.uniform(-dvy_max, dvy_max)
    
    dv = (dvx, dvy)
    return dv
    
def newv_rand(vx, vy, v_max, dv_max_percentage):
    
    dv_max = dv_max_percentage * v_max
    while True:
        dvx = random.uniform(-dv_max, dv_max)
        dvy = random.uniform(-dv_max, dv_max)
        if ((vx + dvx)**2 + (vy + dvy)**2 <= v_max):
            break
    
    new_v = (vx + dvx, vy + dvy)
    return new_v

class Pacjent:
    """Pojedyncza osoba w symulacji.

    Atrybuty:
        x (float): współrzędna x pozycji Pacjenta
        y (float): współrzędna y pozycji Pacjenta
        status (str): status ze zbioru 'zdrowy', 'chory', 'nosiciel','martwy', 'odporny'

    """

    def __init__(self, x=0, y=0, vx=0, vy=0, czy_zdrowy=True):
        self._lifetime = 100
        self._x = x
        self._y = y
        self._vx = vx
        self.vy = vy
        if czy_zdrowy:
            self._status = 'zdrowy'
        else:
            self._status = 'chory'

    def ruch(self):
        """Wykonaj ruch zmieniając współrzędne x,y.

        Zdrowy pacjent przesuwa się o 0-1, a chory o 0-0.1"""
        if self._status == 'chory':
            vmax = 0.5
            self._lifetime = self._lifetime - 1
            if self._lifetime < 1:
                self._status = random.choices(['martwy','odporny'],[50,50])[0]
        else:
            if self._status == 'martwy':
                vmax = 0
                self._vx = 0
                self._vy = 0
            else:
                vmax = 1
        # fascynujące, że jak się poniżej zmieni ostatni argument
        # z 0.5 na 0.4, 0.3, 0.25, to grafika.py przestaje działać - zawiesza się
        if (vmax != 0):
            newv = newv_rand(self._vx, self._vy, vmax, 0.5)
            self._vx = newv[0]
            self._vy = newv[1]
            
        self._x = self._x + self._vx
        self._y = self._y + self._vy

    def __str__(self):
        return "Pacjent " + self._status + " @ "  + str(self._x) + " x " + str(self._y)

    @property
    def lifetime(self):
        return self._lifetime

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,x):
        self._x=x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self,y):
        self._y=y
        
    @property
    def vx(self):
        return self._vx

    @vx.setter
    def vx(self,vx):
        self._vx=vx

    @property
    def vy(self):
        return self._vy

    @vy.setter
    def vy(self,vy):
        self._vy=vy

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,status):
        if status == 'zdrowy' or status == 'chory' or status == 'nosiciel' or status == 'martwy' or status == 'odporny':
            self._status = status
        else:
            print("Nieprawidłowy status")

class Populacja:
    """Zbiór Pacjentów w ograniczonym obszarze przestrzeni

    Atrybuty:
        szerokosc (float): szerokosć dostępnego obszaru
        wysokosc (float): wysokosć dostępnego obszaru

    """

    def __init__(self, n, wysokosc=100, szerokosc=100):
        """Tworzy populację n Pacjentów na danym obszarze.

        Argumenty:
            n (int): liczba pacjentów
            wysokosc (float, optional): wysokosć planszy
            szerokosc (float, optional): szerokosć planszy
        """
        self._pacjenci = []
        self._wysokosc = wysokosc
        self._szerokosc = szerokosc
        self.faza = 0
        self._zarazenia = []

        for i in range(n):
            x = random.uniform(0, szerokosc)
            y = random.uniform(0, wysokosc)
            
            v = newv_rand(0, 0, 1, 1)
            vx = v[0]
            vy = v[1]
            
            zdrowy = random.choices( [True, False], [80, 20] )[0]
            self._pacjenci.append( Pacjent(x, y, vx, vy, zdrowy) )
    @property
    def wysokosc(self):
        return self._wysokosc

    @wysokosc.setter
    def wysokosc(self,wysokosc):
        self._wysokosc = wysokosc
        for i in self._pacjenci:
            if i.y > wysokosc:
                i.y = wysokosc

    @property
    def szerokosc(self):
        return self._szerokosc

    @szerokosc.setter
    def szerokosc(self,szerokosc):
        self._szerokosc = szerokosc
        for i in self._pacjenci:
            if i.x > szerokosc:
                i.x = szerokosc

    def __str__(self):
        s = ""
        for p in self._pacjenci:
            s += str(p) + "\n"
        return s

    def ruch(self):
        """ Wykonaj ruch przesuwając każdego z pacjentów"""
        for p in self._pacjenci:
            p.ruch()
            self.faza = self.faza + 1
            p.x = p.x % self._szerokosc
            p.y = p.y % self._wysokosc
            if p.status == 'zdrowy':
                for x in self._pacjenci:
                    if x.status != 'zdrowy' and d(p,x) < 5:
                        p.status = random.choices(['nosiciel','chory'],[50,50])[0]
                        self._zarazenia.append([p.x, p.y, self.faza, 0])
                        break

    def historia_zarazen(self):
        """ Zwraca listę zarażeń, której każdy element to lista trzech elementów:
            współrzędnej x zarażenia, 
            współrzędnej y zarażenia, 
            liczby ruchów, które minęły od zarażenia do wywołania historia_zarażeń
        """
        faza = self.faza
        for z in self._zarazenia:
            z[3] = faza - z[2]
            
        return self._zarazenia
    
    def print_hist_zar(self):
        for x in range(len(self._zarazenia)): 
            for y in range(4):
                print(self._zarazenia[x][y])