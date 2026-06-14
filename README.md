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

### Faza 2

W drugiej fazie projektu skupimy się na przekształceniu podstawowej wersji gry w pełni stabilną, zaawansowaną i dopracowaną aplikację, koncentrując działania na rozbudowie interfejsu, kontroli jakości oraz finalnej integracji kodu. Ponieważ nasz program posiada już działającą funkcję notatek, w tym etapie skupimy się na podniesieniu czytelności i przejrzystości gry poprzez dodanie specjalnego opisu po boku ekranu, który w prosty sposób wyjaśni graczowi zasadę działania tego mechanizmu podczas rozgrywki. Ważnym krokiem w rozwoju interfejsu użytkownika będzie również wprowadzenie opcji językowych, dzięki czemu gracz będzie mógł swobodnie przełączać aplikację między językiem polskim, angielskim oraz ukraińskim. Dodatkowo, aby ułatwić rozgrywkę, zaimplementujemy opcję podpowiedzi, która w trakcie gry będzie mogła wskazać właściwą cyfrę. Będziemy także udoskonalać diagram UML, co pozwoli dokładniej odwzorować relacje między klasami, grafiką a strukturą danych po wprowadzeniu wszystkich nowych funkcjonalności. Aby zagwarantować niezawodność aplikacji, stworzymy kompleksowy zestaw testów, wykorzystamy tradycyjne testy funkcji do bezpośredniego zweryfikowania poprawności działania algorytmów, a także testy typu Mock, które pozwolą nam zasymulować zachowanie trudniejszych komponentów, takich jak operacje zapisu na dysku czy interakcje z interfejsem graficznym. Pozwoli to na sprawną identyfikację i poprawę wszelkich niedoskonałości programu, optymalizację płynności działania okna gry oraz eliminację błędów, takich jak niepoprawna obsługa znaków czy problemy z zapisem bazy danych. Na koniec przeprowadzimy końcowe połączenie wszystkich kodów w repozytorium Git, rozwiązując ewentualne konflikty powstałe podczas pracy w grupie, co pozwoli scalić grafikę, logikę oraz system rankingowy w jedną, spójną i poprawnie działającą całość.





## Instrukcja uruchomienia gry
### 1. Wymagania
Przed uruchomieniem projektu należy zainstalować:
-	Python 3.13
-	Git
-	Visual Studio Code lub inny edytor kodu
Sudoku korzysta z bibliotek PyQt5 oraz pygame, dlatego zalecamy użycie Pythona 3.13.
Aby sprawdzić, czy Python jest zainstalowany, wpisz w terminalu:
**Windows**
 	``bash
 	py --version
 	``
**macOS**
 	``bash
 	python3 --version
 	``
 	Aby sprawdzić, czy Git jest zainstalowany:
 	``bash
 	git --version
 	``
 	### 2. Pobranie projektu z GitHuba
 	Otwórz terminal i wpisz:
 	``bash
 	git clone https://github.com/Maria6029/aplikacja.git
 	``
 	Następnie wejdź do folderu projektu:
 	``bash
 	cd aplikacja
 	``
 	### 3. Utworzenie środowiska wirtualnego
 	**Windows**
 	``bash
 	py -3.13 -m venv .venv
 	``
 	Aktywacja środowiska:
 	``bash
 	.venv\Scripts\activate
 	``
 	**macOS**
 	``bash
 	python3.13 -m venv .venv
 	``
 	Aktywacja środowiska:
 	``bash
 	source .venv/bin/activate
 	``
 	Po aktywacji środowiska w terminalu powinna pojawić się nazwa .venv.
 	### 4. Instalacja wymaganyc bibliotek
 	``bash
 	python -m pip install PyQt5 PyQt5-sip pygame
 	``
 	### 5. Uruchomienie gry
 	``bash
 	python main.py
 	``






  
 	













  
 	
