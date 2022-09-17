from models import Node
import random
import numpy as np
import matplotlib.pyplot as plt
import copy
import sys

initial_config = [
    [1, 2, 3],
    [4, 5, 6],
    [0, 7, 8]
]

goal_config = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# initial_config = [
#     [2, 8, 3],
#     [1, 6, 4],
#     [7, 0, 5]
# ]
#
# goal_config = [
#     [2, 8, 3],
#     [1, 6, 4],
#     [7, 5, 0]
# ]


def randomize(iterations=None, config=None):
    node_to_check = Node(config=config, historical=[], level=0)
    print("El estado inicial es ", node_to_check.config)
    print("El estado final es ", goal_config)
    for _ in range(iterations):
        node_to_check = random_sub_node(node_to_check)
        print('Iteracion {} la configuracion actual es {}:'.format(_+1, node_to_check.config))

    print("El nuevo estado es ", node_to_check.config)
    return node_to_check.config

def random_sub_node(node):
    children = get_children_nodes(node)
    return random.choice(children)

def bidirectional_search():
    new_config = randomize(iterations=10, config=initial_config)
    initial_node = Node(config=new_config, historical=[], level=0)
    goal_node = Node(config=goal_config, historical=[], level=0)

    recursive_check_bidirectional([initial_node], [goal_node])

def random_search():
    new_config = randomize(iterations=1, config=initial_config)
    initial_node = Node(config=new_config, historical=[], level=0)
    step = 1
    recursirve_random_check([initial_node], step)


def bfs():
    # BFS
    # Dado un estado inicial
    # Obtengo todos los posibles configs
    new_config = randomize(iterations=10, config=initial_config)
    initial_node = Node(config=new_config, historical=[], level=0)
    recursive_check([initial_node])
    

def recursirve_random_check(nodes, step):
    children_nodes = []

    if step > 1000:
        print('Se supero las 1000 iteraciones')
        sys.exit()

    for node in nodes:
        configs = get_children_configs(node.config)
        random_config_index = random.randrange(0, len(configs), 1)

        new_historical_copy = copy.deepcopy(node.historical)
        new_historical_copy.append(node.config)
        children_nodes.append(Node(config=configs[random_config_index], historical=new_historical_copy,
                                   level=node.level + 1))
        # if new_config
    is_solution, possible_node = check_any_node_is_solution(children_nodes)
    if is_solution:
        print('Cantidad de iteraciones alcanzadas para encontrar el objetivo', step)
        sys.exit()

    else:
        step += 1
        recursirve_random_check(children_nodes, step)


def recursive_check(nodes):
    children_nodes = []
    for node in nodes:
        sub_nodes = get_children_nodes(node)
        for sub_node in sub_nodes:
            children_nodes.append(sub_node)

    is_solution, possible_node = check_any_node_is_solution(children_nodes)
    if is_solution:
        print("Hemos encontrado el resultado y es {}{} y su nivel es {}:".format(possible_node.historical, possible_node.config, possible_node.level))
    else:
        recursive_check(children_nodes)


def recursive_check_bidirectional(initial_nodes, goal_nodes):
    initial_children_nodes = []
    goal_children_nodes = []

    children_nodes = []
    for initial_node in initial_nodes:
        initial_sub_nodes = get_children_nodes(initial_node)
        for initial_sub_node in initial_sub_nodes:
            initial_children_nodes.append(initial_sub_node)

    new_node = goal_children_nodes
    if len(goal_children_nodes) == 0:
        new_node = [Node(config=goal_config, historical=[], level=0)]

    is_solution, possible_node = check_any_node_is_solution_bidirectional(initial_children_nodes, new_node)
    if is_solution:
        new_historical = possible_node[0].historical + possible_node[1].config + possible_node[1].historical

        print("Hemos encontrado el resultado y es {} y su nivel es {}:".format(new_historical, possible_node[0].level))

        sys.exit()

    for goal_node in goal_nodes:
        goal_sub_nodes = get_children_nodes(goal_node)
        for goal_sub_node in goal_sub_nodes:
            goal_children_nodes.append(goal_sub_node)

    is_solution, possible_node = check_any_node_is_solution_bidirectional(initial_children_nodes, goal_children_nodes)
    if is_solution:
        new_historical = possible_node[0].historical + possible_node[1].config + possible_node[1].historical
        print("Hemos encontrado el resultado y es {} y su nivel es {}:".format(new_historical, possible_node[0].level))

    else:
        recursive_check_bidirectional(initial_children_nodes, goal_children_nodes)
        #recursive_check(children_nodes)


