import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Importujemy główne okno z Twojego pliku z interfejsem
# UWAGA: Jeśli Twój plik nazywa się inaczej niż 'gui.py', 
# zmień słowo 'gui' poniżej na nazwę Twojego pliku (bez .py)
from okno_gry import GlowneOkno 

def main():
    if sys.platform.startswith("win"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    aplikacja = QApplication(sys.argv)
    
    # Tworzymy i pokazujemy okno
    glowne_okno = GlowneOkno()
    glowne_okno.show()
    
    # Uruchamiamy główną pętlę programu
    sys.exit(aplikacja.exec())

if __name__ == "__main__":
    main()

