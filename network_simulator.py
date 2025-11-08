"""
Network simulator integrating satellites, users, and routing protocols
"""
import random
from satellite import Satellite
from user_terminal import UserTerminal
from routing_protocols import TSARouting, OSPFRouting

class NetworkSimulator:
    def __init__(self, num_satellites=900, num_users=1500):
        self.num_satellites = num_satellites
        self.num_users = num_users
        self.satellites = []
        self.users = []
        self.current_time = 0
        self.routing_protocol = None
        
    def initialize_satellites(self):
        """Create satellite constellation"""
        print(f"Initializing {self.num_satellites} satellites...")
        
        # Create satellites in different orbital shells with realistic variations
        shells = [
            (550, 53.0, 0.4),   # Shell 1: 550km, 53° inclination
            (570, 53.2, 0.3),   # Shell 2: 570km, 53.2° inclination
            (560, 70.0, 0.3),   # Shell 3: 560km, 70° inclination
        ]
        
        # Randomize shell distribution slightly (realistic deployment variations)
        shell_weights = [random.uniform(0.3, 0.5) for _ in shells]
        total_weight = sum(shell_weights)
        shell_weights = [w/total_weight for w in shell_weights]
        
        for i in range(self.num_satellites):
            # Choose shell with weighted randomization
            shell_idx = random.choices(range(len(shells)), weights=shell_weights)[0]
            shell = shells[shell_idx]
            altitude, inclination, _ = shell
            sat = Satellite(i, altitude, inclination)
            self.satellites.append(sat)
            
        print(f"[OK] Created {len(self.satellites)} satellites")
        
    def initialize_users(self):
        """Create user terminals in different regions"""
        print(f"Initializing {self.num_users} user terminals...")
        
        regions = ["north_america", "europe", "asia", "south_america", "africa", "oceania"]
        
        # Realistic population distribution (some regions have more users)
        region_weights = [
            0.25,  # North America
            0.20,  # Europe
            0.30,  # Asia (highest population)
            0.10,  # South America
            0.08,  # Africa
            0.07,  # Oceania
        ]
        
        # Add small random variation to weights (±10%)
        region_weights = [w * random.uniform(0.9, 1.1) for w in region_weights]
        total = sum(region_weights)
        region_weights = [w/total for w in region_weights]
        
        for i in range(self.num_users):
            region = random.choices(regions, weights=region_weights)[0]
            user = UserTerminal(i, region)
            self.users.append(user)
            
        print(f"[OK] Created {len(self.users)} user terminals")
        
    def setup_routing(self, protocol="OSPF"):
        """Setup routing protocol"""
        print(f"Setting up {protocol} routing protocol...")
        
        if protocol == "TSA":
            self.routing_protocol = TSARouting(self.satellites)
            topology = self.routing_protocol.build_topology()
            slots = self.routing_protocol.assign_time_slots()
            print(f"[OK] TSA topology built with {len(topology)} nodes")
            print(f"[OK] Assigned {max(slots.values()) + 1} time slots")
        elif protocol == "OSPF":
            self.routing_protocol = OSPFRouting(self.satellites)
            link_states = self.routing_protocol.build_topology()
            areas = self.routing_protocol.assign_areas()
            print(f"[OK] OSPF topology built with {len(link_states)} nodes")
            print(f"[OK] Network divided into {max(areas.values()) + 1} areas")
        else:
            raise ValueError(f"Unknown protocol: {protocol}")
            
    def connect_users_to_satellites(self):
        """Connect each user to nearest satellite"""
        print("Connecting users to satellites...")
        
        connected = 0
        for user in self.users:
            if user.find_nearest_satellite(self.satellites):
                connected += 1
                
        print(f"[OK] Connected {connected}/{len(self.users)} users to satellites")
        
    def simulate_traffic(self, num_routes=100):
        """Simulate network traffic and routing"""
        print(f"\nSimulating {num_routes} routes...")
        
        total_hops = 0
        successful_routes = 0
        
        for _ in range(num_routes):
            source = random.choice(self.satellites)
            dest = random.choice(self.satellites)
            
            path = self.routing_protocol.calculate_route(source, dest)
            
            if len(path) > 1:
                successful_routes += 1
                total_hops += len(path) - 1
                
                # Update satellite loads with realistic traffic variation
                for sat_id in path:
                    sat = next(s for s in self.satellites if s.id == sat_id)
                    # Traffic load varies (1-3 units per route)
                    sat.load += random.randint(1, 3)
                    
        avg_hops = total_hops / successful_routes if successful_routes > 0 else 0
        
        print(f"[OK] Successful routes: {successful_routes}/{num_routes}")
        print(f"[OK] Average hops per route: {avg_hops:.2f}")
        
        return {
            'successful_routes': successful_routes,
            'total_routes': num_routes,
            'avg_hops': avg_hops
        }
        
    def get_network_statistics(self):
        """Calculate network statistics"""
        total_links = sum(len(sat.neighbors) for sat in self.satellites)
        avg_neighbors = total_links / len(self.satellites)
        
        loads = [sat.load for sat in self.satellites]
        max_load = max(loads) if loads else 0
        avg_load = sum(loads) / len(loads) if loads else 0
        
        connections = [sat.active_connections for sat in self.satellites]
        max_connections = max(connections) if connections else 0
        avg_connections = sum(connections) / len(connections) if connections else 0
        
        return {
            'total_satellites': len(self.satellites),
            'total_users': len(self.users),
            'avg_neighbors': avg_neighbors,
            'max_load': max_load,
            'avg_load': avg_load,
            'max_connections': max_connections,
            'avg_connections': avg_connections
        }
        
    def run_simulation(self, protocol="OSPF", duration=100):
        """Run complete network simulation"""
        print("=" * 80)
        print("SATELLITE NETWORK SIMULATION")
        print("=" * 80)
        print()
        
        self.initialize_satellites()
        self.initialize_users()
        self.setup_routing(protocol)
        self.connect_users_to_satellites()
        
        traffic_stats = self.simulate_traffic(duration)
        network_stats = self.get_network_statistics()
        
        print("\n" + "=" * 80)
        print("NETWORK STATISTICS")
        print("=" * 80)
        print(f"Total Satellites:        {network_stats['total_satellites']}")
        print(f"Total Users:             {network_stats['total_users']}")
        print(f"Avg Neighbors/Satellite: {network_stats['avg_neighbors']:.2f}")
        print(f"Max Satellite Load:      {network_stats['max_load']}")
        print(f"Avg Satellite Load:      {network_stats['avg_load']:.2f}")
        print(f"Max Connections:         {network_stats['max_connections']}")
        print(f"Avg Connections:         {network_stats['avg_connections']:.2f}")
        print("=" * 80)
        
        return {**traffic_stats, **network_stats}


if __name__ == "__main__":
    # Run with OSPF
    print("\n### OSPF ROUTING ###\n")
    sim_ospf = NetworkSimulator(num_satellites=900, num_users=1500)
    ospf_results = sim_ospf.run_simulation(protocol="OSPF", duration=100)
    
    print("\n\n### TSA ROUTING ###\n")
    sim_tsa = NetworkSimulator(num_satellites=900, num_users=1500)
    tsa_results = sim_tsa.run_simulation(protocol="TSA", duration=100)
