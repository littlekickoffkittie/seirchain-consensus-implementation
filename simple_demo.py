#!/usr/bin/env python3
"""
Simple SeirChain Demo without matplotlib dependencies
"""

import time
import hashlib
import random
from seirchain.pof.core import ProofOfFractal, create_pof_puzzle, solve_pof_puzzle, verify_pof_solution
from seirchain.pof.difficulty import DynamicDifficultyAdjuster
from seirchain.consensus.vrf import MinerSelector, register_miner, select_miner, verify_miner_selection
from seirchain.hrc.pbft import PBFTNetwork
from seirchain.hrc.node import TriadNetwork, TriadNode


def demo_pof():
    """Demonstrate Proof-of-Fractal functionality"""
    print("\n" + "="*60)
    print("DEMO: Proof-of-Fractal (PoF)")
    print("="*60)
    
    # Create PoF instance
    pof = ProofOfFractal()
    
    # Create and solve puzzle
    transaction_data = b"Sample transaction for PoF demo"
    difficulty = 8  # Low for demo
    
    puzzle = create_pof_puzzle(transaction_data, difficulty)
    print(f"Created puzzle: {puzzle.puzzle_id}")
    print(f"Difficulty: {puzzle.difficulty}")
    print(f"Hash target: {puzzle.hash_target}")
    
    # Solve puzzle
    print("\nSolving puzzle...")
    solution = solve_pof_puzzle(puzzle, max_iterations=10000)
    
    if solution:
        print(f"Solution found!")
        print(f"Nonce: {solution.nonce}")
        print(f"Hash: {solution.hash_result}")
        print(f"Secondary hash: {solution.secondary_hash}")
        
        # Verify solution
        is_valid = verify_pof_solution(puzzle, solution)
        print(f"Solution valid: {is_valid}")
        
        # Demonstrate self-similar pattern
        secondary_hash = pof._calculate_secondary_hash(solution.hash_result)
        print(f"Self-similar pattern verified: {secondary_hash}")
    else:
        print("No solution found")


def demo_difficulty_adjustment():
    """Demonstrate dynamic difficulty adjustment"""
    print("\n" + "="*60)
    print("DEMO: Dynamic Difficulty Adjustment")
    print("="*60)
    
    adjuster = DynamicDifficultyAdjuster(
        target_generation_time=1.0,
        adjustment_window=5
    )
    
    # Simulate network conditions
    for i in range(8):
        # Simulate varying network conditions
        actual_time = random.uniform(0.5, 2.0)
        hash_rate = random.uniform(1000, 5000)
        
        adjuster.record_generation(actual_time, hash_rate)
        
        if i >= 4:  # Start adjusting after some data
            new_diff = adjuster.calculate_new_difficulty()
            print(f"Generation {i+1}: Time={actual_time:.2f}s, New Difficulty: {new_diff}")
    
    stats = adjuster.get_adjustment_statistics()
    print(f"\nFinal statistics: {stats}")


def demo_vrf_selection():
    """Demonstrate VRF-based miner selection"""
    print("\n" + "="*60)
    print("DEMO: VRF Miner Selection")
    print("="*60)
    
    # Register miners
    miners = []
    for i in range(5):
        miner_id = f"miner_{i}".encode()
        key_pair = register_miner(miner_id)
        miners.append((miner_id, key_pair))
        print(f"Registered miner {i}: {miner_id.hex()[:16]}...")
    
    # Select miners with different seeds
    for trial in range(3):
        seed = f"trial_{trial}".encode()
        seed_hash = hashlib.sha256(seed).digest()
        
        selected_miner, proof = select_miner(seed_hash)
        is_valid = verify_miner_selection(seed_hash, selected_miner, proof)
        
        print(f"\nTrial {trial + 1}:")
        print(f"Seed: {seed_hash.hex()[:16]}...")
        print(f"Selected: {selected_miner.hex()[:16]}...")
        print(f"Valid: {is_valid}")


def demo_pbft_consensus():
    """Demonstrate PBFT consensus with Byzantine fault tolerance"""
    print("\n" + "="*60)
    print("DEMO: PBFT Consensus with Byzantine Fault Tolerance")
    print("="*60)
    
    # Create network with 4 nodes, 1 Byzantine
    network = PBFTNetwork(node_count=4, byzantine_ratio=0.25)
    
    # Simulate consensus
    request_data = {"transaction": "demo_tx", "value": 100}
    result = network.simulate_consensus(request_data)
    
    print(f"Network: {result['total_nodes']} nodes")
    print(f"Byzantine: {result['byzantine_nodes']} nodes")
    print(f"Fault tolerance: {result['fault_tolerance']} nodes")
    print(f"Status: {result['network_status']}")
    
    consensus = result['consensus_result']
    print(f"\nConsensus result:")
    print(f"Success: {consensus.success}")
    print(f"Commit time: {consensus.commit_time:.3f}s")
    print(f"Validators: {consensus.validator_count}")
    print(f"Byzantine validators: {consensus.byzantine_count}")


def demo_complete_hrc():
    """Demonstrate complete HRC system"""
    print("\n" + "="*60)
    print("DEMO: Complete Hierarchical Recursive Consensus")
    print("="*60)
    
    # Create Triad network
    network = TriadNetwork(node_count=9)
    
    # Simulate hierarchy
    results = network.simulate_hierarchy(levels=2)
    
    print(f"Network simulation complete:")
    print(f"Nodes: {results['nodes']}")
    print(f"Triads created: {results['triads_created']}")
    print(f"Consensus rounds: {results['consensus_rounds']}")
    print(f"Successful consensus: {results['successful_consensus']}")
    print(f"Byzantine tolerance: {results['byzantine_tolerance']} nodes")
    print(f"Total time: {results['total_time']:.3f}s")
    
    # Test individual node
    node = list(network.nodes.values())[0]
    stats = node.get_network_statistics()
    print(f"\nNode statistics: {stats}")


def run_simple_demo():
    """Run simple demonstration"""
    print("="*80)
    print("SEIRCHAIN SIMPLE DEMONSTRATION")
    print("Proof-of-Fractal and Hierarchical Recursive Consensus")
    print("="*80)
    
    start_time = time.time()
    
    # Run all demos
    demo_pof()
    demo_difficulty_adjustment()
    demo_vrf_selection()
    demo_pbft_consensus()
    demo_complete_hrc()
    
    end_time = time.time()
    
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("="*80)


if __name__ == "__main__":
    run_simple_demo()
