import pytest
from .bls_aggregation import (
    generate_validator_keys,
    sign_message,
    aggregate_signatures,
    aggregate_public_keys,
    verify_aggregated_signature,
)

@pytest.fixture
def validators():
    return generate_validator_keys(5)

@pytest.fixture
def message():
    return b"This is a test message"

def test_bls_aggregation_valid(validators, message):
    signatures = []
    public_keys = []
    for validator in validators:
        signatures.append(sign_message(validator["private_key"], message))
        public_keys.append(validator["public_key"])

    aggregated_signature = aggregate_signatures(signatures)
    aggregated_public_key = aggregate_public_keys(public_keys)

    assert verify_aggregated_signature(aggregated_signature, aggregated_public_key, message)

def test_bls_aggregation_invalid_signature(validators, message):
    signatures = []
    public_keys = []
    for validator in validators:
        signatures.append(sign_message(validator["private_key"], message))
        public_keys.append(validator["public_key"])

    # Tamper with the first signature
    signatures[0] = signatures[0][:-1] + bytes([0])

    aggregated_signature = aggregate_signatures(signatures)
    aggregated_public_key = aggregate_public_keys(public_keys)

    assert not verify_aggregated_signature(aggregated_signature, aggregated_public_key, message)

def test_bls_aggregation_invalid_message(validators, message):
    signatures = []
    public_keys = []
    for validator in validators:
        signatures.append(sign_message(validator["private_key"], message))
        public_keys.append(validator["public_key"])

    aggregated_signature = aggregate_signatures(signatures)
    aggregated_public_key = aggregate_public_keys(public_keys)

    invalid_message = b"This is an invalid message"

    assert not verify_aggregated_signature(aggregated_signature, aggregated_public_key, invalid_message)
