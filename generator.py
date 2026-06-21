import copy
import random

class Plansza:
    def czy_rozwiazana(self):
        """Sprawdza, czy plansza Sudoku jest rozwiązana.
        Zwraca True, jeśli nie ma pustych pól ani błędów.
        """
        # brak pustych pól
        for wiersz in range(9):
            for kolumna in range(9):
                if self.plansza[wiersz][kolumna] == 0:
                    return False

        # brak błędów
        if len(self.pobierz_bledy()) > 0:
            return False

        return True

    def pobierz_bledy(self):
        """Sprawdza całą planszę i zwraca zbiór pól,
        w których wpisane liczby są niezgodne z zasadami Sudoku.
        """
        bledy = set()

        for wiersz in range(9):
            for kolumna in range(9):
                liczba = self.plansza[wiersz][kolumna]

                if liczba == 0:
                    continue

                # tymczasowo usuwamy liczbę
                self.plansza[wiersz][kolumna] = 0

                if not self.sprawdz_pole(liczba, (wiersz, kolumna)):
                    bledy.add((wiersz, kolumna))

                # przywracamy
                self.plansza[wiersz][kolumna] = liczba

        return bledy

    def __init__(self, kod=None):
        """Tworzy nowy obiekt planszy Sudoku.
        Jeśli podano kod planszy, wczytuje go do tablicy 9x9.
        """
        self.__resetuj_plansze()

        if kod:
            self.kod = kod

            for wiersz in range(9):
                for kolumna in range(9):
                    self.plansza[wiersz][kolumna] = int(kod[0])
                    kod = kod[1:]
        else:
            self.kod = None

    def __resetuj_plansze(self):
        """Resetuje planszę Sudoku, ustawiając wszystkie pola na 0.
        Zero oznacza puste pole."""
        self.plansza = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
        ]
        return self.plansza

    def plansza_na_kod(self, wejsciowa_plansza=None): 
        """Zamienia planszę Sudoku na jeden ciąg znaków.
        Jeśli podano planszę jako argument, zamienia ją na kod.
        W przeciwnym razie zamienia aktualną planszę.
        """
        if wejsciowa_plansza:
            _kod = ''.join([str(i) for j in wejsciowa_plansza for i in j])
            return _kod
        else:
            self.kod = ''.join([str(i) for j in self.plansza for i in j])
            return self.kod

    def znajdz_puste_pole(self): 
        """Szuka pierwszego pustego pola na planszy.
        Puste pole jest oznaczone liczbą 0.
        """
        for wiersz in range(len(self.plansza)):
            for kolumna in range(len(self.plansza[0])):
                if self.plansza[wiersz][kolumna] == 0:
                    return (wiersz, kolumna)

        return False

    def sprawdz_pole(self, liczba, pozycja): 
        """Sprawdza, czy daną liczbę można wpisać w wybrane pole.
        Kontroluje wiersz, kolumnę oraz kwadrat 3x3.
        """
        if not self.plansza[pozycja[0]][pozycja[1]] == 0:  
            return False

        for kolumna in self.plansza[pozycja[0]]:  
            if kolumna == liczba:
                return False

        for wiersz in range(len(self.plansza)):  
            if self.plansza[wiersz][pozycja[1]] == liczba:
                return False

        wewnetrzny_kwadrat_wiersz = pozycja[0] // 3
        wewnetrzny_kwadrat_kolumna = pozycja[1] // 3

        for i in range(3):  
            for j in range(3):
                if self.plansza[i + (wewnetrzny_kwadrat_wiersz * 3)][j + (wewnetrzny_kwadrat_kolumna * 3)] == liczba:
                    return False

        return True

    def rozwiaz(self): 
        """
        Rozwiązuje planszę Sudoku metodą rekurencji i cofania.
        Zwraca rozwiązaną planszę albo False, jeśli nie da się jej rozwiązać.
        """
        dostepne_pola = self.znajdz_puste_pole()

        if not dostepne_pola:
            return True
        else:
            wiersz, kolumna = dostepne_pola

        for n in range(1, 10):
            if self.sprawdz_pole(n, (wiersz, kolumna)):
                self.plansza[wiersz][kolumna] = n

                if self.rozwiaz():
                    return self.plansza

                self.plansza[wiersz][kolumna] = 0

        return False

    def rozwiaz_na_kod(self): 
        """Rozwiązuje planszę Sudoku i zwraca rozwiązanie jako ciąg znaków.
        """
        return self.plansza_na_kod(self.rozwiaz())

    def __generuj_losowa_pelna_plansze(self):  
        """Generuje nową, kompletną i poprawnie uzupełnioną planszę Sudoku.
        Najpierw losowo wypełnia trzy kwadraty 3x3, a potem uzupełnia resztę.
        """
        self.__resetuj_plansze()

        _l = list(range(1, 10))
        for wiersz in range(3):
            for kolumna in range(3):
                _liczba = random.choice(_l)
                self.plansza[wiersz][kolumna] = _liczba
                _l.remove(_liczba)

        _l = list(range(1, 10))
        for wiersz in range(3, 6):
            for kolumna in range(3, 6):
                _liczba = random.choice(_l)
                self.plansza[wiersz][kolumna] = _liczba
                _l.remove(_liczba)

        _l = list(range(1, 10))
        for wiersz in range(6, 9):
            for kolumna in range(6, 9):
                _liczba = random.choice(_l)
                self.plansza[wiersz][kolumna] = _liczba
                _l.remove(_liczba)

        return self.__generuj_kontynuacje()

    def __generuj_kontynuacje(self): 
        """Kontynuuje generowanie pełnej planszy Sudoku.
        Uzupełnia puste pola losowymi liczbami zgodnymi z zasadami gry.
        """
        for wiersz in range(len(self.plansza)):
            for kolumna in range(len(self.plansza[wiersz])):
                if self.plansza[wiersz][kolumna] == 0:
                    _liczba = random.randint(1, 9)

                    if self.sprawdz_pole(_liczba, (wiersz, kolumna)):
                        self.plansza[wiersz][kolumna] = _liczba

                        if self.rozwiaz():
                            self.__generuj_kontynuacje()
                            return self.plansza

                        self.plansza[wiersz][kolumna] = 0

        return False


    def __szukaj_rozwiazan_rekurencja(self, rozwiazania):
        """Pomocnicza funkcja rekurencyjna do zliczania rozwiązań."""
        # Przerywamy natychmiast, gdy znajdziemy drugie rozwiązanie
        if len(rozwiazania) > 1:
            return 

        pole = self.znajdz_puste_pole()
        if not pole:
            rozwiazania.append("znalazlem") # Dodajemy cokolwiek do listy, by zliczyć rozwiązanie
            return

        wiersz, kolumna = pole
        for n in range(1, 10):
            if self.sprawdz_pole(n, (wiersz, kolumna)):
                self.plansza[wiersz][kolumna] = n
                self.__szukaj_rozwiazan_rekurencja(rozwiazania)
                self.plansza[wiersz][kolumna] = 0 # Cofamy krok po powrocie

    def znajdz_liczbe_rozwiazan(self): 
        """Szuka możliwych rozwiązań aktualnej planszy.
        """
        rozwiazania = []
        self.__szukaj_rozwiazan_rekurencja(rozwiazania)
        return rozwiazania


    def generuj_plansze_gry(self, pelna_plansza, trudnosc): 
        """Tworzy planszę do gry na podstawie pełnej rozwiązanej planszy.
        Usuwa określoną liczbę pól w zależności od poziomu trudności.
        """ 
        self.plansza = copy.deepcopy(pelna_plansza)

        if trudnosc == 0:
            _pola_do_usuniecia = 36
        elif trudnosc == 1:
            _pola_do_usuniecia = 46
        elif trudnosc == 2:
            _pola_do_usuniecia = 52
        else:
            return

        _licznik = 0
        while _licznik < 4:
            _losowy_wiersz = random.randint(0, 2)
            _losowa_kolumna = random.randint(0, 2)
            if self.plansza[_losowy_wiersz][_losowa_kolumna] != 0:
                self.plansza[_losowy_wiersz][_losowa_kolumna] = 0
                _licznik += 1

        _licznik = 0
        while _licznik < 4:
            _losowy_wiersz = random.randint(3, 5)
            _losowa_kolumna = random.randint(3, 5)
            if self.plansza[_losowy_wiersz][_losowa_kolumna] != 0:
                self.plansza[_losowy_wiersz][_losowa_kolumna] = 0
                _licznik += 1

        _licznik = 0
        while _licznik < 4:
            _losowy_wiersz = random.randint(6, 8)
            _losowa_kolumna = random.randint(6, 8)
            if self.plansza[_losowy_wiersz][_losowa_kolumna] != 0:
                self.plansza[_losowy_wiersz][_losowa_kolumna] = 0
                _licznik += 1

        _pola_do_usuniecia -= 12
        _licznik = 0
        while _licznik < _pola_do_usuniecia:
            _wiersz = random.randint(0, 8)
            _kolumna = random.randint(0, 8)

            if self.plansza[_wiersz][_kolumna] != 0:
                n = self.plansza[_wiersz][_kolumna]
                self.plansza[_wiersz][_kolumna] = 0

                if len(self.znajdz_liczbe_rozwiazan()) != 1:
                    self.plansza[_wiersz][_kolumna] = n
                    continue

                _licznik += 1

        return self.plansza, pelna_plansza

    def generuj_kod_planszy_gry(self, trudnosc): 
        """Generuje nową planszę Sudoku do gry oraz jej rozwiązanie.
        Zwraca oba elementy jako kody tekstowe.
        """
        self.plansza, _rozwiazana_plansza = self.generuj_plansze_gry(self.__generuj_losowa_pelna_plansze(), trudnosc)
        return self.plansza_na_kod(), self.plansza_na_kod(_rozwiazana_plansza)

    def wypisz_plansze(self):
        """Wypisuje aktualną planszę Sudoku w konsoli.
        Każdy wiersz planszy jest drukowany osobno.
        """
        for i in range(9):
            wiersz = ""
            for j in range(9):
                wartosc = self.plansza[i][j]
                wiersz += str(wartosc) + " "
            print(wiersz)

if __name__ == "__main__":
    plansza_obiekt = Plansza()

    kody_planszy_gry = plansza_obiekt.generuj_kod_planszy_gry(0)

    print("KOD (ciąg znaków):")
    print(kody_planszy_gry[0])

    print("\nPLANSZA (2D):")
    plansza_obiekt.wypisz_plansze()
    zablokowane_komorki = set()

    for wiersz in range(9):
        for kolumna in range(9):
            if plansza_obiekt.plansza[wiersz][kolumna] != 0:
                zablokowane_komorki.add((wiersz, kolumna))









