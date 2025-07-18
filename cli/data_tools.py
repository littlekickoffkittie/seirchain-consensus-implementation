#!/usr/bin/env python3
"""
Data Integrity and Availability CLI Tools
"""

import click
import json
import os
from pathlib import Path
import hashlib

@click.group(name='data')
def data_group():
    """Data integrity and availability operations"""
    pass

@data_group.command()
@click.option('--data-dir', '-d', required=True, help='Directory containing data to check')
@click.option('--sample-size', '-s', default=100, help='Number of samples to check')
@click.option('--output', '-o', help='Output file for results')
def check_availability(data_dir, sample_size, output):
    """Check data availability using light client simulation"""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        click.echo(f"Data directory {data_dir} not found", err=True)
        return
    
    # Simulate data availability check
    files = list(data_path.rglob('*'))[:sample_size]
    
    available_count = 0
    results = []
    
    for file in files:
        if file.is_file():
            try:
                with open(file, 'rb') as f:
                    content = f.read(1024)  # Read first 1KB
                    if content:
                        available_count += 1
                        results.append({
                            'file': str(file),
                            'size': file.stat().st_size,
                            'hash': hashlib.sha256(content).hexdigest()[:16],
                            'available': True
                        })
            except Exception:
                results.append({
                    'file': str(file),
                    'available': False,
                    'error': 'Access denied'
                })
    
    availability_rate = (available_count / len(files)) * 100 if files else 0
    
    report = {
        'total_files': len(files),
        'available_files': available_count,
        'availability_rate': availability_rate,
        'results': results
    }
    
    if output:
        with open(output, 'w') as f:
            json.dump(report, f, indent=2)
        click.echo(f"Availability report saved to {output}")
    else:
        click.echo(json.dumps(report, indent=2))
    
    click.echo(f"Data availability: {availability_rate:.1f}% ({available_count}/{len(files)} files)")

@data_group.command()
@click.option('--data-file', '-f', required=True, help='Data file to generate proof for')
@click.option('--index', '-i', type=int, required=True, help='Index for proof generation')
@click.option('--output', '-o', help='Output file for Merkle proof')
def generate_merkle_proof(data_file, index, output):
    """Generate Merkle proof for data at specific index"""
    try:
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # Simulate Merkle proof generation
        chunk_size = 1024
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        if index >= len(chunks):
            click.echo(f"Index {index} out of range (max: {len(chunks)-1})", err=True)
            return
        
        # Generate simple proof (in real implementation, use actual Merkle tree)
        target_chunk = chunks[index]
        chunk_hash = hashlib.sha256(target_chunk).hexdigest()
        
        proof = {
            'index': index,
            'chunk_hash': chunk_hash,
            'total_chunks': len(chunks),
            'data_size': len(data),
            'proof_type': 'simulated_merkle_proof'
        }
        
        if output:
            with open(output, 'w') as f:
                json.dump(proof, f, indent=2)
            click.echo(f"Merkle proof saved to {output}")
        else:
            click.echo(json.dumps(proof, indent=2))
            
    except Exception as e:
        click.echo(f"Proof generation failed: {e}", err=True)

@data_group.command()
@click.option('--proof-file', '-p', required=True, help='Merkle proof file')
@click.option('--root-hash', '-r', required=True, help='Expected root hash')
@click.option('--data-file', '-f', help='Original data file for verification')
def verify_merkle_proof(proof_file, root_hash, data_file):
    """Verify Merkle proof against root hash"""
    try:
        with open(proof_file, 'r') as f:
            proof = json.load(f)
        
        # Simulate proof verification
        is_valid = True  # In real implementation, verify against actual Merkle tree
        
        if data_file and os.path.exists(data_file):
            with open(data_file, 'rb') as f:
                data = f.read()
            
            # Verify chunk hash
            chunk_size = 1024
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
            
            if proof['index'] < len(chunks):
                expected_hash = hashlib.sha256(chunks[proof['index']]).hexdigest()
                is_valid = expected_hash == proof['chunk_hash']
        
        result = {
            'valid': is_valid,
            'proof': proof,
            'root_hash': root_hash
        }
        
        click.echo(json.dumps(result, indent=2))
        
    except Exception as e:
        click.echo(f"Proof verification failed: {e}", err=True)

@data_group.command()
@click.option('--state-file', '-f', required=True, help='State file to verify')
@click.option('--expected-hash', '-e', required=True, help='Expected state hash')
@click.option('--algorithm', '-a', default='sha256', help='Hash algorithm')
def verify_state(state_file, expected_hash, algorithm):
    """Verify state file integrity"""
    try:
        with open(state_file, 'rb') as f:
            state_data = f.read()
        
        if algorithm == 'sha256':
            actual_hash = hashlib.sha256(state_data).hexdigest()
        elif algorithm == 'md5':
            actual_hash = hashlib.md5(state_data).hexdigest()
        else:
            click.echo(f"Unsupported algorithm: {algorithm}", err=True)
            return
        
        is_valid = actual_hash == expected_hash
        
        result = {
            'file': state_file,
            'expected_hash': expected_hash,
            'actual_hash': actual_hash,
            'valid': is_valid,
            'algorithm': algorithm
        }
        
        click.echo(json.dumps(result, indent=2))
        
    except Exception as e:
        click.echo(f"State verification failed: {e}", err=True)

@data_group.command()
@click.option('--state1', '-1', required=True, help='First state file')
@click.option('--state2', '-2', required=True, help='Second state file')
@click.option('--output', '-o', help='Output file for diff results')
def diff_states(state1, state2, output):
    """Compare two state files"""
    try:
        with open(state1, 'rb') as f:
            data1 = f.read()
        
        with open(state2, 'rb') as f:
            data2 = f.read()
        
        hash1 = hashlib.sha256(data1).hexdigest()
        hash2 = hashlib.sha256(data2).hexdigest()
        
        diff_result = {
            'file1': {
                'path': state1,
                'size': len(data1),
                'hash': hash1
            },
            'file2': {
                'path': state2,
                'size': len(data2),
                'hash': hash2
            },
            'identical': hash1 == hash2,
            'size_difference': abs(len(data1) - len(data2))
        }
        
        if output:
            with open(output, 'w') as f:
                json.dump(diff_result, f, indent=2)
            click.echo(f"Diff results saved to {output}")
        else:
            click.echo(json.dumps(diff_result, indent=2))
        
    except Exception as e:
        click.echo(f"State comparison failed: {e}", err=True)

if __name__ == '__main__':
    data_group()
