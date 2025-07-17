from seirchain.wac_token import WACToken

class SlashingCondition:
    def __init__(self, wac_token):
        self.wac_token = wac_token
        self.signed_blocks = {}

    def detect_double_signing(self, validator_address, block_header):
        if validator_address in self.signed_blocks:
            for signed_block_header in self.signed_blocks[validator_address]:
                if signed_block_header['height'] == block_header['height'] and signed_block_header['hash'] != block_header['hash']:
                    return True
        return False

    def slash_validator(self, validator_address, amount):
        self.wac_token.burn(validator_address, amount)

    def add_signed_block(self, validator_address, block_header):
        if validator_address not in self.signed_blocks:
            self.signed_blocks[validator_address] = []
        self.signed_blocks[validator_address].append(block_header)
