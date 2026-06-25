import sys
import timeit
from generator import Plansza
from Ranking_czasow import RankingManager, RankingOkno, gra_zakonczona_sukcesem

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

LANGUAGES = {
    "pl": {
        "window_title": "Sudoku",
        "sudoku_title": "SUDOKU",
        "registration": "Rejestracja",
        "enter_name": "Wpisz swoje imię:",
        "your_name": "Twoje imię",
        "difficulty_level": "Poziom trudności",
        "easy": "Łatwy",
        "medium": "Średni",
        "hard": "Trudny",
        "start_game": "ROZPOCZNIJ GRĘ",
        "time_label": "Czas: {}",
        "back_to_menu": "Wróć do Menu",
        "lives_label": "Życia: {}",
        "notes_mode": "Tryb Notatek",
        "instruction_btn": "Co to tryb notatek?",
        "instruction_desc": "Tryb notatek to funkcja, która ma ułatwić Ci rozgrywkę. Po jej włączeniu każda wpisana cyfra staje się jedynie małą notatką w prawym górnym rogu pola. Możesz wpisać kilka cyfr jednocześnie lub w dowolnym momencie je skasować. Nie są one traktowane jako ostateczna odpowiedź. By usunąć wpisaną już cyfrę, ponownie ją naciśnij, a zniknie.",
        "surrender_button": "PODDAJĘ SIĘ\n(Zakończ)",
        "hint_button": "Podpowiedź: {}",
        "hint_no_more": "Nie masz już podpowiedzi.",
        "hint_choose_cell": "Najpierw kliknij puste pole na planszy.",
        "hint_start_cell": "Nie można użyć podpowiedzi na polu startowym.",
        "game_won": "WYGRANA !",
        "game_lost": "PRZEGRANA",
        "ranking_window_title": "Ranking Graczy - Sudoku",
        "ranking_title": "RANKING",
        "place": "Miejsce",
        "player": "Gracz",
        "time": "Czas",
        "anonymous": "Anonim",
        "language_label": "Wybierz język:",
        "instructions_title": "Instrukcja Gry",
        "instructions_content": "Witaj w Sudoku!\nTwoim zadaniem jest uzupełnienie planszy cyframi od 1 do 9 tak, aby każda cyfra występowała tylko raz w każdym wierszu, kolumnie oraz w każdym kwadracie 3×3",
    },
    "ua": {
        "window_title": "Судоку",
        "sudoku_title": "СУДОКУ",
        "registration": "Реєстрація",
        "enter_name": "Введіть своє ім'я:",
        "your_name": "Ваше ім'я",
        "difficulty_level": "Рівень складності",
        "easy": "Легкий",
        "medium": "Середній",
        "hard": "Складний",
        "start_game": "РОЗПОЧАТИ ГРУ",
        "time_label": "Час: {}",
        "back_to_menu": "Повернутися до меню",
        "lives_label": "Життя: {}",
        "notes_mode": "Режим нотаток",
        "instruction_btn": "Що таке режим нотаток?",
        "instruction_desc": "Режим нотаток – це funkcja, яка полегшить вам гру. Після його увімкнення кожна введена cyfra стає лише маленькою заміткою у правому верхньому кутку клітинки. Ви можете ввести кілька цифр одночасно або видалити їх у будь-який момент. Вони не вважаються остаточною відповіддю. Щоб видалити вже введену цифру, просто натисніть її ще раз, і вона зникне.",
        "surrender_button": "ЗДАЮСЯ\n(Завершити)",
        "hint_button": "Підказка: {}",
        "hint_no_more": "У тебе більше немає підказок.",
        "hint_choose_cell": "Спочатку натисни порожнє поле на дошці.",
        "hint_start_cell": "Не можна використати підказку на початковому полі.",
        "game_won": "ПЕРЕМОГА!",
        "game_lost": "ПОРАЗКА",
        "ranking_window_title": "Рейтинг гравців - Судоку",
        "ranking_title": "РЕЙТИНГ",
        "place": "Місце",
        "player": "Гравець",
        "time": "Час",
        "anonymous": "Анонім",
        "language_label": "Оберіть мову:",
        "instructions_title": "Інструкція Гри",
        "instructions_content": "Вітаємо в Судоку!\nВашим завданням є заповнити дошку цифрами від 1 до 9 так, щоб кожна цифра з'являлась лише один раз у кожному рядку, стовпці та квадраті 3×3",
    },
    "en": {
        "window_title": "Sudoku",
        "sudoku_title": "SUDOKU",
        "registration": "Registration",
        "enter_name": "Enter your name:",
        "your_name": "Your name",
        "difficulty_level": "Difficulty level",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "start_game": "START GAME",
        "time_label": "Time: {}",
        "back_to_menu": "Back to Menu",
        "lives_label": "Lives: {}",
        "notes_mode": "Notes Mode",
        "instruction_btn": "What is notes mode?",
        "instruction_desc": "Notes mode is a feature designed to make your gameplay easier. When enabled, each entered digit becomes just a small note in the top right corner of the cell. You can type multiple digits at once or delete them at any time. They are not treated as a final answer. To remove an already entered digit, simply press it again, and it will disappear.",
        "surrender_button": "I GIVE UP\n(End)",
        "hint_button": "Hint: {}",
        "hint_no_more": "You have no hints left.",
        "hint_choose_cell": "First click an empty cell on the board.",
        "hint_start_cell": "You cannot use a hint on a starting cell.",
        "game_won": "VICTORY!",
        "game_lost": "DEFEAT",
        "ranking_window_title": "Player Ranking - Sudoku",
        "ranking_title": "RANKING",
        "place": "Place",
        "player": "Player",
        "time": "Time",
        "anonymous": "Anonymous",
        "language_label": "Choose language:",
        "instructions_title": "Game Instructions",
        "instructions_content": "Welcome to Sudoku!\nYour task is to fill the board with digits from 1 to 9 so that each digit appears only once in each row, column, and 3×3 square.",
    }
}

