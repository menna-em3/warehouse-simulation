class Battery:
    def __init__(self, capacity=100, low_threshold=20):
        self.capacity = capacity
        self.level = capacity
        self.low_threshold = low_threshold

    def consume(self, amount=1):
        self.level = max(0, self.level - amount)

    def charge(self, amount=5):
        self.level = min(self.capacity, self.level + amount)

    def is_low(self):
        return self.level <= self.low_threshold

    def is_full(self):
        return self.level == self.capacity


class Package:
    def __init__(self, pkg_id, pickup_loc, dest_loc, priority=1):
        self.id = pkg_id
        self.pickup_loc = pickup_loc
        self.dest_loc = dest_loc
        self.priority = priority
        self.status = "PENDING"  # PENDING, IN_TRANSIT, DELIVERED


class Robot:
    def __init__(self, robot_id, start_pos):
        self.id = robot_id
        self.position = start_pos
        self.battery = Battery()
        self.state = "IDLE"  # IDLE, MOVING, LOADING, DELIVERING, CHARGING, WAITING
        self.current_task = None
        self.path = []

    def update_step(self, warehouse, reserved_positions):
        """تحديث حالة وموقع الروبوت في كل Step"""
        # 1. إذا كانت البطارية منخفضة ولم يكن يحمل شحنة، يتوجه للشاحن
        if self.battery.is_low() and self.state != "CHARGING" and not self.current_task:
            charger_pos = list(warehouse.charging_stations.values())[0]
            from PathPlanner import PathPlanner
            self.path = PathPlanner.a_star(warehouse, self.position, charger_pos)
            self.state = "MOVING"

        # 2. حرق البطارية والشحن
        if self.state == "CHARGING":
            self.battery.charge()
            if self.battery.is_full():
                self.state = "IDLE"
            return

        # 3. التحرك على المسار المحدد مع تجنب الاصطدام بسيط
        if self.path:
            next_pos = self.path[0]
            # نظام الحجز البسيط ومنع الاصطدام
            if next_pos in reserved_positions:
                self.state = "WAITING"
                return  # الانتظار خطوة
            
            # الانتقال للمربع التالي
            self.position = next_pos
            self.path.pop(0)
            self.battery.consume()
            reserved_positions.add(self.position)
            self.state = "MOVING"

            # الوصول للهادف
            if not self.path:
                self._handle_arrival(warehouse)

    def _handle_arrival(self, warehouse):
        if self.position in warehouse.charging_stations.values():
            self.state = "CHARGING"
        elif self.current_task:
            if self.position == self.current_task.pickup_loc and self.current_task.status == "PENDING":
                self.current_task.status = "IN_TRANSIT"
                # إعادة التخطيط لنقطة التسليم
                from PathPlanner import PathPlanner
                self.path = PathPlanner.a_star(warehouse, self.position, self.current_task.dest_loc)
                self.state = "DELIVERING"
            elif self.position == self.current_task.dest_loc and self.current_task.status == "IN_TRANSIT":
                self.current_task.status = "DELIVERED"
                self.current_task = None
                self.state = "IDLE"