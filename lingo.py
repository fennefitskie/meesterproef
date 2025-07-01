# Importeer benodigde modules
import random
from colorama import Fore, Style, init
from lingowords import words  # Zelfgemaakte woordenlijst uit apart bestand

# Initialiseer colorama zodat kleuren automatisch resetten
init(autoreset=True)

# Functie die een woord splitst in losse letters
def woord_splitter(woord):
    return list(woord)

# Kleurt de letters van het geraden woord: groen = juiste plaats, geel = verkeerde plaats, geen kleur = fout
def kleur_letters(geraden_woord, correct_woord):
    correct_woord_lijst = list(correct_woord)
    geraden_woord_lijst = list(geraden_woord)
    gekleurd_woord = []

    # Eerste lus: controleer op correcte letters op de juiste plek (groen)
    for i in range(len(geraden_woord_lijst)):
        if geraden_woord_lijst[i] == correct_woord_lijst[i]:
            gekleurd_woord.append(Fore.GREEN + geraden_woord_lijst[i])
            correct_woord_lijst[i] = None
            geraden_woord_lijst[i] = None
        else:
            gekleurd_woord.append(Fore.RESET + geraden_woord_lijst[i])

    # Tweede lus: controleer op correcte letters op de verkeerde plek (geel)
    for i in range(len(geraden_woord_lijst)):
        if geraden_woord_lijst[i] is not None and geraden_woord_lijst[i] in correct_woord_lijst:
            index_in_correct = correct_woord_lijst.index(geraden_woord_lijst[i])
            if correct_woord_lijst[index_in_correct] is not None:
                gekleurd_woord[i] = Fore.YELLOW + geraden_woord_lijst[i]
                correct_woord_lijst[index_in_correct] = None

    return ''.join(gekleurd_woord)

# Trek een bal uit de ballenbak
def grabbel_bal():
    if not ballenbak:
        print(Fore.RED + "De ballenbak is leeg! Het spel is afgelopen.")
        return None
    bal = random.choice(ballenbak)
    ballenbak.remove(bal)
    return bal

# Genereer een bingo-kaart met 16 unieke getallen van 1 t/m 20
def maak_bingo_kaart():
    nummers = random.sample(range(1, 21), 16)
    kaart = []
    for i in range(4):
        rij = [str(nummers[i * 4 + j]) for j in range(4)]
        kaart.append(rij)
    return kaart

# Toon de bingo-kaart van een team
def toon_bingo_kaart(team):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    print(f"\nBingo-kaart voor {team}:")
    for rij in kaart:
        print(" | ".join(f"{cell:>2}" for cell in rij))

# Markeer een getrokken nummer als "X" op de juiste kaart
def markeer_getal_op_kaart(team, getal):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    getal_str = str(getal)
    for rij in range(4):
        for kolom in range(4):
            if kaart[rij][kolom] == getal_str:
                kaart[rij][kolom] = "X"

# Check of een team bingo heeft behaald (rij, kolom of diagonaal)
def check_bingo(team):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    # Check rijen
    for rij in kaart:
        if all(cell == "X" for cell in rij):
            return True
    # Check kolommen
    for kolom in range(4):
        if all(kaart[rij][kolom] == "X" for rij in range(4)):
            return True
    # Check diagonalen
    if all(kaart[i][i] == "X" for i in range(4)) or all(kaart[i][3 - i] == "X" for i in range(4)):
        return True
    return False

# Check of een team gewonnen heeft volgens één van de spelregels
def check_win_voorwaarden(team, score):
    if score["groene_ballen"] >= 3:
        print(Fore.GREEN + f"{team} heeft 3 groene ballen getrokken en wint het spel!")
        return True
    if check_bingo(team):
        print(Fore.GREEN + f"{team} heeft een lijn op de bingo-kaart en wint het spel!")
        return True
    if score["goed_geraden"] >= 10:
        print(Fore.GREEN + f"{team} heeft 10 woorden goed geraden en wint het spel!")
        return True
    return False

# Check of een team verloren heeft volgens één van de spelregels
def check_verlies_voorwaarden(team, score):
    if score["rode_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 rode ballen getrokken en verliest het spel!")
        return True
    if score["fout_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 woorden op rij fout geraden en verliest het spel!")
        return True
    return False

