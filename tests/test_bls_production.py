#!/usr/bin/env python3
"""
Comprehensive test suite for production-ready BLS implementation.
Tests all aspects of the BLS signature system including security and performance.
"""

import pytest
import time
import json
import os
from seir_chain.crypto.bls_production import ProductionBLS, BLSKeyPair, BLSSignature

class TestProductionBLS:
    """Test suite for production BLS implementation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.bls = ProductionBLS()
    
    def test_key_generation(self):
        """Test key pair generation."""
        key_pair = self.bls.generate_key_pair("test_key")
        assert isinstance(key_pair, BLSKeyPair)
        assert len(key_pair.secret_key) == 32
        assert len(key_pair.public_key) == 48
        assert key_pair.key_id == "test_key"
    
    def test_sign_and_verify(self):
        """Test basic signing and verification."""
        message = b"test_message"
        key_pair = self.bls.generate_key_pair()
        
        signature = self.bls.sign_message(message, key_pair.secret_key)
        assert isinstance(signature, BLSSignature)
        assert signature.message == message
        
        # Verify the signature
        assert self.bls.verify_signature(signature) is True
    
    def test_invalid_signature(self):
        """Test signature verification with invalid data."""
        message = b"test_message"
        key_pair = self.bls.generate_key_pair()
        
        # Create valid signature
        signature = self.bls.sign_message(message, key_pair.secret_key)
        
        # Tamper with the signature
        tampered_signature = BLSSignature(
            signature=signature.signature[:-1] + b'\x00',
            public_key=signature.public_key,
            message=signature.message
        )
        
        assert self.bls.verify_signature(tampered_signature) is False
    
    def test_wrong_public_key(self):
        """Test verification with wrong public key."""
        message = b"test_message"
        key_pair1 = self.bls.generate_key_pair()
        key_pair2 = self.bls.generate_key_pair()
        
        signature = self.bls.sign_message(message, key_pair1.secret_key)
        
        # Use wrong public key
        wrong_signature = BLSSignature(
            signature=signature.signature,
            public_key=key_pair2.public_key,
            message=signature.message
        )
        
        assert self.bls.verify_signature(wrong_signature) is False
    
    def test_wrong_message(self):
        """Test verification with wrong message."""
        key_pair = self.bls.generate_key_pair()
        
        signature = self.bls.sign_message(b"correct_message", key_pair.secret_key)
        
        # Use wrong message
        wrong_signature = BLSSignature(
            signature=signature.signature,
            public_key=signature.public_key,
            message=b"wrong_message"
        )
        
        assert self.bls.verify_signature(wrong_signature) is False
    
    def test_signature_aggregation(self):
        """Test signature aggregation functionality."""
        messages = [b"message1", b"message2", b"message3"]
        key_pairs = [self.bls.generate_key_pair() for _ in range(3)]
        
        signatures = []
        for message, key_pair in zip(messages, key_pairs):
            sig = self.bls.sign_message(message, key_pair.secret_key)
            signatures.append(sig.signature)
        
        # Aggregate signatures
        aggregated = self.bls.aggregate_signatures(signatures)
        assert len(aggregated) == 96  # BLS aggregated signature size
        
        # Aggregate public keys
        public_keys = [kp.public_key for kp in key_pairs]
        aggregated_pk = self.bls.aggregate_public_keys(public_keys)
        assert len(aggregated_pk) == 48  # BLS aggregated public key size
    
    def test_batch_verification(self):
        """Test batch verification of multiple signatures."""
        signatures = []
        for i in range(10):
            key_pair = self.bls.generate_key_pair()
            message = f"test_message_{i}".encode()
            signature = self.bls.sign_message(message, key_pair.secret_key)
            signatures.append(signature)
        
        # Test batch verification
        results = self.bls.batch_verify(signatures)
        assert results["total_signatures"] == 10
        assert results["valid_signatures"] == 10
        assert results["invalid_signatures"] == 0
        assert results["verification_time_ms"] > 0
    
    def test_batch_verification_with_invalid(self):
        """Test batch verification with some invalid signatures."""
        signatures = []
        
        # Create valid signatures
        for i in range(5):
            key_pair = self.bls.generate_key_pair()
            message = f"test_message_{i}".encode()
            signature = self.bls.sign_message(message, key_pair.secret_key)
            signatures.append(signature)
        
        # Add invalid signature
        invalid_key_pair = self.bls.generate_key_pair()
        invalid_signature = BLSSignature(
            signature=os.urandom(96),  # Random invalid signature
            public_key=invalid_key_pair.public_key,
            message=b"invalid_message"
        )
        signatures.append(invalid_signature)
        
        results = self.bls.batch_verify(signatures)
        assert results["total_signatures"] == 6
        assert results["valid_signatures"] == 5
        assert results["invalid_signatures"] == 1
        assert len(results["invalid_indices"]) == 1
    
    def test_serialization(self):
        """Test signature serialization and deserialization."""
        key_pair = self.bls.generate_key_pair()
        message = b"serialization_test"
        signature = self.bls.sign_message(message, key_pair.secret_key)
        
        # Serialize
        serialized = self.bls.serialize_signature(signature)
        assert isinstance(serialized, str)
        
        # Deserialize
        deserialized = self.bls.deserialize_signature(serialized)
        assert isinstance(deserialized, BLSSignature)
        assert deserialized.signature == signature.signature
        assert deserialized.public_key == signature.public_key
        assert deserialized.message == signature.message
    
    def test_error_handling(self):
        """Test error handling for edge cases."""
        # Test empty signature aggregation
        with pytest.raises(ValueError, match="Cannot aggregate empty signature list"):
            self.bls.aggregate_signatures([])
        
        # Test empty public key aggregation
        with pytest.raises(ValueError, match="Cannot aggregate empty public key list"):
            self.bls.aggregate_public_keys([])
        
        # Test invalid signature length
        with pytest.raises(ValueError, match="Invalid signature length"):
            self.bls.aggregate_signatures([b"short_signature"])
        
        # Test invalid public key length
        with pytest.raises(ValueError, match="Invalid public key length"):
            self.bls.aggregate_public_keys([b"short_pubkey"])
    
    def test_performance_benchmark(self):
        """Test performance characteristics."""
        # Generate test data
        signatures = self.bls.generate_test_data(100)
        
        # Measure verification time
        start_time = time.time()
        results = self.bls.batch_verify(signatures)
        end_time = time.time()
        
        total_time = (end_time - start_time) * 1000
        assert total_time < 1000  # Should complete within 1 second for 100 signatures
        assert results["valid_signatures"] == 100
    
    def test_key_pair_generation_uniqueness(self):
        """Test that generated key pairs are unique."""
        key_pairs = [self.bls.generate_key_pair() for _ in range(100)]
        secret_keys = [kp.secret_key for kp in key_pairs]
        public_keys = [kp.public_key for kp in key_pairs]
        
        # Check uniqueness
        assert len(set(secret_keys)) == 100
        assert len(set(public_keys)) == 100
    
    def test_aggregated_signature_verification(self):
        """Test verification of aggregated signatures."""
        message = b"aggregated_test_message"
        key_pairs = [self.bls.generate_key_pair() for _ in range(5)]
        
        # Create individual signatures
        signatures = []
        for key_pair in key_pairs:
            sig = self.bls.sign_message(message, key_pair.secret_key)
            signatures.append(sig.signature)
        
        # Aggregate signatures
        aggregated_sig = self.bls.aggregate_signatures(signatures)
        
        # Aggregate public keys
        public_keys = [kp.public_key for kp in key_pairs]
        aggregated_pk = self.bls.aggregate_public_keys(public_keys)
        
        # Verify aggregated signature
        assert self.bls.verify_aggregated_signature(
            aggregated_sig, 
            aggregated_pk, 
            message
        ) is True
    
    def test_stress_test(self):
        """Stress test with large number of signatures."""
        num_signatures = 1000
        signatures = self.bls.generate_test_data(num_signatures)
        
        results = self.bls.batch_verify(signatures)
        assert results["total_signatures"] == num_signatures
        assert results["valid_signatures"] == num_signatures
        assert results["verification_time_ms"] < 5000  # Should complete within 5 seconds

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
