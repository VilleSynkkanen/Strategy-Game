import heapq

# jonoluokka polunhaun tietojen säilömiseen
class Polunhakujono:
    def __init__(self):
        self.elementit = []

    def empty(self):
        return len(self.elementit) == 0

    def put(self, item, priority):
        heapq.heappush(self.elementit, (priority, item))

    def get(self):
        return heapq.heappop(self.elementit)[1]