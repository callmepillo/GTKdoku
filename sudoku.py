# Python file to generate a random sudoku table

import random
import time

def row_is_valid(table: list[int], num: int) -> tuple[bool, str, int, int]:
    # check row
    row = num // 9
    for i in range(9):
        if row * 9 + i == num:
            continue
        if table[num] == table[row * 9 + i]:
            return False, "Row", num, row * 9 + i
    return True, "", 0, 0

def col_is_valid(table: list[int], num: int) -> tuple[bool, str, int, int]:
    # check column
    col = num % 9
    for i in range(9):
        if col + i * 9 == num:
            continue
        if table[num] == table[i * 9 + col]:
            return False, "Col", num, i * 9 + col
    return True, "", 0, 0

def sq_is_valid(table: list[int], num: int) -> tuple[bool, str, int, int]:
    # check square
    square_x = (num // 3) % 3
    square_y = num // 27
    for i in range(3):
        for j in range(3):
            coord = square_y * 27 + square_x * 3 + j + i * 9
            if coord == num:
                continue
            if table[num] == table[coord]:
                return False, "Sq", num, coord
    return True, "", 0, 0

# check if a move is valid
def is_valid(table: list[int], num: int) -> tuple[bool, str, int, int]:
    if table[num] == 0:
        return True, "", 0, 0
    val, info, a, b = row_is_valid(table, num)
    if not val:
        return val, info, a, b
    val, info, a, b = col_is_valid(table, num)
    if not val:
        return val, info, a, b
    val, info, a, b = sq_is_valid(table, num)
    return val, info, a, b

# make a complete sudoku
def get_sudoku(seed: int = None) -> list[int]:
    if seed is not None:
        random.seed(seed)

    table = [0] * 81

    # Fill diagonal 3x3 squares first — independent, helps speed up generation
    for k in range(3):
        used = set()
        for i in range(3):
            for j in range(3):
                coord = (k * 3) + j + (i + k * 3) * 9
                n = random.randint(1, 9)
                while n in used:
                    n = (n % 9) + 1
                table[coord] = n
                used.add(n)

    if not solve(table):
        raise ValueError("Failed to generate a complete Sudoku")

    return table

# this function solves a table, but also contributes to making a complete sudoku (by solving a table with only the three diagonal squares filled)
def solve(table: list[int]) -> bool:
    for i in range(81):
        if table[i] == 0:
            n = list(range(1,10))
            random.shuffle(n)
            for num in n:
                table[i] = num
                val,_,_,_ = is_valid(table, i)
                if val and solve(table):
                    return True
                table[i] = 0
            return False
    return True

# this function randomly replaces the values of a table with 0
def shadow_elements(table: list[int], num: int, seed: int = None) -> list[int]:
    if seed is not None:
        random.seed(seed)

    tb = table.copy()
    for i in range(num):
        k = random.randint(0, 80)
        while tb[k] == 0:
            k = random.randint(0, 80)
        tb[k] = 0
    return tb

def print_table(table: list[int]):
    for i in range(9):
        for j in range(3):
            print(table[i*9 + j*3 : i*9 + j*3 + 3], end='')
        print()
        if i%3 == 2:
            print("---------------------------")

# check if the whole table is valid
def all_is_valid(table: list[int]):
    for i in range(81):
        if table[i] == 0:
            return False
        val, mot, a, b = is_valid(table, i)
        if not val:
            print(mot, a, b)
            return False
    return True