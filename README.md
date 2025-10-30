# 🛰️ Mega-Constellation Parallel Simulation Modeler

> **Intelligent load balancing for satellite network simulations - achieving 24% better performance**

## 🎯 What This Does

Simulates **900 satellites** and **1500 users** to compare two work distribution strategies:

- **UTP (Simple)**: Round-robin assignment → 15.4x speedup
- **LBTP (Smart)**: Load-aware assignment → **19.0x speedup (24% better!)**

```
┌─────────────────────────────────────────────────────────────┐
│                     SIMULATION ARCHITECTURE                 │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌─────────────────────┐       ┌─────────────────────┐
│  Performance Model  │       │  Network Simulation │
│   (Theoretical)     │       │     (Realistic)     │
│                     │       │                     │
│ • CPU Calculation   │       │ • 900 Satellites    │
│ • Memory Estimation │       │ • 1500 Users        │
│ • Speedup Analysis  │       │ • TSA/OSPF Routing  │
└─────────────────────┘       └─────────────────────┘
```

## 🚀 Quick Start

```bash
# Performance model only (1 second)
python main.py model

# Full simulation (30 seconds)
python main.py ospf

# Interactive demos
python demo.py
```

## 📊 Key Results

```
Strategy | Load Balance | Speedup | Efficiency | Time Saved
---------|--------------|---------|------------|------------
UTP      | 30% imbalance| 15.4x   | 77%        | -
LBTP     | 5% imbalance | 19.0x   | 95%        | 0.85 min
```

**Load Distribution Visualization:**

```
UTP (Unbalanced):
Container 1: ████████████████████████████████ (3200 load)
Container 2: ████████████████ (1600 load)
Container 3: ████████████████████████ (2400 load)

LBTP (Balanced):
Container 1: ████████████████████ (2000 load)
Container 2: ███████████████████ (1950 load)
Container 3: ████████████████████ (2050 load)
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Satellites    │    │      Users      │    │    Routing      │
│                 │    │                 │    │                 │
│ • 900 nodes     │    │ • 1500 terminals│    │ • TSA Protocol  │
│ • 3 orbital     │    │ • 6 regions     │    │ • OSPF Protocol │
│   shells        │    │ • Geo-located   │    │ • Path finding  │
│ • Real physics  │    │ • Realistic     │    │ • Load tracking │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Partitioning        │
                    │                         │
                    │  UTP vs LBTP Comparison │
                    │  Performance Analysis   │
                    └─────────────────────────┘
```

## 🔬 Technical Implementation

**Satellite Network:**

- Orbital mechanics: `v = √(GM/r)`
- Inter-satellite links: Haversine distance calculation
- Communication range: 5000 km

**Routing Protocols:**

