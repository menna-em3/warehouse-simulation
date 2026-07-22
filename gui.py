import pygame
import sys
from main import SimulationEngine
from components import Package

# الألوان الأساسية
WHITE = (245, 245, 245)
GRAY = (200, 200, 200)
BLUE = (41, 128, 185)      # للرفوف والجدران
GREEN = (46, 204, 113)     # للروبوتات
YELLOW = (241, 196, 15)    # لمحطات الشحن
PURPLE = (155, 89, 182)    # لمحطات التسليم

CELL_SIZE = 60

class WarehouseGUI:
    def __init__(self, sim):
        self.sim = sim
        pygame.init()
        self.width = sim.warehouse.width * CELL_SIZE
        self.height = sim.warehouse.height * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Autonomous Warehouse Simulation")
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(WHITE)

        # 1. رسم الشبكة والعوائق
        for x in range(self.sim.warehouse.width):
            for y in range(self.sim.warehouse.height):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

                if (x, y) in self.sim.warehouse.walls or (x, y) in self.sim.warehouse.shelves:
                    pygame.draw.rect(self.screen, BLUE, rect)

        # 2. رسم محطات الشحن والتسليم
        for pos in self.sim.warehouse.charging_stations.values():
            rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, YELLOW, rect)

        for pos in self.sim.warehouse.delivery_stations.values():
            rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, PURPLE, rect)

        # 3. رسم الروبوتات
        for robot in self.sim.robots:
            center = (robot.position[0] * CELL_SIZE + CELL_SIZE // 2,
                      robot.position[1] * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(self.screen, GREEN, center, CELL_SIZE // 3)

        pygame.display.flip()

    def run(self):
        running = True
        pkg_counter = 100
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # 🖱️ إضافة طرد عند الضغط بزر الماوس الأيسر في الشاشة
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    gx, gy = mx // CELL_SIZE, my // CELL_SIZE
                    
                    # التأكد من عدم النقر على جدار
                    if (gx, gy) not in self.sim.warehouse.walls and (gx, gy) not in self.sim.warehouse.shelves:
                        pkg_counter += 1
                        new_pkg = Package(f"P{pkg_counter}", pickup_loc=(gx, gy), dest_loc=(9, 9))
                        self.sim.add_package(new_pkg)
                        print(f"📦 تم إضافة طرد جديد P{pkg_counter} في النقطة ({gx}, {gy})!")

            # تشغيل خطوة محاكاة
            self.sim.run_step()
            self.draw()
            self.clock.tick(2)  # سرعة الحركة (2 خطوة في الثانية)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    sim = SimulationEngine("map.json")
    sim.add_package(Package("P1", pickup_loc=(9, 0), dest_loc=(9, 9)))
    
    gui = WarehouseGUI(sim)
    gui.run()