"""
Comprehensive test suite for SeirChain data structures and integrity features
Tests all cryptographic components, Triad structure, and Fractal Merkle Anchor
"""

import hashlib
import json
import time
from seirchain.crypto.transaction import Transaction
from seirchain.crypto.wallet import Wallet
from seirchain.crypto.dilithium import DilithiumWallet, DilithiumSigner
from seirchain.structures.triad import Triad, TernaryCoordinate, TriadChain
from seirchain.structures.merkle import MerkleTree, compute_merkle_root
from seirchain.integrity.fma import FractalMerkleAnchor


class TestRunner:
    """Test runner for all integrity features"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name: str, test_func):
        """Run a single test and record results"""
        try:
            result = test_func()
            if result:
                self.passed += 1
                self.test_results.append(f"✅ {test_name}")
            else:
                self.failed += 1
                self.test_results.append(f"❌ {test_name}")
        except Exception as e:
            self.failed += 1
            self.test_results.append(f"❌ {test_name} (Error: {str(e)})")
    
    def print_results(self):
        """Print test results"""
        print("\n" + "="*60)
        print("SEIRCHAIN INTEGRITY TEST RESULTS")
        print("="*60)
        for result in self.test_results:
            print(result)
        print(f"\nPassed: {self.passed}, Failed: {self.failed}")
        print("="*60)


def test_transaction_signing():
    """Test transaction signing and verification"""
    print("\n🔐 Testing Transaction Signing...")
    
    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    # Create transaction
    tx = Transaction(wallet1.get_address(), wallet2.get_address(), 10.5)
    
    # Sign transaction
    signature = tx.sign(wallet1.private_key, "ecdsa")
    tx.signature = signature
    
    # Verify signature
    is_valid = tx.verify_signature(wallet1.public_key, signature, "ecdsa")
    
    print(f"   Transaction: {tx}")
    print(f"   Signature valid: {is_valid}")
    
    return is_valid


def test_dilithium_signatures():
    """Test Dilithium post-quantum signatures"""
    print("\n🔮 Testing Dilithium Signatures...")
    
    # Create Dilithium wallet
    dil_wallet = DilithiumWallet()
    
    # Create transaction
    tx_data = {
        'sender': dil_wallet.get_address(),
        'recipient': 'recipient_address',
        'amount': 5.0,
        'nonce': 12345
    }
    
    # Sign with Dilithium
    signature = DilithiumSigner.sign_transaction(tx_data, dil_wallet.get_private_key())
    
    # Verify signature
    is_valid = DilithiumSigner.verify_transaction_signature(tx_data, signature, dil_wallet.get_public_key())
    
    print(f"   Dilithium signature: {signature[:16]}...")
    print(f"   Signature valid: {is_valid}")
    
    return is_valid


def test_merkle_tree():
    """Test Merkle tree construction and proofs"""
    print("\n🌳 Testing Merkle Tree...")
    
    # Create transactions
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    transactions = [
        Transaction(wallet1.get_address(), wallet2.get_address(), 10.0),
        Transaction(wallet2.get_address(), wallet1.get_address(), 5.0),
        Transaction(wallet1.get_address(), wallet2.get_address(), 7.5),
        Transaction(wallet2.get_address(), wallet1.get_address(), 3.0)
    ]
    
    # Build Merkle tree
    tree = MerkleTree(transactions)
    merkle_root = tree.get_root()
    
    # Generate proof for first transaction
    proof = tree.get_proof(transactions[0])
    
    # Verify proof
    is_valid = proof.verify() if proof else False
    
    print(f"   Merkle root: {merkle_root}")
    print(f"   Proof valid: {is_valid}")
    print(f"   Tree size: {len(tree)} transactions")
    
    return is_valid and merkle_root is not None


def test_triad_structure():
    """Test Triad structure and integrity"""
    print("\n🔺 Testing Triad Structure...")
    
    # Create wallets and transactions
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    transactions = [
        Transaction(wallet1.get_address(), wallet2.get_address(), 10.0),
        Transaction(wallet2.get_address(), wallet1.get_address(), 5.0)
    ]
    
    # Create triad
    triad = Triad(
        transactions=transactions,
        coordinates=TernaryCoordinate(1, 1, 0, 0)
    )
    
    # Test integrity
    is_integrity_valid = triad.verify_integrity()
    
    # Test Merkle root
    expected_merkle = compute_merkle_root(transactions)
    is_merkle_valid = triad.merkle_root == expected_merkle
    
    print(f"   Triad hash: {triad.triad_hash[:16]}...")
    print(f"   Integrity valid: {is_integrity_valid}")
    print(f"   Merkle root valid: {is_merkle_valid}")
    print(f"   Coordinates: {triad.coordinates.to_ternary_string()}")
    
    return is_integrity_valid and is_merkle_valid


def test_triad_chain():
    """Test Triad chain with parent linking"""
    print("\n⛓️ Testing Triad Chain...")
    
    # Create wallets
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    # Create chain
    chain = TriadChain()
    
    # Genesis triad
    genesis_tx = [Transaction(wallet1.get_address(), wallet2.get_address(), 50.0)]
    genesis_triad = Triad(
        transactions=genesis_tx,
        coordinates=TernaryCoordinate(0, 0, 0, 0)
    )
    
    # Add to chain
    genesis_added = chain.add_triad(genesis_triad)
    
    # Child triad
    child_tx = [Transaction(wallet2.get_address(), wallet1.get_address(), 25.0)]
    child_triad = Triad(
        transactions=child_tx,
        parent_hash=genesis_triad.triad_hash,
        coordinates=TernaryCoordinate(1, 1, 0, 0)
    )
    
    # Add to chain
    child_added = chain.add_triad(child_triad)
    
    # Verify chain integrity
    chain_integrity = chain.verify_chain_integrity()
    
    print(f"   Genesis added: {genesis_added}")
    print(f"   Child added: {child_added}")
    print(f"   Chain integrity: {chain_integrity}")
    print(f"   Chain length: {chain.get_chain_length()}")
    
    return genesis_added and child_added and chain_integrity


def test_fma_verification():
    """Test Fractal Merkle Anchor verification"""
    print("\n⚓ Testing Fractal Merkle Anchor...")
    
    # Create test triad
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    transactions = [
        Transaction(wallet1.get_address(), wallet2.get_address(), 10.0),
        Transaction(wallet2.get_address(), wallet1.get_address(), 5.0)
    ]
    
    triad = Triad(
        transactions=transactions,
        coordinates=TernaryCoordinate(2, 1, 1, 0)
    )
    
    # Initialize FMA
    fma = FractalMerkleAnchor()
    
    # Create anchor
    anchor = fma.create_anchor(triad, 2)
    
    # Verify triad
    is_valid = fma.verify_fma(triad)
    
    # Create tamper evidence
    demo = fma.create_tamper_evidence_demo(triad)
    
    print(f"   FMA Anchor: {anchor[:16]}...")
    print(f"   Triad valid: {is_valid}")
    print(f"   Tamper detection: {demo['detection_success']}")
    
    return is_valid and demo['detection_success']


def test_tamper_detection():
    """Test comprehensive tamper detection"""
    print("\n🚨 Testing Tamper Detection...")
    
    # Create original triad
    wallet1 = Wallet()
    wallet2 = Wallet()
    
    original_transactions = [
        Transaction(wallet1.get_address(), wallet2.get_address(), 10.0),
        Transaction(wallet2.get_address(), wallet1.get_address(), 5.0)
    ]
    
    original_triad = Triad(
        transactions=original_transactions,
        coordinates=TernaryCoordinate(1, 0, 1, 0)
    )
    
    # Create tampered triad
    tampered_transactions = original_transactions.copy()
    tampered_transactions[0].amount = 1000.0  # Tamper with amount
    
    tampered_triad = Triad(
        transactions=tampered_transactions,
        coordinates=TernaryCoordinate(1, 0, 1, 0)
    )
    
    # Verify integrity
    original_valid = original_triad.verify_integrity()
    tampered_valid = tampered_triad.verify_integrity()
    
    # Check Merkle roots
    original_merkle = original_triad.merkle_root
    tampered_merkle = tampered_triad.merkle_root
    
    print(f"   Original valid: {original_valid}")
    print(f"   Tampered valid: {tampered_valid}")
    print(f"   Merkle roots different: {original_merkle != tampered_merkle}")
    
    return original_valid and not tampered_valid and (original_merkle != tampered_merkle)


def test_ternary_coordinates():
    """Test ternary coordinate system"""
    print("\n🎯 Testing Ternary Coordinates...")
    
    # Create coordinates
    coord = TernaryCoordinate(level=3, x=5, y=2, z=1)
    
    # Test string representation
    coord_str = coord.to_ternary_string()
    
    # Test address generation
    address = coord.to_address()
    
    # Test round-trip conversion
    parsed_coord = TernaryCoordinate.from_string(coord_str)
    
    is_valid = (coord.level == parsed_coord.level and
                coord.x == parsed_coord.x and
                coord.y == parsed_coord.y and
                coord.z == parsed_coord.z)
    
    print(f"   Coordinates: {coord_str}")
    print(f"   Address: {address}")
    print(f"   Round-trip valid: {is_valid}")
    
    return is_valid and len(address) == 32


def test_merkle_proofs():
    """Test Merkle proof generation and verification"""
    print
