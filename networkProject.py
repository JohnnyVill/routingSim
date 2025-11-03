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
    
    def connect(self, name1, name2, cost= 1):
        if name1 in self.routers and name2 in self.routers:
            self.routers[name1].add_connections(name2, cost)
            self.routers[name2].add_connections(name1, cost)
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

    net.connect("R1", "R2", 2)
    net.connect("R2", "R3", 4)
    net.connect("R1", "R3", 7)

    net.show_network()

if __name__ == "__main__":
    main()