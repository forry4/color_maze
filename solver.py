# init_maze = [
#     [1, 1, 1, 1, 1, 1, 1, 1],
#     [1, 1, 0, 0, 0, 0, 1, 1],
#     [1, 0, 0, 1, 0, 0, 0, 1],
#     [1, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 1, 0, 1],
#     [1, 1, 1, 1, 1, 1, 1, 1]
# ]

init_maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


def is_solvable(row: int, column: int, maze: list[list], visited: set[str], uncolored_count: int) -> tuple[bool, int]:
    if uncolored_count == 0:
        return True, 0
    key = f'{row},{column}'
    visited.add(key)
    for direction in ['left', 'right', 'up', 'down']:
        uncolored_count, new_row, new_column = traverse(row, column, maze, direction, uncolored_count)
        if uncolored_count == 0:
            return True, 0
        new_key = f'{new_row},{new_column}'
        if new_key not in visited:
            solvable, uncolored_count = is_solvable(new_row, new_column, maze, visited, uncolored_count)
            if solvable:
                return True, uncolored_count
    return False, uncolored_count


def traverse(row, column, maze, direction, uncolored_count):
    moves = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
    dr, dc = moves[direction]
    while maze[row + dr][column + dc] != 1:
        row, column = row + dr, column + dc
        uncolored_count -= color_check(row, column, maze)
    return uncolored_count, row, column


def color_check(row: int, column: int, maze: list[list]) -> int:
    if maze[row][column] != -2:
        maze[row][column] = -2
        return 1
    return 0

# print(is_solvable(4, 1, init_maze, set(), sum(row.count(0) for row in init_maze))[0])

# python
from collections import deque

def min_moves_to_cover(maze: list[list[int]], start_row: int, start_col: int) -> int:
    # map each zero cell to a bit index
    zero_index: dict[tuple[int,int], int] = {}
    idx = 0
    for r, row in enumerate(maze):
        for c, v in enumerate(row):
            if v == 0:
                zero_index[(r, c)] = idx
                idx += 1
    if idx == 0:
        return 0  # nothing to cover

    target_mask = (1 << idx) - 1
    start_mask = 0
    if (start_row, start_col) in zero_index:
        start_mask |= 1 << zero_index[(start_row, start_col)]

    # BFS over (row, col, mask)
    dq = deque()
    dq.append((start_row, start_col, start_mask, 0))
    seen = {(start_row, start_col, start_mask)}

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    while dq:
        r, c, mask, dist = dq.popleft()
        if mask == target_mask:
            return dist
        for dr, dc in moves:
            nr, nc = r, c
            visited_mask = mask
            moved = False
            # slide until next cell would be a wall (value 1)
            while maze[nr + dr][nc + dc] != 1:
                nr += dr
                nc += dc
                moved = True
                if (nr, nc) in zero_index:
                    visited_mask |= 1 << zero_index[(nr, nc)]
            if not moved:
                continue  # can't move in that direction
            state = (nr, nc, visited_mask)
            if state in seen:
                continue
            seen.add(state)
            dq.append((nr, nc, visited_mask, dist + 1))
    return -1

print(min_moves_to_cover(init_maze, 7, 1))  # Example usage

import sys
import re
from pathlib import Path

def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text()
    return sys.stdin.read()

def to_12x12(text: str):
    tokens = re.findall(r'[.ox]', text)
    mapped = [1 if t == '.' else 0 for t in tokens]
    expected = 12 * 12
    if len(mapped) != expected:
        raise ValueError(f'expected {expected} tokens for a 12x12 grid, found {len(mapped)}')
    cols = 12
    maze = [mapped[i:i+cols] for i in range(0, len(mapped), cols)]
    return maze

def pretty_print(maze):
    print("init_maze = [")
    for row in maze:
        print("    " + str(row) + ",")
    print("]")

if __name__ == "__main__":
    init_text = '.	.	.	.	.	.	.	.	.	.	.	. .	o	o	o	o	o	o	o	.	o	o	. .	o	o	o	.	o	o	o	o	o	o	. .	.	o	o	o	o	o	o	o	.	o	. .	o	o	o	o	.	o	o	o	o	o	. .	o	o	o	o	o	o	.	o	o	o	. .	o	o	.	o	o	o	o	o	o	o	. .	.	o	o	o	o	o	o	o	o	o	. .	o	o	o	o	o	o	o	o	o	.	. .	o	o	o	o	.	o	o	o	o	o	. .	x	.	o	o	o	o	o	.	o	o	. .	.	.	.	.	.	.	.	.	.	.	.'
    init_maze = to_12x12(init_text)
    pretty_print(init_maze)
