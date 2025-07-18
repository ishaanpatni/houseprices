import csv

class Error(Exception):
    def __init__(self, message="Error."):
        self.message = message
        super().__init__(self.message)


def get_data(fname):
    with open(fname, 'r') as file:
        data = csv.reader(file)
        header = next(data)[1:]
        data = [row[1:] for row in data]
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])

    return header, data
    
class Graph:
    def __init__(self, matrix, vertices):
        self.matrix = matrix
        self.vertices = vertices

    def adjacent(self, x, y):
        return self.matrix[x][y] > 0
    
    def neighbours(self, x):
        return self.matrix[x]
    

class Node:
    def __init__(self, state, cost, parent):
        self.state = state
        self.cost = cost
        self.parent = parent
    
    
class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, x):
        self.frontier.append(x)

    def empty(self):
        return len(self.frontier) == 0
    
    def contains(self, x):
        for i in self.frontier:
            if i.state == x:
                return True
        
        return False

    def edit_state(self, state, cost, parent):
        for i in self.frontier:
            if i.state == state and i.cost > cost:
                i.cost = cost
                i.parent = parent
    
    def remove(self):
        mincost = 10 ** 10
        node = None

        for i in self.frontier:
            if i.cost < mincost:
                mincost = i.cost 
                node = i
        
        self.frontier.remove(node)
        return node

    def show(self):
        return self.frontier

class GraphTheory:
    def __init__(self, graph, headers):
        self.graph = graph
        self.headers = headers

    def dijkstra(self, start, destination):
        if start not in self.headers or destination not in self.headers:
            raise Error("Invalid location names.")    

        start = self.headers.index(start)
        destination = self.headers.index(destination)

        open = QueueFrontier()
        closed = set()

        initial = Node(start, 0, None)
        open.add(initial)

        while not open.empty():
            node = open.remove()

            if node.state == destination:
                current = node
                path = []
                while current.parent != None:
                    path.append((current.parent.state, current.state, current.cost-current.parent.cost))
                    current = current.parent
                
                path.reverse()
                output = []
                for i in range(len(path)):
                    output.append(f"{self.headers[path[i][0]]} -> {self.headers[path[i][1]]}.")

                return [output, path, node.cost]
            
            closed.add(node.state)

            neighbours = self.graph.neighbours(node.state)
            for i in range(len(neighbours)):
                if neighbours[i] == 0 or i in closed:
                    continue
                elif open.contains(i):
                    open.edit_state(i, node.cost + neighbours[i] + 5, node)
                else:
                    open.add(Node(i, node.cost + neighbours[i] + 5, node))
                    

        raise Error("Points not connected.")

    def closeness_centrality(self):
        data = []
        for i in range(self.graph.vertices):
            print(i)
            data.append({'name': self.headers[i], 'avg. time': round(sum([self.dijkstra(self.headers[i], self.headers[j])[2] for j in range(self.graph.vertices)]) / self.graph.vertices, 1)})

        with open('avg_times.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

headers, data = get_data("mrts.csv")
graph = Graph(data, len(data))
sg_mrt = GraphTheory(graph, headers)
sg_mrt.closeness_centrality()