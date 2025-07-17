#!/usr/bin/env python3
"""
Test SeirChain Implementation
"""

import time
import hashlib
import random
from seirchain.pof.core import ProofOfFractal, create_pof_puzzle, solve_pof_puzzle, verify_pof_solution
from seirchain.pof.difficulty import DynamicDifficultyAdjuster
from seirchain.consensus.vrf import MinerSelector, register_miner, select_miner, verify_miner_selection
from seirchain.hrc.pbft import PBFTNetwork
from seirchain.hrc.node import TriadNetwork


def test_pof():
    """Test Proof-of-Fractal"""
    print("\n=== Testing Proof-of-Fractal ===")
    
    pof = ProofOfFractal()
    puzzle = create_pof_puzzle(b"test_data", 6)
    solution = solve_pof_puzzle(puzzle, max_iterations=5000)
    
    if solution:
        print(f"✓ PoF puzzle solved: nonce={solution.nonce}")
        print(f"✓ Solution verified: {verify_pof_solution(puzzle, solution)}")
    else:
        print("✗ PoF puzzle not solved")


def test_difficulty():
    """Test difficulty adjustment"""
    print("\n=== Testing Difficulty Adjustment ===")
    
    adjuster = DynamicDifficultyAdjuster()
    
    for i in range(5):
        adjuster.record_generation(random.uniform(0.8, 1.2), 1000, 1)
    
    new_diff = adjuster.calculate_new_difficulty()
    print(f"✓ New difficulty: {new_diff}")


def test_vrf():
    """Test VRF selection"""
    print("\n=== Testing VRF Selection ===")
    
    # Register miners
    miners = []
    for i in range(3):
        miner_id = f"miner_{i}".encode()
        key_pair = register_miner(miner_id)
        miners.append(miner_id)
    
    # Test selection
    seed = hashlib.sha256(b"test_seed").digest()
    selected, proof = select_miner(seed, miners)
    is_valid = verify_miner_selection(seed, selected, proof)
    
    print(f"✓ VRF selection: {is_valid}")
    print(f"✓ Selected miner: {selected.hex()[:8]}...")


def test_pbft():
    """Test PBFT consensus"""
    print("\n=== Testing PBFT Consensus ===")
    
    network = PBFTNetwork(node_count=4, byzantine_ratio=0.25)
    result = network.simulate_consensus({"test": "data"})
    
    print(f"✓ PBFT consensus: {result['consensus_result'].success}")
    print(f"✓ Byzantine tolerance: {result['fault_tolerance']} nodes")


def test_hrc():
    """Test complete HRC system"""
    print("\n=== Testing HRC System ===")
    
    network = TriadNetwork(node_count=9)
    results = network.simulate_hierarchy(levels=2)
    
    print(f"✓ HRC simulation: {results['successful_consensus']}/{results['consensus_rounds']} successful")
    print(f"✓ Total time: {results['total_time']:.2f}s")


def main():
    """Run all tests"""
    print("="*50)
    print("SEIRCHAIN IMPLEMENTATION TEST")
    print("="*50)
    
    start = time.time()
    
    test_pof()
    test_difficulty()
    test_vrf()
    test_pbft()
    test_hrc()
    
    end = time.time()
    print(f"\n✓ All tests completed in {end-start:.2f}s")
    print("="*50)


if __name__ == "__main__":
    main()
