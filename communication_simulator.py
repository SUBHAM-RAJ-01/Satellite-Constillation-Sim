"""
Communication Simulator for Satellite Network
Handles data transmission, packet management, and performance metrics
"""
import random
import time
from collections import defaultdict

class Packet:
    """Represents a data packet in the satellite network"""
    
    # Packet frame format (in bytes)
    HEADER_SIZE = 40  # IP + UDP headers
    PAYLOAD_SIZE = 1460  # Maximum payload
    TOTAL_SIZE = HEADER_SIZE + PAYLOAD_SIZE  # 1500 bytes (standard MTU)
    
    def __init__(self, packet_id, source_id, dest_id, data_size=PAYLOAD_SIZE):
        # Packet identification
        self.packet_id = packet_id
        self.sequence_number = packet_id % 65536  # 16-bit sequence number
        
        # Source and destination
        self.source_id = source_id
        self.dest_id = dest_id
        
        # Packet frame structure
        self.frame = {
            # Layer 3 - Network Layer (20 bytes)
            'ip_header': {
                'version': 4,                    # IPv4
                'header_length': 20,             # bytes
                'type_of_service': 0,            # Best effort
                'total_length': self.TOTAL_SIZE,
                'identification': packet_id,
                'flags': 0,
                'fragment_offset': 0,
                'ttl': 64,                       # Time to live (hops)
                'protocol': 17,                  # UDP
                'checksum': self._calculate_checksum(),
                'source_ip': f"10.0.{source_id // 256}.{source_id % 256}",
                'dest_ip': f"10.0.{dest_id // 256}.{dest_id % 256}"
            },
            
            # Layer 4 - Transport Layer (20 bytes)
            'udp_header': {
                'source_port': 5000 + (source_id % 1000),
                'dest_port': 6000 + (dest_id % 1000),
                'length': 20 + data_size,
                'checksum': self._calculate_checksum()
            },
            
            # Payload (variable size, default 1460 bytes)
            'payload': {
                'data_size': data_size,
                'data': f"DATA_{packet_id}",
                'timestamp': time.time()
            }
        }
        
        # Transmission metadata
        self.creation_time = time.time()
        self.transmission_time = None
        self.delivery_time = None
        self.path = []  # Satellites traversed
        self.hops = 0
        self.retransmissions = 0
        self.is_delivered = False
        self.is_lost = False
        
    def _calculate_checksum(self):
        """Calculate simple checksum for packet integrity"""
        return (self.packet_id * 31 + self.source_id * 17 + self.dest_id * 13) % 65536
    
    def add_hop(self, satellite_id):
        """Record satellite in transmission path"""
        self.path.append(satellite_id)
        self.hops += 1
        # Decrease TTL
        self.frame['ip_header']['ttl'] -= 1
        if self.frame['ip_header']['ttl'] <= 0:
            self.is_lost = True
    
    def get_latency(self):
        """Calculate end-to-end latency in milliseconds"""
        if self.delivery_time and self.creation_time:
            return (self.delivery_time - self.creation_time) * 1000
        return None
    
    def get_size_bytes(self):
        """Get total packet size in bytes"""
        return self.TOTAL_SIZE
    
    def __repr__(self):
        return f"Packet-{self.packet_id}(src={self.source_id}, dst={self.dest_id}, hops={self.hops})"


