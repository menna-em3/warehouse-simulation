import json

class Warehouse:
    def __init__(self, map_file):
        with open(map_file, 'r') as f:
            data = json.load(f)
        
        self.width = data['grid_size']['width']
        self.height = data['grid_size']['height']
        self.walls = set(tuple(p) for p in data['walls'])
        self.shelves = set(tuple(p) for p in data['shelves'])
        self.charging_stations = {cs['id']: tuple(cs['pos']) for cs in data['charging_stations']}
        self.loading_stations = {ls['id']: tuple(ls['pos']) for ls in data['loading_stations']}
        self.delivery_stations = {ds['id']: tuple(ds['pos']) for ds in data['delivery_stations']}

    def is_obstacle(self, pos):
        """تحديد ما إذا كانت الخلية جداراً أو رفاً"""
        x, y = pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return pos in self.walls or pos in self.shelves

    def get_neighbors(self, pos):
        """إرجاع الجيران المتاحين للحركة (أعلى، أسفل، يسار، يمين)"""
        x, y = pos
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [p for p in candidates if not self.is_obstacle(p)]