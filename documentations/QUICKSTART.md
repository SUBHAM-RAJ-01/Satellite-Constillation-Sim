# Quick Start Guide

## Installation

No external dependencies required! Just Python 3.6+

```bash
# Verify Python version
python --version
```

## Running the Simulation

### Option 1: Interactive Mode (Recommended for First Time)

```bash
python main.py
```

Then select from the menu:
1. Full Simulation with OSPF
2. Full Simulation with TSA
3. Compare Both Protocols
4. Performance Model Only
5. Exit

### Option 2: Command Line Mode

**Run with OSPF routing:**
```bash
python main.py ospf
```

**Run with TSA routing:**
```bash
python main.py tsa
```

**Compare both protocols:**
```bash
python main.py compare
```

**Performance model only (fastest):**
```bash
python main.py model
```

## What to Expect

### Execution Time
- **Performance Model Only**: < 1 second
- **Full Simulation**: 10-30 seconds (depending on your CPU)
- **Protocol Comparison**: 20-60 seconds

### Output Sections

1. **Satellite Network Simulation**
   - Satellite initialization
   - User terminal deployment
   - Routing protocol setup
   - Network statistics

2. **Partitioning Comparison**
   - UTP metrics (naive approach)
   - LBTP metrics (optimized approach)
   - Load distribution analysis

3. **Performance Model Analysis**
   - Theoretical CPU work calculation
   - Memory usage estimation
   - Speedup calculations
   - Efficiency comparison

## Understanding the Results

### Key Metrics to Watch

**Network Statistics:**
- **Avg Neighbors/Satellite**: Should be 10-15 (good connectivity)
- **User Connection Rate**: Should be > 95%
- **Average Hops**: Should be 3-5 (efficient routing)

**Partitioning Performance:**
- **LBTP Load Imbalance**: Should be < 10%
- **UTP Load Imbalance**: Typically 25-35%
- **Load Difference**: Shows LBTP's advantage

**Speedup Analysis:**
- **LBTP Speedup**: ~19x with 20 containers
- **UTP Speedup**: ~15x with 20 containers
- **Efficiency Gain**: LBTP is ~24% better

## Example Session

```bash
$ python main.py

================================================================================
               MEGA-CONSTELLATION PARALLEL SIMULATION MODELER
================================================================================

This simulation demonstrates:
  • Satellite constellation with 900 satellites across 3 orbital shells
  • 1500 user terminals distributed globally
  • TSA and OSPF routing protocol implementations
  • LBTP vs UTP partitioning strategy comparison
  • Performance analysis and speedup calculations

================================================================================


Select Simulation Mode:
  1. Full Simulation (OSPF routing + Partition comparison)
  2. Full Simulation (TSA routing + Partition comparison)
  3. Compare Both Routing Protocols
  4. Performance Model Only (Theoretical)
  5. Exit

Enter your choice (1-5): 1

[Simulation runs...]
```

## Troubleshooting

**Problem**: "Python not found"
- **Solution**: Install Python 3.6+ from python.org

**Problem**: Simulation runs but shows errors
- **Solution**: Check that all .py files are in the same directory

**Problem**: Want to modify parameters
- **Solution**: Edit the constants in respective files:
  - Satellites/Users: `main.py` (line with PartitionSimulator)
  - Orbital parameters: `satellite.py`
  - Routing parameters: `routing_protocols.py`

## Next Steps

1. Run the simulation with different protocols
2. Compare the results
3. Modify parameters to see how they affect performance
4. Read the full README.md for technical details
5. Explore individual component files

## Quick Parameter Changes

### Change Number of Satellites/Users

Edit `main.py`, find:
```python
simulator = PartitionSimulator(num_satellites=900, num_users=1500, num_containers=20)
```

Change to:
```python
simulator = PartitionSimulator(num_satellites=500, num_users=1000, num_containers=10)
```

### Change Satellite Communication Range

Edit `satellite.py`, find:
```python
def can_communicate(self, other_satellite, max_range=5000):
```

Change `max_range=5000` to your desired range in km.

### Change Load Imbalance Factors

Edit `simulation_model.py`, find:
```python
self.LBTP_LBF = 0.05  # 5% for LBTP
self.UTP_LBF = 0.30   # 30% for UTP
```

Adjust these values to test different scenarios.

## Getting Help

Run with help flag:
```bash
python main.py help
```

Or check the full documentation in README.md
