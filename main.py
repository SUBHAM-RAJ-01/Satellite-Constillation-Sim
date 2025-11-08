"""
Main entry point for Mega-Constellation Parallel Simulation Modeler
Runs complete integrated simulation with all components
"""
import sys
from partition_simulator import PartitionSimulator

def print_header():
    """Print welcome header"""
    print("\n" + "=" * 80)
    print(" " * 15 + "MEGA-CONSTELLATION PARALLEL SIMULATION MODELER")
    print("=" * 80)
    print()
    print("This simulation demonstrates:")
    print("  - Satellite constellation with 900 satellites across 3 orbital shells")
    print("  - 1500 user terminals distributed globally")
    print("  - TSA and OSPF routing protocol implementations")
    print("  - LBTP vs UTP partitioning strategy comparison")
    print("  - Performance analysis and speedup calculations")
    print()
    print("=" * 80)
    print()

def print_menu():
    """Print simulation options menu"""
    print("\nSelect Simulation Mode:")
    print("  1. Full Simulation (OSPF routing + Partition comparison)")
    print("  2. Full Simulation (TSA routing + Partition comparison)")
    print("  3. Compare Both Routing Protocols")
    print("  4. Performance Model Only (Theoretical)")
    print("  5. Communication Simulation (Packet transmission)")
    print("  6. ⭐ Complete Integrated Report (All simulations)")
    print("  7. Exit")
    print()

def run_full_simulation(protocol="OSPF"):
    """Run complete simulation with specified protocol"""
    simulator = PartitionSimulator(num_satellites=900, num_users=1500, num_containers=20)
    simulator.run_comparison(protocol=protocol)

def run_comparison():
    """Run comparison of both routing protocols"""
    print("\n" + "=" * 80)
    print("ROUTING PROTOCOL COMPARISON")
    print("=" * 80)
    
    print("\n### Running OSPF Simulation ###")
    run_full_simulation(protocol="OSPF")
    
    print("\n\n### Running TSA Simulation ###")
    run_full_simulation(protocol="TSA")

def run_performance_model_only():
    """Run only the theoretical performance model"""
    from simulation_model import SimulationModel
    
    model = SimulationModel()
    model.run_simulation()
    model.generate_report()

def run_communication_simulation():
    """Run communication simulation with packet transmission"""
    from communication_simulator import demo_communication
    demo_communication()

def run_integrated_report():
    """Run complete integrated report with all simulations"""
    from integrated_report import run_integrated_report
    run_integrated_report()

def interactive_mode():
    """Run in interactive mode with menu"""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                run_full_simulation(protocol="OSPF")
            elif choice == "2":
                run_full_simulation(protocol="TSA")
            elif choice == "3":
                run_comparison()
            elif choice == "4":
                run_performance_model_only()
            elif choice == "5":
                run_communication_simulation()
            elif choice == "6":
                run_integrated_report()
            elif choice == "7":
                print("\nExiting simulation. Goodbye!")
                break
            else:
                print("\n⚠ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n⚠ Error: {e}")
            print("Please try again.")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        arg = sys.argv[1].lower()
        
        if arg in ["ospf", "--ospf"]:
            print_header()
            run_full_simulation(protocol="OSPF")
        elif arg in ["tsa", "--tsa"]:
            print_header()
            run_full_simulation(protocol="TSA")
        elif arg in ["compare", "--compare"]:
            print_header()
            run_comparison()
        elif arg in ["model", "--model"]:
            print_header()
            run_performance_model_only()
        elif arg in ["comm", "communication", "--comm"]:
            print_header()
            run_communication_simulation()
        elif arg in ["report", "integrated", "all", "--report"]:
            print_header()
            run_integrated_report()
        elif arg in ["help", "--help", "-h"]:
            print("\nUsage: python main.py [option]")
            print("\nOptions:")
            print("  ospf           Run full simulation with OSPF routing")
            print("  tsa            Run full simulation with TSA routing")
            print("  compare        Compare both routing protocols")
            print("  model          Run performance model only")
            print("  communication  Run communication simulation")
            print("  report         ⭐ Generate complete integrated report")
            print("  help           Show this help message")
            print("\nNo arguments: Run in interactive mode")
        else:
            print(f"Unknown option: {arg}")
            print("Use 'python main.py help' for usage information")
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
