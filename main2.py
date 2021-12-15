from collections import namedtuple
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt



# по сути класс для того, чтобы знать, как двигать фишки
Direction = namedtuple('Direction', ['row_offset', 'column_offset'])
directions: Dict[str, Direction] = {'up': Direction(-1, 0), 'down': Direction(1, 0), 'left': Direction(0, -1),
                                    'right': Direction(0, 1)}
g_sequence = []


# класс, в экземплярах которого будем держать дерево игры
class TreeNode:
    G_WEIGHT = 1.0
    H_WEIGHT = 1.0

    def __init__(self, state: List[List], layer: int, parent, goal: List[List]):
        self.state = state
        self.layer = layer
        self.goal = goal
        self.g = self.calculate_g()
        self.descendants = []
        self.parent = parent

    @staticmethod
    def value_function(g, layer):
        return TreeNode.G_WEIGHT * g + TreeNode.H_WEIGHT * layer

    @staticmethod
    def get_widths(layer, widths):
        widths.append(len(layer))
        next_layer = []
        for node in layer:
            next_layer.extend(node.descendants)
        if not next_layer:
            return
        TreeNode.get_widths(next_layer, widths)

    def show_board(self):
        for row in self.state:
            print(row)

    def move(self, row: int, column: int, direction: str):
        """Takes in a node and moves a piece at row, column in a specified direction.
        Returns a board where said move has been made.
        Doesn't check if a move is possible"""
        board_copy: List[List] = [row.copy() for row in self.state]
        direction_value = directions[direction]
        row_after_move = row + direction_value.row_offset
        column_after_move = column + direction_value.column_offset
        board_copy[row_after_move][column_after_move], board_copy[row][column] = \
            board_copy[row][column], board_copy[row_after_move][column_after_move]
        return board_copy

    def possible_moves(self) -> List[Tuple]:
        """Takes in a board. Returns possible moves (row, column, direction)."""
        for index, row in enumerate(self.state):
            if 0 in row:
                empty_position_row, empty_position_column = index, row.index(0)
                break
        possible_move_lst: List[Tuple] = []
        for direction_str, direction_value in directions.items():
            # figuring out from what row and column we could try moving to an empty space
            possible_move_from_row = empty_position_row - direction_value.row_offset
            possible_move_from_column = empty_position_column - direction_value.column_offset
            if len(self.state) > possible_move_from_column >= 0 and\
                    (0 <= possible_move_from_row < len(self.state)):
                possible_move_lst.append((possible_move_from_row, possible_move_from_column, direction_str))
        return possible_move_lst

    def calculate_g(self) -> int:
        return sum(map(lambda row1, row2: sum([el1 != el2 for el1, el2 in zip(row1, row2)]), self.goal, self.state))

    def build_tree(self, goal: List[List], leaves: List):
        g_sequence.append(self.g)
        pos_mvs: List[Tuple] = self.possible_moves()
        if self.g == 0:
            return self, leaves

        # memorizing the position of the currently chosen node in the sequence of leaves from left to right
        which_leaf = leaves.index(self)
        leaves.remove(self)

        for mov in pos_mvs:
            board_after_move = self.move(*mov)
            if not self.parent or board_after_move != self.parent.state:
                self.descendants.append(TreeNode(self.move(*mov), self.layer + 1, self, self.goal))
        leaves[which_leaf:which_leaf] = self.descendants

        min_f = min([TreeNode.value_function(node.g, node.layer) for node in leaves])

        candidates_for_solution = [leaf for leaf in leaves if TreeNode.value_function(leaf.g, leaf.layer) == min_f]
        return candidates_for_solution[0].build_tree(goal, leaves)

# если количество инверсий (если есть фишка, и после неё дальше идёт фишка с большим числом, это инверсия) нечётное, то
# такую конфигурацию нельзя решить
def validate_board(b):
    inversions_count = 0
    board_flattened = []
    for row in b:
        board_flattened.extend(row)

    for row in b:
        for current in row:
            board_flattened_after_current = board_flattened[board_flattened.index(current) + 1:]
            for piece in board_flattened_after_current:
                # не учитываем пустую фишку(0) как число при подсчёте инверсий
                if piece < current and piece != 0:
                    inversions_count += 1
    return inversions_count % 2 == 0

if __name__ == "__main__":
    # из текста практики
    game = [
        [2, 4, 3],
        [1, 8, 5],
        [7, 0, 6]
    ]

    game2 = [
        [2, 0, 3],
        [1, 6, 8],
        [4, 7, 5]
    ]

    game3 = [
        [2, 6, 3],
        [1, 8, 5],
        [4, 7, 0]
    ]

    # game4 не решится из-за ограничения python по рекурсии
    game4 = [
        [0, 2, 8],
        [7, 6, 5],
        [1, 4, 3]
    ]

    # не решится потому что не решаема в принципе
    game_not_valid = [
        [7, 1, 2],
        [5, 0, 9],
        [8, 3, 6]
    ]

    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    rt = TreeNode(game4, 1, None, goal_board)
    valid = validate_board(rt.state)
    if not valid:
        print("WARNING: ДАННАЯ КОНФИГУРАЦИЯ НЕ РЕШАЕМА")

    # adding the root to the list of leaves at startup is necessary for consistency
    last_leaf, leaves = rt.build_tree(goal_board, [rt])
    node_of_path = last_leaf
    path = []
    while node_of_path:
        path.insert(0, node_of_path)
        node_of_path = node_of_path.parent

    widths = []
    TreeNode.get_widths([rt], widths)
    max_width = max(widths)
    max_depth = max(leaf.layer for leaf in leaves)
    print(f'Максимальная ширина дерева:{max_width}')
    print(f'Максимальная глубина дерева:{max_depth}')

    for node in path:
        node.show_board()
        print('______')

    print(f'Решено за {len(path) - 1} ходов')
    plt.plot(g_sequence)
    plt.show()
    print("END")
