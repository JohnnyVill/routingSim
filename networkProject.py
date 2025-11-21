import math
import sys
import heapq
import networkx as nx
class Router:
    def __init__ (self,name):
        self.name = name
        self.neighbors = {} #holds neighbors_name -> cost
    
    def add_connections(self, neighbor, cost = 1):
        self.neighbors[neighbor] = cost
    
    def __repr__(self):
        return f"Router: {self.name}, connections: {list(self.neighbors.items())})"

class Network:
    def __init__(self):
        self.routers = {}
        
    
    def add_router(self, name):
        if name not in self.routers:
            self.routers[name] = Router(name)
        else:
            return f"Router {name} already exists"
        
    def total_nodal_delay(self, dproc, dqueue, transRate,packet_size):
        dprop = 0
        dtrans = (packet_size/ (transRate * 1000000)) * 1000 #return result in ms
        dnodal = dproc + dqueue + dtrans + dprop
        
        #converting packet size from bits to Mbps and dnodal to from ms to sec 
        # and getthing throughput = amount of data transferred / time taken returning the value in Mbps
        throughput = round((packet_size/1000000) / (dnodal/1000),2) 
        
        return throughput
    
    
    def connect(self, name1, name2, dproc, dqueue, trans, packet_size = 50000):
        throughput = self.total_nodal_delay(dproc, dqueue, trans,packet_size)
        if name1 in self.routers and name2 in self.routers:
            self.routers[name1].add_connections(name2,  throughput)
            self.routers[name2].add_connections(name1,  throughput)
        else:
            if name1 in self.routers:
                return f"Router {name2} does not exist"
            else:
                return f"Router {name1} does not exist"
    
    def routingAlgo(self, start, dest):
        pq = []
        
        dist = {name: math.inf for name in self.routers}
        prev = {name: None for name in self.routers}
        dist[start] = 0        
        heapq.heappush(pq, (0, start))
        
        while pq:
            d, n = heapq.heappop(pq)
            
            if d > dist[n]:
                continue
            
            if n == dest:
                break
            
            for node, throughput in self.routers[n].neighbors.items():
                if dist[n] + throughput < dist[node]:
                    dist[node] = dist[n] + throughput
                    prev[node] = n
                    heapq.heappush(pq, (dist[node], node))
        
        if dist[dest] is math.inf:
            return None, math.inf  # no path  
        
        path = []
        goal = dest
        
        while goal:
            path.append(goal)
            goal = prev[goal]    
        path.reverse()    
        return path, dist
    
    def printPath(self, path, dist):
        path_taken = []
        for node in path:
            path_taken.append(f"{node}: throughput {dist[node]}")
        return " -> ".join(path_taken)
    
    def show_network(self):
        for router in self.routers.values():
            print(router)
                

def main():
    net = Network()
    net.add_router("A")
    net.add_router("B")
    net.add_router("C")
    #   to connect a node add the nodes name the node it want to connect to 
    #   and the dproc, dqueue, trans, packet size. dprop is 0 by default (packet size is optional)
    #ex) net.connect(node1, node1, 3, 4, 10, 80000) or  net.connect(node1, node1, 3, 4)
    # we are assuming all transmission rate are in megabits
    # dprop is 0ms by default
    # packet size is 50,000bits by default
    net.connect("A", "B", 3, 10, 10)
    net.connect("B", "C", 2, 1, 10, 80000)
    net.connect("A", "C", 7, 7, 7, 60000)

    net.show_network()
    path, dest = net.routingAlgo("A", "C")
    print(f"Path: {net.printPath(path, dest)}")
if __name__ == "__main__":
    main()