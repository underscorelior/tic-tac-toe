# Constants
GRID_SIZE: int = 3  # Does not support values other than 3, don't care.
PLAYER_1: str = "X"
PLAYER_2: str = "O"
EMPTY: str = "-"

type grid_type = list[list[str]]


class Board:
    def __init__(self) -> None:
        self.grid: grid_type = self.setup_grid()
        self.current_player: int = 1
        self.over: bool = False

    def __str__(self) -> str:
        board: str = ""

        for i in self.grid:
            board += "-" * (3 * GRID_SIZE + 4) + "\n"
            board += "| " + " | ".join(i) + " |" + "\n"
        board += "-" * (3 * GRID_SIZE + 4)

        return board

    def setup_grid(self) -> list[list[str]]:
        grid: grid_type = []

        for i in range(GRID_SIZE):
            grid.insert(i, [])
            for j in range(GRID_SIZE):
                grid[i].insert(j, EMPTY)

        return grid

    def make_move(self, idx: int) -> str | bool:
        if not self.place(idx):
            return "Error, unable to place at index!"
        else:
            end = self.is_end()
            if not end:
                if self.current_player == 1:
                    self.current_player = 2
                else:
                    self.current_player = 1
                return True
            else:
                return end

    def is_end(self) -> str | bool:
        if self.is_full():
            self.over = True
            return "Tie! Board is full."
        elif self.check_for_win():
            self.over = True
            return f"{self.current_player} won!"

        return False

    def is_valid(self, idx: int) -> bool:
        return idx >= 0 and idx <= GRID_SIZE**2 - 1

    def is_occupied(self, idx: int) -> bool:
        return self.grid[idx // GRID_SIZE][idx % GRID_SIZE] is not EMPTY

    def is_full(self) -> bool:
        for i in range(GRID_SIZE**2):
            if not self.is_occupied(i):
                return False
        return True

    def place(self, idx: int) -> bool:
        if self.current_player == 1:
            self.grid[idx // GRID_SIZE][idx % GRID_SIZE] = PLAYER_1
        elif self.current_player == 2:
            self.grid[idx // GRID_SIZE][idx % GRID_SIZE] = PLAYER_2
        else:
            return False

        return True

    def check_for_win(self) -> bool:
        grid = self.grid

        for i in range(GRID_SIZE):
            if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i] is not EMPTY:
                return True

            if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0] is not EMPTY:
                return True

        if grid[1][1] is not EMPTY:
            if (
                grid[0][0] == grid[1][1] == grid[2][2]
                or grid[0][2] == grid[1][1] == grid[2][0]
            ):
                return True

        return False


board: Board = Board()

board.setup_grid()

while not board.over:
    print(board)

    ipt: str = input(f"Your turn, Player {board.current_player} (1-{GRID_SIZE**2}): ")
    ipt_valid: bool = False

    while not ipt_valid:
        if not ipt:
            print("Invalid input, input cannot be empty!")
        elif not ipt.isnumeric():
            print("Invalid input, input cannot contain non numbers!")
        elif not board.is_valid(int(ipt) - 1):
            print(f"Invalid input, input is out of range (1-{GRID_SIZE**2})!")
        elif board.is_occupied(int(ipt) - 1):
            print("Error, location is occupied!")
        else:
            ipt_valid = True
            out: str | bool = board.make_move(int(ipt) - 1)
            if not isinstance(out, bool) and not board.over:
                print(out)
            elif board.over:
                print(f"\n\n{out}")
                break
            else:
                print("\n")
                break

        ipt = input(f"Try again, Player {board.current_player}: ")

print(board)
