import copy
import random
import pygame
class Board:
    def isSolved(self):
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
    def boardToCode(self, input_board=None): # turn a pre-existing board into a code
        if input_board:
            _code = ''.join([str(i) for j in input_board for i in j])
            return _code
        else:
            self.code = ''.join([str(i) for j in self.board for i in j])
            return self.code
    def findSpaces(self): # finds the first empty space in the board, which is represented by a 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return (row, col)

        return False


    def checkSpace(self, num, space):  # checks to see if a number can be fitted into a specifc space; row, col
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


    def solve(self):  # solves a board using recursion
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
    def solveForCode(self): # solves a board and returns the code of the solved board
        return self.boardToCode(self.solve())

    def __generateRandomCompleteBoard(self):  # generates a brand new completely random board full of numbers
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
    def __generateCont(self): # uses recursion to finish generating a random board
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

    def __solveToFindNumberOfSolutions(self, row,
                                        col):  # solves the board using recursion, is used within the findNumberOfSolutions method
        for n in range(1, 10):
            if self.checkSpace(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False
    def __findSpacesToFindNumberOfSolutions(self, board, h): # finds the first empty space it comes across, is used within the findNumberOfSolutions method
        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == h:
                        return (row, col)

                    _k += 1

        return False


    def findNumberOfSolutions(self):  # finds the number of solutions to a board and returns the list of solutions
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
                                difficulty):  # generates a question board with a certain number of cells removed depending on the chosen difficulty
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
    def generateQuestionBoardCode(self, difficulty): # generates a new random board and its board code depending on the difficulty
        self.board, _solution_board = self.generateQuestionBoard(self.__generateRandomCompleteBoard(), difficulty)
        return self.boardToCode(), self.boardToCode(_solution_board)
    def printBoard(self):
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
WIDTH = 540
HEIGHT = 540
CELL_SIZE = WIDTH // 9

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
font = pygame.font.SysFont(None, 40)
won = False
running = True
selected = None
while running:
    errors = board.getErrors()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            selected = (row, col)

        elif event.type == pygame.KEYDOWN and selected:
            row, col = selected

            if (row, col) not in fixed_cells:

                if pygame.K_1 <= event.key <= pygame.K_9:
                    board.board[row][col] = event.key - pygame.K_0

                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_0):
                    board.board[row][col] = 0
    if not won and board.isSolved():
        won = True
    screen.fill(WHITE)
    if selected:
        row, col = selected

        pygame.draw.rect(
            screen,
            BLUE,
            (
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
        )
    # liczby
    for row in range(9):
        for col in range(9):
            value = board.board[row][col]

            if value != 0:
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2

                if (row, col) in errors:
                    color = (220, 50, 50)  # czerwony = błąd
                else:
                    color = BLACK

                text = font.render(str(value), True, color)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)

    # linie siatki
    for i in range(10):
        width = 3 if i % 3 == 0 else 1

        pygame.draw.line(screen, BLACK,
                         (0, i * CELL_SIZE),
                         (WIDTH, i * CELL_SIZE), width)

        pygame.draw.line(screen, BLACK,
                         (i * CELL_SIZE, 0),
                         (i * CELL_SIZE, HEIGHT), width)

    # WIN overlay
    if won:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        win_text = font.render("YOU WIN!", True, (0, 255, 0))
        text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(win_text, text_rect)
    pygame.display.flip()
pygame.quit()
if __name__ == "__main__":
    board = Board()
    board.generateQuestionBoardCode(1)






