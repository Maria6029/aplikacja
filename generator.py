import copy
import random
from typing import List, Tuple, Set, Optional

class Plansza:
    """Klasa reprezentująca planszę i logikę gry Sudoku."""

    def czy_rozwiazana(self) -> bool:
        """
        Sprawdza, czy plansza Sudoku jest rozwiązana.
        Zwraca True, jeśli nie ma pustych pól ani błędów.
        """
        for wiersz in range(9):
            for kolumna in range(9):
                if self.plansza[wiersz][kolumna] == 0:
                    return False

        if self.pobierz_bledy():
            return False

        return True

    def pobierz_bledy(self) -> Set[Tuple[int, int]]:
        """
        Sprawdza całą planszę i zwraca zbiór współrzędnych pól,
        w których wpisane liczby łamią zasady Sudoku.
        """
        bledy = set()

        for wiersz in range(9):
            for kolumna in range(9):
                liczba = self.plansza[wiersz][kolumna]
                if liczba == 0:
                    continue

                self.plansza[wiersz][kolumna] = 0
                if not self.sprawdz_pole(liczba, (wiersz, kolumna)):
                    bledy.add((wiersz, kolumna))
                self.plansza[wiersz][kolumna] = liczba

        return bledy

    def __init__(self, kod: Optional[str] = None) -> None:
        """Tworzy nowy obiekt planszy Sudoku."""
        self.__resetuj_plansze()
        self.kod = kod

        if kod:
            for wiersz in range(9):
                for kolumna in range(9):
                    self.plansza[wiersz][kolumna] = int(kod[0])
                    kod = kod[1:]

    def __resetuj_plansze(self) -> List[List[int]]:
        """Resetuje planszę, ustawiając wszystkie pola na 0."""
        self.plansza = [[0] * 9 for _ in range(9)]
        return self.plansza

    def plansza_na_kod(self, wejsciowa_plansza: Optional[List[List[int]]] = None) -> str:
        """Zamienia planszę Sudoku na jeden ciąg znaków."""
        plansza_do_zamiany = wejsciowa_plansza if wejsciowa_plansza else self.plansza
        self.kod = ''.join([str(liczba) for wiersz in plansza_do_zamiany for liczba in wiersz])
        return self.kod

    def znajdz_puste_pole(self) -> Optional[Tuple[int, int]]:
        """Szuka pierwszego pustego pola (0) na planszy."""
        for wiersz in range(9):
            for kolumna in range(9):
                if self.plansza[wiersz][kolumna] == 0:
                    return (wiersz, kolumna)
        return None

    def sprawdz_pole(self, liczba: int, pozycja: Tuple[int, int]) -> bool:
        """Sprawdza, czy daną liczbę można wpisać w wybrane pole."""
        wiersz, kolumna = pozycja

        if self.plansza[wiersz][kolumna] != 0:
            return False

        if liczba in self.plansza[wiersz]:
            return False

        for i in range(9):
            if self.plansza[i][kolumna] == liczba:
                return False

        start_wiersz = (wiersz // 3) * 3
        start_kolumna = (kolumna // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.plansza[start_wiersz + i][start_kolumna + j] == liczba:
                    return False

        return True

    def rozwiaz(self) -> bool:
        """Rozwiązuje planszę Sudoku metodą rekurencji i cofania (backtracking)."""
        dostepne_pola = self.znajdz_puste_pole()

        if not dostepne_pola:
            return True
        else:
            wiersz, kolumna = dostepne_pola

        for n in range(1, 10):
            if self.sprawdz_pole(n, (wiersz, kolumna)):
                self.plansza[wiersz][kolumna] = n
                if self.rozwiaz():
                    return True
                self.plansza[wiersz][kolumna] = 0

        return False

    def rozwiaz_na_kod(self) -> str:
        """Rozwiązuje planszę Sudoku i zwraca rozwiązanie jako kod."""
        self.rozwiaz()
        return self.plansza_na_kod()

    def __wypelnij_kwadrat(self, wiersz_start: int, kolumna_start: int) -> None:
        """Pomocnicza metoda (Faza 3) usuwająca duplikację kodu z generatora."""
        liczby = list(range(1, 10))
        random.shuffle(liczby)
        for wiersz in range(3):
            for kolumna in range(3):
                self.plansza[wiersz_start + wiersz][kolumna_start + kolumna] = liczby.pop()

    def __generuj_losowa_pelna_plansze(self) -> List[List[int]]:
        """Generuje całkowicie nową planszę losując główne przekątne."""
        self.__resetuj_plansze()
        # Wypełnianie po przekątnej (bezpieczne, niezależne kwadraty)
        self.__wypelnij_kwadrat(0, 0)
        self.__wypelnij_kwadrat(3, 3)
        self.__wypelnij_kwadrat(6, 6)
        
        self.__generuj_kontynuacje()
        return self.plansza

    def __generuj_kontynuacje(self) -> bool:
        """Dokończenie generowania pełnej planszy za pomocą rekurencji."""
        for wiersz in range(9):
            for kolumna in range(9):
                if self.plansza[wiersz][kolumna] == 0:
                    liczby = list(range(1, 10))
                    random.shuffle(liczby)
                    for liczba in liczby:
                        if self.sprawdz_pole(liczba, (wiersz, kolumna)):
                            self.plansza[wiersz][kolumna] = liczba
                            if self.rozwiaz():
                                self.__generuj_kontynuacje()
                                return True
                            self.plansza[wiersz][kolumna] = 0
                    return False
        return True

    def __szukaj_rozwiazan_rekurencja(self, rozwiazania: List[str]) -> None:
        """Rekurencyjne zliczanie ilości unikalnych rozwiązań."""
        if len(rozwiazania) > 1:
            return 

        pole = self.znajdz_puste_pole()
        if not pole:
            rozwiazania.append("znalazlem")
            return

        wiersz, kolumna = pole
        for n in range(1, 10):
            if self.sprawdz_pole(n, (wiersz, kolumna)):
                self.plansza[wiersz][kolumna] = n
                self.__szukaj_rozwiazan_rekurencja(rozwiazania)
                self.plansza[wiersz][kolumna] = 0

    def znajdz_liczbe_rozwiazan(self) -> List[str]:
        """Zwraca listę reprezentującą znalezione rozwiązania."""
        rozwiazania = []
        self.__szukaj_rozwiazan_rekurencja(rozwiazania)
        return rozwiazania

    def generuj_plansze_gry(self, pelna_plansza: List[List[int]], trudnosc: int) -> Tuple[List[List[int]], List[List[int]]]:
        """Tworzy zagrażalną planszę na podstawie pełnej, usuwając odpowiednią ilość pól."""
        self.plansza = copy.deepcopy(pelna_plansza)

        if trudnosc == 0:
            pola_do_usuniecia = 36
        elif trudnosc == 1:
            pola_do_usuniecia = 46
        else:
            pola_do_usuniecia = 52

        usuwanie_bezpieczne = min(12, pola_do_usuniecia)
        licznik = 0
        while licznik < usuwanie_bezpieczne:
            wiersz = random.randint(0, 8)
            kolumna = random.randint(0, 8)
            if self.plansza[wiersz][kolumna] != 0:
                self.plansza[wiersz][kolumna] = 0
                licznik += 1

        pola_do_usuniecia -= usuwanie_bezpieczne
        licznik = 0
        while licznik < pola_do_usuniecia:
            wiersz = random.randint(0, 8)
            kolumna = random.randint(0, 8)

            if self.plansza[wiersz][kolumna] != 0:
                n = self.plansza[wiersz][kolumna]
                self.plansza[wiersz][kolumna] = 0

                if len(self.znajdz_liczbe_rozwiazan()) != 1:
                    self.plansza[wiersz][kolumna] = n
                    continue

                licznik += 1

        return self.plansza, pelna_plansza

    def generuj_kod_planszy_gry(self, trudnosc: int) -> Tuple[str, str]:
        """Generuje nową planszę Sudoku do gry oraz jej ukryte rozwiązanie w formacie kodu."""
        self.plansza, rozwiazana_plansza = self.generuj_plansze_gry(self.__generuj_losowa_pelna_plansze(), trudnosc)
        return self.plansza_na_kod(), self.plansza_na_kod(rozwiazana_plansza)

    def wypisz_plansze(self) -> None:
        """Wypisuje aktualną planszę Sudoku w konsoli (do debugowania)."""
        for i in range(9):
            print(" ".join(str(self.plansza[i][j]) for j in range(9)))









