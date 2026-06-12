import sys
import timeit
from generator import Board 
from Ranking_czasów import RankingManager, RankingOkno

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QGroupBox, QRadioButton, QPushButton, QStackedWidget, QSizePolicy, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QIntValidator

def rgb(r, g, b):
    """
    Funkcja pomocnicza do łatwiejszego formatowania kolorów w stylu CSS.
    Zwraca string w formacie 'rgb(r, g, b)'.
    """
    return f"rgb({r}, {g}, {b})"

# KOMÓRKA PLANSZY
class SudokuCell(QLineEdit):
    """
    Klasa reprezentująca pojedynczą komórkę (kratkę) na planszy Sudoku.
    Dziedziczy po QLineEdit, co pozwala na interakcję z klawiaturą,
    ale jej domyślne zachowanie zostało nadpisane na potrzeby gry.
    """
    fokus_otrzymany = pyqtSignal(int, int)

    def __init__(self, row, col, glowne_okno, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.glowne_okno = glowne_okno 
        
        # Zmienne przechowujące stan danej komórki
        self.wartosc = ""
        self.notatki = set()
        self.wygenerowane = False
        self.odgadnieta = False
        
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setMinimumSize(180, 180)
        self.setMaximumSize(200, 200) 

        # Blokada standardowego wpisywania (obsługujemy to ręcznie)
        self.setReadOnly(True)
        self.setCursor(Qt.ArrowCursor)

    def focusInEvent(self, event):
        """Wykrywa kliknięcie w komórkę i wysyła sygnał do podświetlenia odpowiednich obszarów."""
        super().focusInEvent(event)
        self.fokus_otrzymany.emit(self.row, self.col)

    def keyPressEvent(self, event):
        """
        Główna funkcja obsługująca klawiaturę.
        Odpowiada za:
        1. Nawigację strzałkami oraz klawiszami W, S, A, D.
        2. Wpisywanie cyfr (jako główne odpowiedzi lub notatki).
        3. Weryfikację poprawności wpisanej cyfry i odejmowanie żyć.
        4. Usuwanie cyfr (Backspace/Delete).
        """
        klawisz_qt = event.key()

        # nawigacja strzałkami i wsad
        if klawisz_qt in (Qt.Key_W, Qt.Key_Up):
            nowy_wiersz = max(0, self.row - 1)
            self.glowne_okno.komorki[nowy_wiersz][self.col].setFocus()
            return
        elif klawisz_qt in (Qt.Key_S, Qt.Key_Down):
            nowy_wiersz = min(8, self.row + 1)
            self.glowne_okno.komorki[nowy_wiersz][self.col].setFocus()
            return
        elif klawisz_qt in (Qt.Key_A, Qt.Key_Left):
            nowa_kolumna = max(0, self.col - 1)
            self.glowne_okno.komorki[self.row][nowa_kolumna].setFocus()
            return
        elif klawisz_qt in (Qt.Key_D, Qt.Key_Right):
            nowa_kolumna = min(8, self.col + 1)
            self.glowne_okno.komorki[self.row][nowa_kolumna].setFocus()
            return

        # Blokada edycji dla cyfr startowych, prawidłowo odgadniętych i po zakończeniu gry
        if self.wygenerowane or self.odgadnieta or getattr(self.glowne_okno, 'gra_zakonczona', False):
            return 

        klawisz_tekst = event.text()
        if klawisz_tekst in "123456789":
            # Obsługa trybu notatek
            if self.glowne_okno.checkbox_notatki.isChecked():
                if klawisz_tekst in self.notatki:
                    self.notatki.remove(klawisz_tekst) 
                else:
                    self.notatki.add(klawisz_tekst)
                self.wartosc = "" 
            # Normalne wpisywanie cyfry
            else:
                self.wartosc = klawisz_tekst
                self.glowne_okno.plansza.board[self.row][self.col] = int(klawisz_tekst)
                
                # Weryfikacja poprawności wpisanej cyfry z ukrytym rozwiązaniem
                indeks = self.row * 9 + self.col
                poprawna = self.glowne_okno.rozwiazanie[indeks] 
                
                if klawisz_tekst == poprawna:
                    self.odgadnieta = True # Cyfra prawidłowa -> blokada edycji
                    self.notatki.clear()
                else:
                    # Wykryto błąd na planszy
                    bledy = self.glowne_okno.plansza.getErrors()
                    if (self.row, self.col) in bledy:
                        zyje = self.glowne_okno.odejmij_zycie()
                        if not zyje:
                            return 
        
        # Usuwanie zawartości komórki
        elif klawisz_qt in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Space):
            self.wartosc = ""
            self.glowne_okno.plansza.board[self.row][self.col] = 0
        else:
            super().keyPressEvent(event)
            return

        # Odświeżenie wyglądu po zmianach
        self.odswiez_tekst()
        self.glowne_okno.sprawdz_stan_gry()

    def ustaw_poczatkowa(self, val):
        """
        Inicjuje stan komórki na początku gry.
        Jeśli wartość nie jest zerem, oznacza ją jako "wygenerowaną" (zablokowaną).
        """
        if val != 0:
            self.wartosc = str(val)
            self.wygenerowane = True
        else:
            self.wartosc = ""
            self.wygenerowane = False
        
        self.odgadnieta = False
        self.notatki.clear()
        self.odswiez_tekst()

    def odswiez_tekst(self):
        """
        Aktualizuje tekst i wyrównanie wewnątrz komórki.
        Rysuje główną cyfrę na środku lub małe notatki w prawym górnym rogu.
        """
        if self.wartosc:
            self.setText(self.wartosc)
            self.setAlignment(Qt.AlignCenter)
        elif self.notatki:
            tekst = " ".join(sorted(list(self.notatki)))
            self.setText(tekst)
            self.setAlignment(Qt.AlignRight | Qt.AlignTop)
        else:
            self.setText("")
            self.setAlignment(Qt.AlignCenter)


