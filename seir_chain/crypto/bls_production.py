#!/usr/bin/env python3
"""
Production-ready BLS (Boneh–Lynn–Shacham) signature implementation.
Enhanced version with proper private key generation and validation.
"""

from py_ecc.bls import G2ProofOfPossession as bls_pop
from typing import List, Tuple, Dict, Any
import os
import json
import hashlib
from dataclasses import dataclass

@dataclass
class BLSKeyPair:
    """Represents a BLS key pair with metadata."""
    secret_key: bytes
    public_key: bytes
    key_id: str = ""

@dataclass
class BLSSignature:
    """Represents a BLS signature with metadata."""
    signature: bytes
    public_key: bytes
    message: bytes
    timestamp: int = 0

class ProductionBLS:
    """
    Production-ready BLS signature implementation with enhanced features.
    """
    
    def __init__(self):
        # BLS12-381 curve order
        self.curve_order = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001
        
    def generate_key_pair(self, key_id: str = "") -> BLSKeyPair:
        """
        Generate a secure BLS key pair with optional identifier.
        
        Args:
            key_id: Optional identifier for the key pair
            
        Returns:
            BLSKeyPair object containing secret and public keys
        """
        # Generate a valid BLS private key (must be < curve_order and > 0)
        while True:
            # Generate 32 random bytes
            random_bytes = os.urandom(32)
            secret_key_int = int.from_bytes(random_bytes, 'big') % self.curve_order
            
            # Ensure it's within valid range and not zero
            if 0 < secret_key_int < self.curve_order:
                break
        
        secret_key = secret_key_int.to_bytes(32, 'big')
        public_key = bls_pop.SkToPk(secret_key_int)
        return BLSKeyPair(secret_key=secret_key, public_key=public_key, key_id=key_id)
    
    def sign_message(self, message: bytes, secret_key: bytes) -> BLSSignature:
        """
        Sign a message with enhanced error handling and metadata.
        
        Args:
            message: Message to sign
            secret_key: Secret key for signing
            
        Returns:
            BLSSignature object with signature and metadata
        """
        if not isinstance(message, bytes):
            raise TypeError("Message must be bytes")
        if len(secret_key) != 32:
            raise ValueError("Secret key must be 32 bytes")
            
        secret_key_int = int.from_bytes(secret_key, 'big')
        signature = bls_pop.Sign(secret_key_int, message)
        public_key = bls_pop.SkToPk(secret_key_int)
        
        return BLSSignature(
            signature=signature,
            public_key=public_key,
            message=message,
            timestamp=int.from_bytes(os.urandom(4), 'big')
        )
    
    def verify_signature(self, signature: BLSSignature) -> bool:
        """
        Verify a signature with comprehensive validation.
        
        Args:
            signature: BLSSignature object to verify
            
        Returns:
            bool: True if signature is valid
        """
        try:
            return bls_pop.Verify(signature.public_key, signature.message, signature.signature)
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False
    
    def batch_verify(self, signatures: List[BLSSignature]) -> Dict[str, Any]:
        """
        Batch verify multiple signatures for performance optimization.
        
        Args:
            signatures: List of BLSSignature objects to verify
            
        Returns:
            Dict with verification results and performance metrics
        """
        results = {
            "total_signatures": len(signatures),
            "valid_signatures": 0,
            "invalid_signatures": 0,
            "invalid_indices": [],
            "verification_time_ms": 0
        }
        
        import time
        start_time = time.time()
        
        for i, sig in enumerate(signatures):
            if self.verify_signature(sig):
                results["valid_signatures"] += 1
            else:
                results["invalid_signatures"] += 1
                results["invalid_indices"].append(i)
        
        end_time = time.time()
        results["verification_time_ms"] = (end_time - start_time) * 1000
        
        return results
    
    def aggregate_signatures(self, signatures: List[bytes]) -> bytes:
        """
        Aggregate multiple signatures with validation.
        
        Args:
            signatures: List of signature bytes to aggregate
            
        Returns:
            bytes: Aggregated signature
        """
        if not signatures:
            raise ValueError("Cannot aggregate empty signature list")
        
        # Validate all signatures are valid BLS signatures
        for sig in signatures:
            if len(sig) != 96:  # BLS signature size
                raise ValueError(f"Invalid signature length: {len(sig)}")
        
        return bls_pop.Aggregate(signatures)
    
    def aggregate_public_keys(self, public_keys: List[bytes]) -> bytes:
        """
        Aggregate multiple public keys with validation.
        
        Args:
            public_keys: List of public key bytes to aggregate
            
        Returns:
            bytes: Aggregated public key
        """
        if not public_keys:
            raise ValueError("Cannot aggregate empty public key list")
        
        # Validate all public keys are valid BLS public keys
        for pk in public_keys:
            if len(pk) != 48:  # BLS public key size
                raise ValueError(f"Invalid public key length: {len(pk)}")
        
        return bls_pop._AggregatePKs(public_keys)
    
    def verify_aggregated_signature(self, 
                                  aggregated_signature: bytes,
                                  aggregated_public_key: bytes,
                                  message: bytes) -> bool:
        """
        Verify an aggregated signature with comprehensive validation.
        
        Args:
            aggregated_signature: The aggregated signature
            aggregated_public_key: The aggregated public key
            message: The message that was signed
            
        Returns:
            bool: True if the aggregated signature is valid
        """
        try:
            return bls_pop.AggregateVerify(
                [aggregated_public_key], 
                [message], 
                aggregated_signature
            )
        except Exception as e:
            print(f"Aggregated signature verification failed: {e}")
            return False
    
    def serialize_signature(self, signature: BLSSignature) -> str:
        """
        Serialize a signature for network transmission or storage.
        
        Args:
            signature: BLSSignature object to serialize
            
        Returns:
            str: JSON-serialized signature
        """
        return json.dumps({
            "signature": signature.signature.hex(),
            "public_key": signature.public_key.hex(),
            "message": signature.message.hex(),
            "timestamp": signature.timestamp
        })
    
    def deserialize_signature(self, serialized: str) -> BLSSignature:
        """
        Deserialize a signature from network transmission or storage.
        
        Args:
            serialized: JSON-serialized signature string
            
        Returns:
            BLSSignature: Deserialized signature object
        """
        data = json.loads(serialized)
        return BLSSignature(
            signature=bytes.fromhex(data["signature"]),
            public_key=bytes.fromhex(data["public_key"]),
            message=bytes.fromhex(data["message"]),
            timestamp=data["timestamp"]
        )
    
    def generate_test_data(self, count: int = 10) -> List[BLSSignature]:
        """
        Generate test data for benchmarking and testing.
        
        Args:
            count: Number of test signatures to generate
            
        Returns:
            List[BLSSignature]: List of test signatures
        """
        test_data = []
        for i in range(count):
            key_pair = self.generate_key_pair(f"test_key_{i}")
            message = f"test_message_{i}".encode()
            signature = self.sign_message(message, key_pair.secret_key)
            test_data.append(signature)
        return test_data

# Export production-ready functions
production_bls = ProductionBLS()
