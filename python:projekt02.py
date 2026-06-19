"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Alex Mičáň
email: mican.alex@gmail.com
"""

import random
import time

def generuj_cislo():
    cislice = list(range(10))
    random.shuffle(cislice)
    return ''.join(map(str, cislice[:4]))

def vyhodnot_hadanie(hadanie, tajne_cislo):
    bulls = sum(a == b for a, b in zip(hadanie, tajne_cislo))
    cows = len(set(hadanie) & set(tajne_cislo)) - bulls
    return bulls, cows

def uloz_statistiku(pokusy,cas_hry):
    with open("statistiky.txt", "a") as f:
        f.write(f"Pokusy: {pokusy}, Čas: {cas_hry:.2f} sekúnd\n")

print("Vitajte v hre Bulls & Cows!")
tajne_cislo = generuj_cislo()
pokusy = 0

while True:
    hadanie = input("Zadaj štvormiestne číslo s rôznymi číslicami: ")

    if not hadanie.isdigit() or len(hadanie) != 4 or len(set(hadanie)) != 4:
        print("Nesprávny vstup, skúste znova!")
        continue

    pokusy += 1
    bulls, cows = vyhodnot_hadanie(hadanie, tajne_cislo)

    if bulls == 4:
        print(f"Gratulujem! Uhádol si číslo {tajne_cislo} v {pokusy} pokusoch.")
        break

    print(f"Bulls: {bulls}, Cows: {cows}")
