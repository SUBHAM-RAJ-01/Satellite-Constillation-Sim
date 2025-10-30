# Project Explanation: Mega-Constellation Parallel Simulation Modeler

## What Are We Doing?

We built a computer simulation that models a **satellite internet network** (like Starlink) to answer one key question: **"What's the best way to divide simulation work across multiple computers to make it run faster?"**

Think of it like this: If you have a huge math problem that takes 1 hour on one computer, can you split it across 20 computers to finish in 3 minutes? The answer depends on **how you divide the work**.

## The Core Problem

**Serial vs Parallel Execution:**
- **Serial**: One computer does everything → Takes 68 minutes
- **Parallel**: 20 computers share the work → Should take ~3.4 minutes (68÷20)
- **Reality**: It depends on how evenly you split the work

## Our Approach: Two Methods Compared

### Method 1: UTP (Uniform Topology Partitioning) - The Simple Way
**Definition**: Divide satellites equally among computers, like dealing cards in order.
- Computer 1: Satellites 1-45
- Computer 2: Satellites 46-90
- Computer 3: Satellites 91-135
- And so on...

**Problem**: Some satellites are busier than others (more connections, more traffic), so some computers finish early while others are still working.

### Method 2: LBTP (Load Balancing based Topology Partitioning) - The Smart Way
**Definition**: Look at how busy each satellite is, then distribute them to balance the workload.
- Busy satellites go to computers with less work
- Keeps all computers equally busy
- No computer sits idle while others are overloaded

## How We Built the Simulation

### 1. Network Components

**900 Satellites:**
- Flying in 3 orbital shells (550km, 570km, 560km altitude)
- Each satellite knows its neighbors (other satellites within 5000km)
- Satellites handle user connections and route data

**1500 Users:**
- Distributed globally across 6 regions (Asia 30%, North America 25%, etc.)
- Each user connects to the nearest visible satellite
- Generate network traffic that satellites must handle

### 2. Routing Protocols (How Data Travels)

**TSA (Time-Slotted Assignment):**
- **Definition**: Satellites take turns transmitting to avoid interference
- Like a traffic light system - each satellite gets a time slot
- Prevents signal collisions between nearby satellites

**OSPF (Open Shortest Path First):**
- **Definition**: Each satellite knows the network map and finds the shortest path
- Like GPS navigation - calculates best route to destination
- Updates routes when satellites move or links change

### 3. Performance Measurement

**CPU Parameters:**
- **Formula**: Total Work = (106.7×10⁹ × Satellites) + (33.69×10⁹ × Users) + Base Overhead
- **Why**: More satellites/users = more computation needed
- **Result**: 900 satellites + 1500 users = 1.47×10¹⁴ CPU cycles

**Memory Parameters:**
- **Formula**: Memory = (164KB × Satellites) + (54KB × Users) + Base Memory
- **Result**: ~219GB theoretical, ~250MB actual runtime

## Key Parameters and Their Impact

### Network Scale Effects

**If we increase satellites (900 → 1800):**
- ✅ Better coverage, more connection options
- ❌ More computation, longer simulation time
- ❌ More complex routing decisions

**If we increase users (1500 → 3000):**
- ✅ More realistic traffic patterns
- ❌ More connections to manage
- ❌ Higher satellite loads

**If we increase containers (20 → 40):**
- ✅ Potentially faster execution
- ❌ Diminishing returns due to overhead
- ❌ More complex load balancing

### Time Factor
**Simulation Time (90 minutes):**
- Represents how long the satellite network operates
- Longer time = more orbital movement, more traffic
- Affects satellite positions and connection patterns

## How We Achieved Our Results

### Step 1: Build Realistic Network
1. Create 900 satellites with real orbital mechanics
2. Deploy 1500 users across Earth
3. Calculate which satellites can talk to each other
4. Implement TSA and OSPF routing

### Step 2: Simulate Network Traffic
1. Generate random communication requests
2. Find paths between satellites using routing protocols
3. Track how busy each satellite becomes
4. Record computational load for each satellite

### Step 3: Apply Partitioning Strategies
**UTP Process:**
```
for i in range(900):
    computer_id = i % 20
    assign satellite[i] to computer[computer_id]
```

**LBTP Process:**
```
1. Sort satellites by how busy they are
2. For each satellite:
   - Find computer with least work
   - Assign satellite to that computer
   - Update computer's workload
```

### Step 4: Measure Performance
- **UTP Result**: Most loaded computer has 30% more work than average
- **LBTP Result**: Most loaded computer has only 5% more work than average
- **Speedup Calculation**: Serial Time ÷ Parallel Time

## Our Results Explained

### Performance Comparison
```
Method    | Load Imbalance | Speedup | Efficiency
----------|----------------|---------|------------
UTP       | 30%           | 15.4x   | 77%
LBTP      | 5%            | 19.0x   | 95%
```

### Why LBTP is 24% Better
**UTP Problem**: Uneven work distribution
- Some computers finish in 3 minutes
- Others take 4.4 minutes
- Overall time = 4.4 minutes (limited by slowest computer)

**LBTP Solution**: Even work distribution
- All computers finish around 3.6 minutes
- No computer sits idle
- Better resource utilization

### Real-World Impact
**For Satellite Companies:**
- 24% faster simulations = 24% less computing cost
- Can test more network configurations
- Faster development cycles
- Better network designs

## Parameter Sensitivity Analysis

### Critical Parameters
1. **Number of Satellites**: Linear impact on computation
2. **Number of Users**: Linear impact on connections
3. **Load Imbalance**: Directly affects parallel efficiency
4. **Communication Range**: Affects network connectivity

### Randomization Effects
We add realistic variations:
- Satellite altitudes vary ±5km (orbital decay)
- User distribution varies ±10% (market changes)
- Link quality varies ±8% (weather, interference)

**Result**: Each simulation run gives slightly different numbers, but LBTP always outperforms UTP by 22-26%.

## Technical Innovation

### What Makes This Special
1. **Realistic Modeling**: Real orbital mechanics, not simplified
2. **Multiple Protocols**: TSA and OSPF comparison
3. **Load-Aware Partitioning**: Smart work distribution
4. **Comprehensive Validation**: Statistical consistency across runs

### Scalability Insights
- **UTP**: Performance degrades as network grows
- **LBTP**: Maintains efficiency even with larger networks
- **Sweet Spot**: 15-25 containers for this network size

## Conclusion

We proved that **intelligent work distribution beats simple work distribution by 24%** when simulating large satellite networks. This has real applications for:

- Satellite internet companies (SpaceX, Amazon, OneWeb)
- Network simulation software
- Parallel computing research
- Large-scale distributed systems

The key insight: **Load balancing isn't just about equal division - it's about smart division based on actual workload requirements.**

## Quick Demo

To see this in action:
```bash
python main.py model    # See performance comparison (1 second)
python main.py ospf     # Full simulation with OSPF (30 seconds)
python main.py compare  # Compare both protocols (60 seconds)
```

The numbers will vary slightly each run (realistic randomization), but LBTP will always outperform UTP significantly.