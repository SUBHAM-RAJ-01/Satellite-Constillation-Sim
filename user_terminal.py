"""
User terminal entity with geographical location
"""
import random

class UserTerminal:
    def __init__(self, user_id, region="random"):
        self.id = user_id
        self.region = region
        
        # Geographical location
        if region == "random":
            self.latitude = random.uniform(-60, 60)  # Most population
            self.longitude = random.uniform(-180, 180)
        else:
            self.latitude, self.longitude = self._get_region_coords(region)
            
        # Network parameters
        self.connected_satellite = None
        self.data_rate = 0
        self.latency = 0
        self.packet_loss = 0
        
    def _get_region_coords(self, region):
        """Get approximate coordinates for major regions"""
        regions = {
            "north_america": (40.0, -100.0),
            "europe": (50.0, 10.0),
            "asia": (35.0, 105.0),
            "south_america": (-15.0, -60.0),
            "africa": (0.0, 20.0),
            "oceania": (-25.0, 135.0)
        }
        base_lat, base_lon = regions.get(region, (0.0, 0.0))
        return (
            base_lat + random.uniform(-10, 10),
            base_lon + random.uniform(-15, 15)
        )
        
    def find_nearest_satellite(self, satellites):
        """Find and connect to nearest visible satellite"""
        import math
        import random
        
        min_distance = float('inf')
        nearest_sat = None
        
        for sat in satellites:
            # Calculate distance
            lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
            lat2, lon2 = math.radians(sat.latitude), math.radians(sat.longitude)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            distance = c * 6371
            
            # Check elevation angle (simplified) with weather variation
            max_range = 3000 * random.uniform(0.95, 1.05)  # ±5% due to weather
            if distance < min_distance and distance < max_range:
                min_distance = distance
                nearest_sat = sat
                
        self.connected_satellite = nearest_sat
        if nearest_sat:
            nearest_sat.active_connections += 1
            # Add realistic latency variation (processing delays, atmospheric effects)
            base_latency = min_distance / 300000 * 1000  # Speed of light, ms
            self.latency = base_latency * random.uniform(1.05, 1.15)  # +5-15% overhead
            
        return nearest_sat
        
    def __repr__(self):
        return f"User-{self.id}({self.latitude:.1f}°, {self.longitude:.1f}°)"
