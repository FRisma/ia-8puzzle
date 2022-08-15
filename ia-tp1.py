import copy

initialConfig = [
    [1,2,3],
    [5,0,6],
    [4,7,8]
]
goalConfig = [
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

class Node():
    def __init__(self, config=None, historical=[]):
        self.config = config
        self.historical = historical


def start():
    # Dado un estado inicial
    # Obtengo todos los posibles configs
    
    initialNode = Node(config=initialConfig, historical=[])
    recursiveCheck([initialNode])
    

def recursiveCheck(nodes):
    childrenNodes = []
    for node in nodes:
        subNodes = getChilderNodes(node)
        for subNode in subNodes:
            # Chequear si es igual que algun antecesor para descartarlo
            # if isSameConfig(initialChild, config):
            #     print('continue')
            #     continue
        
            childrenNodes.append(subNode)

    isSolution, possibleNode = checkIfAnyNodeIsSolution(childrenNodes)
    if isSolution:
        print("Hemos encontrado el resultado y es ", possibleNode.historical, possibleNode.config)
    else:
        recursiveCheck(childrenNodes)

def getChilderNodes(node):
    childrenNodes = []
    configs = getChildrenConfigs(node.config)
    for config in configs:
        print('historical', node.historical)
        newHistorical = None
        newHistoricalCopy = copy.deepcopy(node.historical)
        newHistoricalCopy.append(node.config)
        print('newHistoricalCopy', newHistoricalCopy)
        # if node.historical is None:
        #     newHistorical = [node.config]
        #     print("New node historical ", newHistorical)
        # else:
        #     newHistorical = node.historical.append(node.config)
        #     print("append node historical ", newHistorical)

        childrenNodes.append(Node(config=config, historical=newHistoricalCopy))
    return childrenNodes
    
def checkIfAnyNodeIsSolution(nodes):
    for node in nodes:
        if isSameConfig(node.config, goalConfig):
            return True, node
    return False, None

def getChildrenConfigs(config=None):
    # Encontrar los vecinos del 0 (devolver [3,5.8])
    possibleValuesToMove = getZeroNeighbors(config)
    
    children = []

    # Generar todas las posibles combinaciones
    for valueToMove in possibleValuesToMove:
        newConfig = switchValue(valueToMove, config)
        children.append(newConfig)
    return children

def getZeroNeighbors(config):
    neighbors = find_neighbours(config)
    return next(item for item in neighbors if item["value"] == 0).get("neighbors")

def switchValue(posValue, config):
    print('intercambiando el valor', posValue)
    zeroIndex = find_indexOfValue(0, config)
    itemIndex = find_indexOfValue(posValue, config)
    targetConfig = copy.deepcopy(config)
    targetConfig[itemIndex[0]][itemIndex[1]] = 0
    targetConfig[zeroIndex[0]][zeroIndex[1]] = posValue
    return targetConfig

def isSameConfig(someConfig, anotherConfig):
    
    return someConfig == anotherConfig

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


def find_indexOfValue(value, config):
    index_array = [(index, row.index(value)) for index, row in enumerate(config) if value in row]
    return index_array[0]

start()