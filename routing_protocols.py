"""
Routing protocol implementations: TSA and OSPF
"""
import heapq
import random
from collections import defaultdict

class TSARouting:
    """Time-Slotted Assignment (TSA) routing for satellite networks"""
    
    def __init__(self, satellites):
        self.satellites = satellites
        self.time_slots = {}
        self.slot_duration = 10  # seconds
        
    def build_topology(self):
        """Build network topology based on satellite visibility"""
        topology = defaultdict(list)
        
        for sat in self.satellites:
            sat.neighbors = []
            for other_sat in self.satellites:
                if sat.id != other_sat.id and sat.can_communicate(other_sat):
                    sat.neighbors.append(other_sat)
                    topology[sat.id].append(other_sat.id)
                    
        return topology
        
    def assign_time_slots(self):
        """Assign time slots to avoid interference"""
        slot_assignment = {}
        current_slot = 0
        
        # Graph coloring approach for time slot assignment
        for sat in self.satellites:
            neighbor_slots = set()
            for neighbor in sat.neighbors:
                if neighbor.id in slot_assignment:
                    neighbor_slots.add(slot_assignment[neighbor.id])
                    
            # Find first available slot
            slot = 0
            while slot in neighbor_slots:
                slot += 1
            slot_assignment[sat.id] = slot
            
        self.time_slots = slot_assignment
        return slot_assignment
        
    def calculate_route(self, source_sat, dest_sat):
        """Calculate route using time-aware shortest path"""
        if source_sat == dest_sat:
            return [source_sat]
            
        # Dijkstra's algorithm with time slot awareness
        distances = {sat.id: float('inf') for sat in self.satellites}
        distances[source_sat.id] = 0
        previous = {}
        pq = [(0, source_sat.id)]
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_id == dest_sat.id:
                break
                
            current_sat = next(s for s in self.satellites if s.id == current_id)
            
            for neighbor in current_sat.neighbors:
                # Time slot penalty with realistic jitter
                slot_penalty = abs(self.time_slots.get(current_id, 0) - 
                                 self.time_slots.get(neighbor.id, 0))
                # Add link quality variation (±10%)
                link_quality = random.uniform(0.9, 1.1)
                distance = (current_sat.distance_to(neighbor) + slot_penalty * 100) * link_quality
                new_dist = current_dist + distance
                
                if new_dist < distances[neighbor.id]:
                    distances[neighbor.id] = new_dist
                    previous[neighbor.id] = current_id
                    heapq.heappush(pq, (new_dist, neighbor.id))
                    
        # Reconstruct path
        path = []
        current = dest_sat.id
        while current in previous:
            path.insert(0, current)
            current = previous[current]
        path.insert(0, source_sat.id)
        
        return path


class OSPFRouting:
    """Open Shortest Path First (OSPF) routing for satellite networks"""
    
    def __init__(self, satellites):
        self.satellites = satellites
        self.link_state_db = {}
        self.areas = {}
        
    def build_topology(self):
        """Build OSPF topology with link states"""
        for sat in self.satellites:
            sat.neighbors = []
            link_states = []
            
            for other_sat in self.satellites:
                if sat.id != other_sat.id and sat.can_communicate(other_sat):
                    sat.neighbors.append(other_sat)
                    cost = sat.distance_to(other_sat) / 1000  # Normalize
                    link_states.append({
                        'neighbor': other_sat.id,
                        'cost': cost,
                        'bandwidth': 1000 / (cost + 1)  # Mbps
                    })
                    
            self.link_state_db[sat.id] = link_states
            
        return self.link_state_db
        
    def assign_areas(self, num_areas=4):
        """Divide network into OSPF areas"""
        sats_per_area = len(self.satellites) // num_areas
        
        for i, sat in enumerate(self.satellites):
            area_id = i // sats_per_area
            if area_id >= num_areas:
                area_id = num_areas - 1
            self.areas[sat.id] = area_id
            
        return self.areas
        
    def calculate_route(self, source_sat, dest_sat):
        """Calculate route using OSPF SPF algorithm"""
        if source_sat == dest_sat:
            return [source_sat]
            
        # Dijkstra's algorithm with link costs
        distances = {sat.id: float('inf') for sat in self.satellites}
        distances[source_sat.id] = 0
        previous = {}
        pq = [(0, source_sat.id)]
        visited = set()
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_id in visited:
                continue
            visited.add(current_id)
            
            if current_id == dest_sat.id:
                break
                
            # Get link states for current satellite
            link_states = self.link_state_db.get(current_id, [])
            
            for link in link_states:
                neighbor_id = link['neighbor']
                if neighbor_id in visited:
                    continue
                    
                # Add realistic cost variation (congestion, interference ±8%)
                cost = link['cost'] * random.uniform(0.92, 1.08)
                new_dist = current_dist + cost
                
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_id
                    heapq.heappush(pq, (new_dist, neighbor_id))
                    
        # Reconstruct path
        path = []
        current = dest_sat.id
        while current in previous:
            path.insert(0, current)
            current = previous[current]
        if path or source_sat.id == dest_sat.id:
            path.insert(0, source_sat.id)
        
        return path
