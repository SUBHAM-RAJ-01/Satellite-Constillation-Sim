# Commands Reference

## Quick Start
```bash
python main.py report    # Complete analysis (2 min) ⭐
```

## Individual Simulations
```bash
python main.py model          # Performance model (1s)
python main.py ospf           # OSPF simulation (30s)
python main.py tsa            # TSA simulation (30s)
python main.py compare        # Compare protocols (60s)
python main.py communication  # Packet transmission (30s)
```

## Interactive
```bash
python main.py    # Menu with options 1-7
python demo.py    # Component demos
```

## Save Output
```bash
python main.py report > results.txt
```

## Visualization (Optional)
```bash
pip install matplotlib    # Install for graphs
python main.py report     # Auto-generates charts
```

## Help
```bash
python main.py help
```
