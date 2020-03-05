from ruutu import Ruutu
from koordinaatit import Koordinaatit
from polunhakujono import Polunhakujono
import heapq



class Polunhaku:

    '''
    osa koodista ja algoritmin periaate perustuu seuraaviin sivustoihin:
    https://www.geeksforgeeks.org/a-search-algorithm/
    https://www.redblobgames.com/pathfinding/a-star/implementation.html
    '''

    def __init__(self, ruudut):
        # ruudut toimivat polunhaun graafina
        self.ruudut = ruudut

    def a_star_search(self, alku, loppu):
        frontier = Polunhakujono()
        frontier.put(alku, 0)
        came_from = {}
        cost_so_far = {}
        came_from[alku] = None
        cost_so_far[alku] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == loppu:
                break

            # current = ruutu (?)
            for next in current.naapurit:
                new_cost = cost_so_far[current] + next.maasto.liikkumisen_hinta
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(loppu, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)  # optional
        path.reverse()  # optional
        return path

    # heuristiikan laskeminen, voi liikkua vain neljään suuntaan
    def heuristic(self, paikka, kohde):
        x = abs(paikka.koordinaatit.x - kohde.koordinaatit.x)
        y = abs(paikka.koordinaatit.y - kohde.koordinaatit.y)
        return x + y