def get_children_nodes(node):
    children_nodes = []
    configs = get_children_configs(node.config)
    for config in configs:
        #print('historical', node.historical)
        new_historical_copy = copy.deepcopy(node.historical)
        new_historical_copy.append(node.config)
        #print('newHistoricalCopy', new_historical_copy)

        try:
            if config != node.historical[-1]:
                children_nodes.append(Node(config=config, historical=new_historical_copy, level=node.level + 1))
        except Exception as e:
            children_nodes.append(Node(config=config, historical=new_historical_copy, level=node.level + 1))

    return children_nodes


def check_any_node_is_solution(nodes):
    for node in nodes:
        if is_same_config(node.config, goal_config):
            return True, node
    return False, None

def check_any_node_is_solution_bidirectional(initial_nodes, goal_nodes):
    for node in initial_nodes:
        for goal_node in goal_nodes:
            if is_same_config(goal_node.config, node.config):
                return True, (node, goal_node)

    return False, None


def get_children_configs(config=None):
    # Encontrar los vecinos del 0 (devolver [3,5.8])
    possible_values_to_move = get_zero_neighbors(config)
    
    children = []

    # Generar todas las posibles combinaciones
    for value_to_move in possible_values_to_move:
        new_config = switch_value(value_to_move, config)
        children.append(new_config)
    return children


def get_zero_neighbors(config):
    neighbors = find_neighbours(config)
    return next(item for item in neighbors if item["value"] == 0).get("neighbors")


def switch_value(pos_value, config):
    zero_index = find_index_value(0, config)
    item_index = find_index_value(pos_value, config)
    target_config = copy.deepcopy(config)
    target_config[item_index[0]][item_index[1]] = 0
    target_config[zero_index[0]][zero_index[1]] = pos_value
    return target_config


def is_same_config(some_config, another_config):
    return some_config == another_config


def find_neighbours(arr):
    neighbors = []

    for i in range(len(arr)):
        for j, value in enumerate(arr[i]):

            if i == 0 or i == len(arr) - 1 or j == 0 or j == len(arr[i]) - 1:
                # corners
                new_neighbors = []
                if i != 0:
                    new_neighbors.append(arr[i - 1][j])  # top neighbor
                if j != len(arr[i]) - 1:
                    new_neighbors.append(arr[i][j + 1])  # right neighbor
                if i != len(arr) - 1:
                    new_neighbors.append(arr[i + 1][j])  # bottom neighbor
                if j != 0:
                    new_neighbors.append(arr[i][j - 1])  # left neighbor

            else:
                # add neighbors
                new_neighbors = [
                    arr[i - 1][j],  # top neighbor
                    arr[i][j + 1],  # right neighbor
                    arr[i + 1][j],  # bottom neighbor
                    arr[i][j - 1]   # left neighbor
                ]

            neighbors.append({
                "value": value,
                "neighbors": new_neighbors})

    return neighbors


def find_index_value(value, config):
    index_array = [(index, row.index(value)) for index, row in enumerate(config) if value in row]
    return index_array[0]

def draw_config(config, title=None):
    data = np.array(config)
    fig, ax = plt.subplots()

    if title:
        fig.canvas.set_window_title(str(title))

    for (i, j), z in np.ndenumerate(data):
        ax.text(j, i, '{}'.format(z), ha='center', va='center', size=9)

    plt.imshow(data, interpolation='none', cmap='Pastel1')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    bfs()
    # bidirectional_search()

    # random_search()
    # randomize(iterations=50, config=goal_config)
    sys.exit()
