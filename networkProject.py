import math
class Router:
    def __init__ (self,name):
        self.name = name
        self.neigbors = {}
    
    def add_connections(self, neighbor, cost = 1):
        self.neigbors[neighbor] = cost
    
    def __repr__(self):
        return f"Router: {self.name}, connections: {list(self.neigbors.items())})"

class Network:
    def __init__(self):
        self.routers = {}
    
    def add_router(self, name):
        if name not in self.routers:
            self.routers[name] = Router(name)
        else:
            return f"Router {name} already exists"
        
    def total_nodal_delay(self, dproc, dqueue, transRate,dprop,packet_size):
        dtrans = (packet_size/ (transRate * 1000000)) * 1000
        dnodal = dproc + dqueue + dtrans + dprop
        throughput = round((packet_size/1000000) / (dnodal/1000),2)
        return throughput
    
    
    def connect(self, name1, name2, dproc, dqueue, trans, dprop = 0 ,packet_size = 50000):
        if name1 in self.routers and name2 in self.routers:
            self.routers[name1].add_connections(name2, {"throughput_Mbps": self.total_nodal_delay(dproc, dqueue, trans, dprop, packet_size)})
            self.routers[name2].add_connections(name1, {"throughput_Mbps":self.total_nodal_delay(dproc, dqueue, trans, dprop, packet_size)})
        else:
            if name1 in self.routers:
                return f"Router {name2} does not exist"
            else:
                return f"Router {name1} does not exist"
    
   
    def show_network(self):
        for router in self.routers.values():
            print(router)
                

def main():
    net = Network()
    net.add_router("R1")
    net.add_router("R2")
    net.add_router("R3")
    #   to connect a node add the nodes name the node it want to connect to 
    #   and the dproc, dqueue, trans, packet size (dprop, packet size is optional)
    #ex) net.connect(node1, node1, 3, 4, 10, 10000000)
    # we are assuming all transmission rate are in megabits
    # dprop is 0ms by default
    # packet size is 10,000 by default and is in bits
    net.connect("R1", "R2", 3, 10, 5, 1, 50000)
    net.connect("R2", "R3", 2,1,10,0.5,80000)
    net.connect("R1", "R3", 7,7,7, 0, 60000)

    net.show_network()

if __name__ == "__main__":
    main()