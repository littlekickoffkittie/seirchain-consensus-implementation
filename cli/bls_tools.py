#!/usr/bin/env python3
"""
BLS Cryptography CLI Tools
"""

import click
import json
import os
from pathlib import Path
import time

# Import BLS production module
from seir_chain.crypto.bls_production import ProductionBLS

bls = ProductionBLS()

@click.group(name='bls')
def bls_group():
    """BLS signature operations"""
    pass

@bls_group.command()
@click.option('--count', '-n', default=1, help='Number of key pairs to generate')
@click.option('--output-dir', '-o', default='./keys', help='Output directory for keys')
@click.option('--prefix', '-p', default='key', help='Key file prefix')
def generate_keys(count, output_dir, prefix):
    """Generate BLS key pairs"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    keys = []
    for i in range(count):
        key_pair = bls.generate_key_pair(f"{prefix}_{i}")
        
        # Save keys to files
        secret_file = output_path / f"{prefix}_{i}_secret.key"
        public_file = output_path / f"{prefix}_{i}_public.key"
        
        with open(secret_file, 'w') as f:
            f.write(key_pair.secret_key.hex())
        
        with open(public_file, 'w') as f:
            f.write(key_pair.public_key.hex())
        
        keys.append({
            'id': key_pair.key_id,
            'secret_file': str(secret_file),
            'public_file': str(public_file)
        })
    
    click.echo(f"Generated {count} key pairs in {output_dir}")
    for key in keys:
        click.echo(f"  {key['id']}: {key['public_file']}")

@bls_group.command()
@click.option('--message', '-m', required=True, help='Message to sign')
@click.option('--private-key', '-k', required=True, help='Private key (hex string or file)')
@click.option('--output', '-o', help='Output file for signature')
def sign(message, private_key, output):
    """Sign a message with BLS"""
    # Handle private key input
    if os.path.isfile(private_key):
        with open(private_key, 'r') as f:
            private_key = f.read().strip()
    
    try:
        private_key_bytes = bytes.fromhex(private_key)
    except ValueError:
        click.echo("Error: Invalid private key format", err=True)
        return
    
    signature = bls.sign_message(message.encode(), private_key_bytes)
    serialized = bls.serialize_signature(signature)
    
    if output:
        with open(output, 'w') as f:
            f.write(serialized)
        click.echo(f"Signature saved to {output}")
    else:
        click.echo(serialized)

@bls_group.command()
@click.option('--signature', '-s', required=True, help='Signature file or JSON string')
@click.option('--public-key', '-p', required=True, help='Public key (hex string or file)')
@click.option('--message', '-m', required=True, help='Original message')
def verify(signature, public_key, message):
    """Verify a BLS signature"""
    # Handle signature input
    if os.path.isfile(signature):
        with open(signature, 'r') as f:
            signature_data = f.read()
    else:
        signature_data = signature
    
    # Handle public key input
    if os.path.isfile(public_key):
        with open(public_key, 'r') as f:
            public_key = f.read().strip()
    
    try:
        sig_obj = bls.deserialize_signature(signature_data)
        sig_obj.message = message.encode()
        sig_obj.public_key = bytes.fromhex(public_key)
        
        is_valid = bls.verify_signature(sig_obj)
        click.echo(f"Signature valid: {is_valid}")
        
    except Exception as e:
        click.echo(f"Verification failed: {e}", err=True)

@bls_group.command()
@click.option('--signatures-file', '-f', required=True, help='File containing signatures (one per line)')
@click.option('--output', '-o', help='Output file for aggregated signature')
def aggregate_signatures(signatures_file, output):
    """Aggregate multiple BLS signatures"""
    signatures = []
    
    with open(signatures_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    sig = bytes.fromhex(line)
                    signatures.append(sig)
                except ValueError:
                    click.echo(f"Invalid signature format: {line}", err=True)
                    return
    
    if not signatures:
        click.echo("No signatures found", err=True)
        return
    
    try:
        aggregated = bls.aggregate_signatures(signatures)
        result = aggregated.hex()
        
        if output:
            with open(output, 'w') as f:
                f.write(result)
            click.echo(f"Aggregated signature saved to {output}")
        else:
            click.echo(result)
            
    except Exception as e:
        click.echo(f"Aggregation failed: {e}", err=True)

@bls_group.command()
@click.option('--count', '-n', default=10, help='Number of test signatures to generate')
@click.option('--output-dir', '-o', default='./test_data', help='Output directory')
def generate_test_data(count, output_dir):
    """Generate test data for BLS operations"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    test_data = bls.generate_test_data(count)
    
    # Save signatures
    signatures_file = output_path / 'signatures.json'
    with open(signatures_file, 'w') as f:
        json.dump([bls.serialize_signature(sig) for sig in test_data], f, indent=2)
    
    # Save public keys
    public_keys_file = output_path / 'public_keys.txt'
    with open(public_keys_file, 'w') as f:
        for sig in test_data:
            f.write(sig.public_key.hex() + '\n')
    
    # Save messages
    messages_file = output_path / 'messages.txt'
    with open(messages_file, 'w') as f:
        for sig in test_data:
            f.write(sig.message.decode() + '\n')
    
    click.echo(f"Generated test data in {output_dir}")
    click.echo(f"  Signatures: {signatures_file}")
    click.echo(f"  Public keys: {public_keys_file}")
    click.echo(f"  Messages: {messages_file}")

@bls_group.command()
@click.option('--signatures-file', '-f', required=True, help='File containing serialized signatures')
def batch_verify(signatures_file):
    """Batch verify multiple signatures"""
    try:
        with open(signatures_file, 'r') as f:
            signatures_data = json.load(f)
        
        signatures = [bls.deserialize_signature(sig_data) for sig_data in signatures_data]
        results = bls.batch_verify(signatures)
        
        click.echo(f"Total signatures: {results['total_signatures']}")
        click.echo(f"Valid signatures: {results['valid_signatures']}")
        click.echo(f"Invalid signatures: {results['invalid_signatures']}")
        click.echo(f"Verification time: {results['verification_time_ms']:.2f}ms")
        
        if results['invalid_indices']:
            click.echo(f"Invalid indices: {results['invalid_indices']}")
            
    except Exception as e:
        click.echo(f"Batch verification failed: {e}", err=True)

if __name__ == '__main__':
    bls_group()
