import os
from py_ecc.bls import G2ProofOfPossession as bls
# 1. Setup: Generate keys for a committee of validators
committee_size = 10
# Note: Using a simple counter for private keys for deterministic testing.
# In production, use a secure random source as originally intended.
private_keys = [i + 1 for i in range(committee_size)]
public_keys = [bls.SkToPk(sk) for sk in private_keys]

print(f"Generated {committee_size} validator key pairs.\n")

# 2. Define the message to be signed (representing Triad data)
# In a real scenario, this would be the hash of the Triad's canonical representation.
message = b"Triad_Data_Hash_#12345"
print(f"Message to sign: {message.decode('utf-8')}\n")

# 3. Each validator signs the message
signatures = [bls.Sign(sk, message) for sk in private_keys]
print("Each validator has signed the message.\n")

# 4. Aggregate the signatures
aggregated_signature = bls.Aggregate(signatures)
print(f"Aggregated Signature (first 10 bytes): {aggregated_signature[:10]}...\n")

# 5. Aggregate the public keys
aggregated_public_key = bls._AggregatePKs(public_keys)
print(f"Aggregated Public Key (first 10 bytes): {aggregated_public_key[:10]}...\n")

# 6. Verify the aggregated signature
# A single verification checks that all original signers approved the message.
is_valid = bls.Verify(aggregated_public_key, message, aggregated_signature)

print("--- Verification Result ---")
if is_valid:
    print("SUCCESS: The aggregated signature is valid.")
    print("This single check confirms that the entire committee approved the Triad data.")
else:
    print("FAILURE: The aggregated signature is invalid.")

# 7. (Optional) Tampering Simulation: Verify with a wrong message
wrong_message = b"Malicious_Triad_Data"
is_valid_tampered = bls.Verify(aggregated_public_key, wrong_message, aggregated_signature)

print("\n--- Tampering Simulation ---")
print(f"Verifying with wrong message: {wrong_message.decode('utf-8')}")
if not is_valid_tampered:
    print("SUCCESS: The signature correctly fails to verify with tampered data.")
else:
    print("FAILURE: The signature verified tampered data, which is a security risk.")
