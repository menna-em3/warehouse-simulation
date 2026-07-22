import time
from warehouse import Warehouse
from components import Robot, Package
from scheduler import TaskScheduler

class SimulationEngine:
    def __init__(self, map_file):
        self.warehouse = Warehouse(map_file)
        self.robots = [
            Robot("R1", (1, 1)),
            Robot("R2", (1, 2)),
            Robot("R3", (8, 8))
        ]
        self.pending_packages = []
        self.scheduler = TaskScheduler(strategy="NEAREST")
        self.step_count = 0

    def add_package(self, pkg):
        self.pending_packages.append(pkg)

    def run_step(self):
        self.step_count += 1
        print(f"\n--- TIMESTEP {self.step_count} ---")
        
        # 1. إسناد المهام
        self.scheduler.assign_tasks(self.warehouse, self.robots, self.pending_packages)

        # 2. تحديث مواقع الروبوتات وحالاتها
        reserved_positions = set()
        for robot in self.robots:
            robot.update_step(self.warehouse, reserved_positions)
            print(f"Robot {robot.id} | Pos: {robot.position} | Battery: {robot.battery.level}% | State: {robot.state}")

if __name__ == "__main__":
    # إنشاء المحاكاة
    sim = SimulationEngine("map.json")

    # إضافة شحنات تجريبية
    sim.add_package(Package("P1", pickup_loc=(9, 0), dest_loc=(9, 9)))
    sim.add_package(Package("P2", pickup_loc=(9, 0), dest_loc=(0, 9)))

    # تشغيل 15 خطوة محاكاة
    for _ in range(15):
        sim.run_step()
        time.sleep(0.5)