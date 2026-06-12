import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QGroupBox, QRadioButton, QCheckBox, QPushButton
)
from PyQt5.QtGui import QFont

from generator import Board
from PyQt5.QtGui import QIntValidator

def rgb(r, g, b):
    return f"rgb({r}, {g}, {b})"


class GlowneOkno(QMainWindow):
    """tworzymy klasę nadrzędną, ustawiamy pozycję okna na ekranie, wymiary, tytuł okna"""
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 1100, 750)
        self.setWindowTitle("Sudoku")
        self.initUI()
        
    def initUI(self):
        """tworzymy menu i poszczególne kolumny. Ustawiamy rozmiar czcionki, kolor tła, tworzymy boxy"""

        # Główny układ pionowy dla całej zawartości okna
        layout_strony = QVBoxLayout()
        layout_strony.setContentsMargins(50, 50, 50, 50)
        layout_strony.setSpacing(30)

        #dodajemy "rozciąganie" okna
        layout_strony.addStretch(1)

        #Nagłówek Sudoku
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

        #Układ poziomy dla kolumn/boksów
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(50)

        #dodajemy "rozciąganie" strony
        menu_layout.addStretch(1)

        #Wspólny styl dla boksów (GroupBox)
        style_boxa = f"""
             QGroupBox {{
                font-family: 'Segoe UI';
                font-size: 24px;\
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
       #pierwsza koluma-rejestracja użytkownika
        kolumna1 = QVBoxLayout()

        grupa1 = QGroupBox("Rejestracja")
        grupa1.setStyleSheet(style_boxa)

        grupa1.setMinimumWidth(500)
        grupa1.setMaximumWidth(650)
    
        napis_nazwa_swoja = QLabel("Wpisz swoje imię:")

        napis_nazwa_swoja.setStyleSheet(f"""
            font-family: 'Segoe UI';
            font-size: 18px; 
            color: {rgb(100, 116, 139)};
            font-weight: normal;
            background-color: transparent;
        """)

        kolumna1.addWidget(napis_nazwa_swoja)

        self.lineedit_nazwa_swoja = QLineEdit()
        self.lineedit_nazwa_swoja.setPlaceholderText("Twoje imię")

        self.lineedit_nazwa_swoja.setStyleSheet(f"""
            QLineEdit {{
                padding: 18px;
                font-size: 20px;
                border: 1px solid {rgb(203, 213, 225)};
                border-radius: 8px;
                background: {rgb(255, 255, 255)};
                color: {rgb(0, 0, 0)};
            }}
            QLineEdit::placeholder {{
                color: {rgb(148, 163, 184)};
            }}
        """)
        kolumna1.addWidget(self.lineedit_nazwa_swoja)

        kolumna1.addStretch()
        
        grupa1.setLayout(kolumna1)
        menu_layout.addWidget(grupa1)

        #druga kolumna-wybór poziomu trudności
        kolumna2 = QVBoxLayout()

        grupa2 = QGroupBox("Poziom trudności")
        grupa2.setStyleSheet(style_boxa)

        grupa2.setMinimumWidth(500)
        grupa2.setMaximumWidth(650)

        self.radio_latwy = QRadioButton("Łatwy")
        self.radio_sredni = QRadioButton("Średni")
        self.radio_trudny = QRadioButton("Trudny")
        
        self.radio_sredni.setChecked(True)
        #ustawiamy styl boxow kolor, czcionke, obramowania
        style_radio = f"""
            QRadioButton {{
                font-family: 'Segoe UI';
                font-size: 20px;
                color: {rgb(40, 40, 40)};
                padding: 18px;
                font-weight: normal;
                background-color: {rgb(255, 255, 255)};
                border-radius: 10px;
                border: 1px solid {rgb(220, 220, 220)};
            }}

            QRadioButton:hover {{
                background-color: {rgb(245, 245, 245)};
            }}

            QRadioButton::indicator {{
                width: 22px;
                height: 22px;
            }}
        """

        for rb in [self.radio_latwy, self.radio_sredni, self.radio_trudny]:
            rb.setStyleSheet(style_radio)
            kolumna2.addWidget(rb)

        kolumna2.addStretch()

        grupa2.setLayout(kolumna2)
        menu_layout.addWidget(grupa2)

        #dodawanie "rozciągania"
        menu_layout.addStretch(1)

        #Dodajemy boki do głównego układu strony
        layout_strony.addLayout(menu_layout)

        #Przycisk startu
        layout_przycisku = QHBoxLayout()
        layout_przycisku.addStretch(1)
        
        self.przycisk_start = QPushButton("ROZPOCZNIJ GRĘ")

        self.przycisk_start.setFixedWidth(550)
        #ustawiamy kolory, czcionkę, obramowania
        self.przycisk_start.setStyleSheet(f"""
            QPushButton {{
                background-color: {rgb(30, 41, 59)};
                color: {rgb(255, 255, 255)};
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
                border-radius: 12px;
                margin-top: 25px;
            }}

            QPushButton:hover {{
                background-color: {rgb(51, 65, 85)};
            }}
        """)

        self.przycisk_start.clicked.connect(self.otworz_gre)

        layout_przycisku.addWidget(self.przycisk_start)
        layout_przycisku.addStretch(1)
        
        layout_strony.addLayout(layout_przycisku)

        #dodawanie "rozciągania"
        layout_strony.addStretch(1)

        #Głowne osadzenie layoutu
        centralny_widget = QWidget()

        centralny_widget.setStyleSheet(
            f"background-color: {rgb(162, 171, 31)};"
        )

        centralny_widget.setLayout(layout_strony)
        self.setCentralWidget(centralny_widget)

    def otworz_gre(self):
        trudnosc = 1 # domyślnie średni
        if self.radio_latwy.isChecked(): trudnosc = 0
        elif self.radio_trudny.isChecked(): trudnosc = 2
        
        # Otwieramy nowe okno i zamykamy stare
        self.nowe_okno = OknoGry(trudnosc)
        self.nowe_okno.show()
        self.close()

# ==========================================================
# CZĘŚĆ GRY I PODŚWIETLANIA (WKLEJONE NA DOLE)
# ==========================================================
class SudokuCell(QLineEdit):
    fokus_otrzymany = pyqtSignal(int, int)

    def __init__(self, row, col, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.setMaxLength(1)
        self.setAlignment(Qt.AlignCenter)
        self.setValidator(QIntValidator(1, 9))

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.fokus_otrzymany.emit(self.row, self.col)

class OknoGry(QWidget):
    def __init__(self, trudnosc):
        super().__init__()
        self.setWindowTitle("Gra w Sudoku - Plansza")
        self.setGeometry(150, 150, 800, 800)
        self.setStyleSheet(f"background-color: rgb(162, 171, 31);")
        
        layout_glowny_gry = QHBoxLayout()
        self.siatka_gry = QGridLayout()
        self.siatka_gry.setSpacing(0)
        self.komorki = [[None for _ in range(9)] for _ in range(9)]

        for wiersz in range(9):
            for kolumna in range(9):
                komorka = SudokuCell(wiersz, kolumna)
                komorka.fokus_otrzymany.connect(self.podswietl_obszary)
                self.komorki[wiersz][kolumna] = komorka
                self.siatka_gry.addWidget(komorka, wiersz, kolumna)

        layout_glowny_gry.addLayout(self.siatka_gry)
        self.setLayout(layout_glowny_gry)
        
        self.wczytaj_logike(trudnosc)

    def wczytaj_logike(self, trudnosc):
        plansza = Board()
        plansza.generateQuestionBoardCode(trudnosc)

        for wiersz in range(9):
            for kolumna in range(9):
                wartosc = plansza.board[wiersz][kolumna]
                komorka = self.komorki[wiersz][kolumna]
                komorka.clear()
                self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")
                if wartosc != 0:
                    komorka.setText(str(wartosc))
                    komorka.setReadOnly(True)
                else:
                    komorka.setReadOnly(False)

    def ustaw_styl_komorki(self, komorka, r, c, kolor_tla):
        top = "2px solid black" if r % 3 == 0 else "1px solid #cbd5e1"
        left = "2px solid black" if c % 3 == 0 else "1px solid #cbd5e1"
        bottom = "2px solid black" if r == 8 else "0px"
        right = "2px solid black" if c == 8 else "0px"

        komorka.setStyleSheet(f"""
            QLineEdit {{
                background-color: {kolor_tla};
                color: black;
                border-top: {top}; border-left: {left}; border-bottom: {bottom}; border-right: {right};
                font-size: 24px; font-weight: bold;
            }}
        """)

    def podswietl_obszary(self, klik_wiersz, klik_kolumna):
        start_wiersza = (klik_wiersz // 3) * 3
        start_kolumny = (klik_kolumna // 3) * 3
        
        for wiersz in range(9):
            for kolumna in range(9):
                komorka = self.komorki[wiersz][kolumna]
                
                ten_sam_wiersz = (wiersz == klik_wiersz)
                ta_sama_kolumna = (kolumna == klik_kolumna)
                ten_sam_kwadrat = (start_wiersza <= wiersz < start_wiersza + 3 and start_kolumny <= kolumna < start_kolumny + 3)
                
                if wiersz == klik_wiersz and kolumna == klik_kolumna:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#bae6fd")
                elif ten_sam_wiersz or ta_sama_kolumna or ten_sam_kwadrat:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#e0f2fe")
                else:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")


#Uruchomienie
def main():
    aplikacja = QApplication(sys.argv)
    glowne_okno = GlowneOkno()
    glowne_okno.show()
    sys.exit(aplikacja.exec())


if __name__ == "__main__":
    main()

