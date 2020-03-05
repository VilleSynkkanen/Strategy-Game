# prioriteettijono polunhakua varten
class Polunhakujono:
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == []

    # for inserting an element in the queue
    def put(self, item, priority):
        self.queue.append((item, priority))     # tuplessa ruutu ja prioriteetti

    # for popping an element based on Priority
    def get(self):
        min = 0     # pienimmän indeksi
        for i in range(len(self.queue)):
            if self.queue[i][1] < self.queue[min][1]:
                min = i
        item = self.queue[min][0]
        del self.queue[min]
        return item

