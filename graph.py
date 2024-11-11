

class Graph():
    def __init__(self):
        self.graph = {}
    
    def createNode(self, currentState, nextStates):
        currentStateKey = (
            tuple(sorted(currentState['squares'])), 
            tuple(sorted(currentState['goals']))
        )
        
        if currentStateKey not in self.graph:
            self.graph[currentStateKey] = []
        
        for next in nextStates:
            nextStateKey = (
                tuple(sorted([(sq[0], sq[1], sq[2]) for sq in next['squares']])),
                tuple(sorted([(g[0], g[1], g[2]) for g in next['goals']]))
            )
            
            if nextStateKey not in self.graph:
                self.graph[nextStateKey] = []
            
            self.graph[currentStateKey].append(nextStateKey)
        
        print("Graph:", self.graph)
        return self.graph
    