"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Alex Mičáň
email: mican.alex@gmail.com
"""
import re

TEXTS = [
    '''Situated about 10 miles west of Kemmerer,
    Fossil Butte is a ruggedly impressive
    topographic feature that rises sharply
    some 1000 feet above Twin Creek Valley
    to an elevation of more than 7500 feet
    above sea level. The butte is located just
    north of US 30 and the Union Pacific Railroad,
    which traverse the valley.''',
    '''At the base of Fossil Butte are the bright
    red, purple, yellow and gray beds of the Wasatch
    Formation. Eroded portions of these horizontal
    beds slope gradually upward from the valley floor
    and steepen abruptly. Overlying them and extending
    to the top of the butte are the much steeper
    buff-to-white beds of the Green River Formation,
    which are about 300 feet thick.''',
    '''The monument contains 8198 acres and protects
    a portion of the largest deposit of freshwater fish
    fossils in the world. The richest fossil fish deposits
    are found in multiple limestone layers, which lie some
    100 feet below the top of the butte. The fossils
    represent several varieties of perch, as well as
    other freshwater genera and herring similar to those
    in modern oceans. Other fish such as paddlefish,
    garpike and stingray are also present.'''
]

# Registrovaní uživatelé podle tabulky
registrovani_uzivatele = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

# Přihlášení uživatele
uzivatel = input("Zadej uživatelské jméno: ")
heslo = input("Zadej heslo: ")

vyber = input(f"Zadajte číslo textu na analýzu (1 až {len(TEXTS)}): ")

# Ověření přihlášení
if uzivatel in registrovani_uzivatele and registrovani_uzivatele[uzivatel] == heslo:
    print(f"Vítej, {uzivatel}!\n")
    print("Máme 3 texty k analýze. Vyber číslo textu (1, 2 nebo 3):")
    
    # Ověření vstupu – číslo
    if not vyber.isdigit():
        print("⚠️ Zadal jsi něco jiného než číslo. Program končí.")
    else:
        cislo = int(vyber)
        if 1 <= cislo <= len(TEXTS):
            vybrany_text = TEXTS[cislo - 1]
            print("\nVybraný text:")
            print(vybrany_text)
        else:
            print("Text s tímto číslem není k dispozici. Program končí.")
else:
    print("Neplatné jméno nebo heslo. Přístup odepřen.")

if not vyber.isdigit() or not (1 <= int(vyber) <= len(TEXTS)):
    print("Neplatný výber, ukončujem program.")
    exit()

text = TEXTS[int(vyber)-1]

# Analýza vybraného textu
slova = re.findall(r'\b\w+\b', text)

pocet_slov = len(slova)
pocet_velkych_pismen = sum(1 for slovo in slova if slovo[0].isupper())
pocet_velkymi_pismenami = sum(1 for slovo in slova if slovo.isupper())
pocet_malymi_pismenami = sum(1 for slovo in slova if slovo.islower())
pocet_cisel = len([slovo for slovo in slova if slovo.isdigit()])
suma_cisel = sum(int(slovo) for slovo in slova if slovo.isdigit())

# Zobrazení výsledků analýzy
print("-" * 40)
print(f"Celkový počet slov: {pocet_slov}")
print(f"Počet slov začínajúcich veľkým písmenom: {pocet_velkych_pismen}")
print(f"Počet slov písaných VELKÝMI PÍSMENAMI: {pocet_velkymi_pismenami}")
print(f"Počet slov písaných malými písmenami: {pocet_malymi_pismenami}")
print(f"Počet čísel: {pocet_cisel}")
print(f"Suma všetkých čísel: {suma_cisel}")
print("-" * 40)

# Vygenerovaní jednoduchého sloupcového grafu délek slov
print("\nStĺpcový graf výskytu rôznych dĺžok slov:")
slovnik_dlzok = {}
for slovo in slova:
    dlzka = len(slovo)
    slovnik_dlzok[dlzka] = slovnik_dlzok.get(dlzka, 0) + 1

for dlzka in sorted(slovnik_dlzok):
    pocet = slovnik_dlzok[dlzka]
    print(f"{dlzka:2} | {'*' * pocet} ({pocet})")
