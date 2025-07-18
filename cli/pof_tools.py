#!/usr/bin/env python3
"""
Proof-of-Fractal (PoF) Mining CLI Tools
"""

import click
import json
import os
from pathlib import Path
import time

# Import PoF module
from seir_chain.consensus.pof import PoF
from seir_chain.data_structures.triad import Triad

@click.group(name='pof')
def pof_group():
    """Proof-of-Fractal mining operations"""
    pass

@pof_group.command()
@click.option('--triad-file', '-t', required=True, help='Triad JSON file')
@click.option('--difficulty', '-d', default=20, help='Mining difficulty')
@click.option('--threads', '-n', default=1, help='Number of mining threads')
@click.option('--output', '-o', help='Output file for solution')
def mine(triad_file, difficulty, threads, output):
    """Mine PoF puzzle"""
    try:
        with open(triad_file, 'r') as f:
            triad_data = json.load(f)
        
        triad = Triad.from_dict(triad_data)
        pof = PoF(triad, difficulty)
        
        click.echo(f"Starting PoF mining for Triad height {triad.height}")
        click.echo(f"Difficulty: {difficulty}")
        click.echo(f"Threads: {threads}")
        
        start_time = time.time()
        
        # Create puzzle
        vdf_output, vdf_proof = pof.create_puzzle()
        
        # Solve puzzle
        nonce = pof.solve_puzzle(triad, vdf_output)
        
        end_time = time.time()
        mining_time = end_time - start_time
        
        solution = {
            'triad_hash': triad.get_header_hash().hex(),
            'vdf_output': vdf_output.hex(),
            'vdf_proof': vdf_proof.hex(),
            'nonce': nonce,
            'difficulty': difficulty,
            'mining_time': mining_time,
            'timestamp': int(time.time())
        }
        
        if output:
            with open(output, 'w') as f:
                json.dump(solution, f, indent=2)
            click.echo(f"Solution saved to {output}")
        else:
            click.echo(json.dumps(solution, indent=2))
            
        click.echo(f"Mining completed in {mining_time:.2f} seconds")
        
    except Exception as e:
        click.echo(f"Mining failed: {e}", err=True)

@pof_group.command()
@click.option('--triad-file', '-t', required=True, help='Triad JSON file')
@click.option('--solution-file', '-s', required=True, help='Solution JSON file')
@click.option('--vdf-difficulty', '-d', type=int, help='VDF difficulty (optional)')
def verify(triad_file, solution_file, vdf_difficulty):
    """Verify PoF solution"""
    try:
        with open(triad_file, 'r') as f:
            triad_data = json.load(f)
        
        with open(solution_file, 'r') as f:
            solution = json.load(f)
        
        triad = Triad.from_dict(triad_data)
        
        # Use provided difficulty or extract from solution
        difficulty = vdf_difficulty or solution.get('difficulty', 20)
        
        is_valid = PoF.verify_solution(
            triad, 
            difficulty, 
            bytes.fromhex(solution['vdf_output']), 
            bytes.fromhex(solution['vdf_proof'])
        )
        
        click.echo(f"Solution verification: {'VALID' if is_valid else 'INVALID'}")
        
    except Exception as e:
        click.echo(f"Verification failed: {e}", err=True)

@pof_group.command()
@click.option('--triad-file', '-t', required=True, help='Triad JSON file')
@click.option('--difficulty', '-d', default=20, help='Difficulty level')
@click.option('--output', '-o', help='Output file for puzzle')
def generate_puzzle(triad_file, difficulty, output):
    """Generate PoF puzzle"""
    try:
        with open(triad_file, 'r') as f:
            triad_data = json.load(f)
        
        triad = Triad.from_dict(triad_data)
        pof = PoF(triad, difficulty)
        
        vdf_output, vdf_proof = pof.create_puzzle()
        
        puzzle = {
            'triad': triad_data,
            'vdf_output': vdf_output.hex(),
            'vdf_proof': vdf_proof.hex(),
            'difficulty': difficulty,
            'timestamp': int(time.time())
        }
        
        if output:
            with open(output, 'w') as f:
                json.dump(puzzle, f, indent=2)
            click.echo(f"Puzzle saved to {output}")
        else:
            click.echo(json.dumps(puzzle, indent=2))
            
    except Exception as e:
        click.echo(f"Puzzle generation failed: {e}", err=True)

