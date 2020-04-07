# -*- coding: utf-8 -*-
"""Program do symulacji rozprzestrzeniania choroby w populacji

Kod do wykorzystania na zajęciach 01.04.2020
"""
import math
import random

def d(p1,p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


class Pacjent:
    """Pojedyncza osoba w symulacji.

    Atrybuty:
        x (float): współrzędna x pozycji Pacjenta
        y (float): współrzędna y pozycji Pacjenta
        status (str): status ze zbioru 'zdrowy', 'chory', 'nosiciel','martwy', 'odporny'

    """

    def __init__(self, x=0, y=0, czy_zdrowy=True):
        self._lifetime = 100
        self._x = x
        self._y = y
        if czy_zdrowy:
            self._status = 'zdrowy'
        else:
            self._status = 'chory'

    def ruch(self):
        """Wykonaj ruch zmieniając współrzędne x,y.

        Zdrowy pacjent przesuwa się o 0-1, a chory o 0-0.1"""
        if self._status == 'chory':
            zasieg = 5
            self._lifetime = self._lifetime - 1
            if self._lifetime < 1:
                self._status = random.choices(['martwy','odporny'],[50,50])[0]
        else:
            if self._status == 'martwy':
                zasieg = 0
            else:
                zasieg = 1
        self._x = self._x + random.uniform(-zasieg, zasieg)
        self._y = self._y + random.uniform(-zasieg, zasieg)

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

        for i in range(n):
            x = random.uniform(0, szerokosc)
            y = random.uniform(0, wysokosc)
            zdrowy = random.choices( [True, False], [80, 20] )[0]
            self._pacjenci.append( Pacjent(x, y, zdrowy) )
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
                        break
