import json
import os
import timeit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QAbstractItemView, QTabWidget, QWidget
)


class RankingManager:
    """Klasa tworząca ranking czasów graczy z podziałem na poziomy trudności"""

    def __init__(self, plik_bazy="ranking.json"):
        self.plik_bazy = plik_bazy
        self.wyniki = self.wczytaj_ranking()

    def wczytaj_ranking(self):
        if os.path.exists(self.plik_bazy):
            with open(self.plik_bazy, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"Łatwy": {}, "Średni": {}, "Trudny": {}}

    def zapisz_ranking(self):
        with open(self.plik_bazy, "w", encoding="utf-8") as f:
            json.dump(self.wyniki, f, ensure_ascii=False, indent=4)

    def dodaj_wynik(self, imie, poziom, czas_sekundy):
        imie = imie.strip()
        if not imie:
            imie = "Anonim"

        # Zabezpieczenie na wypadek, gdyby w pliku brakowało jakiegoś poziomu
        if poziom not in self.wyniki:
            self.wyniki[poziom] = {}

        # Sprawdzamy imię wewnątrz konkretnego poziomu trudności
        baza_poziomu = self.wyniki[poziom]
        if imie in baza_poziomu:
            if czas_sekundy < baza_poziomu[imie]:
                baza_poziomu[imie] = czas_sekundy
        else:
            baza_poziomu[imie] = czas_sekundy

        self.zapisz_ranking()

    def pobierz_posortowany_ranking(self, poziom):
        baza_poziomu = self.wyniki.get(poziom, {})
        return sorted(baza_poziomu.items(), key=lambda x: x[1])


class RankingOkno(QDialog):
    """Okno rankingu z zakładkami dla każdego poziomu trudności"""

    def __init__(self, manager, domyslny_poziom="Średni", parent=None):
        super().__init__(parent)
        self.manager = manager
        self.domyslny_poziom = domyslny_poziom
        self.setWindowTitle("Ranking Graczy - Sudoku")
        self.resize(700, 650)
        self.tabele_widzety = {}  # Słownik do przechowywania tabel dla odświeżania
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        self.setStyleSheet("background-color: rgb(248, 249, 250);")

        # Główny nagłówek - dopasowany do stylu nagłówka SUDOKU z głównego okna
        tytul = QLabel("RANKING")
        tytul.setAlignment(Qt.AlignCenter)
        tytul.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 65px;
            font-weight: 900;
            color: rgb(30, 41, 59);
            letter-spacing: 12px;
            margin-bottom: 25px;
        """)
        layout.addWidget(tytul)

        # Tworzymy panel z zakładkami
        self.zakladki = QTabWidget()
        self.zakladki.setStyleSheet("""
            QTabWidget { qproperty-elideMode: "ElideNone"; }
            QTabWidget::panel { 
                border: 1px solid rgb(226, 232, 240); 
                background: rgb(255, 255, 255); 
                border-radius: 15px; 
            }
            QTabBar::tab { 
                font-family: 'Segoe UI'; 
                font-size: 18px; 
                min-width: 120px; 
                height: 45px;
                padding: 0px 30px; 
                background: rgb(248, 249, 250); 
                color: rgb(100, 116, 139); 
                border: 1px solid rgb(226, 232, 240); 
                border-bottom: none; 
                border-top-left-radius: 8px; 
                border-top-right-radius: 8px; 
                margin-right: 6px;
            }
            QTabBar::tab:selected { 
                background: rgb(255, 255, 255); 
                color: rgb(30, 41, 59); 
                font-weight: bold; 
                border-top: 3px solid rgb(30, 41, 59); 
            }
            QTabBar::tab:hover {
                background-color: rgb(245, 245, 245);
            }
        """)

        # Poziomy, dla których tworzymy zakładki
        poziomy = ["Łatwy", "Średni", "Trudny"]

        for poziom in poziomy:
            widzet_karty = QWidget()
            karta_layout = QVBoxLayout(widzet_karty)
            karta_layout.setContentsMargins(15, 15, 15, 15)

            # Tworzymy tabelę dla danej zakładki
            tabela = QTableWidget()
            tabela.setColumnCount(3)
            tabela.setHorizontalHeaderLabels(["Miejsce", "Gracz", "Czas"])
            tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabela.horizontalHeader().setMinimumSectionSize(50)
            tabela.horizontalHeader().setDefaultSectionSize(50)

            tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tabela.setStyleSheet("""
                QTableWidget { 
                    font-family: 'Segoe UI'; 
                    font-size: 18px; 
                    background-color: rgb(255, 255, 255); 
                    border: none; 
                    color: rgb(51, 65, 85); 
                }
                QHeaderView::section { 
                    background-color: rgb(248, 249, 250); 
                    font-weight: bold; 
                    font-size: 18px;
                    padding: 12px; 
                    border: 1px solid rgb(226, 232, 240); 
                    color: rgb(51, 65, 85); 
                }
            """)

            karta_layout.addWidget(tabela)
            self.zakladki.addTab(widzet_karty, poziom)

            # Zapisujemy referencję do tabeli, żeby ją uzupełnić danymi
            self.tabele_widzety[poziom] = tabela

        layout.addWidget(self.zakladki)

        # Ładujemy dane do wszystkich tabel
        self.odswiez_wszystkie_tabele()

        # Ustawiamy aktywną zakładkę na ten poziom, na którym właśnie grano
        if self.domyslny_poziom in poziomy:
            indeks = poziomy.index(self.domyslny_poziom)
            self.zakladki.setCurrentIndex(indeks)

    def formatuj_czas(self, sekundy):
        minuty = sekundy // 60
        sek = sekundy % 60
        return f"{minuty:02d}:{sek:02d}"

    def odswiez_wszystkie_tabele(self):
        for poziom, tabela in self.tabele_widzety.items():
            wyniki_posortowane = self.manager.pobierz_posortowany_ranking(poziom)
            tabela.setRowCount(len(wyniki_posortowane))

            for index, (imie, czas) in enumerate(wyniki_posortowane):
                item_miejsce = QTableWidgetItem(f"#{index + 1}")
                item_gracz = QTableWidgetItem(imie)
                item_czas = QTableWidgetItem(self.formatuj_czas(czas))

                item_miejsce.setTextAlignment(Qt.AlignCenter)
                item_gracz.setTextAlignment(Qt.AlignCenter)
                item_czas.setTextAlignment(Qt.AlignCenter)

                tabela.setItem(index, 0, item_miejsce)
                tabela.setItem(index, 1, item_gracz)
                tabela.setItem(index, 2, item_czas)
            tabela.resizeRowsToContents()
