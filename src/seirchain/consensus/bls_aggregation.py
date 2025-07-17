from py_ecc.bls import G2ProofOfPossession as bls_pop

def generate_validator_keys(num_validators):
    """
    Generates a list of validator private and public keys.
    """
    validators = []
    for _ in range(num_validators):
        private_key = bls_pop.KeyGen(bytes([_]))
        public_key = bls_pop.SkToPk(private_key)
        validators.append({"private_key": private_key, "public_key": public_key})
    return validators

def sign_message(private_key, message):
    """
    Signs a message with a private key.
    """
    return bls_pop.Sign(private_key, message)

def aggregate_signatures(signatures):
    """
    Aggregates a list of signatures into a single signature.
    """
    return bls_pop.Aggregate(signatures)

def aggregate_public_keys(public_keys):
    """
    Aggregates a list of public keys into a single public key.
    """
    return bls_pop._AggregatePKs(public_keys)

def verify_aggregated_signature(aggregated_signature, aggregated_public_key, message):
    """
    Verifies an aggregated signature against an aggregated public key and a message.
    """
    return bls_pop.Verify(aggregated_public_key, message, aggregated_signature)
