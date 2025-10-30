"""
Partition simulator integrating network simulation with LBTP/UTP comparison
"""
from network_simulator import NetworkSimulator
from simulation_model import SimulationModel

class PartitionSimulator:
    def __init__(self, num_satellites=900, num_users=1500, num_containers=20):
        self.num_satellites = num_satellites
        self.num_users = num_users
        self.num_containers = num_containers
        
    def partition_utp(self, satellites):
        """Uniform Topology Partitioning - naive approach"""
        partitions = [[] for _ in range(self.num_containers)]
        
        # Simple round-robin assignment
        for i, sat in enumerate(satellites):
            partition_id = i % self.num_containers
            partitions[partition_id].append(sat)
            
        return partitions
        
    def partition_lbtp(self, satellites):
        """Load Balancing based Topology Partitioning"""
        import random
        
        partitions = [[] for _ in range(self.num_containers)]
        partition_loads = [0] * self.num_containers
        
        # Sort satellites by load (connections + routing load)
        sorted_sats = sorted(satellites, 
                           key=lambda s: s.active_connections + s.load, 
                           reverse=True)
        
        # Assign to least loaded partition with small randomization
        # to simulate real-world scheduling variations
        for sat in sorted_sats:
            # Find partitions with lowest loads
            min_load = min(partition_loads)
            candidates = [i for i, load in enumerate(partition_loads) 
                         if load <= min_load * 1.05]  # Within 5% of minimum
            
            # Choose randomly among good candidates (realistic scheduler behavior)
            min_load_idx = random.choice(candidates) if candidates else 0
            
            partitions[min_load_idx].append(sat)
            partition_loads[min_load_idx] += sat.active_connections + sat.load
            
        return partitions
        
    def calculate_partition_metrics(self, partitions):
        """Calculate load distribution metrics"""
        loads = []
        for partition in partitions:
            load = sum(sat.active_connections + sat.load for sat in partition)
            loads.append(load)
            
        max_load = max(loads) if loads else 0
        min_load = min(loads) if loads else 0
        avg_load = sum(loads) / len(loads) if loads else 0
        
        load_imbalance = (max_load - avg_load) / avg_load if avg_load > 0 else 0
        
        return {
            'max_load': max_load,
            'min_load': min_load,
            'avg_load': avg_load,
            'load_imbalance': load_imbalance,
            'loads': loads
        }
        
    def run_comparison(self, protocol="OSPF"):
        """Run complete comparison of UTP vs LBTP"""
        print("=" * 80)
        print("INTEGRATED PARTITION AND NETWORK SIMULATION")
        print("=" * 80)
        print()
        
        # Run network simulation
        sim = NetworkSimulator(self.num_satellites, self.num_users)
        sim.run_simulation(protocol=protocol, duration=200)
        
        print("\n" + "=" * 80)
        print("PARTITIONING COMPARISON")
        print("=" * 80)
        
        # UTP Partitioning
        print("\n### UTP (Uniform Topology Partitioning) ###")
        utp_partitions = self.partition_utp(sim.satellites)
        utp_metrics = self.calculate_partition_metrics(utp_partitions)
        
        print(f"Max Load:        {utp_metrics['max_load']}")
        print(f"Min Load:        {utp_metrics['min_load']}")
        print(f"Avg Load:        {utp_metrics['avg_load']:.2f}")
        print(f"Load Imbalance:  {utp_metrics['load_imbalance']:.2%}")
        
        # LBTP Partitioning
        print("\n### LBTP (Load Balancing based Topology Partitioning) ###")
        lbtp_partitions = self.partition_lbtp(sim.satellites)
        lbtp_metrics = self.calculate_partition_metrics(lbtp_partitions)
        
        print(f"Max Load:        {lbtp_metrics['max_load']}")
        print(f"Min Load:        {lbtp_metrics['min_load']}")
        print(f"Avg Load:        {lbtp_metrics['avg_load']:.2f}")
        print(f"Load Imbalance:  {lbtp_metrics['load_imbalance']:.2%}")
        
        # Performance model
        print("\n" + "=" * 80)
        print("PERFORMANCE MODEL ANALYSIS")
        print("=" * 80)
        print()
        
        model = SimulationModel()
        model.run_simulation()
        model.generate_report()
        
        # Summary comparison
        print("\n" + "=" * 80)
        print("SUMMARY: ACTUAL vs THEORETICAL")
        print("=" * 80)
        print(f"{'Metric':<30} {'UTP':<20} {'LBTP':<20}")
        print("-" * 80)
        print(f"{'Actual Load Imbalance':<30} {utp_metrics['load_imbalance']:<20.2%} {lbtp_metrics['load_imbalance']:<20.2%}")
        print(f"{'Theoretical Load Imbalance':<30} {model.UTP_LBF:<20.2%} {model.LBTP_LBF:<20.2%}")
        print(f"{'Theoretical Speedup':<30} {model.Speedup_UTP:<20.2f}x {model.Speedup_LBTP:<20.2f}x")
        print("=" * 80)


if __name__ == "__main__":
    simulator = PartitionSimulator(num_satellites=900, num_users=1500, num_containers=20)
    simulator.run_comparison(protocol="OSPF")
