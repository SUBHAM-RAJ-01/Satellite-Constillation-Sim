"""
Satellite entity with orbital parameters and geographical positioning
"""
import math
import random

class Satellite:
    def __init__(self, sat_id, orbit_altitude=550, inclination=53.0):
        self.id = sat_id
        # Add realistic altitude variation (±5km)
        self.orbit_altitude = orbit_altitude + random.uniform(-5, 5)  # km
        # Add slight inclination variation (±0.5°)
        self.inclination = inclination + random.uniform(-0.5, 0.5)  # degrees
        
        # Orbital parameters
        self.longitude = random.uniform(-180, 180)
        self.latitude = random.uniform(-90, 90)
        self.velocity = self._calculate_orbital_velocity()
        
        # Network parameters
        self.neighbors = []
        self.routing_table = {}
        self.load = 0
        self.active_connections = 0
        
    def _calculate_orbital_velocity(self):
        """Calculate orbital velocity based on altitude"""
        earth_radius = 6371  # km
        G = 6.674e-11  # gravitational constant
        M = 5.972e24  # Earth mass
        r = (earth_radius + self.orbit_altitude) * 1000  # convert to meters
        return math.sqrt(G * M / r) / 1000  # km/s
        
    def update_position(self, time_delta):
        """Update satellite position based on orbital mechanics"""
        # Simplified orbital propagation
        angular_velocity = self.velocity / (6371 + self.orbit_altitude)
        delta_longitude = math.degrees(angular_velocity * time_delta)
        self.longitude = (self.longitude + delta_longitude) % 360
        if self.longitude > 180:
            self.longitude -= 360
            
    def distance_to(self, other_satellite):
        """Calculate distance to another satellite"""
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_satellite.latitude), math.radians(other_satellite.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        earth_radius = 6371
        distance = c * earth_radius
        
        # Account for altitude difference
        alt_diff = abs(self.orbit_altitude - other_satellite.orbit_altitude)
        return math.sqrt(distance**2 + alt_diff**2)
        
    def can_communicate(self, other_satellite, max_range=5000):
        """Check if satellite can communicate with another"""
        # Add realistic range variation due to atmospheric conditions (±3%)
        actual_range = max_range * random.uniform(0.97, 1.03)
        return self.distance_to(other_satellite) <= actual_range
        
    def __repr__(self):
        return f"Sat-{self.id}({self.latitude:.1f}°, {self.longitude:.1f}°)"
