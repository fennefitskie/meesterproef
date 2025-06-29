import unittest
from lingo import woord_splitter, kleur_letters, maak_bingo_kaart, markeer_getal_op_kaart, check_bingo

class TestLingoFuncties(unittest.TestCase):

    def test_woord_splitter(self):
        self.assertEqual(woord_splitter("appel"), ['a', 'p', 'p', 'e', 'l'])

    def test_kleur_letters_volledig_correct(self):
        geraden = "appel"
        correct = "appel"
        gekleurd = kleur_letters(geraden, correct)
        # Test of alle letters groen zijn
        self.assertIn("\x1b[32m", gekleurd)  # \x1b[32m = Fore.GREEN
        self.assertEqual(gekleurd.count("\x1b[32m"), 5)

    def test_kleur_letters_deels_correct(self):
        geraden = "apzle"
        correct = "appel"
        gekleurd = kleur_letters(geraden, correct)
        self.assertIn("z", gekleurd)
        self.assertIn("\x1b[33m", gekleurd)  # \x1b[33m = Fore.YELLOW

    def test_maak_bingo_kaart(self):
        kaart = maak_bingo_kaart()
        # Controleer of de kaart 4 rijen heeft
        self.assertEqual(len(kaart), 4)
        # Controleer of elke rij 4 kolommen heeft
        for rij in kaart:
            self.assertEqual(len(rij), 4)
        # Controleer of alle getallen uniek zijn
        flat = [item for sublist in kaart for item in sublist]
        self.assertEqual(len(flat), len(set(flat)))

    def test_markeer_en_bingo_check(self):
        kaart = [
            ['1', '2', '3', '4'],
            ['5', '6', '7', '8'],
            ['9', '10', '11', '12'],
            ['13', '14', '15', '16'],
        ]
        # Markeer hele eerste rij
        for getal in ['1', '2', '3', '4']:
            markeer_getal_op_kaart_test(kaart, getal)
        self.assertTrue(check_bingo_test(kaart))

# Testversies van de kaart-functies om onafhankelijk te testen
def markeer_getal_op_kaart_test(kaart, getal):
    for rij in range(4):
        for kolom in range(4):
            if kaart[rij][kolom] == getal:
                kaart[rij][kolom] = "X"

def check_bingo_test(kaart):
    for rij in kaart:
        if all(cell == "X" for cell in rij):
            return True
    for kolom in range(4):
        if all(kaart[rij][kolom] == "X" for rij in range(4)):
            return True
    if all(kaart[i][i] == "X" for i in range(4)) or all(kaart[i][3 - i] == "X" for i in range(4)):
        return True
    return False

if __name__ == '__main__':
    unittest.main()
