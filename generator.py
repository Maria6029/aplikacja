import copy
import random
class Board:
    def isSolved(self):
         """Sprawdza, czy plansza Sudoku jest rozwiązana.
        Zwraca True, jeśli nie ma pustych pól ani błędów.
        """
        # brak pustych pól
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False

        # brak błędów
        if len(self.getErrors()) > 0:
            return False

        return True
    def getErrors(self):
        """Sprawdza całą planszę i zwraca zbiór pól,
        w których wpisane liczby są niezgodne z zasadami Sudoku.
        """
        errors = set()

        for row in range(9):
            for col in range(9):
                num = self.board[row][col]

                if num == 0:
                    continue

                # tymczasowo usuwamy liczbę
                self.board[row][col] = 0

                if not self.checkSpace(num, (row, col)):
                    errors.add((row, col))

                # przywracamy
                self.board[row][col] = num

        return errors
    def __init__(self, code=None):
        """Tworzy nowy obiekt planszy Sudoku.
        Jeśli podano kod planszy, wczytuje go do tablicy 9x9.
        """
        self.__resetBoard()

        if code:
            self.code = code

            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(code[0])
                    code = code[1:]
        else:
            self.code = None

    def __resetBoard(self):
        """Resetuje planszę Sudoku, ustawiając wszystkie pola na 0.
        Zero oznacza puste pole."""
        self.board = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
        ]
        return self.board
    def boardToCode(self, input_board=None): 
         """Zamienia planszę Sudoku na jeden ciąg znaków.
        Jeśli podano planszę jako argument, zamienia ją na kod.
        W przeciwnym razie zamienia aktualną planszę.
        """
        if input_board:
            _code = ''.join([str(i) for j in input_board for i in j])
            return _code
        else:
            self.code = ''.join([str(i) for j in self.board for i in j])
            return self.code
    def findSpaces(self): 
        """Szuka pierwszego pustego pola na planszy.
        Puste pole jest oznaczone liczbą 0.
        """
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

        return False


    def checkSpace(self, num, space): 
        """Sprawdza, czy daną liczbę można wpisać w wybrane pole.
        Kontroluje wiersz, kolumnę oraz kwadrat 3x3.
        """
        if not self.board[space[0]][space[1]] == 0:  # check to see if space is a number already
            return False

        for col in self.board[space[0]]:  # check to see if number is already in row
            if col == num:
                return False

        for row in range(len(self.board)):  # check to see if number is already in column
            if self.board[row][space[1]] == num:
                return False

        _internalBoxRow = space[0] // 3
        _internalBoxCol = space[1] // 3

        for i in range(3):  # check to see if internal box already has number
            for j in range(3):
                if self.board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
                    return False

        return True


    def solve(self): 
         """
        Rozwiązuje planszę Sudoku metodą rekurencji i cofania.
        Zwraca rozwiązaną planszę albo False, jeśli nie da się jej rozwiązać.
        """
        _spacesAvailable = self.findSpaces()

        if not _spacesAvailable:
            return True
        else:
            row, col = _spacesAvailable

        for n in range(1, 10):
            if self.checkSpace(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False
    def solveForCode(self): 
        """Rozwiązuje planszę Sudoku i zwraca rozwiązanie jako ciąg znaków.
        """
        return self.boardToCode(self.solve())

    def __generateRandomCompleteBoard(self):  
        """Generuje nową, kompletną i poprawnie uzupełnioną planszę Sudoku.
        Najpierw losowo wypełnia trzy kwadraty 3x3, a potem uzupełnia resztę.
        """
        self.__resetBoard()

        _l = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        return self.__generateCont()
    def __generateCont(self): 
         """Kontynuuje generowanie pełnej planszy Sudoku.
        Uzupełnia puste pola losowymi liczbami zgodnymi z zasadami gry.
        """
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _num = random.randint(1, 9)

                    if self.checkSpace(_num, (row, col)):
                        self.board[row][col] = _num

                        if self.solve():
                            self.__generateCont()
                            return self.board

                        self.board[row][col] = 0

        return False

    def __solveToFindNumberOfSolutions(self, row, col):  
     """Pomocniczo rozwiązuje planszę od wskazanego pola.
        Funkcja jest używana podczas sprawdzania liczby możliwych rozwiązań.
        """
        for n in range(1, 10):
            if self.checkSpace(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False
    def __findSpacesToFindNumberOfSolutions(self, board, h): # finds the first empty space it comes across, is used within the findNumberOfSolutions method
         """Znajduje h-te puste pole na planszy.
        Funkcja pomocnicza używana przy sprawdzaniu liczby rozwiązań.
        """
        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == h:
                        return (row, col)

                    _k += 1

        return False


    def findNumberOfSolutions(self):  # finds the number of solutions to a board and returns the list of solutions
        """Szuka możliwych rozwiązań aktualnej planszy.
        Zwraca listę unikalnych rozwiązań zapisanych jako kody tekstowe.
        """
        
        _z = 0
        _list_of_solutions = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _z += 1

        for i in range(1, _z + 1):
            _board_copy = copy.deepcopy(self)

            _row, _col = self.__findSpacesToFindNumberOfSolutions(_board_copy.board, i)
            _board_copy_solution = _board_copy.__solveToFindNumberOfSolutions(_row, _col)

            _list_of_solutions.append(self.boardToCode(input_board=_board_copy_solution))

        return list(set(_list_of_solutions))

    def generateQuestionBoard(self, fullBoard,
                                difficulty): 
       """Tworzy planszę do gry na podstawie pełnej rozwiązanej planszy.
        Usuwa określoną liczbę pól w zależności od poziomu trudności.
        """ 
        self.board = copy.deepcopy(fullBoard)

        if difficulty == 0:
            _squares_to_remove = 36
        elif difficulty == 1:
            _squares_to_remove = 46
        elif difficulty == 2:
            _squares_to_remove = 52
        else:
            return

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(0, 2)
            _rCol = random.randint(0, 2)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(3, 5)
            _rCol = random.randint(3, 5)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(6, 8)
            _rCol = random.randint(6, 8)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _squares_to_remove -= 12
        _counter = 0
        while _counter < _squares_to_remove:
            _row = random.randint(0, 8)
            _col = random.randint(0, 8)

            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0

                if len(self.findNumberOfSolutions()) != 1:
                    self.board[_row][_col] = n
                    continue

                _counter += 1

        return self.board, fullBoard
    def generateQuestionBoardCode(self, difficulty): 
        """Generuje nową planszę Sudoku do gry oraz jej rozwiązanie.
        Zwraca oba elementy jako kody tekstowe.
        """
        self.board, _solution_board = self.generateQuestionBoard(self.__generateRandomCompleteBoard(), difficulty)
        return self.boardToCode(), self.boardToCode(_solution_board)
    def printBoard(self):
        """Wypisuje aktualną planszę Sudoku w konsoli.
        Każdy wiersz planszy jest drukowany osobno.
        """
        for i in range(9):
            row = ""
            for j in range(9):
                val = self.board[i][j]
                row += str(val) + " "
            print(row)
if __name__ == "__main__":
    board = Board()

    question_board_code = board.generateQuestionBoardCode(0)


    print("CODE (string):")
    print(question_board_code[0])

    print("\nBOARD (2D):")
    board.printBoard()
    fixed_cells = set()

    for row in range(9):
        for col in range(9):
            if board.board[row][col] != 0:
                fixed_cells.add((row, col))









