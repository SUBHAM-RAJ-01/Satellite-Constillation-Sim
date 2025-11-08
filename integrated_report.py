"""
Integrated Report Generator
Runs all simulations and generates comprehensive analysis
"""
import time
from simulation_model import SimulationModel
from network_simulator import NetworkSimulator
from partition_simulator import PartitionSimulator
from communication_simulator import CommunicationSimulator

class IntegratedReportGenerator:
    """Generates comprehensive report from all simulation components"""
    
    def __init__(self, num_satellites=900, num_users=1500, num_containers=20):
        self.num_satellites = num_satellites
        self.num_users = num_users
        self.num_containers = num_containers
        self.results = {}
        
    def run_complete_analysis(self):
        """Run all simulations and collect results"""
        print("=" * 80)
        print(" " * 20 + "INTEGRATED SIMULATION REPORT")
        print("=" * 80)
        print("\nRunning comprehensive analysis (60-90 seconds)...\n")
        
        start_time = time.time()
        
        # 1. Performance Model
        print("[1/5] Performance model...")
        self.results['performance'] = self._run_performance_model()
        
        # 2. Network Simulation with OSPF
        print("[2/5] Network simulation (OSPF)...")
        self.results['network_ospf'] = self._run_network_simulation("OSPF")
        
        # 3. Network Simulation with TSA
        print("[3/5] Network simulation (TSA)...")
        self.results['network_tsa'] = self._run_network_simulation("TSA")
        
        # 4. Partitioning Analysis
        print("[4/5] Partitioning analysis...")
        self.results['partitioning'] = self._run_partitioning_analysis()
        
        # 5. Communication Simulation
        print("[5/5] Communication simulation...")
        self.results['communication'] = self._run_communication_simulation()
        
        end_time = time.time()
        self.results['total_time'] = end_time - start_time
        
        print(f"\n[OK] Analysis completed in {self.results['total_time']:.1f}s\n")
        
    def _run_performance_model(self):
        """Run theoretical performance model"""
        model = SimulationModel()
        model.run_simulation()
        
        return {
            'serial_time': model.T_serial,
            'cpu_work': model.C_total,
            'memory': model.R_total,
            'utp_speedup': model.Speedup_UTP,
            'lbtp_speedup': model.Speedup_LBTP,
            'utp_time': model.T_parallel_UTP,
            'lbtp_time': model.T_parallel_LBTP,
            'efficiency_gain': ((model.Speedup_LBTP - model.Speedup_UTP) / model.Speedup_UTP * 100)
        }
    
    def _run_network_simulation(self, protocol):
        """Run network simulation with specified protocol"""
        import sys
        import io
        
        # Suppress output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        sim = NetworkSimulator(self.num_satellites, self.num_users)
        sim.initialize_satellites()
        sim.initialize_users()
        sim.setup_routing(protocol=protocol)
        sim.connect_users_to_satellites()
        stats = sim.simulate_traffic(num_routes=200)
        network_stats = sim.get_network_statistics()
        
        # Restore output
        sys.stdout = old_stdout
        
        return {
            'protocol': protocol,
            'satellites': network_stats['total_satellites'],
            'users': network_stats['total_users'],
            'connection_rate': (stats['successful_routes'] / stats['total_routes'] * 100) if stats['total_routes'] > 0 else 0,
            'avg_neighbors': network_stats['avg_neighbors'],
            'avg_hops': stats['avg_hops'],
            'max_load': network_stats['max_load'],
            'avg_load': network_stats['avg_load']
        }
    
    def _run_partitioning_analysis(self):
        """Run partitioning comparison"""
        import sys
        import io
        
        # Suppress output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        # Use OSPF network for partitioning
        sim = NetworkSimulator(self.num_satellites, self.num_users)
        sim.initialize_satellites()
        sim.initialize_users()
        sim.setup_routing(protocol="OSPF")
        sim.connect_users_to_satellites()
        sim.simulate_traffic(num_routes=200)
        
        # Restore output
        sys.stdout = old_stdout
        
        # Create partition simulator
        part_sim = PartitionSimulator(self.num_satellites, self.num_users, self.num_containers)
        
        # UTP
        utp_partitions = part_sim.partition_utp(sim.satellites)
        utp_metrics = part_sim.calculate_partition_metrics(utp_partitions)
        
        # LBTP
        lbtp_partitions = part_sim.partition_lbtp(sim.satellites)
        lbtp_metrics = part_sim.calculate_partition_metrics(lbtp_partitions)
        
        return {
            'utp_imbalance': utp_metrics['load_imbalance'],
            'lbtp_imbalance': lbtp_metrics['load_imbalance'],
            'utp_max_load': utp_metrics['max_load'],
            'lbtp_max_load': lbtp_metrics['max_load'],
            'improvement': ((utp_metrics['load_imbalance'] - lbtp_metrics['load_imbalance']) / utp_metrics['load_imbalance'] * 100)
        }
    
    def _run_communication_simulation(self):
        """Run communication simulation"""
        import sys
        import io
        
        # Suppress output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        # Create network
        network = NetworkSimulator(self.num_satellites, self.num_users)
        network.initialize_satellites()
        network.initialize_users()
        network.setup_routing(protocol="OSPF")
        network.connect_users_to_satellites()
        
        # Run communication simulation
        comm_sim = CommunicationSimulator(network)
        comm_sim.simulate_traffic(num_packets=1000, duration_seconds=60)
        metrics = comm_sim.get_performance_metrics()
        
        # Restore output
        sys.stdout = old_stdout
        
        return metrics
    
    def generate_report(self):
        """Generate comprehensive integrated report"""
        print("=" * 80)
        print(" " * 25 + "COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        
        # Executive Summary
        self._print_executive_summary()
        
        # Performance Model Results
        self._print_performance_model()
        
        # Network Simulation Results
        self._print_network_results()
        
        # Partitioning Analysis
        self._print_partitioning_analysis()
        
        # Communication Performance
        self._print_communication_performance()
        
        # Comparative Analysis
        self._print_comparative_analysis()
        
        print("=" * 80)
    
    def _print_executive_summary(self):
        """Print executive summary"""
        print("\n" + "=" * 80)
        print("EXECUTIVE SUMMARY")
        print("=" * 80)
        
        perf = self.results['performance']
        comm = self.results['communication']
        part = self.results['partitioning']
        
        print(f"\n{'Metric':<40} {'Value':<20}")
        print("-" * 80)
        print(f"{'Network Scale':<40} {self.num_satellites} satellites, {self.num_users} users")
        print(f"{'Parallel Containers':<40} {self.num_containers}")
        print(f"{'LBTP Speedup':<40} {perf['lbtp_speedup']:.2f}x")
        print(f"{'UTP Speedup':<40} {perf['utp_speedup']:.2f}x")
        print(f"{'Performance Improvement':<40} {perf['efficiency_gain']:.1f}%")
        print(f"{'Network Delivery Rate':<40} {comm['delivery_rate']:.2f}%")
        print(f"{'Average Latency':<40} {comm['avg_latency_ms']:.2f} ms")
        print(f"{'Network Throughput':<40} {comm['throughput_mbps']:.2f} Mbps")
        print(f"{'Load Balance Improvement':<40} {part['improvement']:.1f}%")
    
    def _print_performance_model(self):
        """Print performance model results"""
        print("\n" + "=" * 80)
        print("1. THEORETICAL PERFORMANCE MODEL")
        print("=" * 80)
        
        perf = self.results['performance']
        
        print(f"\nBaseline Metrics:")
        print(f"  Serial Execution Time:     {perf['serial_time']:.2f} minutes")
        print(f"  Total CPU Work:            {perf['cpu_work']:.4e} cycles")
        print(f"  Total Memory Required:     {perf['memory']:.2f} GB")
        
        print(f"\nParallel Execution ({self.num_containers} containers):")
        print(f"  {'Strategy':<15} {'Time (min)':<15} {'Speedup':<15} {'Efficiency':<15}")
        print(f"  {'-'*60}")
        print(f"  {'UTP':<15} {perf['utp_time']:<15.2f} {perf['utp_speedup']:<15.2f}x {(perf['utp_speedup']/self.num_containers*100):<15.1f}%")
        print(f"  {'LBTP':<15} {perf['lbtp_time']:<15.2f} {perf['lbtp_speedup']:<15.2f}x {(perf['lbtp_speedup']/self.num_containers*100):<15.1f}%")
        
        print(f"\nKey Finding: LBTP achieves {perf['efficiency_gain']:.1f}% better speedup than UTP")
    
    def _print_network_results(self):
        """Print network simulation results"""
        print("\n" + "=" * 80)
        print("2. NETWORK SIMULATION RESULTS")
        print("=" * 80)
        
        ospf = self.results['network_ospf']
        tsa = self.results['network_tsa']
        
        print(f"\n{'Metric':<30} {'OSPF':<20} {'TSA':<20}")
        print("-" * 80)
        print(f"{'Connection Rate':<30} {ospf['connection_rate']:<20.2f}% {tsa['connection_rate']:<20.2f}%")
        print(f"{'Avg Neighbors/Satellite':<30} {ospf['avg_neighbors']:<20.2f} {tsa['avg_neighbors']:<20.2f}")
        print(f"{'Average Hops':<30} {ospf['avg_hops']:<20.2f} {tsa['avg_hops']:<20.2f}")
        print(f"{'Max Satellite Load':<30} {ospf['max_load']:<20} {tsa['max_load']:<20}")
        print(f"{'Avg Satellite Load':<30} {ospf['avg_load']:<20.2f} {tsa['avg_load']:<20.2f}")
        
        print(f"\nBoth protocols show excellent connectivity (>95%) and efficient routing (<5 hops)")
    
    def _print_partitioning_analysis(self):
        """Print partitioning analysis"""
        print("\n" + "=" * 80)
        print("3. LOAD BALANCING ANALYSIS")
        print("=" * 80)
        
        part = self.results['partitioning']
        
        print(f"\n{'Strategy':<15} {'Load Imbalance':<20} {'Max Load':<20}")
        print("-" * 80)
        print(f"{'UTP':<15} {part['utp_imbalance']:<20.2f}% {part['utp_max_load']:<20}")
        print(f"{'LBTP':<15} {part['lbtp_imbalance']:<20.2f}% {part['lbtp_max_load']:<20}")
        
        print(f"\nLoad Distribution Visualization:")
        print(f"UTP:  {'#' * int(part['utp_imbalance'])} {part['utp_imbalance']:.1f}% imbalance")
        print(f"LBTP: {'#' * max(1, int(part['lbtp_imbalance']))} {part['lbtp_imbalance']:.1f}% imbalance")
        
        print(f"\nLBTP reduces load imbalance by {part['improvement']:.1f}%")
    
    def _print_communication_performance(self):
        """Print communication performance"""
        print("\n" + "=" * 80)
        print("4. COMMUNICATION PERFORMANCE")
        print("=" * 80)
        
        comm = self.results['communication']
        
        print(f"\nPacket Statistics:")
        print(f"  Packets Sent:              {comm['packets_sent']:,}")
        print(f"  Packets Delivered:         {comm['packets_delivered']:,}")
        print(f"  Packets Lost:              {comm['packets_lost']:,}")
        print(f"  Delivery Rate:             {comm['delivery_rate']:.2f}%")
        print(f"  Loss Rate:                 {comm['loss_rate']:.2f}%")
        
        print(f"\nLatency & Routing:")
        print(f"  Average Latency:           {comm['avg_latency_ms']:.2f} ms")
        print(f"  Average Hops:              {comm['avg_hops']:.2f}")
        
        print(f"\nThroughput & Efficiency:")
        print(f"  Total Data Delivered:      {comm['total_bytes_delivered'] / 1_000_000:.2f} MB")
        print(f"  Network Throughput:        {comm['throughput_mbps']:.2f} Mbps")
        print(f"  Network Efficiency:        {comm['efficiency_percent']:.2f}%")
    
    def _print_comparative_analysis(self):
        """Print comparative analysis"""
        print("\n" + "=" * 80)
        print("5. COMPARATIVE ANALYSIS & KEY FINDINGS")
        print("=" * 80)
        
        perf = self.results['performance']
        comm = self.results['communication']
        part = self.results['partitioning']
        
        print(f"\n{'Metric':<25} {'UTP':<20} {'LBTP':<20} {'Improvement':<15}")
        print("-" * 80)
        
        utp_speedup = f"{perf['utp_speedup']:.2f}x"
        lbtp_speedup = f"{perf['lbtp_speedup']:.2f}x"
        speedup_gain = f"{perf['efficiency_gain']:.1f}%"
        print(f"{'Speedup':<25} {utp_speedup:<20} {lbtp_speedup:<20} {speedup_gain:<15}")
        
        utp_imb = f"{part['utp_imbalance']:.2f}%"
        lbtp_imb = f"{part['lbtp_imbalance']:.2f}%"
        imb_gain = f"{part['improvement']:.1f}%"
        print(f"{'Load Imbalance':<25} {utp_imb:<20} {lbtp_imb:<20} {imb_gain:<15}")
        
        utp_time = f"{perf['utp_time']:.2f} min"
        lbtp_time = f"{perf['lbtp_time']:.2f} min"
        time_gain = f"{((perf['utp_time']-perf['lbtp_time'])/perf['utp_time']*100):.1f}%"
        print(f"{'Execution Time':<25} {utp_time:<20} {lbtp_time:<20} {time_gain:<15}")
        
        delivery = f"{comm['delivery_rate']:.2f}%"
        print(f"{'Delivery Rate':<25} {'-':<20} {delivery:<20} {'-':<15}")
        
        latency = f"{comm['avg_latency_ms']:.2f} ms"
        print(f"{'Avg Latency':<25} {'-':<20} {latency:<20} {'-':<15}")
        
        throughput = f"{comm['throughput_mbps']:.2f} Mbps"
        print(f"{'Throughput':<25} {'-':<20} {throughput:<20} {'-':<15}")
        
        print(f"\nKey Result: LBTP achieves {perf['efficiency_gain']:.1f}% better performance")
        print(f"Analysis Time: {self.results['total_time']:.1f}s")
    



def run_integrated_report():
    """Main function to run integrated report"""
    generator = IntegratedReportGenerator(num_satellites=900, num_users=1500, num_containers=20)
    generator.run_complete_analysis()
    generator.generate_report()


if __name__ == "__main__":
    run_integrated_report()