- **TSA**: Time-slot assignment (graph coloring)
- **OSPF**: Link-state routing (Dijkstra's algorithm)

**Performance Model:**

```
CPU Work = (106.7×10⁹ × Satellites) + (33.69×10⁹ × Users) + Base
Speedup = Serial Time / Parallel Time
```

## 📁 Project Structure

```
📦 Satellite-Constellation-Sim
├── 🚀 main.py                    # Entry point
├── 📊 simulation_model.py        # Performance calculations
├── 🌐 network_simulator.py       # Network topology & traffic
├── ⚖️  partition_simulator.py     # UTP vs LBTP comparison
├── 🛰️ satellite.py              # Satellite entities
├── 📡 user_terminal.py          # User terminals
├── 🔀 routing_protocols.py      # TSA & OSPF routing
├── 🎮 demo.py                   # Interactive demos
└── 📚 documentations/           # Detailed guides
```

## Installation

No external dependencies required. This project uses only Python standard library.

**Requirements:**

- Python 3.6 or higher

## Usage

### Quick Start - Run Complete Simulation

```bash
python main.py
```

This runs the full integrated simulation including:

- Satellite constellation initialization
- User terminal deployment
- Network topology building
- Routing protocol execution (OSPF and TSA)
- Partition comparison (UTP vs LBTP)
- Performance analysis

### Individual Components

**1. Performance Model Only (Theoretical Analysis)**

```bash
python simulation_model.py
```

**2. Network Simulation with Routing Protocols**

```bash
python network_simulator.py
```

**3. Integrated Partition and Network Simulation**

```bash
python partition_simulator.py
```

### Expected Output

The program generates a three-part report:

1. **Project Overview**: Scenario details and baseline metrics
2. **Load Distribution Comparison**: Side-by-side comparison of UTP vs LBTP
3. **Final Speedup Analysis**: Performance gains and efficiency metrics

### Sample Output

```
================================================================================
MEGA-CONSTELLATION PARALLEL SIMULATION MODELER
================================================================================

1. PROJECT OVERVIEW
--------------------------------------------------------------------------------
Scenario Parameters:
  Satellites (N):           900
  Users (M):                1500
  Containers (k*):          20
  Simulation Time:          90 minutes (5400 seconds)

Baseline Metrics:
  Total CPU Work (C_total): 1.4738e+14 cycles
  Total Memory (R_total):   228.51 GB
  Serial Time (T_serial):   68.23 minutes

2. LOAD DISTRIBUTION COMPARISON
--------------------------------------------------------------------------------
Strategy   Load Imbalance (ζ)        Max Container Load        Parallel Time
           (cycles)                  (minutes)
--------------------------------------------------------------------------------
UTP        30.00%                    9.5797e+12                4.43 minutes
LBTP       5.00%                     7.7382e+12                3.58 minutes

3. FINAL SPEEDUP ANALYSIS
--------------------------------------------------------------------------------
UTP Speedup:  15.40x
LBTP Speedup: 19.05x
```

## Key Findings

- **LBTP achieves ~24% better speedup** than UTP through intelligent load balancing
- **Time savings**: Approximately 0.85 minutes per simulation run
- **Near-optimal parallelization**: LBTP achieves 19.05x speedup with 20 containers (95% efficiency)

## 🧠 Algorithms Explained

### Partitioning Strategies

```
UTP (Simple):                    LBTP (Smart):
┌─────────────────┐              ┌─────────────────┐
│ for i in range: │              │ 1. Sort by load │
│   container =   │              │ 2. Find min     │
│     i % 20      │              │ 3. Assign to    │
│   assign(sat)   │              │    least loaded │
└─────────────────┘              └─────────────────┘
     O(N)                             O(N log N)
```

### Routing Protocols

```
TSA (Time-Slotted):              OSPF (Link-State):
┌─────────────────┐              ┌─────────────────┐
│ 1. Graph color  │              │ 1. Build LSA DB │
│ 2. Assign slots │              │ 2. Divide areas │
│ 3. Time-aware   │              │ 3. Run Dijkstra │
│    routing      │              │ 4. Update table │
└─────────────────┘              └─────────────────┘
```

## 📈 Performance Comparison

```
Execution Flow:
Serial (1 CPU):     ████████████████████████████████████ 68 min
UTP (20 CPUs):      ████████ 4.4 min (15.4x speedup)
LBTP (20 CPUs):     ██████ 3.6 min (19.0x speedup) ⭐

Efficiency:         UTP: 77%    LBTP: 95%
```

## Research Context

This implementation replicates the core performance claims from research on parallel simulation of mega satellite communication networks, demonstrating the practical benefits of load-balanced topology partitioning for large-scale distributed simulations.

## License

This project is provided for educational and research purposes.

### Command Line Options

```bash
# Run with OSPF routing
python main.py ospf

# Run with TSA routing
python main.py tsa

# Compare both routing protocols
python main.py compare

# Run performance model only
python main.py model

# Show help
python main.py help
```

### Interactive Mode

Run without arguments for interactive menu:

```bash
python main.py
```

## Sample Output

### Network Simulation Output

```
================================================================================
SATELLITE NETWORK SIMULATION
================================================================================

Initializing 900 satellites...
✓ Created 900 satellites
Initializing 1500 user terminals...
✓ Created 1500 user terminals
Setting up OSPF routing protocol...
✓ OSPF topology built with 900 nodes
✓ Network divided into 4 areas
Connecting users to satellites...
✓ Connected 1450/1500 users to satellites

Simulating 100 routes...
✓ Successful routes: 98/100
✓ Average hops per route: 3.45

================================================================================
NETWORK STATISTICS
================================================================================
Total Satellites:        900
Total Users:             1500
Avg Neighbors/Satellite: 12.34
Max Satellite Load:      156
Avg Satellite Load:      45.67
Max Connections:         8
Avg Connections:         1.61
================================================================================
```

### Partition Comparison Output

```
================================================================================
PARTITIONING COMPARISON
================================================================================

### UTP (Uniform Topology Partitioning) ###
Max Load:        2890
Min Load:        1234
Avg Load:        2045.50
Load Imbalance:  41.28%

### LBTP (Load Balancing based Topology Partitioning) ###
Max Load:        2156
Min Load:        1987
Avg Load:        2051.30
Load Imbalance:  5.10%
```

### Performance Analysis Output

```
================================================================================
FINAL SPEEDUP ANALYSIS
================================================================================
UTP Speedup:  15.40x
LBTP Speedup: 19.05x

Efficiency Gain: LBTP achieves 23.7% better speedup than UTP
Time Saved:      0.85 minutes per simulation
================================================================================
```

## Technical Implementation Details

### Satellite Orbital Mechanics

- Uses simplified two-body orbital propagation
- Haversine formula for great-circle distance calculation
- Altitude-aware distance computation for inter-satellite links
- Orbital velocity: v = √(GM/r)

### Routing Algorithm Complexity

- **TSA**: O(V²) for topology building, O(V log V) for routing
- **OSPF**: O(E log V) for SPF calculation using Dijkstra's algorithm
- V = number of satellites, E = number of links

### Partitioning Algorithm Complexity

- **UTP**: O(N) - simple round-robin
- **LBTP**: O(N log N) - sorting + greedy assignment
- N = number of satellites

### Load Calculation

```
Satellite Load = Active Connections + Routing Load
Container Load = Σ(Satellite Loads in Container)
Load Imbalance = (Max Load - Avg Load) / Avg Load
```

## Performance Characteristics

### Expected Results

Results vary slightly between runs due to realistic randomization:

- **Network Connectivity**: ~94-98% user connection rate
- **Routing Success**: ~95-99% successful route calculation
- **Average Hops**: 3.2-4.8 hops per route
- **LBTP Load Imbalance**: 4-6%
- **UTP Load Imbalance**: 28-32%
- **LBTP Speedup**: 18.8-19.3x with 20 containers
- **UTP Speedup**: 15.0-15.8x with 20 containers
- **Efficiency Gain**: 22-26% (LBTP consistently better)

**Note**: Each run produces different results simulating real-world variations in atmospheric conditions, hardware performance, traffic patterns, and operational factors. See RANDOMIZATION_GUIDE.md for details.

### Scalability

The simulation scales with:

- O(N²) for topology building (can be optimized with spatial indexing)
- O(N log N) for LBTP partitioning
- O(M) for user-satellite connections
- Memory: ~230 GB for full 900-satellite simulation

## Extending the Project

### Adding New Routing Protocols

1. Create new class in `routing_protocols.py`
2. Implement `build_topology()` and `calculate_route()` methods
3. Add protocol option in `network_simulator.py`

### Modifying Satellite Parameters

Edit constants in `satellite.py`:

- `orbit_altitude`: Orbital height in km
- `inclination`: Orbital inclination in degrees
- `max_range`: Maximum communication range in km

### Custom Partitioning Strategies

Implement new partitioning method in `partition_simulator.py`:

```python
def partition_custom(self, satellites):
    # Your partitioning logic here
    return partitions
```

## Troubleshooting

**Issue**: Low user connection rate

- **Solution**: Increase satellite communication range or add more satellites

**Issue**: High routing failures

- **Solution**: Check satellite density and inter-satellite link connectivity

**Issue**: Unexpected load imbalance

- **Solution**: Verify satellite load calculation includes both connections and routing load

## References

This implementation is based on research in:

- Mega-constellation satellite network simulation
- Parallel discrete event simulation
- Load balancing for distributed systems
- Satellite routing protocols (TSA, OSPF adaptations)
