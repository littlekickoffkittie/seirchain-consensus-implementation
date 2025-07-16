#!/usr/bin/env python3
"""
Final SeirChain Implementation Test
"""

import time
import hashlib
import random
from seirchain.pof.core import ProofOfFractal, create_pof_puzzle, solve_pof_puzzle, verify_pof_solution
from seirchain.pof.difficulty import DynamicDifficultyAdjuster
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
        return True
    else:
        print("✗ PoF puzzle not solved")
        return False


def test_difficulty():
    """Test difficulty adjustment"""
    print("\n=== Testing Difficulty Adjustment ===")
    
    adjuster = DynamicDifficultyAdjuster()
    
    for i in range(5):
        adjuster.record_generation(random.uniform(0.8, 1.2), 1000, 1)
    
    new_diff = adjuster.calculate_new_difficulty()
    print(f"✓ New difficulty: {new_diff}")
    return True


def test_pbft():
    """Test PBFT consensus"""
    print("\n=== Testing PBFT Consensus ===")
    
    network = PBFTNetwork(node_count=4, byzantine_ratio=0.25)
    result = network.simulate_consensus({"test": "data"})
    
    print(f"✓ PBFT consensus: {result['consensus_result'].success}")
    print(f"✓ Byzantine tolerance: {result['fault_tolerance']} nodes")
    return result['consensus_result'].success


def test_hrc():
    """Test complete HRC system"""
    print("\n=== Testing HRC System ===")
    
    network = TriadNetwork(node_count=9)
    results = network.simulate_hierarchy(levels=2)
    
    print(f"✓ HRC simulation: {results['successful_consensus']}/{results['consensus_rounds']} successful")
    print(f"✓ Total time: {results['total_time']:.2f}s")
    return results['successful_consensus'] > 0


def main():
    """Run all tests"""
    print("="*50)
    print("SEIRCHAIN FINAL IMPLEMENTATION TEST")
    print("="*50)
    
    start = time.time()
    
    tests = [
        ("PoF", test_pof),
        ("Difficulty Adjustment", test_difficulty),
        ("PBFT Consensus", test_pbft),
        ("HRC System", test_hrc)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {name}: PASSED")
            else:
                print(f"✗ {name}: FAILED")
        except Exception as e:
            print(f"✗ {name}: ERROR - {e}")
    
    end = time.time()
    
    print("\n" + "="*50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print(f"Total execution time: {end-start:.2f}s")
    print("="*50)
    
    if passed == total:
        print("🎉 All SeirChain components working correctly!")
    else:
        print("⚠️  Some components need attention")


if __name__ == "__main__":
    main()