# GŁÓWNE OKNO
class GlowneOkno(QMainWindow):
    """
    Główna klasa aplikacji zarządzająca oknami (Menu i Gra),
    stoperem, systemem żyć oraz integracją logiki z widokiem (GUI).
    """
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 1100, 750)
        self.setWindowTitle("Sudoku")
        
        self.stos_ekranow = QStackedWidget()    # pozwala na przełączanie między ekranem Menu a ekranem Gry
        self.setCentralWidget(self.stos_ekranow)
        
        self.czas_startu = 0 
        self.zycia = 3
        self.gra_zakonczona = False
        
        self.initUI()      
        self.initGraUI()   
        
    def initUI(self):
        """Inicjuje wygląd ekranu Menu Głównego (Rejestracja i Poziom trudności)."""
        self.ekran_menu = QWidget()
        layout_strony = QVBoxLayout()
        layout_strony.setContentsMargins(50, 50, 50, 50)
        layout_strony.setSpacing(30)
        layout_strony.addStretch(1)

        napis_sudoku = QLabel("SUDOKU")
        napis_sudoku.setAlignment(Qt.AlignCenter)
        napis_sudoku.setStyleSheet(f"""
            font-family: 'Segoe UI', sans-serif;
            font-size: 95px;
            font-weight: 900;
            color: {rgb(30, 41, 59)};
            letter-spacing: 12px;
            margin-bottom: 25px;
        """)
        layout_strony.addWidget(napis_sudoku)

        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(50)
        menu_layout.addStretch(1)

        style_boxa = f"""
             QGroupBox {{
                font-family: 'Segoe UI';
                font-size: 24px;
                font-weight: bold;
                color: {rgb(51, 65, 85)};
                background-color: {rgb(248, 249, 250)};
                border: 1px solid {rgb(226, 232, 240)};
                border-radius: 15px;
                margin-top: 0px;
                padding: 30px; 
                padding-top: 35px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 15px;
            }}
        """

        kolumna1 = QVBoxLayout()
        grupa1 = QGroupBox("Rejestracja")
        grupa1.setStyleSheet(style_boxa)
        grupa1.setMinimumWidth(500)
        grupa1.setMaximumWidth(650)
        
        napis_nazwa_swoja = QLabel("Wpisz swoje imię:")
        napis_nazwa_swoja.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 18px; color: {rgb(100, 116, 139)}; font-weight: normal; background-color: transparent;")
        kolumna1.addWidget(napis_nazwa_swoja)

        self.lineedit_nazwa_swoja = QLineEdit()
        self.lineedit_nazwa_swoja.setPlaceholderText("Twoje imię")
        self.lineedit_nazwa_swoja.setStyleSheet(f"QLineEdit {{ padding: 18px; font-size: 20px; border: 1px solid {rgb(203, 213, 225)}; border-radius: 8px; background: {rgb(255, 255, 255)}; color: {rgb(0, 0, 0)}; }} QLineEdit::placeholder {{ color: {rgb(148, 163, 184)}; }}")
        kolumna1.addWidget(self.lineedit_nazwa_swoja)
        kolumna1.addStretch()
        grupa1.setLayout(kolumna1)
        menu_layout.addWidget(grupa1)

        kolumna2 = QVBoxLayout()
        grupa2 = QGroupBox("Poziom trudności")
        grupa2.setStyleSheet(style_boxa)
        grupa2.setMinimumWidth(500)
        grupa2.setMaximumWidth(650)

        self.radio_latwy = QRadioButton("Łatwy")
        self.radio_sredni = QRadioButton("Średni")
        self.radio_trudny = QRadioButton("Trudny")
        self.radio_sredni.setChecked(True)
        
        style_radio = f"QRadioButton {{ font-family: 'Segoe UI'; font-size: 20px; color: {rgb(40, 40, 40)}; padding: 18px; font-weight: normal; background-color: {rgb(255, 255, 255)}; border-radius: 10px; border: 1px solid {rgb(220, 220, 220)}; }} QRadioButton:hover {{ background-color: {rgb(245, 245, 245)}; }} QRadioButton::indicator {{ width: 22px; height: 22px; }}"
        for rb in [self.radio_latwy, self.radio_sredni, self.radio_trudny]:
            rb.setStyleSheet(style_radio)
            kolumna2.addWidget(rb)

        kolumna2.addStretch()
        grupa2.setLayout(kolumna2)
        menu_layout.addWidget(grupa2)
        menu_layout.addStretch(1)
        layout_strony.addLayout(menu_layout)

        layout_przycisku = QHBoxLayout()
        layout_przycisku.addStretch(1)
        
        self.przycisk_start = QPushButton("ROZPOCZNIJ GRĘ")
        self.przycisk_start.setFixedWidth(550)
        self.przycisk_start.setStyleSheet(f"QPushButton {{ background-color: {rgb(30, 41, 59)}; color: {rgb(255, 255, 255)}; font-size: 24px; font-weight: bold; padding: 20px; border-radius: 12px; margin-top: 25px; }} QPushButton:hover {{ background-color: {rgb(51, 65, 85)}; }}")
        
        self.przycisk_start.clicked.connect(self.uruchom_gre)
        
        layout_przycisku.addWidget(self.przycisk_start)
        layout_przycisku.addStretch(1)
        layout_strony.addLayout(layout_przycisku)
        layout_strony.addStretch(1)

        self.ekran_menu.setStyleSheet(f"background-color: {rgb(162, 171, 31)};")
        self.ekran_menu.setLayout(layout_strony)
        self.stos_ekranow.addWidget(self.ekran_menu)

    def initGraUI(self):
        """Inicjuje wygląd ekranu Gry (Plansza, stoper, przyciski boczne)."""
        self.ekran_gry = QWidget()
        self.ekran_gry.setStyleSheet(f"background-color: {rgb(162, 171, 31)};")
        
        layout_glowny_gry = QHBoxLayout()
        
        # PANEL BOCZNY
        lewy_panel = QVBoxLayout()
        przycisk_wroc = QPushButton("Wróć do Menu")
        przycisk_wroc.setStyleSheet(f"""
            QPushButton {{ background-color: {rgb(30, 41, 59)}; color: white; font-size: 18px; font-weight: bold; padding: 15px 25px; border-radius: 10px; }}
            QPushButton:hover {{ background-color: {rgb(51, 65, 85)}; }}
        """)
        przycisk_wroc.clicked.connect(lambda: self.stos_ekranow.setCurrentWidget(self.ekran_menu))
        lewy_panel.addWidget(przycisk_wroc)
        
        self.etykieta_zycia = QLabel()
        self.etykieta_zycia.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 32px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 20px;")
        lewy_panel.addWidget(self.etykieta_zycia)

        self.etykieta_czasu = QLabel("Czas: 00:00")
        self.etykieta_czasu.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 24px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 5px;")
        lewy_panel.addWidget(self.etykieta_czasu)
        
        # Narzędzie odmierzające czas (co 1 sekundę)
        self.stoper = QTimer(self)
        self.stoper.timeout.connect(self.aktualizuj_czas)

        self.checkbox_notatki = QCheckBox("Tryb Notatek")
        self.checkbox_notatki.setStyleSheet(f"""
            QCheckBox {{ font-family: 'Segoe UI'; font-size: 20px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 30px; }}
            QCheckBox::indicator {{ width: 25px; height: 25px; }}
        """)
        lewy_panel.addWidget(self.checkbox_notatki)
        
        self.przycisk_zakoncz = QPushButton("PODDAJĘ SIĘ\n(Zakończ)")
        self.przycisk_zakoncz.setStyleSheet(f"""
            QPushButton {{ background-color: rgb(220, 38, 38); color: white; font-size: 16px; font-weight: bold; padding: 15px; border-radius: 10px; margin-top: 30px; }}
            QPushButton:hover {{ background-color: rgb(185, 28, 28); }}
        """)
        self.przycisk_zakoncz.clicked.connect(lambda: self.zakoncz_gre(wygrana=False))
        lewy_panel.addWidget(self.przycisk_zakoncz)

        lewy_panel.addStretch() 
        layout_glowny_gry.addLayout(lewy_panel)

        # PLANSZA
        self.siatka_gry = QGridLayout()
        self.siatka_gry.setSpacing(0)
        self.komorki = [[None for _ in range(9)] for _ in range(9)]

        for wiersz in range(9):
            for kolumna in range(9):
                komorka = SudokuCell(wiersz, kolumna, self)
                komorka.fokus_otrzymany.connect(self.podswietl_obszary)
                self.komorki[wiersz][kolumna] = komorka
                self.siatka_gry.addWidget(komorka, wiersz, kolumna)
                self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")

        # Zapewnienie, że plansza zawsze będzie wyśrodkowana na ekranie
        srodek_pion = QVBoxLayout()
        srodek_pion.addStretch(1)
        
        srodek_poziom = QHBoxLayout()
        srodek_poziom.addStretch(1)
        srodek_poziom.addLayout(self.siatka_gry)
        srodek_poziom.addStretch(1)
        
        srodek_pion.addLayout(srodek_poziom)
        srodek_pion.addStretch(1)

        layout_glowny_gry.addLayout(srodek_pion, stretch=1)
        self.ekran_gry.setLayout(layout_glowny_gry)
        self.stos_ekranow.addWidget(self.ekran_gry)

    def uruchom_gre(self):
        """
        Przygotowuje program do nowej rozgrywki: generuje nową planszę,
        uruchamia czasomierz, resetuje życia i ukryte rozwiązanie.
        """
        self.czas_startu = timeit.default_timer()
        self.gra_zakonczona = False
        
        self.etykieta_czasu.setText("Czas: 00:00")
        self.stoper.start(1000) 

        self.zycia = 3
        self.zaktualizuj_widok_zyc()

        trudnosc = 1 
        if self.radio_latwy.isChecked(): trudnosc = 0
        elif self.radio_trudny.isChecked(): trudnosc = 2

        self.plansza = Board()
        kod_pytania, kod_rozwiazania = self.plansza.generateQuestionBoardCode(trudnosc)
        self.rozwiazanie = kod_rozwiazania

        for wiersz in range(9):
            for kolumna in range(9):
                wartosc = self.plansza.board[wiersz][kolumna]
                komorka = self.komorki[wiersz][kolumna]
                
                komorka.ustaw_poczatkowa(wartosc)
                self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")

        self.stos_ekranow.setCurrentWidget(self.ekran_gry)

    def aktualizuj_czas(self):
        """Aktualizuje stoper na ekranie w formacie MM:SS."""
        if self.gra_zakonczona:
            return
        sekundy_minely = int(timeit.default_timer() - self.czas_startu)
        minuty = sekundy_minely // 60
        sekundy = sekundy_minely % 60
        self.etykieta_czasu.setText(f"Czas: {minuty:02d}:{sekundy:02d}")

    def zaktualizuj_widok_zyc(self):
        """Generuje wizualizację żyć (czerwone/czarne serduszka) za pomocą kodu HTML."""
        czerwone = "<span style='color: #ef4444;'>♥</span>" * self.zycia
        czarne = "<span style='color: #64748b;'>♥</span>" * (3 - self.zycia)
        self.etykieta_zycia.setText(f"Życia: {czerwone}{czarne}")

    def odejmij_zycie(self):
        """
        Zmniejsza liczbę żyć gracza o 1. 
        Jeśli liczba żyć spadnie do 0, kończy grę porażką.
        Zwraca wartość logiczną (True = gracz nadal żyje, False = koniec gry).
        """
        if self.gra_zakonczona: return False
        
        self.zycia -= 1
        self.zaktualizuj_widok_zyc()
        
        if self.zycia <= 0:
            self.zakoncz_gre(wygrana=False)
            return False
        return True

    def sprawdz_stan_gry(self):
        """Sprawdza warunek wygranej wykorzystując funkcję isSolved() z generatora."""
        if self.gra_zakonczona: return
        self.odswiez_obecne_podswietlenie()

        if hasattr(self, 'plansza') and self.plansza.isSolved():
            self.zakoncz_gre(wygrana=True)

    def zakoncz_gre(self, wygrana=True):
        """
        Zatrzymuje czas, blokuje planszę i wyświetla na niej animowany napis 
        (WYGRANA/PRZEGRANA). Po 3 sekundach przenosi gracza do rankingu.
        """
        if self.gra_zakonczona: return
        self.gra_zakonczona = True
        
        self.stoper.stop()
        
        # Wyszarzenie całej planszy
        for r in range(9):
            for c in range(9):
                komorka = self.komorki[r][c]
                komorka.setReadOnly(True)
                komorka.setStyleSheet("background-color: #f1f5f9; color: #cbd5e1; border: 1px solid #e2e8f0; font-size: 36px;")

        tekst = "WYGRANA !" if wygrana else "PRZEGRANA"
        kolor = "#16a34a" if wygrana else "#dc2626" 
        
        # Formatowanie środkowego wiersza na napis końcowy
        for c in range(9):
            komorka = self.komorki[4][c]
            komorka.notatki.clear()
            komorka.wartosc = tekst[c]
            komorka.setText(tekst[c])
            komorka.setAlignment(Qt.AlignCenter) 
            
            komorka.setStyleSheet(f"""
                background-color: white;
                color: {kolor};
                font-size: 48px;
                font-weight: 900;
                border: 4px solid {kolor};
                border-radius: 8px;
                padding: 0px; 
            """)

        # Odliczanie 3 sekund przed wywołaniem tabeli wyników
        QTimer.singleShot(3000, lambda: self.przejdz_do_rankingu(wygrana))

    def przejdz_do_rankingu(self, wygrana):
        """
        Zapisuje ostateczny wynik do bazy danych (tylko jeśli gracz wygrał)
        i wyświetla klasę RankingOkno pochodzącą z zewnętrznego pliku.
        """
        if self.radio_latwy.isChecked(): poziom = "Łatwy"
        elif self.radio_trudny.isChecked(): poziom = "Trudny"
        else: poziom = "Średni"

        manager_rankingu = RankingManager()

        if wygrana:
            czas_konca = timeit.default_timer()
            laczny_czas = int(czas_konca - self.czas_startu)

            imie = self.lineedit_nazwa_swoja.text().strip()
            if not imie: 
                imie = "Anonim"
            manager_rankingu.dodaj_wynik(imie, poziom, laczny_czas)

        okno_wynikow = RankingOkno(manager_rankingu, domyslny_poziom=poziom, parent=self)
        okno_wynikow.exec_() 
        self.stos_ekranow.setCurrentWidget(self.ekran_menu)

    def ustaw_styl_komorki(self, komorka, r, c, kolor_tla, czy_blad=False):
        """
        Nadaje komórce odpowiednie obramowanie (zgodne z gridem 3x3 Sudoku)
        oraz kolor czcionki zależny od jej aktualnego stanu (błąd, notatka, cyfra własna).
        """
        top = "3px solid black" if r % 3 == 0 else "1px solid #cbd5e1"
        left = "3px solid black" if c % 3 == 0 else "1px solid #cbd5e1"
        bottom = "3px solid black" if r == 8 else "0px"
        right = "3px solid black" if c == 8 else "0px"

        if komorka.wygenerowane:
            kolor_tekstu = "black"       
            rozmiar = "36px"
        else:
            if komorka.wartosc:     
                kolor_tekstu = "red" if czy_blad else "#0284c7"     
                rozmiar = "36px"
            elif komorka.notatki:   
                kolor_tekstu = "#64748b" 
                rozmiar = "14px"
            else:                   
                kolor_tekstu = "black"
                rozmiar = "36px"

        komorka.setStyleSheet(f"""
            QLineEdit {{
                background-color: {kolor_tla};
                color: {kolor_tekstu};
                border-top: {top}; border-left: {left}; border-bottom: {bottom}; border-right: {right};
                font-size: {rozmiar}; 
                font-weight: bold;
                border-radius: 0px; 
                padding: 4px;
            }}
        """)

    def odswiez_obecne_podswietlenie(self):
        """Służy do ponownego przeliczenia podświetlenia bez zmiany fokusu gracza."""
        if hasattr(self, 'akt_wiersz') and hasattr(self, 'akt_kolumna'):
            self.podswietl_obszary(self.akt_wiersz, self.akt_kolumna)

    def podswietl_obszary(self, klik_wiersz, klik_kolumna):
        """
        Odpowiada za logikę krzyżowego podświetlania wiersza, kolumny
        oraz wewnętrznego kwadratu 3x3 w którym znajduje się kursor.
        Zarządza również podświetlaniem błędów logicznych na czerwono.
        """
        if self.gra_zakonczona: return

        self.akt_wiersz = klik_wiersz
        self.akt_kolumna = klik_kolumna
        
        start_wiersza = (klik_wiersz // 3) * 3
        start_kolumny = (klik_kolumna // 3) * 3
        
        bledy = self.plansza.getErrors() if hasattr(self, 'plansza') else set()
        
        for wiersz in range(9):
            for kolumna in range(9):
                komorka = self.komorki[wiersz][kolumna]
                
                ten_sam_wiersz = (wiersz == klik_wiersz)
                ta_sama_kolumna = (kolumna == klik_kolumna)
                ten_sam_kwadrat = (start_wiersza <= wiersz < start_wiersza + 3 and start_kolumny <= kolumna < start_kolumny + 3)
                
                czy_blad = (wiersz, kolumna) in bledy
                
                # Podświetlanie wskazanej komórki, jej kolumny i wiersza
                if wiersz == klik_wiersz and kolumna == klik_kolumna:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#b1e2fc", czy_blad) 
                elif ten_sam_wiersz or ta_sama_kolumna or ten_sam_kwadrat:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#e0f2fe", czy_blad) 
                else:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white", czy_blad)