@pof_group.command()
@click.option('--triads-dir', '-d', required=True, help='Directory containing triad files')
@click.option('--difficulty', '-d', default=20, help='Difficulty level')
@click.option('--output-dir', '-o', default='./solutions', help='Output directory for solutions')
@click.option('--max-iterations', '-m', type=int, help='Maximum iterations per triad')
def mine_continuous(triads_dir, difficulty, output_dir, max_iterations):
    """Continuous mining of multiple triads"""
    triads_path = Path(triads_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    triad_files = list(triads_path.glob('*.json'))
    
    if not triad_files:
        click.echo("No triad files found", err=True)
        return
    
    click.echo(f"Found {len(triad_files)} triad files")
    
    for triad_file in triad_files:
        click.echo(f"\nProcessing {triad_file.name}")
        
        try:
            with open(triad_file, 'r') as f:
                triad_data = json.load(f)
            
            triad = Triad.from_dict(triad_data)
            pof = PoF(triad, difficulty)
            
            # Create puzzle
            vdf_output, vdf_proof = pof.create_puzzle()
            
            # Solve puzzle
            nonce = pof.solve_puzzle(triad, vdf_output)
            
            solution = {
                'triad_file': str(triad_file),
                'triad_hash': triad.get_header_hash().hex(),
                'vdf_output': vdf_output.hex(),
                'vdf_proof': vdf_proof.hex(),
                'nonce': nonce,
                'difficulty': difficulty,
                'timestamp': int(time.time())
            }
            
            solution_file = output_path / f"{triad_file.stem}_solution.json"
            with open(solution_file, 'w') as f:
                json.dump(solution, f, indent=2)
            
            click.echo(f"  Solution saved to {solution_file}")
            
        except Exception as e:
            click.echo(f"  Failed to process {triad_file.name}: {e}", err=True)

@pof_group.command()
@click.option('--target-time', '-t', type=float, required=True, help='Target mining time in seconds')
@click.option('--triad-file', '-f', required=True, help='Sample triad file')
@click.option('--iterations', '-n', default=10, help='Number of test iterations')
def estimate_difficulty(target_time, triad_file, iterations):
    """Estimate appropriate difficulty for target mining time"""
    try:
        with open(triad_file, 'r') as f:
            triad_data = json.load(f)
        
        triad = Triad.from_dict(triad_data)
        
        click.echo(f"Estimating difficulty for target time: {target_time}s")
        click.echo(f"Running {iterations} test iterations...")
        
        results = []
        for difficulty in range(10, 31, 2):  # Test difficulties 10-30
            times = []
            for _ in range(iterations):
                pof = PoF(triad, difficulty)
                vdf_output, vdf_proof = pof.create_puzzle()
                
                start_time = time.time()
                nonce = pof.solve_puzzle(triad, vdf_output)
                end_time = time.time()
                
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            results.append({
                'difficulty': difficulty,
                'average_time': avg_time,
                'times': times
            })
            
            click.echo(f"  Difficulty {difficulty}: {avg_time:.2f}s average")
        
        # Find closest to target
        closest = min(results, key=lambda x: abs(x['average_time'] - target_time))
        
        click.echo(f"\nRecommended difficulty: {closest['difficulty']} (avg time: {closest['average_time']:.2f}s)")
        
    except Exception as e:
        click.echo(f"Difficulty estimation failed: {e}", err=True)

if __name__ == '__main__':
    pof_group()
