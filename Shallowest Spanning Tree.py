import heapq

class Queue:
    """
    A class that is to represent a normal queue (push to back, pop from front, no sorting or taking smallest item)
    """
    def __init__(self):
        """
        The constructor of the Queue class that initializes the queue as well as the pointers in the queue
        (front, back)
        :param: None
        :return: None
        :complexity: O(1)
        """
        self.head = 0
        self.tail = 0
        self.queue = []

    def push(self, data):
        """
        a function to push data into the queue (from the back which is just using append)
        updates tail variable (pointer to the back of the queue)
        :param: data, which is the data that is going to be added to the queue
        :return: None
        :complexity: O(1)
        """
        self.queue.append(data)
        self.tail += 1

    def pop(self):
        """
        a function to pop data from the queue (from the front) by using the head variable as a
        pointer (front of queue pointer) and updates the head variable to indicate the data was popped
        and the new front is the next value
        :param: data, which is the data that is going to be added to the queue
        :return: None
        :complexity: O(1)
        """
        front = self.queue[self.head] # pop the first item in the queue
        self.head += 1 # move the pointer to next item (popped item from front)
        return front


class Graph:
    """
    A class that (when passed in the file) it will build the graph in a adjacency list
    representation where the first line in the list is the amount of vertices
    """
    def __init__(self, gfile):
        """
        the constructor of the Graph class that takes input a file to extract data from the file,
        the first line in the file indicates the amount of vertices in the graph, the rest are edges
        of the vertices that connect following by weights

        :param: gfile, a text file containing the data needed to fill in the graph (as adjacency list)
        :return: None
        :complexity: O(V^2) where V is the number of vertices in the graph (first line in the text file)
        """
        text = open(gfile, 'r')
        vertices = text.readline() # read first line (vertices)
        self.vertices = int(vertices) # store number of vertices
        self.graph = [0] * self.vertices
        # for each line in the text
        for line in text:
            lst = []
            line = line.split() # turn them into list (ignoring " ")
            # if there is nothing in the graph at that index
            # when trying to edges from u to v it will be in a format of (v, weight from u to v)
            if self.graph[int(line[0])] == 0:
                lst.append((int(line[1]), int(line[2])))
                self.graph[int(line[0])] = lst
            else:
                # else append it to the array
                # example: [[(0, 1), (0, 4)],0, 0] if it is trying to add (0, 5) to the
                # first index, after appending it will be [[(0, 1), (0, 4), (0, 5)],0, 0]
                self.graph[int(line[0])].append((int(line[1]), int(line[2])))
            lst = []
            # after adding the edges to u as (v, weight from u to v)
            # add the same format to v as well so it won't be like a directed graph
            # so after adding it will be in a format as
            # u: (v, weight)
            # v: (u, weight)
            if self.graph[int(line[1])] == 0:
                lst.append((int(line[0]), int(line[2])))
                self.graph[int(line[1])] = lst
            else:
                self.graph[int(line[1])].append((int(line[0]), int(line[2])))
        text.close()

    def shallowest_spanning_tree(self):
        """
        A function that finds the vertex that finds a spanning tree, from a certain start point, which minimizes the
        number of edges from root to deepest leaf while ignoring edge weights.

        :param: None
        :return: a tuple that contains the starting vertex that creates a spanning tree where from start to deepest leaf
        is the shortest compared to other vertex followed by the length of the depth itself
        :complexity: O(V^3) where V is the number of vertices in the graph (first line in the text file)
        """
        # if the graph has only one vertex
        if self.graph == [0]:
            return 0, 0
        # root is vertex used, short_dept is the shortest dept the graph has to traverse from that point
        root, self.short_depth = 0, 2 ** 999
        # run through using every vertex as the root and use breadth first to traverse and find deepest leaf
        # compare the deepest leaf distance and if one is less than the other then update it
        for i in range(self.vertices):
            # this entire block of code is a breadth first search that uses each vertices in the graph
            # as
            max_depth = 0 # records max-dept of each vertex and compares with lowest max dept
            dist = [None] * self.vertices
            dist[i] = 0
            q = Queue()
            q.push(i)
            # according to the queue i made, if head is greater or equal to tail, it means that
            # the queue is empty (according to pointers)
            while q.tail > q.head:
            # this entire block of code is a breadth-first search
                u = q.pop()
                for edge in self.graph[u]:
                    v = edge[0] # get v adjacent to u
                    if dist[v] is None:
                        dist[v] = dist[u] + 1
                        q.push(v)
                    if dist[v] > max_depth:
                        max_depth = dist[v] # set max dept it has to traverse
            # if it the max dept is less than the current, update it and update the root
            if max_depth < self.short_depth:
                root = i
                self.short_depth = max_depth
        return root, self.short_depth