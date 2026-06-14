# aplikacja: SUDOKU


### Natalia Dańko 293183
### Maria Wołodko 293154
### Aleksander Wieczorek 293173
### Hanna Kordas 293160
### Bartosz Grabowiec 293166

Nasz projekt będzie polegał na stworzeniu gry Sudoku w języku Python. Chcemy, aby gotowy program był prosty w obsłudze, przejrzysty i jednocześnie wyglądał estetycznie. Gracz będzie mógł uruchomić nową grę, wpisywać liczby do planszy, sprawdzać poprawność swoich ruchów oraz zobaczyć czas, w jakim udało mu się ukończyć Sudoku. Planujemy przygotować kilka poziomów trudności, żeby gra nie była zbyt łatwa ani monotonna. Całość będzie działała w oknie z graficznym interfejsem, a nie tylko w konsoli, dzięki czemu korzystanie z aplikacji będzie wygodniejsze i bardziej atrakcyjne.
Wybraliśmy właśnie Sudoku, ponieważ jest to gra logiczna, którą zna większość osób, a jednocześnie daje dużo możliwości podczas programowania. Projekt wydaje nam się ciekawy, bo łączy elementy logiki, grafiki i pracy z danymi. Dodatkowo dobrze nadaje się do pracy w grupie, bo każdy może zająć się inną częścią programu, na przykład generowaniem planszy, interfejsem graficznym albo zapisywaniem wyników. Dzięki temu łatwiej będzie podzielić pracę i sprawnie rozwijać projekt.
Pracę planujemy rozłożyć etapami. Najpierw stworzymy podstawową wersję gry i mechanizm działania planszy Sudoku. Następnie zajmiemy się grafiką oraz obsługą użytkownika. Kolejnym krokiem będzie dodanie licznika czasu, sprawdzania poprawności wpisywanych liczb i możliwości zapisywania wyników. Na końcu skupimy się na poprawianiu błędów i dopracowaniu wyglądu programu, żeby całość działała płynnie i była przyjemna w użyciu.
Do wykonania projektu planujemy wykorzystać kilka bibliotek Pythona. Biblioteka pygame pomoże nam stworzyć interfejs graficzny oraz obsłużyć okno gry. numpy wykorzystamy do pracy z planszą Sudoku i przechowywania danych w tablicach. Moduł random będzie potrzebny do losowania plansz, a sys i time przydadzą się do działania programu oraz mierzenia czasu gry. Wyniki chcemy zapisywać w plikach tekstowych lub w formacie JSON. Dzięki tym bibliotekom stworzenie funkcjonalnej gry będzie łatwiejsze i bardziej uporządkowane.

## Faza 2

### Podsumowanie pracy nad prototypem
W drugiej fazie projektu pracę rozpoczęliśmy od zaimplementowania logiki generowania planszy Sudoku oraz sprawdzania jej poprawności (plik generator.py). Następnie skupiliśmy się na przekształceniu tej logiki w w pełni grywalną aplikację. Wykorzystując bibliotekę PyQt5, stworzyliśmy okienkowy interfejs użytkownika z nowym Menu Głównym (rejestracja gracza i wybór poziomu trudności). Plansza zyskała płynną nawigację (mysz, WSAD, strzałki) oraz mechaniki rozgrywki: system notatek, interaktywny stoper i system żyć.

Ważnym krokiem była weryfikacja poprawności wpisywanych cyfr w czasie rzeczywistym, blokowanie odgadniętych pól oraz automatyczne wykrywanie wygranej lub przegranej. Dodatkowo zintegrowaliśmy działający system rankingu zapisujący wyniki do pliku (ranking.json). Opracowaliśmy wstępny diagram UML (klasy_uml) i przeprowadziliśmy przebudowę kodu, dzieląc go na moduły (main.py, generator.py, okno_gry.py, Ranking_czasów.py). Całość scaliliśmy w repozytorium Git z wyizolowanym środowiskiem (.venv) i plikiem .gitignore.

### Plany na Fazę 3
W trzeciej, finałowej fazie projektu skoncentrujemy się na wielojęzyczności, ułatwieniach dla gracza oraz testowaniu aplikacji. Wprowadzimy opcje językowe, umożliwiające swobodne przełączanie gry między językiem polskim, angielskim i ukraińskim. Aby ułatwić rozgrywkę, zaimplementujemy system „podpowiedzi”, który w trudnych momentach wskaże graczowi właściwą cyfrę w wybranym polu.

Zadbamy o pełną dokumentację techniczną, aktualizując diagram UML o nowo powstałe relacje między klasami. Stworzymy kompleksowy zestaw testów: klasyczne testy jednostkowe do weryfikacji algorytmów (np. generatora planszy) oraz testy typu Mock, symulujące bardziej złożone operacje, takie jak zapis rankingu do pliku czy interakcje z GUI. Całość zwieńczymy ogólnym dopracowaniem kodu, wyłapywaniem i naprawianiem błędów, co zapewni płynność i stabilność finalnej wersji gry.




