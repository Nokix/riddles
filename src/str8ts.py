from typing import List, Dict, Tuple, Mapping

Position = Tuple[int, int]


class Str8ts:
    def __init__(self, x_size: int = 9, y_size: int = 9):
        self.x_size: int = x_size
        self.y_size: int = y_size
        self.board_numbers: Dict[Position, int] = {(i, j): None for i in range(self.x_size) for j in
                                                   range(self.y_size)}
        self.board_blocks: List[Position] = list()
        self.possilities_per_field: List[int] = list(range(1, max(x_size, y_size) + 1))

    def insert_fields(self, inputs: Dict[Position, int] = dict(),
                      blocks: List[Tuple[int, int]] = list()) -> None:
        for k, v in inputs.items():
            self.board_numbers[k] = v
        self.board_blocks.extend(blocks)

    def get_whole_x_line(self, pos: Position) -> List[Position]:
        x, y = pos
        return [(x, i) for i in range(self.y_size) if (x, i) not in self.board_blocks]

    def get_whole_y_line(self, pos: Position) -> List[Position]:
        x, y = pos
        return [(i, y) for i in range(self.x_size) if (i, y) not in self.board_blocks]

    def get_small_x_line(self, pos: Position) -> List[Position]:
        x, y = pos
        result = [pos]

        if pos in self.board_blocks: return result

        for sl in range(y - 1, -1, -1):
            if (x, sl) not in self.board_blocks:
                result.append((x, sl))
            else:
                break

        for sr in range(y + 1, self.y_size):
            if (x, sr) not in self.board_blocks:
                result.append((x, sr))
            else:
                break

        return result

    def get_small_y_line(self, pos: Position) -> List[Position]:
        x, y = pos
        result = [pos]

        if pos in self.board_blocks: return result

        for sl in range(x - 1, -1, -1):
            if (sl, y) not in self.board_blocks:
                result.append((sl, y))
            else:
                break

        for sr in range(x + 1, self.x_size):
            if (sr, y) not in self.board_blocks:
                result.append((sr, y))
            else:
                break

        return result

    def get_solution(self):
        solution: Dict[Position, int] = {(i, j): None for i in range(self.x_size) for j in range(self.y_size)}
        board_possibilities: Dict[Position, List[int]] = {(i, j): self.possilities_per_field.copy()
                                                          for i in range(self.x_size) for j in
                                                          range(self.y_size)}
        # remove blocks
        for pos in self.board_blocks:
            try:
                del board_possibilities[pos]
            except KeyError:
                pass
            solution[pos] = 0

            # if number is in Block, then add it and remove it from other possibilities in row and column
            num = self.board_numbers[pos]
            if num is not None:
                solution[pos] = num
                to_cut: List[Position] = self.get_whole_x_line(pos) + self.get_whole_y_line(pos)
                for pos in to_cut:
                    try:
                        board_possibilities[pos].remove(num)
                    except ValueError:
                        pass

        for pos, num in self.board_numbers.items():
            if pos not in self.board_blocks and num:
                board_possibilities[pos] = [num]

        while True:
            next_possibilities = get_next_pos_with_least(board_possibilities)

            if not next_possibilities: break

            # choose first Option
            pos = next_possibilities[0]
            possibilities = board_possibilities[pos]

            # choose first possibility
            value = possibilities[0]

            solution[pos] = value
            del board_possibilities[pos]

            for p in self.get_whole_y_line(pos) + self.get_whole_x_line(pos):
                try:
                    board_possibilities[p].remove(value)
                except ValueError:
                    pass
                except KeyError:
                    pass

            small_x_line = self.get_small_x_line(pos)
            for p in small_x_line:
                possibles_in_small_line = get_possibles_in_small_line(len(small_x_line), value)
                try:
                    board_possibilities[p] = [pp for pp in board_possibilities[p] if pp in possibles_in_small_line]
                except KeyError:
                    pass

            small_y_line = self.get_small_y_line(pos)
            for p in small_y_line:
                possibles_in_small_line = get_possibles_in_small_line(len(small_y_line), value)
                try:
                    board_possibilities[p] = [pp for pp in board_possibilities[p] if pp in possibles_in_small_line]
                except:
                    pass

        return solution




def get_possibles_in_small_line(small_line_size, value):
    eps = small_line_size - 1
    return list(range(value - eps, value + eps + 1))


def get_next_pos_with_least(wave: Dict[Position, List[int]], verbose=False) -> List[Position]:
    sorted_wave = sorted(wave.items(), key=lambda item: len(item[1]))
    if not sorted_wave: return []
    min = len(sorted_wave[0][1])
    possibles = [pos for pos, possiblities in dict(sorted_wave).items() if len(possiblities) == min]
    if min == 0: raise NoSolutionPossibleException(f"No Solution possible for: {possibles}")
    if min > 1 and verbose: print("Multiple solutions possible.")
    return possibles


class NoSolutionPossibleException(Exception):
    pass
