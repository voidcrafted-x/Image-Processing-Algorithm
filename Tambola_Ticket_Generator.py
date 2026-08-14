import random


def generate_ticket():
    ROWS = 3
    COLS = 9

    # Number ranges for each column
    ranges = [
        range(1, 10),
        range(10, 20),
        range(20, 30),
        range(30, 40),
        range(40, 50),
        range(50, 60),
        range(60, 70),
        range(70, 80),
        range(80, 91)
    ]

    # ------------------------------------------------
    # Step 1: Generate valid row/column arrangement
    # ------------------------------------------------

    # 0 = empty, 1 = number
    layout = [[0] * COLS for _ in range(ROWS)]

    # Each row must contain exactly 5 numbers
    row_count = [0] * ROWS

    # Each column must contain at least 1 number
    col_count = [0] * COLS

    def fill(position):
        # All 27 cells filled
        if position == ROWS * COLS:
            return (
                all(count == 5 for count in row_count)
                and all(count >= 1 for count in col_count)
            )

        row = position // COLS
        col = position % COLS

        # Randomize whether we place a number
        choices = [0, 1]
        random.shuffle(choices)

        for value in choices:

            # Don't exceed 5 numbers in a row
            if value == 1 and row_count[row] >= 5:
                continue

            # Don't allow more than 3 numbers in a column
            if value == 1 and col_count[col] >= 3:
                continue

            # Don't leave too few cells for remaining numbers
            remaining_cells = COLS - col - 1

            if value == 1:
                row_count[row] += 1
                col_count[col] += 1

            layout[row][col] = value

            if fill(position + 1):
                return True

            layout[row][col] = 0

            if value == 1:
                row_count[row] -= 1
                col_count[col] -= 1

        return False

    fill(0)

    # ------------------------------------------------
    # Step 2: Put random numbers into each column
    # ------------------------------------------------

    ticket = [[None] * COLS for _ in range(ROWS)]

    for col in range(COLS):

        # Find rows that need a number in this column
        rows = [
            row for row in range(ROWS)
            if layout[row][col] == 1
        ]

        # Generate unique numbers for this column
        numbers = random.sample(
            list(ranges[col]),
            len(rows)
        )

        # Sort numbers from top to bottom
        numbers.sort()

        for row, number in zip(rows, numbers):
            ticket[row][col] = number

    return ticket


def print_ticket(ticket):

    print("+----" * 9 + "+")

    for row in ticket:

        print("|", end="")

        for number in row:

            if number is None:
                print("    |", end="")
            else:
                print(f" {number:2d} |", end="")

        print()
        print("+----" * 9 + "+")


# Generate ticket
ticket = generate_ticket()

# Display ticket
print_ticket(ticket)