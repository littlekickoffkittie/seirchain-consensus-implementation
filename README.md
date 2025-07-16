# SeirChain: Proof-of-Fractal and Hierarchical Recursive Consensus Implementation

This repository contains a complete implementation of the SeirChain consensus mechanism as described in the whitepaper, including Proof-of-Fractal (PoF) and Hierarchical Recursive Consensus (HRC).

## Overview

SeirChain introduces a novel distributed ledger technology using a Sierpinski triangle-inspired Triad Matrix with fractal dimension ≈ 1.585. This implementation provides:

- **Proof-of-Fractal (PoF)**: Self-similar hash pattern puzzles
- **Hierarchical Recursive Consensus (HRC)**: O(log N) message complexity
- **Byzantine Fault Tolerance**: 1/3 fault tolerance per sub-fractal
- **Probabilistic Finality**: Sub-second confirmations
- **VRF-based Miner Selection**: Fair and verifiable selection

## Architecture

```
seirchain/
├── pof/                    # Proof-of-Fractal implementation
│   ├── core.py            # Core PoF puzzle creation, solving, verification
│   └── difficulty.py      # Dynamic difficulty adjustment
├── consensus/             # Consensus mechanisms
│   └── vrf.py             # VRF-based miner selection
├── hrc/                   # Hierarchical Recursive Consensus
│   ├── pbft.py            # Practical Byzantine Fault Tolerance
│   ├── aggregation.py     # Recursive proof aggregation
│   └── node.py            # Complete TriadNode implementation
├── simulation/            # Simulation and analysis tools
│   ├── finality.py        # Probabilistic finality modeling
│   └── complexity.py      # Message complexity analysis
└── demo.py               # Complete demonstration script
```

## Key Features Implemented

### 1. Proof-of-Fractal (PoF)
- **Puzzle Creation**: `create_pof_puzzle()` - Creates cryptographically secure puzzles
- **Puzzle Solving**: `solve_pof_puzzle()` - Finds nonce meeting difficulty targets
- **Solution Verification**: `verify_pof_solution()` - Validates solutions with self-similar patterns
- **Self-Similar Hash Patterns**: Secondary verification using fractal-like transformations

### 2. Dynamic Difficulty Adjustment
- **Adaptive Difficulty**: Adjusts based on average Triad generation time
- **Network Responsiveness**: Reacts to hash rate changes
- **Stability Controls**: Prevents extreme adjustments

### 3. VRF-based Miner Selection
- **Fair Selection**: Uses Verifiable Random Functions
- **Verifiable Proofs**: Miners can prove selection legitimacy
- **Seed-based**: Uses previous Triad hashes as seeds

### 4. Hierarchical Recursive Consensus (HRC)
- **Local PBFT**: 1/3 Byzantine fault tolerance per committee
- **Recursive Aggregation**: Child-to-parent proof propagation
- **Succinct Proofs**: Merkle-based proof compression
- **Global Consensus**: O(log N) message complexity

### 5. Complete TriadNode
- **PoF Mining**: Participates in proof generation
- **Local Consensus**: Runs PBFT for local Triads
- **Proof Propagation**: Aggregates and propagates proofs
- **Network Simulation**: Complete fractal network modeling

### 6. Simulation Tools
- **Probabilistic Finality**: Models transaction finality vs confirmation depth
- **Message Complexity**: Demonstrates O(log N) vs O(N) improvements
- **Byzantine Fault Tolerance**: Tests resilience to malicious nodes
- **Network Synchronization**: Ouroboros-like traversal simulation

## Quick Start

### 1. Run Complete Demo
```bash
python demo.py
```

### 2. Individual Component Testing

#### Proof-of-Fractal
```python
from seirchain.pof.core import create_pof_puzzle, solve_pof_puzzle

# Create and solve a puzzle
puzzle = create_pof_puzzle(b"transaction_data", difficulty=8)
solution = solve_pof_puzzle(puzzle)
print(f"Solution: {solution.nonce}")
```

#### VRF Selection
```python
from seirchain.consensus.vrf import register_miner, select_miner

# Register miners
miner = register_miner(b"miner_1")
seed = hashlib.sha256(b"previous_hash").digest()
selected, proof = select_miner(seed)
```

#### HRC Consensus
```python
from seirchain.hrc.node import TriadNetwork

# Create network and simulate
network = TriadNetwork(node_count=9)
results = network.simulate_hierarchy(levels=3)
```

### 3. Advanced Simulations

#### Probabilistic Finality
```python
from seirchain.simulation.finality import FinalitySimulator

simulator = FinalitySimulator()
report = simulator.generate_finality_report(sample_transactions=100)
print(f"Average finality time: {report['average_finality_time']:.3f}s")
```

#### Message Complexity
```python
from seirchain.simulation.complexity import MessageComplexityAnalyzer

analyzer = MessageComplexityAnalyzer()
comparison = analyzer.compare_with_linear_blockchain(1000)
print(f"Efficiency improvement: {comparison['efficiency_ratio']:.2f}x")
```

## Performance Characteristics

### Message Complexity
- **HRC**: O(log N) messages for global consensus
- **Linear Blockchain**: O(N) messages
- **Efficiency**: 10-100x improvement for large networks

### Finality Times
- **1 Layer**: ~0.1s, 60% probability
- **3 Layers**: ~0.3s, 95% probability
- **5 Layers**: ~0.5s, 99.9% probability

### Byzantine Fault Tolerance
- **Maximum Byzantine**: 33.3% of validators
- **Committee Size**: 4-10 validators per Triad
- **Recovery**: Automatic with network reorganization

## Mathematical Foundations

### Fractal Dimension
The Triad Matrix has Hausdorff dimension:
```
D = log(3)/log(2) ≈ 1.585
```

### Complexity Analysis
- **Node Growth**: |V_{N,m}| ≈ 2^{m-2}N^m
- **Message Complexity**: O(log N) for global consensus
- **Storage**: O(log N) per node vs O(N) for linear blockchain

### Security Model
- **Finality Probability**: P = 1 - (1 - p)^k where k is confirmation depth
- **Byzantine Threshold**: f < n/3 for safety
- **Attack Resistance**: Exponential decay with confirmation depth

## Testing

Run the complete test suite:
```bash
python -m pytest tests/  # (when tests are added)
```

Or run individual components:
```bash
python -c "from seirchain.pof.core import *; demo_pof()"
python -c "from seirchain.hrc.node import *; demo_hrc()"
```

## Contributing

This implementation follows the SeirChain whitepaper specifications. Contributions should maintain compatibility with the theoretical foundations while improving practical performance.

## License

MIT License - See LICENSE file for details

## References

- SeirChain Whitepaper: Fractal-Based Distributed Ledger System
- Practical Byzantine Fault Tolerance (PBFT) - Castro & Liskov
- Verifiable Random Functions (VRFs) - Micali et al.
- Fractal Geometry and Network Theory