## Instrukcja uruchomienia gry 
### 1. Wymagania 
Przed uruchomieniem projektu należy zainstalować: 
- Python 3.13
- Git
- Visual Studio Code lub inny edytor kodu — opcjonalnie

Sudoku korzysta z bibliotek **PyQt5** oraz **pygame**, dlatego zalecamy użycie **Pythona 3.13**.

Aby sprawdzić, czy Python jest zainstalowany, wpisz w terminalu: 

**Windows** 
```bash
py --version
```
**macOS** 
```bash
python3.13 --version
```
**Linux** 
```bash
python3.13 --version
```
Aby sprawdzić, czy Git jest zainstalowany: 
```bash
git --version
```
### 2. Pobranie projektu z GitHuba 

Otwórz terminal i wpisz: 
```bash
git clone https://github.com/Maria6029/aplikacja.git
```
Następnie wejdź do folderu projektu: 
```bash
cd aplikacja 
```
### 3. Utworzenie środowiska wirtualnego 
**Windows** 
```bash 
py -3.13 -m venv .venv
```
Aktywacja środowiska:
```bash
.\.venv\Scripts\activate
```
**macOS** 
```bash 
python3.13 -m venv .venv
```
Aktywacja środowiska:
```bash
source .venv/bin/activate
```
**Linux** 
```bash 
python3.13 -m venv .venv
```
Aktywacja środowiska: 
```bash 
source .venv/bin/activate
```
Po aktywacji środowiska w terminalu powinna pojawić się nazwa `.venv`. 
### 4. Instalacja wymaganych bibliotek 
W aktywnym środowisku wirtualnym wpisz: 
```bash 
python -m pip install PyQt5 PyQt5-sip pygame
```
 ### 5. Uruchomienie gry Aby uruchomić grę, wpisz: 
 ```bash 
 python main.py
```
### Najczęstsze problemy #### 
Problem z aktywacją środowiska wirtualnego na Windowsie 
Jeśli pojawi się problem z aktywacją środowiska wirtualnego, należy wpisać w PowerShell: 
```bash 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Jeśli system zapyta o potwierdzenie, wpisz `Y` lub `T` i naciśnij Enter. Następnie ponownie aktywuj środowisko: 
```bash
.\.venv\Scripts\activate
```
### Opcjonalnie: otwarcie projektu w Visual Studio Code
Aby otworzyć projekt w Visual Studio Code: 
1. Uruchom Visual Studio Code.
2. Wybierz **File**, a później **Open Folder**.
3. Wskaż folder **aplikacja**.
4. Otwórz terminal: **Terminal**, a później **New Terminal**.
5. Wykonaj komendy z instrukcji, czyli aktywuj środowisko, zainstaluj biblioteki i uruchom grę:
```bash
python main.py
```

## Instrukcja użytkowania
Zacznij od uruchomienia gry, tak jak zostało to przedstawione w poprzednim kroku. Zobaczysz interfejs z okienkiem na twoje imię, a także poziomem trudności do wyboru, zdecyduj jaki poziom trudności tobie odpowiada, łatwy, średni czy trudny. Kliknij start i odpal planszę.

Gra polega na uzupełnianiu siatki cyframi od 1 do 9. Aby poprawnie ją wypełnić kieruj się tymi zasadami:

W każdym rzędzie muszą znaleźć się cyfry od 1 do 9. Żadna cyfra nie może się powtórzyć – jeśli w rzędzie jest już np. 4, to druga czwórka w tym samym rzędzie jest błędem.

Dokładnie to samo dotyczy pionu. W każdej z 9 pionowych kolumn muszą wystąpić cyfry od 1 do 9, każda dokładnie jeden raz.

Cała plansza jest podzielona liniami na 9 mniejszych kwadratów o wymiarach 3×3 pola. Wewnątrz każdego takiego małego kwadratu również muszą znaleźć się wszystkie cyfry od 1 do 9, bez powtórzeń.

Podczas wpisywania musisz uważać, bo masz limit maksymalnie dwóch błędów. Trzecia pomyłka oznacza automatyczną przegraną i koniec zabawy. W trakcie gry masz opcję notatek. Możesz zaznaczyć okienko po lewej stronie planszy, a twoje cyfry wpiszą się "na brudno", jako małe cyfry w rogach okienek, co ułatwi ci grę.

Gdy uda Ci się poprawnie zapełnić ostatnie wolne pole, gra się zakończy. Zobaczysz swój końcowy czas w okienku z rankingiem, gdzie możesz porównać wynik z osiągnięciami innych graczy.

Jeżeli w jakimkolwiek momencie chcesz zakończyć rozgrywkę, możesz kliknąć krzyżyk w prawym górnym rogu, lub przycisk „Zakończ grę”.




  
 	













  
 	
