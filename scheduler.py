from PathPlanner import PathPlanner

class TaskScheduler:
    def __init__(self, strategy="NEAREST"):
        self.strategy = strategy

    def assign_tasks(self, warehouse, robots, pending_packages):
        """توزيع الشحنات المنتظرة على الروبوتات المتاحة"""
        for pkg in list(pending_packages):
            idle_robots = [r for r in robots if r.state == "IDLE" and not r.battery.is_low()]
            if not idle_robots:
                break

            best_robot = None
            if self.strategy == "NEAREST":
                # اختيار أقرب روبوت لنقطة الاستلام
                best_robot = min(
                    idle_robots,
                    key=lambda r: PathPlanner.heuristic(r.position, pkg.pickup_loc)
                )

            if best_robot:
                best_robot.current_task = pkg
                best_robot.path = PathPlanner.a_star(warehouse, best_robot.position, pkg.pickup_loc)
                best_robot.state = "MOVING"
                pending_packages.remove(pkg)