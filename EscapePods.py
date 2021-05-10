class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}

    def __str__(self):
        return str(self.id)

    def addNeighbor(self, neighbor_id, weight=None):
        self.adjacent[neighbor_id] = weight

    def removeNeighbor(self, neighbor_id):
        del self.adjacent[neighbor_id]

    def getConnections(self):
        return list(self.adjacent.keys())

    def getID(self):
        return self.id

    def getWeight(self, neighbor_id):
        return self.adjacent[neighbor_id]

    def setWeight(self, neighbor_id, weight):
        self.adjacent[neighbor_id] = weight


class Graph:
    def __init__(self):
        self.vertices = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vertices.values())

    def addVertex(self, node):
        self.num_vertices += 1
        new_vertex = Vertex(node)
        self.vertices[node] = new_vertex
        return new_vertex

    def getVertex(self, vtx_id):
        if vtx_id in self.vertices:
            return self.vertices[vtx_id]
        else:
            return None

    def addEdge(self, start, end, cost=None, directed=False):
        if start not in self.vertices:
            self.addVertex(start)
        if end not in self.vertices:
            self.addVertex(end)

        self.vertices[start].addNeighbor(self.vertices[end].getID(), cost)
        if not directed:
            self.vertices[end].addNeighbor(self.vertices[start].getID(), cost)

    def removeEdge(self, start, end, directed=False):
        if end in self.vertices[start].getConnections():
            self.vertices[start].removeNeighbor(end)
        if not directed:
            if start in self.vertices[end].getConnections():
                self.vertices[end].removeNeighbor(start)

    def getVertices(self):
        return list(self.vertices.keys())

    def findAllPathsHelper(self, start, end, visited, curr_path, all_paths):
        visited[start] = True
        curr_path.append(start)

        if start == end:
            all_paths.append(curr_path[:])
        else:
            start_vtx = self.getVertex(start)
            for nbr in start_vtx.getConnections():
                if visited[nbr] is False:
                    self.findAllPathsHelper(nbr, end, visited, curr_path,
                                            all_paths)
        curr_path.pop()
        visited[start] = False

    def findAllPaths(self, start, end):
        visited = {}
        for vtx_id in self.vertices:
            visited[vtx_id] = False

        curr_path = []
        all_paths = []

        self.findAllPathsHelper(start, end, visited, curr_path, all_paths)

        return all_paths

    def findSmallestWeight(self, path):
        smallest_weight = None
        for i in range(len(path)-1):
            curr_vtx = self.getVertex(path[i])
            neighbor = self.getVertex(path[i+1])
            curr_weight = curr_vtx.getWeight(neighbor.getID())
            if smallest_weight is None or curr_weight < smallest_weight:
                smallest_weight = curr_weight
        return smallest_weight


def createGraph(g, e_map):
    for i in range(len(e_map)):
        g.addVertex(i)
        row = e_map[i]
        for j in range(len(row)):
            if row[j] != 0:
                g.addEdge(i, j, row[j], True)


def findPaths(g, starts, ends):
    all_paths = []
    for start in starts:
        for end in ends:
            paths = g.findAllPaths(start, end)
            for path in paths:
                all_paths.append([path, 0])
    for path in all_paths:
        path[1] = g.findSmallestWeight(path[0])
    return all_paths


def solution(starts, ends, e_map):
    g = Graph()
    throughput = 0
    createGraph(g, e_map)
    all_paths = findPaths(g, starts, ends)
    while len(all_paths) > 0:
        all_paths.sort(key=lambda x: x[1], reverse=True)
        curr_path, weight = all_paths[0]
        throughput += weight
        for i in range(len(curr_path)-1):
            vtx_id = curr_path[i]
            vtx = g.getVertex(vtx_id)
            nbr = g.getVertex(curr_path[i+1])
            new_weight = max(0, vtx.getWeight(nbr.getID()) - weight)
            vtx.setWeight(nbr.getID(), new_weight)
            if new_weight == 0:
                g.removeEdge(vtx_id, nbr.getID(), True)
        all_paths = findPaths(g, starts, ends)
    return throughput


starts = [0, 1]
ends = [4, 5]
e_map = [[0, 0, 4, 6, 0, 0],
         [0, 0, 5, 2, 0, 0],
         [0, 0, 0, 0, 4, 4],
         [0, 0, 0, 0, 6, 6],
         [0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0]]

sol = solution(starts, ends, e_map)
print(sol)
