#!/usr/bin/env python3
"""
TPS (Transactions Per Second) benchmark for SeirChain blockchain system.
Validates performance claims and measures real-world throughput.
"""

import time
import threading
import multiprocessing
from typing import List, Dict, Any
from seir_chain.crypto.bls_production import ProductionBLS

class TPSBenchmark:
    """Comprehensive TPS benchmarking suite."""
    
    def __init__(self):
        self.bls = ProductionBLS()
        self.results = {}
    
    def generate_test_transactions(self, count: int) -> List[Dict[str, Any]]:
        """Generate test transactions for benchmarking."""
        transactions = []
        for i in range(count):
            key_pair = self.bls.generate_key_pair(f"benchmark_{i}")
            message = f"transaction_{i}_{time.time()}".encode()
            signature = self.bls.sign_message(message, key_pair.secret_key)
            
            transactions.append({
                "id": i,
                "signature": signature,
                "sender": key_pair.public_key.hex(),
                "timestamp": time.time()
            })
        return transactions
    
    def benchmark_signature_verification(self, transaction_count: int = 1000) -> Dict[str, Any]:
        """Benchmark signature verification performance."""
        print(f"Benchmarking signature verification for {transaction_count} transactions...")
        
        transactions = self.generate_test_transactions(transaction_count)
        signatures = [tx["signature"] for tx in transactions]
        
        start_time = time.time()
        results = self.bls.batch_verify(signatures)
        end_time = time.time()
        
        total_time = end_time - start_time
        tps = transaction_count / total_time
        
        return {
            "operation": "signature_verification",
            "transaction_count": transaction_count,
            "total_time": total_time,
            "tps": tps,
            "avg_time_per_tx": total_time / transaction_count * 1000,  # ms
            "valid_signatures": results["valid_signatures"]
        }
    
    def benchmark_signature_aggregation(self, validator_count: int = 100) -> Dict[str, Any]:
        """Benchmark signature aggregation performance."""
        print(f"Benchmarking signature aggregation for {validator_count} validators...")
        
        message = b"benchmark_aggregation_message"
        key_pairs = [self.bls.generate_key_pair(f"val_{i}") for i in range(validator_count)]
        
        # Generate individual signatures
        signatures = []
        start_time = time.time()
        
        for key_pair in key_pairs:
            sig = self.bls.sign_message(message, key_pair.secret_key)
            signatures.append(sig.signature)
        
        signature_generation_time = time.time() - start_time
        
        # Aggregate signatures
        start_time = time.time()
        aggregated_signature = self.bls.aggregate_signatures(signatures)
        aggregation_time = time.time() - start_time
        
        # Aggregate public keys
        public_keys = [kp.public_key for kp in key_pairs]
        aggregated_pk = self.bls.aggregate_public_keys(public_keys)
        
        # Verify aggregated signature
        start_time = time.time()
        is_valid = self.bls.verify_aggregated_signature(
            aggregated_signature, 
            aggregated_pk, 
            message
        )
        verification_time = time.time() - start_time
        
        return {
            "operation": "signature_aggregation",
            "validator_count": validator_count,
            "signature_generation_time": signature_generation_time,
            "aggregation_time": aggregation_time,
            "verification_time": verification_time,
            "aggregated_signature_valid": is_valid,
            "total_time": signature_generation_time + aggregation_time + verification_time
        }
    
    def benchmark_concurrent_verification(self, 
                                        transaction_count: int = 1000,
                                        thread_count: int = 4) -> Dict[str, Any]:
        """Benchmark concurrent signature verification."""
        print(f"Benchmarking concurrent verification with {thread_count} threads...")
        
        transactions = self.generate_test_transactions(transaction_count)
        signatures = [tx["signature"] for tx in transactions]
        
        # Split work among threads
        chunk_size = len(signatures) // thread_count
        threads = []
        results = [None] * thread_count
        
        def verify_chunk(start_idx, end_idx, thread_id):
            chunk_signatures = signatures[start_idx:end_idx]
            chunk_results = self.bls.batch_verify(chunk_signatures)
            results[thread_id] = chunk_results
        
        start_time = time.time()
        
        # Create and start threads
        for i in range(thread_count):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < thread_count - 1 else len(signatures)
            
            thread = threading.Thread(
                target=verify_chunk,
                args=(start_idx, end_idx, i)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Combine results
        total_valid = sum(result["valid_signatures"] for result in results if result)
        total_time = end_time - start_time
        tps = transaction_count / total_time
        
        return {
            "operation": "concurrent_verification",
            "transaction_count": transaction_count,
            "thread_count": thread_count,
            "total_time": total_time,
            "tps": tps,
            "valid_signatures": total_valid,
            "speedup": (transaction_count / (total_time / thread_count)) / tps
        }
    
    def benchmark_memory_usage(self, transaction_count: int = 10000) -> Dict[str, Any]:
        """Benchmark memory usage during operations."""
        print(f"Benchmarking memory usage for {transaction_count} transactions...")
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Measure baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Generate transactions
        transactions = self.generate_test_transactions(transaction_count)
        signatures = [tx["signature"] for tx in transactions]
        
        # Measure memory after generation
        after_generation_memory = process.memory_info().rss / 1024 / 1024
        
        # Perform batch verification
        results = self.bls.batch_verify(signatures)
        
        # Measure memory after verification
        after_verification_memory = process.memory_info().rss / 1024 / 1024
        
        return {
            "operation": "memory_usage",
            "transaction_count": transaction_count,
            "baseline_memory_mb": baseline_memory,
            "after_generation_mb": after_generation_memory,
            "after_verification_mb": after_verification_memory,
            "memory_increase_mb": after_verification_memory - baseline_memory,
            "memory_per_transaction_mb": (after_verification_memory - baseline_memory) / transaction_count
        }
    
    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive TPS benchmark suite."""
        print("=" * 60)
        print("SeirChain TPS Benchmark Suite")
        print("=" * 60)
        
        all_results = {}
        
        # Test different transaction volumes
        test_volumes = [100, 1000, 5000, 10000]
        
        for volume in test_volumes:
            print(f"\nTesting with {volume} transactions...")
            
            # Signature verification benchmark
            sig_results = self.benchmark_signature_verification(volume)
            all_results[f"signature_verification_{volume}"] = sig_results
            
            # Signature aggregation benchmark
            agg_results = self.benchmark_signature_aggregation(min(volume // 10, 100))
            all_results[f"signature_aggregation_{volume}"] = agg_results
            
            # Concurrent verification benchmark
            if volume <= 5000:  # Skip for very large volumes
                concurrent_results = self.benchmark_concurrent_verification(volume)
                all_results[f"concurrent_verification_{volume}"] = concurrent_results
        
        # Memory usage benchmark
        memory_results = self.benchmark_memory_usage(10000)
        all_results["memory_usage"] = memory_results
        
        # Summary report
        self.print_summary(all_results)
        
        return all_results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print benchmark summary."""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        
        # Find best TPS
        best_tps = 0
        best_config = ""
        
        for key, result in results.items():
            if "tps" in result:
                if result["tps"] > best_tps:
                    best_tps = result["tps"]
                    best_config = key
        
        print(f"Best TPS achieved: {best_tps:.2f} ({best_config})")
        
        # Memory efficiency
        if "memory_usage" in results:
            mem_result = results["memory_usage"]
            print(f"Memory per transaction: {mem_result['memory_per_transaction_mb']:.6f} MB")
        
        # Performance validation
        target_tps = 1000
        if best_tps >= target_tps:
            print(f"✅ Target TPS of {target_tps} achieved!")
        else:
            print(f"⚠️  Target TPS of {target_tps} not achieved (got {best_tps:.2f})")
        
        print("=" * 60)

if __name__ == "__main__":
    benchmark = TPSBenchmark()
    results = benchmark.run_comprehensive_benchmark()
    
    # Save results to file
    import json
    with open("tps_benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to tps_benchmark_results.json")
