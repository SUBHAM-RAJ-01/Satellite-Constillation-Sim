"""
Mega-Constellation Parallel Simulation Modeler
Compares LBTP vs UTP network partitioning strategies
"""

class SimulationModel:
    def __init__(self):
        import random
        
        # Scenario parameters
        self.N = 900  # satellites
        self.M = 1500  # users
        self.T_sim = 5400  # seconds
        self.T_sim_min = 90  # minutes
        
        # CPU fit coefficients with realistic variation (±2%)
        self.a1 = 106.7e9 * random.uniform(0.98, 1.02)
        self.b1 = 33.69e9 * random.uniform(0.98, 1.02)
        self.c1 = 102.6e9 * random.uniform(0.98, 1.02)
        
        # Memory fit coefficients with realistic variation (±3%)
        self.a2 = 164559 * random.uniform(0.97, 1.03)
        self.b2 = 54203 * random.uniform(0.97, 1.03)
        self.c2 = 30576 * random.uniform(0.97, 1.03)
        
        # Hardware parameters with realistic variation
        self.C_rate = 3.6e10 * random.uniform(0.98, 1.02)  # CPU speed varies
        self.k_star = 20  # containers
        
        # Load imbalance factors with realistic variation
        # LBTP: 4-6% (very good load balancing)
        self.LBTP_LBF = random.uniform(0.04, 0.06)
        # UTP: 28-32% (poor load balancing)
        self.UTP_LBF = random.uniform(0.28, 0.32)
        
    def calculate_baseline_metrics(self):
        """Calculate serial execution baseline metrics"""
        # Total CPU work (cycles)
        self.C_total = (self.a1 * self.N + self.b1 * self.M + self.c1) * 1.0
        
        # Total memory usage (convert KB to GB)
        R_total_KB = self.a2 * self.N + self.b2 * self.M + self.c2
        self.R_total = R_total_KB / (1024 * 1024)  # KB to GB
        
        # Serial simulation time (minutes)
        self.T_serial = (self.C_total / self.C_rate) / 60
        
        # Average container load
        self.C_average = self.C_total / self.k_star
        
    def calculate_utp_performance(self):
        """Model UTP (Uniform Topology Partitioning) performance"""
        self.C_max_UTP = self.C_average * (1 + self.UTP_LBF)
        self.T_parallel_UTP = (self.C_max_UTP / self.C_rate) / 60  # minutes
        self.Speedup_UTP = self.T_serial / self.T_parallel_UTP
        
    def calculate_lbtp_performance(self):
        """Model LBTP (Load Balancing based Topology Partitioning) performance"""
        self.C_max_LBTP = self.C_average * (1 + self.LBTP_LBF)
        self.T_parallel_LBTP = (self.C_max_LBTP / self.C_rate) / 60  # minutes
        self.Speedup_LBTP = self.T_serial / self.T_parallel_LBTP
        
    def run_simulation(self):
        """Execute complete simulation analysis"""
        self.calculate_baseline_metrics()
        self.calculate_utp_performance()
        self.calculate_lbtp_performance()
        
    def generate_report(self):
        """Generate comprehensive output report"""
        print("=" * 80)
        print("MEGA-CONSTELLATION PARALLEL SIMULATION MODELER")
        print("=" * 80)
        print()
        
        # Part 1: Project Overview
        print("1. PROJECT OVERVIEW")
        print("-" * 80)
        print(f"Scenario Parameters:")
        print(f"  Satellites (N):           {self.N}")
        print(f"  Users (M):                {self.M}")
        print(f"  Containers (k*):          {self.k_star}")
        print(f"  Simulation Time:          {self.T_sim_min} minutes ({self.T_sim} seconds)")
        print()
        print(f"Baseline Metrics:")
        print(f"  Total CPU Work (C_total): {self.C_total:.4e} cycles")
        print(f"  Total Memory (R_total):   {self.R_total:.2f} GB")
        print(f"  Serial Time (T_serial):   {self.T_serial:.2f} minutes")
        print()
        
        # Part 2: Load Distribution Comparison
        print("2. LOAD DISTRIBUTION COMPARISON")
        print("-" * 80)
        print(f"{'Strategy':<10} {'Load Imbalance (ζ)':<25} {'Max Container Load':<25} {'Parallel Time':<20}")
        print(f"{'':10} {'':25} {'(cycles)':<25} {'(minutes)':<20}")
        print("-" * 80)
        print(f"{'UTP':<10} {self.UTP_LBF:<25.2%} {self.C_max_UTP:<25.4e} {self.T_parallel_UTP:<20.2f}")
        print(f"{'LBTP':<10} {self.LBTP_LBF:<25.2%} {self.C_max_LBTP:<25.4e} {self.T_parallel_LBTP:<20.2f}")
        print()
        
        # Part 3: Final Speedup Analysis
        print("3. FINAL SPEEDUP ANALYSIS")
        print("-" * 80)
        print(f"UTP Speedup:  {self.Speedup_UTP:.2f}x")
        print(f"LBTP Speedup: {self.Speedup_LBTP:.2f}x")
        print()
        print(f"Efficiency Gain: LBTP achieves {((self.Speedup_LBTP - self.Speedup_UTP) / self.Speedup_UTP * 100):.1f}% better speedup than UTP")
        print(f"Time Saved:      {(self.T_parallel_UTP - self.T_parallel_LBTP):.2f} minutes per simulation")
        print("=" * 80)


if __name__ == "__main__":
    model = SimulationModel()
    model.run_simulation()
    model.generate_report()
