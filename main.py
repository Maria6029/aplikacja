import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

# Importujemy zintegrowane i spolszczone główne okno z interfejsem gry
from okno_gry import GlowneOkno


def main():
    # Globalne włączenie skalowania High DPI dla wszystkich systemów operacyjnych.
    # Zapobiega to ucinaniu okien lub ich "gigantycznym" rozmiarom na ekranach Mac/Huawei.
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    aplikacja = QApplication(sys.argv)

    # Tworzymy i wyświetlamy główne okno gry Sudoku
    glowne_okno = GlowneOkno()
    glowne_okno.show()
    QTimer.singleShot(0, glowne_okno.wycentruj_okno)

    # Uruchamiamy główną pętlę programu (zgodną ze standardem PyQt5)
    sys.exit(aplikacja.exec_())


if __name__ == "__main__":
    main()
