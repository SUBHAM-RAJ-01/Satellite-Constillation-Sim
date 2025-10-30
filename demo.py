"""
Demo script showing key features of the simulation
Quick demonstration of all components
"""

def demo_satellites():
    """Demonstrate satellite functionality"""
    print("\n" + "=" * 80)
    print("DEMO 1: Satellite Entities")
    print("=" * 80)
    
    from satellite import Satellite
    
    # Create sample satellites
    sat1 = Satellite(1, orbit_altitude=550, inclination=53.0)
    sat2 = Satellite(2, orbit_altitude=550, inclination=53.0)
    
    print(f"\nCreated two satellites:")
    print(f"  {sat1}")
    print(f"  {sat2}")
    
    distance = sat1.distance_to(sat2)
    can_comm = sat1.can_communicate(sat2)
    
    print(f"\nDistance between satellites: {distance:.2f} km")
    print(f"Can communicate: {can_comm}")
    print(f"Orbital velocity: {sat1.velocity:.2f} km/s")
    
    # Simulate position update
    sat1.update_position(60)  # 60 seconds
    print(f"\nAfter 60 seconds, {sat1}")

def demo_users():
    """Demonstrate user terminal functionality"""
    print("\n" + "=" * 80)
    print("DEMO 2: User Terminals")
    print("=" * 80)
    
    from user_terminal import UserTerminal
    from satellite import Satellite
    
    # Create user in different regions
    user1 = UserTerminal(1, "north_america")
    user2 = UserTerminal(2, "europe")
    user3 = UserTerminal(3, "asia")
    
    print(f"\nCreated users in different regions:")
    print(f"  {user1} - {user1.region}")
    print(f"  {user2} - {user2.region}")
    print(f"  {user3} - {user3.region}")
    
    # Create some satellites
    satellites = [Satellite(i, 550, 53.0) for i in range(10)]
    
    # Connect user to nearest satellite
    nearest = user1.find_nearest_satellite(satellites)
    if nearest:
        print(f"\n{user1} connected to {nearest}")
        print(f"Latency: {user1.latency:.2f} ms")

def demo_routing():
    """Demonstrate routing protocols"""
    print("\n" + "=" * 80)
    print("DEMO 3: Routing Protocols")
    print("=" * 80)
    
    from satellite import Satellite
    from routing_protocols import OSPFRouting, TSARouting
    
    # Create small constellation
    satellites = [Satellite(i, 550, 53.0) for i in range(20)]
    
    print(f"\nCreated constellation of {len(satellites)} satellites")
    
    # OSPF
    print("\n### OSPF Routing ###")
    ospf = OSPFRouting(satellites)
    ospf.build_topology()
    ospf.assign_areas(num_areas=2)
    
    route = ospf.calculate_route(satellites[0], satellites[10])
    print(f"Route from Sat-0 to Sat-10: {len(route)} hops")
    print(f"Path: {' -> '.join([f'Sat-{r}' for r in route[:5]])}...")
    
    # TSA
    print("\n### TSA Routing ###")
    tsa = TSARouting(satellites)
    tsa.build_topology()
    slots = tsa.assign_time_slots()
    
    print(f"Time slots assigned: {max(slots.values()) + 1} slots needed")
    print(f"Sat-0 slot: {slots[0]}, Sat-1 slot: {slots[1]}")

def demo_partitioning():
    """Demonstrate partitioning strategies"""
    print("\n" + "=" * 80)
    print("DEMO 4: Partitioning Strategies")
    print("=" * 80)
    
    from satellite import Satellite
    from partition_simulator import PartitionSimulator
    
    # Create satellites with varying loads
    satellites = []
    for i in range(100):
        sat = Satellite(i, 550, 53.0)
        sat.load = i % 20  # Varying load
        sat.active_connections = i % 5
        satellites.append(sat)
    
    print(f"\nCreated {len(satellites)} satellites with varying loads")
    
    simulator = PartitionSimulator(num_containers=5)
    
    # UTP
    print("\n### UTP Partitioning ###")
    utp_parts = simulator.partition_utp(satellites)
    utp_metrics = simulator.calculate_partition_metrics(utp_parts)
    
    print(f"Partitions: {len(utp_parts)}")
    print(f"Max load: {utp_metrics['max_load']}")
    print(f"Min load: {utp_metrics['min_load']}")
    print(f"Load imbalance: {utp_metrics['load_imbalance']:.2%}")
    
    # LBTP
    print("\n### LBTP Partitioning ###")
    lbtp_parts = simulator.partition_lbtp(satellites)
    lbtp_metrics = simulator.calculate_partition_metrics(lbtp_parts)
    
    print(f"Partitions: {len(lbtp_parts)}")
    print(f"Max load: {lbtp_metrics['max_load']}")
    print(f"Min load: {lbtp_metrics['min_load']}")
    print(f"Load imbalance: {lbtp_metrics['load_imbalance']:.2%}")
    
    improvement = (utp_metrics['load_imbalance'] - lbtp_metrics['load_imbalance']) / utp_metrics['load_imbalance']
    print(f"\nLBTP reduces imbalance by {improvement:.1%}")

def demo_performance_model():
    """Demonstrate performance model"""
    print("\n" + "=" * 80)
    print("DEMO 5: Performance Model")
    print("=" * 80)
    
    from simulation_model import SimulationModel
    
    model = SimulationModel()
    model.run_simulation()
    
    print(f"\nScenario: {model.N} satellites, {model.M} users, {model.k_star} containers")
    print(f"\nSerial execution time: {model.T_serial:.2f} minutes")
    print(f"Total CPU work: {model.C_total:.4e} cycles")
    print(f"Total memory: {model.R_total:.2f} GB")
    
    print(f"\nUTP parallel time: {model.T_parallel_UTP:.2f} minutes")
    print(f"UTP speedup: {model.Speedup_UTP:.2f}x")
    
    print(f"\nLBTP parallel time: {model.T_parallel_LBTP:.2f} minutes")
    print(f"LBTP speedup: {model.Speedup_LBTP:.2f}x")
    
    print(f"\nLBTP is {((model.Speedup_LBTP - model.Speedup_UTP) / model.Speedup_UTP * 100):.1f}% faster")

def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print(" " * 20 + "SIMULATION COMPONENT DEMOS")
    print("=" * 80)
    print("\nThis script demonstrates individual components of the simulation.")
    print("Each demo shows a specific feature in isolation.")
    print("=" * 80)
    
    try:
        demo_satellites()
        input("\nPress Enter to continue to next demo...")
        
        demo_users()
        input("\nPress Enter to continue to next demo...")
        
        demo_routing()
        input("\nPress Enter to continue to next demo...")
        
        demo_partitioning()
        input("\nPress Enter to continue to next demo...")
        
        demo_performance_model()
        
        print("\n" + "=" * 80)
        print("All demos completed!")
        print("=" * 80)
        print("\nNext steps:")
        print("  • Run 'python main.py' for full simulation")
        print("  • Read QUICKSTART.md for usage guide")
        print("  • Read PROJECT_INFO.md for technical details")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")

if __name__ == "__main__":
    main()