# KOMÓRKA PLANSZY
class SudokuCell(QLineEdit):
    """
    Klasa reprezentująca pojedynczą komórkę (kratkę) na planszy Sudoku.
    """
    fokus_otrzymany = pyqtSignal(int, int)

    def __init__(self, row, col, glowne_okno, parent=None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.glowne_okno = glowne_okno
        
        self.wartosc = ""
        self.notatki = set()
        self.wygenerowane = False
        self.odgadnieta = False
        self.czy_bledna = False 
        self.poprzednie_bledy = set()  # Pamięć błędów popełnionych w tym konkretnym polu
        
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.setMinimumSize(60, 60)
        self.setMaximumSize(80, 80)

        self.setReadOnly(True)
        self.setCursor(Qt.ArrowCursor)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.fokus_otrzymany.emit(self.row, self.col)

    def keyPressEvent(self, event):
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

        # Blokada edycji dla cyfr startowych, odgadniętych i po zakończeniu gry
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
                self.czy_bledna = False
            # Normalne wpisywanie cyfry
            else:
                self.wartosc = klawisz_tekst
                
                # Szybka weryfikacja z kluczem rozwiązania
                poprawna = self.glowne_okno.poprawna_plansza[self.row][self.col]
                
                if int(klawisz_tekst) == poprawna:
                    self.odgadnieta = True
                    self.czy_bledna = False
                    self.notatki.clear()
                    self.glowne_okno.aktualna_plansza[self.row][self.col] = int(klawisz_tekst)
                else:
                    # Ignorowanie powtarzania tego samego błędu (Faza 3)
                    if klawisz_tekst in self.poprzednie_bledy:
                        return
                    self.poprzednie_bledy.add(klawisz_tekst)

                    self.odgadnieta = False
                    self.czy_bledna = True
                    zyje = self.glowne_okno.odejmij_zycie()
                    if not zyje:
                        return
        
        # Usuwanie zawartości komórki
        elif klawisz_qt in (Qt.Key_Backspace, Qt.Key_Delete, Qt.Key_Space):
            self.wartosc = ""
            self.czy_bledna = False
            self.glowne_okno.aktualna_plansza[self.row][self.col] = 0
        else:
            super().keyPressEvent(event)
            return

        self.odswiez_tekst()
        self.glowne_okno.sprawdz_stan_gry()

    def ustaw_poczatkowa(self, val):
        if val != 0:
            self.wartosc = str(val)
            self.wygenerowane = True
        else:
            self.wartosc = ""
            self.wygenerowane = False
        
        self.odgadnieta = False
        self.czy_bledna = False
        self.notatki.clear()
        self.poprzednie_bledy.clear() # Czyścimy pamięć błędów przy nowej grze
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
            self.setAlignment(Qt.AlignCenter)


# GŁÓWNE OKNO
class GlowneOkno(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.resize(1100, 750)

        self.jezyk = "pl"
        self.translations = LANGUAGES
        self.setWindowTitle(self.translate("window_title"))

        self.stos_ekranow = QStackedWidget()
        self.setCentralWidget(self.stos_ekranow)

        self.czas_startu = 0
        self.zycia = 3

        self.gra_zakonczona = False
        self.liczba_podpowiedzi = 3

        self.initUI()
        self.initGraUI()

    def translate(self, key):
        return self.translations.get(self.jezyk, {}).get(key, key)

    def setJezyk(self, jezyk):
        if jezyk not in self.translations or self.jezyk == jezyk:
            return
        self.jezyk = jezyk
        self.setWindowTitle(self.translate("window_title"))

        self.napis_sudoku.setText(self.translate("sudoku_title"))
        self.grupa1.setTitle(self.translate("registration"))
        self.napis_nazwa_swoja.setText(self.translate("enter_name"))
        self.lineedit_nazwa_swoja.setPlaceholderText(self.translate("your_name"))
        self.grupa2.setTitle(self.translate("difficulty_level"))
        self.radio_latwy.setText(self.translate("easy"))
        self.radio_sredni.setText(self.translate("medium"))
        self.radio_trudny.setText(self.translate("hard"))
        self.przycisk_start.setText(self.translate("start_game"))
        self.etykieta_jezyk.setText(self.translate("language_label"))
        self.przycisk_wroc.setText(self.translate("back_to_menu"))
        self.checkbox_notatki.setText(self.translate("notes_mode"))
        self.przycisk_zakoncz.setText(self.translate("surrender_button"))
        self.etykieta_czasu.setText(self.translate("time_label").format("00:00"))
        self.zaktualizuj_widok_zyc()
        self.przycisk_instrukcja.setText(self.translate("instruction_btn"))
        self.etykieta_opis_notatek.setText(self.translate("instruction_desc"))
        self.przycisk_instrukcja_menu.setText(self.translate("instructions_title"))
        self.grupa3.setTitle(self.translate("instructions_title"))
        self.etykieta_instrukcja.setText(self.translate("instructions_content"))
        
        if hasattr(self, 'ekran_gry') and self.stos_ekranow.currentWidget() == self.ekran_gry:
            self.etykieta_czasu.setText(self.translate("time_label").format("00:00"))
            self.zaktualizuj_widok_zyc()
            
    def wycentruj_okno(self):
        ekran = QApplication.primaryScreen()
        geometria_ekranu = ekran.availableGeometry()
    
        geometria_okna = self.frameGeometry()
        geometria_okna.moveCenter(geometria_ekranu.center())
    
        self.move(geometria_okna.topLeft())
        
    def initUI(self):
        self.ekran_menu = QWidget()
    
        layout_strony = QVBoxLayout()
        layout_strony.setContentsMargins(50, 25, 50, 30)
        layout_strony.setSpacing(20)
        layout_strony.addSpacing(10)
    
        self.napis_sudoku = QLabel(self.translate("sudoku_title"))
        self.napis_sudoku.setAlignment(Qt.AlignCenter)
        self.napis_sudoku.setStyleSheet(f"""
            font-family: 'Segoe UI', sans-serif;
            font-size: 64px;
            font-weight: 900;
            color: {rgb(30, 41, 59)};
            letter-spacing: 10px;
            margin-bottom: 0px;
        """)
        layout_strony.addWidget(self.napis_sudoku)
    
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(30)
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
                margin-top: 35px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 15px;
            }}
        """
    
            # ---------------- REJESTRACJA ----------------
    
        kolumna1 = QVBoxLayout()
        kolumna1.setSpacing(12)
        kolumna1.setContentsMargins(20, 15, 20, 15)
    
        self.grupa1 = QGroupBox(self.translate("registration"))
        self.grupa1.setStyleSheet(style_boxa)
        self.grupa1.setFixedSize(420, 230)
    
        self.napis_nazwa_swoja = QLabel(self.translate("enter_name"))
        self.napis_nazwa_swoja.setStyleSheet(
            f"font-family: 'Segoe UI'; font-size: 18px; "
            f"color: {rgb(100, 116, 139)}; font-weight: normal; "
            f"background-color: transparent;"
        )
        kolumna1.addWidget(self.napis_nazwa_swoja)
    
        self.lineedit_nazwa_swoja = QLineEdit()
        self.lineedit_nazwa_swoja.setFixedHeight(42)
        self.lineedit_nazwa_swoja.setPlaceholderText(self.translate("your_name"))
        self.lineedit_nazwa_swoja.setStyleSheet(
            f"""
            QLineEdit {{
                padding-left: 15px;
                padding-right: 15px;
                font-size: 20px;
                border: 1px solid {rgb(203, 213, 225)};
                border-radius: 8px;
                background: {rgb(255, 255, 255)};
                color: {rgb(0, 0, 0)};
            }}
            QLineEdit::placeholder {{
                color: {rgb(148, 163, 184)};
            }}
            """
        )
        self.lineedit_nazwa_swoja.setMaxLength(15)
        kolumna1.addWidget(self.lineedit_nazwa_swoja)
    
        self.etykieta_jezyk = QLabel(self.translate("language_label"))
        self.etykieta_jezyk.setStyleSheet(
            f"font-family: 'Segoe UI'; font-size: 18px; "
            f"color: {rgb(100, 116, 139)}; font-weight: normal; "
            f"background-color: transparent;"
        )
        kolumna1.addWidget(self.etykieta_jezyk)
    
        self.pasek_jezyka = QHBoxLayout()
        self.pasek_jezyka.setSpacing(12)
    
        self.przycisk_pl = QPushButton("Polski")
        self.przycisk_ua = QPushButton("Українська")
        self.przycisk_en = QPushButton("English")
    
        style_language_button = f"""
            QPushButton {{
                background-color: {rgb(248, 249, 250)};
                color: {rgb(30, 41, 59)};
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid {rgb(203, 213, 225)};
            }}
            QPushButton:hover {{
                background-color: {rgb(226, 232, 240)};
            }}
        """
    
        self.przycisk_pl.setFixedSize(100, 36)
        self.przycisk_ua.setFixedSize(150, 36)
        self.przycisk_en.setFixedSize(110, 36)
    
        for btn in [self.przycisk_pl, self.przycisk_ua, self.przycisk_en]:
            btn.setStyleSheet(style_language_button)
            self.pasek_jezyka.addWidget(btn)
    
        self.przycisk_pl.clicked.connect(lambda: self.setJezyk("pl"))
        self.przycisk_ua.clicked.connect(lambda: self.setJezyk("ua"))
        self.przycisk_en.clicked.connect(lambda: self.setJezyk("en"))
    
        self.pasek_jezyka.addStretch(1)
        kolumna1.addLayout(self.pasek_jezyka)
    
        self.grupa1.setLayout(kolumna1)
        menu_layout.addWidget(self.grupa1, alignment=Qt.AlignTop)
    
            # ---------------- POZIOM TRUDNOŚCI ----------------
    
        kolumna2 = QVBoxLayout()
        kolumna2.setSpacing(12)
        kolumna2.setContentsMargins(20, 15, 20, 15)
    
        self.grupa2 = QGroupBox(self.translate("difficulty_level"))
        self.grupa2.setStyleSheet(style_boxa)
        self.grupa2.setFixedSize(420, 230)
    
        self.radio_latwy = QRadioButton(self.translate("easy"))
        self.radio_sredni = QRadioButton(self.translate("medium"))
        self.radio_trudny = QRadioButton(self.translate("hard"))
        self.radio_sredni.setChecked(True)
    
        style_radio = f"""
            QRadioButton {{
                font-family: 'Segoe UI';
                font-size: 20px;
                color: {rgb(40, 40, 40)};
                font-weight: normal;
                background-color: {rgb(255, 255, 255)};
                border-radius: 10px;
                border: 1px solid {rgb(220, 220, 220)};
                padding-left: 15px;
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
            rb.setFixedHeight(42)
            rb.setStyleSheet(style_radio)
            kolumna2.addWidget(rb)
    
        self.grupa2.setLayout(kolumna2)
        menu_layout.addWidget(self.grupa2, alignment=Qt.AlignTop)
    
        menu_layout.addStretch(1)
    
        layout_strony.addLayout(menu_layout, stretch=0)
        layout_strony.addSpacing(20)
    
            # ---------------- PRZYCISK START ----------------
    
        layout_przycisku = QHBoxLayout()
        layout_przycisku.addStretch(1)
    
        self.przycisk_start = QPushButton(self.translate("start_game"))
        self.przycisk_start.setFixedSize(480, 55)
        self.przycisk_start.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {rgb(30, 41, 59)};
                color: {rgb(255, 255, 255)};
                font-size: 24px;
                font-weight: bold;
                border-radius: 12px;
            }}
            QPushButton:hover {{
                background-color: {rgb(51, 65, 85)};
            }}
            """
        )
    
        self.przycisk_start.clicked.connect(self.uruchom_gre)
    
        layout_przycisku.addWidget(self.przycisk_start)
        layout_przycisku.addStretch(1)
    
        layout_strony.addLayout(layout_przycisku)
        
        # PRZYCISK INSTRUKCJI
        layout_instrukcji = QHBoxLayout()
        layout_instrukcji.addStretch(1)
        
        self.przycisk_instrukcja_menu = QPushButton(self.translate("instructions_title"))
        self.przycisk_instrukcja_menu.setFixedSize(480, 45)
        self.przycisk_instrukcja_menu.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {rgb(71, 85, 105)};
                color: {rgb(255, 255, 255)};
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                margin-top: 15px;
            }}
            QPushButton:hover {{
                background-color: {rgb(51, 65, 85)};
            }}
            """
        )
        layout_instrukcji.addWidget(self.przycisk_instrukcja_menu)
        layout_instrukcji.addStretch(1)
        
        layout_strony.addLayout(layout_instrukcji)
        
        # KAFELEK INSTRUKCJI
        layout_kafelka = QHBoxLayout()
        layout_kafelka.addStretch(1)
        
        self.grupa3 = QGroupBox(self.translate("instructions_title"))
        self.grupa3.setStyleSheet(style_boxa)
        self.grupa3.setFixedWidth(480)
        
        kolumna3 = QVBoxLayout()
        kolumna3.setSpacing(12)
        kolumna3.setContentsMargins(20, 15, 20, 15)
        
        self.etykieta_instrukcja = QLabel(self.translate("instructions_content"))
        self.etykieta_instrukcja.setWordWrap(True)
        self.etykieta_instrukcja.setStyleSheet(
            f"font-family: 'Segoe UI'; font-size: 12px; "
            f"color: {rgb(51, 65, 85)}; font-weight: normal; "
            f"background-color: transparent; line-height: 1.4;"
        )
        kolumna3.addWidget(self.etykieta_instrukcja)
        
        self.grupa3.setLayout(kolumna3)
        self.grupa3.setVisible(False)
        
        layout_kafelka.addWidget(self.grupa3)
        layout_kafelka.addStretch(1)
        
        layout_strony.addLayout(layout_kafelka)
        
        def przelacz_instrukcje_menu():
            stan_obecny = self.grupa3.isVisible()
            self.grupa3.setVisible(not stan_obecny)
        
        self.przycisk_instrukcja_menu.clicked.connect(przelacz_instrukcje_menu)
        
        layout_strony.addSpacing(10)
    
        self.ekran_menu.setStyleSheet(f"background-color: {rgb(162, 171, 31)};")
        self.ekran_menu.setLayout(layout_strony)
        self.stos_ekranow.addWidget(self.ekran_menu)

    def initGraUI(self):
        self.ekran_gry = QWidget()
        self.ekran_gry.setStyleSheet(f"background-color: {rgb(162, 171, 31)};")
        
        layout_glowny_gry = QHBoxLayout()
        
        # PANEL BOCZNY
        lewy_panel = QVBoxLayout()
        self.przycisk_wroc = QPushButton(self.translate("back_to_menu"))
        self.przycisk_wroc.setStyleSheet(f"""
            QPushButton {{ background-color: {rgb(30, 41, 59)}; color: white; font-size: 18px; font-weight: bold; padding: 15px 25px; border-radius: 10px; }}
            QPushButton:hover {{ background-color: {rgb(51, 65, 85)}; }}
        """)
        self.przycisk_wroc.clicked.connect(lambda: self.stos_ekranow.setCurrentWidget(self.ekran_menu))
        lewy_panel.addWidget(self.przycisk_wroc)
        
        self.etykieta_zycia = QLabel()
        self.etykieta_zycia.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 32px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 20px;")
        lewy_panel.addWidget(self.etykieta_zycia)

        self.etykieta_czasu = QLabel(self.translate("time_label").format("00:00"))
        self.etykieta_czasu.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 24px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 5px;")
        lewy_panel.addWidget(self.etykieta_czasu)
        
        self.stoper = QTimer(self)
        self.stoper.timeout.connect(self.aktualizuj_czas)

        self.checkbox_notatki = QCheckBox(self.translate("notes_mode"))
        self.checkbox_notatki.setStyleSheet(f"""
            QCheckBox {{ font-family: 'Segoe UI'; font-size: 20px; font-weight: bold; color: {rgb(30, 41, 59)}; margin-top: 30px; }}
            QCheckBox::indicator {{ width: 25px; height: 25px; }}
        """)
        lewy_panel.addWidget(self.checkbox_notatki)
        
        self.przycisk_podpowiedz = QPushButton(self.translate("hint_button").format(3))
        self.przycisk_podpowiedz.setStyleSheet(f"""
            QPushButton {{
                background-color: {rgb(30, 41, 59)};
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
                margin-top: 15px;
            }}
            QPushButton:hover {{
                background-color: {rgb(51, 65, 85)};
            }}
            QPushButton:disabled {{
                background-color: #94a3b8;
                color: #e2e8f0;
            }}
        """)
        self.przycisk_podpowiedz.clicked.connect(self.uzyj_podpowiedzi)
        lewy_panel.addWidget(self.przycisk_podpowiedz)

        self.przycisk_instrukcja = QPushButton(self.translate("instruction_btn"))
        self.przycisk_instrukcja.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {rgb(30, 41, 59)}; 
                color: white; 
                font-size: 14px; 
                font-weight: bold; 
                padding: 8px; 
                border-radius: 8px; 
                margin-top: 10px; 
            }}
            QPushButton:hover {{ background-color: {rgb(51, 65, 85)}; }}
        """)
        lewy_panel.addWidget(self.przycisk_instrukcja)

        self.etykieta_opis_notatek = QLabel(self.translate("instruction_desc"))
        self.etykieta_opis_notatek.setWordWrap(True)
        self.etykieta_opis_notatek.setFixedWidth(200)
        self.etykieta_opis_notatek.setStyleSheet(f"""
            font-family: 'Segoe UI'; font-size: 13px; color: {rgb(51, 65, 85)};
            margin-top: 5px; margin-bottom: 5px; background-color: transparent;
        """)
        self.etykieta_opis_notatek.setVisible(False)
        lewy_panel.addWidget(self.etykieta_opis_notatek)
        def przelacz_instrukcje():
            stan_obecny = self.etykieta_opis_notatek.isVisible()
            self.etykieta_opis_notatek.setVisible(not stan_obecny)

        self.przycisk_instrukcja.clicked.connect(przelacz_instrukcje)

        self.przycisk_zakoncz = QPushButton(self.translate("surrender_button"))
        self.przycisk_zakoncz.setStyleSheet(f"""
            QPushButton {{ background-color: rgb(220, 38, 38); color: white; font-size: 16px; font-weight: bold; padding: 15px; border-radius: 10px; margin-top: 30px; }}
            QPushButton:hover {{ background-color: rgb(185, 28, 28); }}
        """)
        self.przycisk_zakoncz.clicked.connect(lambda: self.zakoncz_gre(wygrana=False))
        lewy_panel.addWidget(self.przycisk_zakoncz)

        lewy_panel.addStretch()
        layout_glowny_gry.addLayout(lewy_panel)

        # BLOKADA KRADZIEŻY FOKUSU
        for btn in [self.przycisk_wroc, self.checkbox_notatki, self.przycisk_podpowiedz, self.przycisk_instrukcja, self.przycisk_zakoncz]:
            btn.setFocusPolicy(Qt.NoFocus)

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
        self.czas_startu = timeit.default_timer()
        self.gra_zakonczona = False
        self.ekran_gry.setEnabled(True) # Odblokowanie ekranu po poprzedniej grze
        
        self.etykieta_czasu.setText(self.translate("time_label").format("00:00"))
        self.stoper.start(1000)

        self.zycia = 3
        self.zaktualizuj_widok_zyc()
        self.liczba_podpowiedzi = 3
        self.przycisk_podpowiedz.setText(self.translate("hint_button").format(self.liczba_podpowiedzi))
        self.przycisk_podpowiedz.setEnabled(True)

        trudnosc = 1
        if self.radio_latwy.isChecked(): trudnosc = 0
        elif self.radio_trudny.isChecked(): trudnosc = 2

        # ZMIANA
        generator = Plansza()
        kod_gry, kod_rozwiazania = generator.generuj_kod_planszy_gry(trudnosc)
        
        self.aktualna_plansza = [[int(kod_gry[r*9 + c]) for c in range(9)] for r in range(9)]
        self.poprawna_plansza = [[int(kod_rozwiazania[r*9 + c]) for c in range(9)] for r in range(9)]

        for wiersz in range(9):
            for kolumna in range(9):
                wartosc = self.aktualna_plansza[wiersz][kolumna]
                komorka = self.komorki[wiersz][kolumna]
                
                komorka.ustaw_poczatkowa(wartosc)
                self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white")

        self.stos_ekranow.setCurrentWidget(self.ekran_gry)

    def aktualizuj_czas(self):
        if self.gra_zakonczona:
            return
        sekundy_minely = int(timeit.default_timer() - self.czas_startu)
        minuty = sekundy_minely // 60
        sekundy = sekundy_minely % 60
        self.etykieta_czasu.setText(self.translate("time_label").format(f"{minuty:02d}:{sekundy:02d}"))

    def zaktualizuj_widok_zyc(self):
        czerwone = "<span style='color: #ef4444;'>♥</span>" * self.zycia
        czarne = "<span style='color: #64748b;'>♥</span>" * (3 - self.zycia)
        self.etykieta_zycia.setText(self.translate("lives_label").format(f"{czerwone}{czarne}"))

    def odejmij_zycie(self):
        if self.gra_zakonczona: return False
        
        self.zycia -= 1
        self.zaktualizuj_widok_zyc()
        
        if self.zycia <= 0:
            self.zakoncz_gre(wygrana=False)
            return False
        return True
        
    def uzyj_podpowiedzi(self):
        """Wpisuje poprawną cyfrę w aktualnie wybrane pole.
        Gracz może użyć maksymalnie 3 podpowiedzi."""
        if self.gra_zakonczona:
            return
    
        if self.liczba_podpowiedzi <= 0:
            QMessageBox.information(self, "Podpowiedź", self.translate("hint_no_more"))
            return
    
        if not hasattr(self, "akt_wiersz") or not hasattr(self, "akt_kolumna"):
            QMessageBox.information(self, "Podpowiedź", self.translate("hint_choose_cell"))
            return
    
        wiersz = self.akt_wiersz
        kolumna = self.akt_kolumna
        komorka = self.komorki[wiersz][kolumna]
    
        if komorka.wygenerowane:
            QMessageBox.information(self, "Podpowiedź", self.translate("hint_start_cell"))
            return
    
        poprawna_cyfra = self.poprawna_plansza[wiersz][kolumna]
    
        komorka.wartosc = str(poprawna_cyfra)
        komorka.notatki.clear()
        komorka.czy_bledna = False
        komorka.odgadnieta = True
        komorka.odswiez_tekst()
    
        self.aktualna_plansza[wiersz][kolumna] = poprawna_cyfra
    
        self.liczba_podpowiedzi -= 1
        self.przycisk_podpowiedz.setText(self.translate("hint_button").format(self.liczba_podpowiedzi))
    
        if self.liczba_podpowiedzi == 0:
            self.przycisk_podpowiedz.setEnabled(False)
    
        self.odswiez_obecne_podswietlenie()
        self.sprawdz_stan_gry()
        
    def sprawdz_stan_gry(self):
        if self.gra_zakonczona: return
        self.odswiez_obecne_podswietlenie()

        czy_wygrana = True
        for wiersz in range(9):
            for kolumna in range(9):
                komorka = self.komorki[wiersz][kolumna]
                if not (komorka.wygenerowane or komorka.odgadnieta):
                    czy_wygrana = False
                    break
            if not czy_wygrana:
                break
                
        if czy_wygrana:
            self.zakoncz_gre(wygrana=True)

    def zakoncz_gre(self, wygrana=True):
        if self.gra_zakonczona: return
        self.gra_zakonczona = True
        
        self.stoper.stop()
        self.ekran_gry.setEnabled(False) # Zamrożenie gry
        
        for r in range(9):
            for c in range(9):
                komorka = self.komorki[r][c]
                komorka.setReadOnly(True)
                komorka.setStyleSheet("background-color: #f1f5f9; color: #cbd5e1; border: 1px solid #e2e8f0; font-size: 36px;")

        tekst = self.translate("game_won") if wygrana else self.translate("game_lost")
        kolor = "#16a34a" if wygrana else "#dc2626"
        tekst = tekst.center(9)[:9]
        
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

        # Zmniejszony czas czekania
        QTimer.singleShot(1000, lambda: self.przejdz_do_rankingu(wygrana))

    def przejdz_do_rankingu(self, wygrana):
        """
        Pokazuje ranking ZAWSZE. Ale tylko dla zwycięzców zapisuje nowy czas.
        """
        self.stos_ekranow.setCurrentWidget(self.ekran_menu)

        if self.radio_latwy.isChecked(): poziom = "Łatwy"
        elif self.radio_trudny.isChecked(): poziom = "Trudny"
        else: poziom = "Średni"

        if wygrana:
            # Gracz wygrał: Zapisz wynik i pokaż okno
            gra_zakonczona_sukcesem(self, self.czas_startu)
        else:
            # Gracz przegrał/poddał się: Pokaż ranking bez zapisu
            manager_rankingu = RankingManager()
            okno_wynikow = RankingOkno(manager_rankingu, domyslny_poziom=poziom, jezyk=self.jezyk, parent=self)
            okno_wynikow.exec_()

    def ustaw_styl_komorki(self, komorka, r, c, kolor_tla, czy_blad=False):
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
        if hasattr(self, 'akt_wiersz') and hasattr(self, 'akt_kolumna'):
            self.podswietl_obszary(self.akt_wiersz, self.akt_kolumna)

    def podswietl_obszary(self, klik_wiersz, klik_kolumna):
        if self.gra_zakonczona: return

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
                
                czy_blad = komorka.czy_bledna
                
                if wiersz == klik_wiersz and kolumna == klik_kolumna:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#b1e2fc", czy_blad) 
                elif ten_sam_wiersz or ta_sama_kolumna or ten_sam_kwadrat:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "#e0f2fe", czy_blad) 
                else:
                    self.ustaw_styl_komorki(komorka, wiersz, kolumna, "white", czy_blad)
