import math
import random
import itertools


def distance(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def closest_pair(points):
    comparisons = 0
    first = second = min_distance = None

    class Counter:
        def __init__(self, key):
            self.key = key

        def __lt__(self, other):
            nonlocal comparisons
            comparisons += 1
            return self.key < other.key

    def update_solution(x, y):
        nonlocal min_distance, first, second, comparisons
        comparisons += 1
        d = distance(x, y)
        if min_distance is None or d < min_distance:
            first, second, min_distance = x, y, d
        return d

    def solve(_points):
        assert len(_points) >= 2
        if len(_points) <= 3:
            list(itertools.starmap(update_solution, itertools.combinations(_points, 2)))
            return

        middle = len(_points) // 2
        midpoint = _points[middle][0]
        solve(_points[:middle])
        solve(_points[middle:])

        dist = min_distance
        candidates = sorted((p for p in _points if abs(p[0] - midpoint) < dist), key=lambda p: p[1])
        for i in range(len(candidates)):
            for j in reversed(range(0, i)):
                d = update_solution(candidates[i], candidates[j])
                if d >= dist:
                    break

    points = sorted(points, key=Counter)
    after_sorted = comparisons
    solve(points)
    return min_distance, first, second, comparisons, after_sorted


def naive_closest_pair(points):
    comparisons = 0
    first = second = min_distance = None

    for x, y in itertools.combinations(points, 2):
        comparisons += 1
        d = distance(x, y)
        if min_distance is None or d < min_distance:
            first, second, min_distance = x, y, d

    return min_distance, first, second, comparisons, 0


def print_solution(min_distance, first, second, comparisons, sorting):
    print('Closest pair of points:', *sorted([first, second]))
    print('Distance:', min_distance)
    print('Comparisons performed:', comparisons)
    print('Comparisons for sorting:', sorting)
    print('Comparisons for the algorithm:', comparisons - sorting)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-c', default=1000, type=int, required=False)
    parser.add_argument('--box', '-b', default=1000, type=int, required=False)
    args = parser.parse_args()

    pts = [[random.uniform(0, args.box), random.uniform(0, args.box)] for _ in range(args.count)]
    print('Fast solution:')
    print_solution(*closest_pair(pts))
    print()
    print('Naive solution:')
    print_solution(*naive_closest_pair(pts))