# Start het spel en regel de beurten, scores en het spelverloop
def start_spel():
    global team1, team2, ballenbak, bingo_kaart_team1, bingo_kaart_team2

    # Vraag teamnamen op
    team1 = input('Hallo Team 1, wat is jullie teamnaam? ').lower()
    team2 = input('Hallo Team 2, wat is jullie teamnaam? ').lower()

    # Scores bijhouden
    team1_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}
    team2_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}

    # Ballenbak vullen
    ballenbak = ["groen"] * 3 + ["rood"] * 3 + [str(i) for i in range(1, 21)]

    # Bingo-kaarten maken
    bingo_kaart_team1 = maak_bingo_kaart()
    bingo_kaart_team2 = maak_bingo_kaart()

    ronde = 0
    beurt = 1
    game_running = True

    while game_running:
        if not ballenbak:
            print(Fore.RED + "De ballenbak is leeg! Het spel is afgelopen.")
            break

        ronde += 1
        woord = random.choice(words)
        split_word = woord_splitter(woord)
        print(f'\nRonde {ronde}')
        print(f'DEBUG: Het woord is "{woord}".')
        print(f'De eerste letter is: {Fore.GREEN + split_word[0] + Fore.RESET} _ _ _ _')

        huidig_team = team1 if beurt == 1 else team2
        huidig_score = team1_score if beurt == 1 else team2_score

        # 5 pogingen om het woord te raden
        for poging in range(5):
            while True:
                print(f'\nPoging {poging + 1} voor {huidig_team}:')
                raden = input('Raad het woord: ').lower()
                if len(raden) == 5:
                    break
                print(Fore.RED + "Het woord moet precies 5 letters lang zijn. Probeer opnieuw.")

            if raden == woord:
                print(Fore.GREEN + 'Gefeliciteerd! Je hebt het woord geraden!')
                huidig_score["goed_geraden"] += 1
                huidig_score["fout_ballen"] = 0

                # Trek de eerste bal
                bal1 = grabbel_bal()
                if not bal1:
                    game_running = False
                    break

                if bal1 == "groen":
                    huidig_score["groene_ballen"] += 1
                    print(Fore.GREEN + f"{huidig_team} heeft een groene bal getrokken.")
                elif bal1 == "rood":
                    huidig_score["rode_ballen"] += 1
                    print(Fore.RED + f"{huidig_team} heeft een rode bal getrokken.")
                else:
                    print(f"{huidig_team} heeft een {bal1} bal getrokken.")
                    markeer_getal_op_kaart(huidig_team, bal1)

                # Trek een tweede bal als de eerste geen rode was
                if bal1 != "rood" and ballenbak:
                    bal2 = grabbel_bal()
                    if not bal2:
                        game_running = False
                        break
                    if bal2 == "groen":
                        huidig_score["groene_ballen"] += 1
                        print(Fore.GREEN + f"{huidig_team} heeft een groene bal getrokken.")
                    elif bal2 == "rood":
                        huidig_score["rode_ballen"] += 1
                        print(Fore.RED + f"{huidig_team} heeft een rode bal getrokken.")
                    else:
                        print(f"{huidig_team} heeft een {bal2} bal getrokken.")
                        markeer_getal_op_kaart(huidig_team, bal2)

                # Toon de bijgewerkte bingo-kaart
                toon_bingo_kaart(huidig_team)

                # Check of iemand gewonnen/verloren heeft
                if check_win_voorwaarden(huidig_team, huidig_score) or check_verlies_voorwaarden(huidig_team, huidig_score):
                    game_running = False
                else:
                    beurt = 2 if beurt == 1 else 1
                break
            else:
                # Toon het woord met kleuren per letter
                print(kleur_letters(raden, woord))
        else:
            # Als na 5 pogingen het woord niet is geraden
            print(Fore.RED + 'Helaas, je hebt het woord niet geraden.')
            huidig_score["fout_ballen"] += 1
            if check_verlies_voorwaarden(huidig_team, huidig_score):
                game_running = False
            beurt = 2 if beurt == 1 else 1

    # Vraag of het spel opnieuw gestart moet worden
    while True:
        opnieuw = input("Wil je opnieuw spelen? (ja/nee): ").lower()
        if opnieuw == "ja":
            start_spel()
            break
        elif opnieuw == "nee":
            print("Tot de volgende keer!")
            break
        else:
            print("Ongeldige invoer. Typ 'ja' of 'nee'.")

# Start het spel
print('Welkom bij Lingo')
start_spel()
