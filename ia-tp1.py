from models import Node
import copy

initial_config = [
    [1, 2, 3],
    [5, 0, 6],
    [4, 7, 8]
]

goal_config = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


def start():
    # Dado un estado inicial
    # Obtengo todos los posibles configs
    
    initial_node = Node(config=initial_config, historical=[])
    recursive_check([initial_node])
    

def recursive_check(nodes):
    children_nodes = []
    for node in nodes:
        sub_nodes = get_children_nodes(node)
        for sub_node in sub_nodes:
            # Chequear si es igual que algun antecesor para descartarlo
            # if isSameConfig(initialChild, config):
            #     print('continue')
            #     continue
        
            children_nodes.append(sub_node)

    is_solution, possible_node = check_any_node_is_solution(children_nodes)
    if is_solution:
        print("Hemos encontrado el resultado y es ", possible_node.historical, possible_node.config)
    else:
        recursive_check(children_nodes)


def get_children_nodes(node):
    children_nodes = []
    configs = get_children_configs(node.config)
    for config in configs:
        print('historical', node.historical)
        new_historical_copy = copy.deepcopy(node.historical)
        new_historical_copy.append(node.config)
        print('newHistoricalCopy', new_historical_copy)
        # if node.historical is None:
        #     newHistorical = [node.config]
        #     print("New node historical ", newHistorical)
        # else:
        #     newHistorical = node.historical.append(node.config)
        #     print("append node historical ", newHistorical)

        children_nodes.append(Node(config=config, historical=new_historical_copy))
    return children_nodes


def check_any_node_is_solution(nodes):
    for node in nodes:
        if is_same_config(node.config, goal_config):
            return True, node
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
    print('intercambiando el valor', pos_value)
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


if __name__ == '__main__':
    start()
