class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position


def breadthFirst(maze, start, end):
    """
    Breadth-first algorithm for pathfinding
    Start and end coordinates are [row, col]
    """
    start_node = Node(None, start)
    end_node = Node(None, end) # Used to check if done
    nodeList = []
    visitedNodes = []
    nodeList.append(start_node) # Start at first node
    while len(nodeList) > 0:
        neighbors = [] # Nearby valid nodes
        for node in nodeList:
            nodeList.remove(node)
            visitedNodes.append(node)
            if node == end_node: # Reached end, return path
                path = []
                current = node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Neighbor positions
                neighborNode = (node.position[0] + new_position[0], node.position[1] + new_position[1])

                #Neighbor is in bounds
                if neighborNode[0] > (len(maze)-1) or neighborNode[0] < 0 or neighborNode[1] > (len(maze[0])-1) or neighborNode[1] < 0:
                    continue
                
                #Neighbor is not a wall
                if maze[neighborNode[0]][neighborNode[1]] == '1':
                    continue
                
                # Make sure we haven't touched this node ever yet
                add = True
                newNode = Node(node, neighborNode)
                for tNode in nodeList:
                    if tNode == newNode:
                        add = False
                for tNode in visitedNodes:
                    if tNode == newNode:
                        add = False
                for tNode in neighbors:
                    if tNode == newNode:
                        add = False
                
                if add:
                    neighbors.append(newNode)
        
        for node in neighbors:
            nodeList.append(node)
    
    return None # End is not reachable