class CommunicationSimulator:
    """Simulates data transmission in satellite network"""
    
    def __init__(self, network_simulator):
        self.network = network_simulator
        self.packets = []
        self.packet_counter = 0
        
        # Performance metrics
        self.metrics = {
            'total_packets_sent': 0,
            'total_packets_delivered': 0,
            'total_packets_lost': 0,
            'total_bytes_sent': 0,
            'total_bytes_delivered': 0,
            'total_latency': 0,
            'total_hops': 0,
            'retransmissions': 0,
            'simulation_start_time': None,
            'simulation_end_time': None
        }
        
        # Per-satellite metrics
        self.satellite_metrics = defaultdict(lambda: {
            'packets_forwarded': 0,
            'bytes_forwarded': 0,
            'packets_dropped': 0,
            'queue_overflow': 0,
            'processing_time': 0
        })
        
    def generate_packet(self, source_user, dest_user):
        """Generate a new packet from source to destination"""
        packet = Packet(
            packet_id=self.packet_counter,
            source_id=source_user.id,
            dest_id=dest_user.id,
            data_size=random.randint(500, 1460)  # Variable payload size
        )
        self.packet_counter += 1
        self.packets.append(packet)
        return packet
    
    def transmit_packet(self, packet, source_satellite, dest_satellite):
        """Simulate packet transmission through satellite network"""
        # Calculate route
        if not self.network.routing_protocol:
            return False
        
        path = self.network.routing_protocol.calculate_route(source_satellite, dest_satellite)
        
        if not path or len(path) < 2:
            packet.is_lost = True
            self.metrics['total_packets_lost'] += 1
            return False
        
        # Simulate transmission through each hop
        packet.transmission_time = time.time()
        
        for i, sat_id in enumerate(path):
            # Add hop to packet
            packet.add_hop(sat_id)
            
            # Check if packet exceeded TTL
            if packet.is_lost:
                self.metrics['total_packets_lost'] += 1
                self.satellite_metrics[sat_id]['packets_dropped'] += 1
                return False
            
            # Simulate processing delay and potential packet loss
            if self._simulate_transmission_loss(sat_id):
                packet.is_lost = True
                self.metrics['total_packets_lost'] += 1
                self.satellite_metrics[sat_id]['packets_dropped'] += 1
                return False
            
            # Update satellite metrics
            self.satellite_metrics[sat_id]['packets_forwarded'] += 1
            self.satellite_metrics[sat_id]['bytes_forwarded'] += packet.get_size_bytes()
        
        # Packet successfully delivered
        packet.is_delivered = True
        packet.delivery_time = time.time()
        self.metrics['total_packets_delivered'] += 1
        self.metrics['total_bytes_delivered'] += packet.get_size_bytes()
        self.metrics['total_latency'] += packet.get_latency()
        self.metrics['total_hops'] += packet.hops
        
        return True
    
    def _simulate_transmission_loss(self, satellite_id):
        """Simulate realistic packet loss (interference, congestion, etc.)"""
        # Base packet loss rate: 0.1% to 2% depending on satellite load
        sat = next((s for s in self.network.satellites if s.id == satellite_id), None)
        if not sat:
            return False
        
        # Higher load = higher loss probability
        base_loss_rate = 0.001  # 0.1%
        load_factor = min(sat.load / 100, 1.0)  # Normalize load
        loss_probability = base_loss_rate + (load_factor * 0.019)  # Up to 2%
        
        return random.random() < loss_probability
    
    def simulate_traffic(self, num_packets=1000, duration_seconds=60):
        """Simulate network traffic with multiple packets"""
        print(f"\nSimulating {num_packets} packet transmissions...")
        
        self.metrics['simulation_start_time'] = time.time()
        
        # Generate and transmit packets
        successful = 0
        failed = 0
        
        for i in range(num_packets):
            # Select random source and destination users
            source_user = random.choice(self.network.users)
            dest_user = random.choice(self.network.users)
            
            # Skip if same user
            if source_user.id == dest_user.id:
                continue
            
            # Get connected satellites
            source_sat = source_user.connected_satellite
            dest_sat = dest_user.connected_satellite
            
            if not source_sat or not dest_sat:
                failed += 1
                continue
            
            # Generate packet
            packet = self.generate_packet(source_user, dest_user)
            self.metrics['total_packets_sent'] += 1
            self.metrics['total_bytes_sent'] += packet.get_size_bytes()
            
            # Transmit packet
            if self.transmit_packet(packet, source_sat, dest_sat):
                successful += 1
            else:
                failed += 1
        
        self.metrics['simulation_end_time'] = time.time()
        
        print(f"[OK] Transmitted {successful}/{num_packets} packets successfully")
        print(f"[X] Failed/Lost: {failed} packets")
        
        return self.get_performance_metrics()
    
    def get_performance_metrics(self):
        """Calculate and return comprehensive performance metrics"""
        total_sent = self.metrics['total_packets_sent']
        total_delivered = self.metrics['total_packets_delivered']
        
        if total_sent == 0:
            return None
        
        # Calculate metrics
        delivery_rate = (total_delivered / total_sent) * 100
        loss_rate = ((total_sent - total_delivered) / total_sent) * 100
        avg_latency = self.metrics['total_latency'] / total_delivered if total_delivered > 0 else 0
        avg_hops = self.metrics['total_hops'] / total_delivered if total_delivered > 0 else 0
        
        # Calculate throughput
        sim_duration = (self.metrics['simulation_end_time'] - 
                       self.metrics['simulation_start_time'])
        throughput_mbps = (self.metrics['total_bytes_delivered'] * 8) / (sim_duration * 1_000_000)
        
        # Calculate efficiency
        theoretical_max_throughput = total_sent * Packet.TOTAL_SIZE * 8 / (sim_duration * 1_000_000)
        efficiency = (throughput_mbps / theoretical_max_throughput * 100) if theoretical_max_throughput > 0 else 0
        
        return {
            'packets_sent': total_sent,
            'packets_delivered': total_delivered,
            'packets_lost': self.metrics['total_packets_lost'],
            'delivery_rate': delivery_rate,
            'loss_rate': loss_rate,
            'avg_latency_ms': avg_latency,
            'avg_hops': avg_hops,
            'total_bytes_sent': self.metrics['total_bytes_sent'],
            'total_bytes_delivered': self.metrics['total_bytes_delivered'],
            'throughput_mbps': throughput_mbps,
            'efficiency_percent': efficiency,
            'simulation_duration': sim_duration
        }
    
    def generate_report(self):
        """Generate detailed communication performance report"""
        metrics = self.get_performance_metrics()
        
        if not metrics:
            print("No metrics available")
            return
        
        print("\n" + "=" * 80)
        print("COMMUNICATION PERFORMANCE REPORT")
        print("=" * 80)
        
        print("\n1. PACKET STATISTICS")
        print("-" * 80)
        print(f"Total Packets Sent:        {metrics['packets_sent']:,}")
        print(f"Packets Delivered:         {metrics['packets_delivered']:,}")
        print(f"Packets Lost:              {metrics['packets_lost']:,}")
        print(f"Delivery Rate:             {metrics['delivery_rate']:.2f}%")
        print(f"Loss Rate:                 {metrics['loss_rate']:.2f}%")
        
        print("\n2. LATENCY & ROUTING")
        print("-" * 80)
        print(f"Average Latency:           {metrics['avg_latency_ms']:.2f} ms")
        print(f"Average Hops:              {metrics['avg_hops']:.2f}")
        
        print("\n3. THROUGHPUT & EFFICIENCY")
        print("-" * 80)
        print(f"Total Data Sent:           {metrics['total_bytes_sent'] / 1_000_000:.2f} MB")
        print(f"Total Data Delivered:      {metrics['total_bytes_delivered'] / 1_000_000:.2f} MB")
        print(f"Throughput:                {metrics['throughput_mbps']:.2f} Mbps")
        print(f"Network Efficiency:        {metrics['efficiency_percent']:.2f}%")
        print(f"Simulation Duration:       {metrics['simulation_duration']:.2f} seconds")
        
        print("\n4. PACKET FRAME FORMAT")
        print("-" * 80)
        print(f"IP Header Size:            20 bytes")
        print(f"UDP Header Size:           20 bytes")
        print(f"Payload Size:              {Packet.PAYLOAD_SIZE} bytes (max)")
        print(f"Total Packet Size:         {Packet.TOTAL_SIZE} bytes")
        
        print("\n5. TOP BUSIEST SATELLITES")
        print("-" * 80)
        print(f"{'Satellite ID':<15} {'Packets Fwd':<15} {'Bytes Fwd':<15} {'Dropped':<10}")
        print("-" * 80)
        
        # Sort satellites by packets forwarded
        sorted_sats = sorted(self.satellite_metrics.items(), 
                           key=lambda x: x[1]['packets_forwarded'], 
                           reverse=True)[:10]
        
        for sat_id, metrics in sorted_sats:
            print(f"Sat-{sat_id:<12} {metrics['packets_forwarded']:<15} "
                  f"{metrics['bytes_forwarded'] / 1000:.1f} KB{'':<7} "
                  f"{metrics['packets_dropped']:<10}")
        
        print("=" * 80)


def demo_communication():
    """Demonstration of communication simulation"""
    from network_simulator import NetworkSimulator
    
    print("=" * 80)
    print("COMMUNICATION SIMULATION DEMO")
    print("=" * 80)
    
    # Create small network for demo
    print("\nCreating network (100 satellites, 200 users)...")
    network = NetworkSimulator(num_satellites=100, num_users=200)
    network.initialize_satellites()
    network.initialize_users()
    network.setup_routing(protocol="OSPF")
    network.connect_users_to_satellites()
    
    # Create communication simulator
    comm_sim = CommunicationSimulator(network)
    
    # Simulate traffic
    comm_sim.simulate_traffic(num_packets=500, duration_seconds=30)
    
    # Generate report
    comm_sim.generate_report()


if __name__ == "__main__":
    demo_communication()
