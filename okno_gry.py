import sys
from generator import Board  # Łączymy się z Twoim pierwszym plikiem!

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QGroupBox, QRadioButton, QPushButton, QStackedWidget, QSizePolicy, QCheckBox
)
from PyQt5.QtGui import QIntValidator

def rgb(r, g, b):
    return f"rgb({r}, {g}, {b})"

# ==========================================================
# KOMÓRKA PLANSZY
# ==========================================================
class SudokuCell(QLineEdit):
    fokus_otrzymany = pyqtSignal(int, int)

    def __init__(self, row, col, glowne_okno, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.glowne_okno = glowne_okno 
        
        self.wartosc = ""
        self.notatki = set()
        self.wygenerowane = False
        
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Powiększone domyślne limity, żeby plansza była odpowiednio duża na Twoim monitorze!
        self.setMinimumSize(180, 180)
        self.setMaximumSize(250, 250) 

        self.setReadOnly(True)
        self.setCursor(Qt.ArrowCursor)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.fokus_otrzymany.emit(self.row, self.col)

    def keyPressEvent(self, event):
        if self.wygenerowane:
            return 

        klawisz = event.text()
        if klawisz in "123456789":
            if self.glowne_okno.checkbox_notatki.isChecked():
                if klawisz in self.notatki:
                    self.notatki.remove(klawisz) 
                else:
                    self.notatki.add(klawisz)
                self.wartosc = "" 
            else:
                self.wartosc = klawisz
                # USUNIĘTO: self.notatki.clear() - dzięki temu notatki zostają w pamięci!
        
        # Kasowanie (Backspace / Delete)
        elif event.key() in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Space):
            self.wartosc = ""
            # USUNIĘTO: self.notatki.clear() - dzięki temu Backspace odkrywa notatki z powrotem!
        else:
            super().keyPressEvent(event)
            return

        self.odswiez_tekst()
        self.glowne_okno.odswiez_obecne_podswietlenie()

    def ustaw_poczatkowa(self, val):
        if val != 0:
            self.wartosc = str(val)
            self.wygenerowane = True
        else:
            self.wartosc = ""
            self.wygenerowane = False
        self.notatki.clear()
        self.odswiez_tekst()

    def odswiez_tekst(self):
        if self.wartosc:
            self.setText(self.wartosc)
            self.setAlignment(Qt.AlignCenter)
        elif self.notatki:
            tekst = " ".join(sorted(list(self.notatki)))
            self.setText(tekst)
            self.setAlignment(Qt.AlignRight | Qt.AlignTop)
        else:
            self.setText("")


# ==========================================================
# GŁÓWNE OKNO
# ==========================================================
class GlowneOkno(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(100, 100, 1100, 750)
        self.setWindowTitle("Sudoku")
        
        self.stos_ekranow = QStackedWidget()
        self.setCentralWidget(self.stos_ekranow)
        
        self.initUI()      
        self.initGraUI()   
        
    def initUI(self):
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
        self.ekran_gry = QWidget()
        self.ekran_gry.setStyleSheet(f"background-color: {rgb(162, 171, 31)};")
        
        layout_glowny_gry = QHBoxLayout()
        
        lewy_panel = QVBoxLayout()
        przycisk_wroc = QPushButton("Wróć do Menu")
        przycisk_wroc.setStyleSheet(f"""
            QPushButton {{
                background-color: {rgb(30, 41, 59)};
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px 25px;
                border-radius: 10px;
            }}
            QPushButton:hover {{ background-color: {rgb(51, 65, 85)}; }}
        """)
        przycisk_wroc.clicked.connect(lambda: self.stos_ekranow.setCurrentWidget(self.ekran_menu))
        lewy_panel.addWidget(przycisk_wroc)
        
        self.checkbox_notatki = QCheckBox("Tryb Notatek")
        self.checkbox_notatki.setStyleSheet(f"""
            QCheckBox {{
                font-family: 'Segoe UI';
                font-size: 20px;
                font-weight: bold;
                color: {rgb(30, 41, 59)};
                margin-top: 30px;
            }}
            QCheckBox::indicator {{ width: 25px; height: 25px; }}
        """)
        lewy_panel.addWidget(self.checkbox_notatki)
        
        lewy_panel.addStretch() 
        layout_glowny_gry.addLayout(lewy_panel)

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
        trudnosc = 1 
        if self.radio_latwy.isChecked(): trudnosc = 0
        elif self.radio_trudny.isChecked(): trudnosc = 2

        plansza = Board()
        plansza.generateQuestionBoardCode(trudnosc)

        for wiersz in range(9):
            for kolumna in range(9):
                wartosc = plansza.board[wiersz][kolumna]
                komorka = self.komorki[wiersz][kolumna]
                
                komorka.ustaw_poczatkowa(wartosc)
                self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")

        self.stos_ekranow.setCurrentWidget(self.ekran_gry)

    def ustaw_styl_komorki(self, komorka, r, c, kolor_tla):
        top = "3px solid black" if r % 3 == 0 else "1px solid #cbd5e1"
        left = "3px solid black" if c % 3 == 0 else "1px solid #cbd5e1"
        bottom = "3px solid black" if r == 8 else "0px"
        right = "3px solid black" if c == 8 else "0px"

        if komorka.wygenerowane:
            kolor_tekstu = "black"       
            rozmiar = "50px"
        else:
            if komorka.wartosc:     
                kolor_tekstu = "#0284c7"     
                rozmiar = "50px"
            elif komorka.notatki:   
                kolor_tekstu = "#64748b" 
                rozmiar = "25px"
            else:                   
                kolor_tekstu = "black"
                rozmiar = "50px"

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
        if hasattr(self, 'akt_wiersz') and hasattr(self, 'akt_kolumna'):
            self.podswietl_obszary(self.akt_wiersz, self.akt_kolumna)

    def podswietl_obszary(self, klik_wiersz, klik_kolumna):
        self.akt_wiersz = klik_wiersz
        self.akt_kolumna = klik_kolumna
        
        start_wiersza = (klik_wiersz // 3) * 3
        start_kolumny = (klik_kolumna // 3) * 3
        
        for wiersz in range(9):
            for kolumna in range(9):
                komorka = self.komorki[wiersz][kolumna]
                
                ten_sam_wiersz = (wiersz == klik_wiersz)
                ta_sama_kolumna = (kolumna == klik_kolumna)
                ten_sam_kwadrat = (start_wiersza <= wiersz < start_wiersza + 3 and start_kolumny <= kolumna < start_kolumny + 3)
                
                if wiersz == klik_wiersz and kolumna == klik_kolumna:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#b1e2fc") 
                elif ten_sam_wiersz or ta_sama_kolumna or ten_sam_kwadrat:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#e0f2fe") 
                else:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white") 

def main():
    aplikacja = QApplication(sys.argv)
    glowne_okno = GlowneOkno()
    glowne_okno.show()
    sys.exit(aplikacja.exec())

if __name__ == "__main__":
    main()