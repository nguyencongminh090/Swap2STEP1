import math
import BitBoardGomoku
import os
import msvcrt

cnt5x2 = math.sqrt(17)
cnt5x3 = math.sqrt(20)
cnt5x4 = math.sqrt(25)
cnt6x2 = math.sqrt(26)
cnt6x3 = math.sqrt(29)
cnt6x4 = math.sqrt(34)


# noinspection PyShadowingBuiltins
def round(number, places=0):
    place = 10 ** places
    rounded = (int(number * place + 0.5 if number >= 0 else -0.5)) / place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def distance(vectoA, vectoB):
    return math.sqrt((vectoB[0] - vectoA[0]) ** 2 + (vectoB[1] - vectoA[1]) ** 2)


def checkValid(vecto, boardSize=15):
    return (boardSize - 1) >= vecto[0] >= 0 and (boardSize - 1) >= vecto[1] >= 0


def circleDot(x, y, r):
    spot = []
    k = round(r)
    for i in range(round(r) + 1):
        while distance((x, y), (x + i, y + k)) > r and k > 0:
            k -= 1
        if distance((x, y), (x + i, y + k)) <= r:
            for j in range(k + 1):
                if (x + i, y + j) not in spot and checkValid((x + i, y + j)):
                    spot.append((x + i, y + j))
                if (x - i, y - j) not in spot and checkValid((x - i, y - j)):
                    spot.append((x - i, y - j))
                if (x - i, y + j) not in spot and checkValid((x - i, y + j)):
                    spot.append((x - i, y + j))
                if (x + i, y - j) not in spot and checkValid((x + i, y - j)):
                    spot.append((x + i, y - j))
    return spot


def circleBorder(x, y, r):
    circle = circleDot(x, y, r)
    points = []
    for i, j in circle:
        if r - distance((i, j), (x, y)) <= 1:
            points.append((i, j))
    return points


def squareLine(x, y, sq, ln):
    direction = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
    listCoord = []
    for k in range(1, ln + 1):
        for i, j in direction:
            coord = (x + i * k, y + j * k)
            if checkValid(coord, 15):
                listCoord.append(coord)

    for i in range(1, sq + 1):
        for j in range(1, sq + 1):
            coords = [(x + i, y + j), (x + i, y - j), (x - i, y + j), (x - i, y - j)]

            for coord in coords:
                if checkValid(coord, 15):
                    listCoord.append(coord)

    return listCoord


class ParseMove:
    @classmethod
    def __valid(cls, move: str, size=15):
        if len(move) < 2:
            return False

        x = ord(move[0]) - 96
        y = int(move[1:])
        return 0 < x < size + 1 and 0 < y < size + 1

    @classmethod
    def coord2Num(cls, move):
        return ord(move[0]) - 97, int(move[1:]) - 1

    @classmethod
    def num2coord(cls, num: (int, int)):
        return f'{chr(97 + num[0])}{num[1] + 1}'

    @classmethod
    def num2Num(cls, move, size=15):
        return int(move.split(',')[0]), size - 1 - int(move.split(',')[1])

    @classmethod
    def get(cls, string, numCoord=False, size=15):
        result = []
        while string:
            cur = string[0]
            string = string[1:]
            while string and string[0].isnumeric():
                cur += string[0]
                string = string[1:]
            if cls.__valid(cur, size=size):
                result.append(cur if not numCoord else cls.coord2Num(cur))
        return result


def generateF1(pos: [(int, int)], style: int = 0):
    """Style: [0, 1, 2 ,3]
       NOTE: output can be None
    """
    candidate = list(set(circleDot(*pos[0], cnt6x4) + circleDot(*pos[2], cnt6x4) + circleDot(*pos[1], cnt6x4)))
    blackCandidate = list(set(squareLine(*pos[0], 3, 4) + squareLine(*pos[2], 3, 4)))
    for move in pos:
        candidate.remove(move)

    candidate = {i: 0 for i in candidate}
    for move in candidate:
        if move in squareLine(*pos[0], 2, 3) or move in squareLine(*pos[2], 2, 3):
            candidate[move] += 1
        if move in squareLine(*pos[1], 2, 4) or \
                (move in squareLine(*pos[1], 4, 4) and move not in blackCandidate):
            candidate[move] -= 3
        if move in circleBorder(*pos[0], cnt6x4) or move in circleBorder(*pos[2], cnt6x4):
            candidate[move] += 2
        if move in circleBorder(*pos[1], cnt6x4):
            candidate[move] -= 1

    valDict = dict(filter(lambda item: item[1] == style, candidate.items()))
    return [*valDict]


def main():
    while True:
        os.system('cls')
        position = input('Opening:                    [3 moves only]\rOpening: ').strip()
        style    = int(input('Style  :                    [0, 1, 2, 3]\rStyle  : ').strip())
        coord = ParseMove.get(position, numCoord=True)
        boardV = BitBoardGomoku.BitBoard(15, 'x')
        # 0 is best option
        coords = generateF1(coord, style)
        for i in coords:
            boardV.addMove((i[0], 14 - i[1]))
            print(f'Move: {ParseMove.num2coord(i).upper()}')
        print(boardV.view())
        print('\n\nPress Any Key To Continue')
        msvcrt.getch()


if __name__ == '__main__':
    main()
