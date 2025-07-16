OPCODE_GAS_COSTS = {
    "ADD": 3,
    "SUB": 3,
    "MUL": 5,
    "DIV": 5,
    "STOP": 0,
    "PUSH": 2,
    "POP": 2,
    "LOAD": 3,
    "STORE": 5,
}

def calculate_gas(opcodes: list[str]) -> int:
    """
    Calculates the execution cost of a smart contract based on its operation codes.

    Args:
        opcodes: A list of operation codes.

    Returns:
        The total gas cost.
    """
    total_gas = 0
    for opcode in opcodes:
        total_gas += OPCODE_GAS_COSTS.get(opcode.upper(), 1)  # Default to 1 for unknown opcodes
    return total_gas
