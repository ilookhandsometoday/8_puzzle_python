# доска - это матрица (ряды и столбцы)
# можно использовать массивы из numpy
# 1 делать ход
# 2 какие ходы можно сделать
    # делать ходы и сравнивать с родителем
# 3 поиск новой точки "роста"
# 4 поиск пути

#TODO Оставить класс
def show_board(board):
    row = ""
    for row in board:
        print(row)


class Node:
    def __init__(self, board, layer, target_board, previous_node=None):
        self.board = board
        self.layer: int = layer
        self.g: int = self.__calculate_g(target_board)
        self.children = []
        self.previous_node = previous_node

    def __calculate_g(self, target_board) -> int:
        g = 0
        for target_row, current_row in zip(target_board, self.board):
            for target_column, current_column in zip(target_row, current_row):
                if target_column != current_column:
                    g += 1
        return g

    def get_leaves(self, leaves_container):
        if not self.children:
            leaves_container.append(self)
        else:
            for child in self.children:
                child.get_leaves(leaves_container)


if __name__ == "__main__":
    game = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]

    target_board = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]

print_board(board)

