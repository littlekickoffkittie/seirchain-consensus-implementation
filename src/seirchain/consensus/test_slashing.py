import pytest
from seirchain.wac_token import WACToken
from seirchain.consensus.slashing import SlashingCondition

@pytest.fixture
def wac_token():
    return WACToken(1000, "genesis_address")

@pytest.fixture
def slashing_condition(wac_token):
    return SlashingCondition(wac_token)

def test_detect_double_signing(slashing_condition):
    validator_address = "validator_1"
    block_header_1 = {"height": 1, "hash": "hash_1"}
    block_header_2 = {"height": 1, "hash": "hash_2"}

    slashing_condition.add_signed_block(validator_address, block_header_1)
    assert slashing_condition.detect_double_signing(validator_address, block_header_2)

def test_slash_validator(slashing_condition):
    validator_address = "validator_1"
    initial_balance = 100
    slashing_condition.wac_token.balances[validator_address] = initial_balance
    slash_amount = 10

    slashing_condition.slash_validator(validator_address, slash_amount)
    assert slashing_condition.wac_token.balances[validator_address] == initial_balance - slash_amount

def test_no_double_signing(slashing_condition):
    validator_address = "validator_1"
    block_header_1 = {"height": 1, "hash": "hash_1"}
    block_header_2 = {"height": 2, "hash": "hash_2"}

    slashing_condition.add_signed_block(validator_address, block_header_1)
    assert not slashing_condition.detect_double_signing(validator_address, block_header_2)
