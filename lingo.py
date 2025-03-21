import random
from colorama import Fore, Style, init
from lingowords import words  # Importeer de woordenlijst

# Initialiseer colorama
init(autoreset=True)

# Globale variabelen
game_running = True
ronde = 0
beurt = 1  # 1 voor Team 1, 2 voor Team 2

# Score bijhouden
team1_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}
team2_score = {"groene_ballen": 0, "rode_ballen": 0, "goed_geraden": 0, "fout_ballen": 0}

# Bingo-kaarten voor elk team
bingo_kaart_team1 = [[None for _ in range(4)] for _ in range(4)]
bingo_kaart_team2 = [[None for _ in range(4)] for _ in range(4)]

# Ballenbak
ballenbak = ["groen"] * 3 + ["rood"] * 3 + [str(i) for i in range(1, 21)]  # 3 groene, 3 rode, 20 nummers

print('Welkom bij Lingo')

team1 = input('Hallo Team 1, wat is jullie teamnaam? ').lower()
team2 = input('Hallo Team 2, wat is jullie teamnaam? ').lower()

def woord_splitter(woord):
    return list(woord)

def kleur_letters(geraden_woord, correct_woord):
    correct_woord_lijst = list(correct_woord)
    geraden_woord_lijst = list(geraden_woord)
    gekleurd_woord = []

    # Eerst markeer we de letters die op de juiste plaats staan (groen)
    for i in range(len(geraden_woord_lijst)):
        if geraden_woord_lijst[i] == correct_woord_lijst[i]:
            gekleurd_woord.append(Fore.GREEN + geraden_woord_lijst[i])
            correct_woord_lijst[i] = None  # Markeer deze letter als gebruikt
            geraden_woord_lijst[i] = None  # Markeer deze letter als gebruikt
        else:
            gekleurd_woord.append(Fore.RESET + geraden_woord_lijst[i])

    # Daarna markeren we letters die in het woord zitten maar op de verkeerde plaats (geel)
    for i in range(len(geraden_woord_lijst)):
        if geraden_woord_lijst[i] is not None and geraden_woord_lijst[i] in correct_woord_lijst:
            index_in_correct = correct_woord_lijst.index(geraden_woord_lijst[i])
            if correct_woord_lijst[index_in_correct] is not None:
                gekleurd_woord[i] = Fore.YELLOW + geraden_woord_lijst[i]
                correct_woord_lijst[index_in_correct] = None  # Markeer deze letter als gebruikt

    return ''.join(gekleurd_woord)

def grabbel_bal():
    if not ballenbak:  # Als de ballenbak leeg is, stop het spel
        print(Fore.RED + "De ballenbak is leeg! Het spel is afgelopen.")
        return None
    bal = random.choice(ballenbak)
    ballenbak.remove(bal)  # Verwijder de bal uit de ballenbak
    return bal

def update_bingo_kaart(team, bal):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    vrije_cellen = [(rij, kolom) for rij in range(4) for kolom in range(4) if kaart[rij][kolom] is None]
    if vrije_cellen:
        rij, kolom = random.choice(vrije_cellen)
        kaart[rij][kolom] = bal

def check_bingo(team):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    # Controleer rijen
    for rij in kaart:
        if all(cell is not None for cell in rij):
            return True
    # Controleer kolommen
    for kolom in range(4):
        if all(kaart[rij][kolom] is not None for rij in range(4)):
            return True
    # Controleer diagonalen
    if all(kaart[i][i] is not None for i in range(4)) or all(kaart[i][3 - i] is not None for i in range(4)):
        return True
    return False

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

def check_verlies_voorwaarden(team, score):
    if score["rode_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 rode ballen getrokken en verliest het spel!")
        return True
    if score["fout_ballen"] >= 3:
        print(Fore.RED + f"{team} heeft 3 woorden op rij fout geraden en verliest het spel!")
        return True
    return False

def toon_bingo_kaart(team):
    kaart = bingo_kaart_team1 if team == team1 else bingo_kaart_team2
    print(f"\nBingo-kaart voor {team}:")
    for rij in kaart:
        print(" | ".join(cell if cell is not None else " " for cell in rij))

while game_running:
    ronde += 1
    woord = random.choice(words)  # Kies een willekeurig woord uit de lijst
    split_word = woord_splitter(woord)
    print(f'\nRonde {ronde}')
    print(f'DEBUG: Het woord is "{woord}".')  # Debug-print om het woord te tonen
    print(f'De eerste letter is: {Fore.GREEN + split_word[0] + Fore.RESET} _ _ _ _')

    huidig_team = team1 if beurt == 1 else team2
    huidig_score = team1_score if beurt == 1 else team2_score

    for poging in range(5):
        while True:
            print(f'\nPoging {poging + 1} voor {huidig_team}:')
            raden = input('Raad het woord: ').lower()
            if len(raden) == 5:  # Controleer of het woord precies 5 letters lang is
                break
            print(Fore.RED + "Het woord moet precies 5 letters lang zijn. Probeer opnieuw.")

        if raden == woord:
            print(Fore.GREEN + 'Gefeliciteerd! Je hebt het woord geraden!')
            huidig_score["goed_geraden"] += 1
            huidig_score["fout_ballen"] = 0  # Reset fout geraden teller

            # Grabbel 2 ballen
            for _ in range(2):
                bal = grabbel_bal()
                if bal is None:  # Als de ballenbak leeg is, stop het spel
                    game_running = False
                    break
                if bal == "groen":
                    huidig_score["groene_ballen"] += 1
                    print(Fore.GREEN + f"{huidig_team} heeft een {bal} bal getrokken.")
                elif bal == "rood":
                    huidig_score["rode_ballen"] += 1
                    print(Fore.RED + f"{huidig_team} heeft een {bal} bal getrokken.")
                else:
                    update_bingo_kaart(huidig_team, bal)
                    print(f"{huidig_team} heeft een {bal} bal getrokken.")

            # Toon bingo-kaart
            toon_bingo_kaart(huidig_team)

            # Controleer win- en verliesvoorwaarden
            if check_win_voorwaarden(huidig_team, huidig_score) or check_verlies_voorwaarden(huidig_team, huidig_score):
                game_running = False
                break

            beurt = 2 if beurt == 1 else 1  # Wissel van beurt
            break
        else:
            print(kleur_letters(raden, woord))
    else:
        print(Fore.RED + 'Helaas, je hebt het woord niet geraden.')
        huidig_score["fout_ballen"] += 1
        if check_verlies_voorwaarden(huidig_team, huidig_score):
            game_running = False
        beurt = 2 if beurt == 1 else 1  # Wissel van beurt

print('Bedankt voor het spelen!')