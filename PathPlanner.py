import heapq

class PathPlanner:
    @staticmethod
    def heuristic(a, b):
        """حساب مسافة مانهاتن"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def a_star(warehouse, start, goal):
        """تطبيق خوارزمية A* لإيجاد أقصر مسار"""
        if start == goal:
            return [start]

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for neighbor in warehouse.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + PathPlanner.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))

        return []  # لا يوجد مسار