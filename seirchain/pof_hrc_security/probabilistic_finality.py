import math

def calculate_required_confirmations(prob_error, fraction_malicious):
    """
    Calculates the number of confirmations required to achieve a certain
    probability of error, given a fraction of malicious nodes.

    This is based on the formula from the Bitcoin whitepaper:
    P = 1 - sum_{k=0 to z-1} [ (lambda^k * e^-lambda) / k! ]
    where lambda = z * q / p

    We can simplify this for our model. If an attacker has a fraction `q`
    of the network's power, the probability of them producing the next `k`
    blocks is `q^k`. We want to find `k` such that this probability is
    below a certain error threshold.
    """
    if fraction_malicious <= 0:
        return 1
    if fraction_malicious >= 0.5:
        return float('inf') # Finality is not possible

    # We want to find k such that q^k < prob_error
    # k * log(q) < log(prob_error)
    # k > log(prob_error) / log(q)  (since log(q) is negative)

    k = math.log(prob_error) / math.log(fraction_malicious)
    return math.ceil(k)

def simulate_finality_under_attack(malicious_fraction_scenarios, error_probability=1e-6):
    """
    Simulates the time-to-finality under different attack scenarios.
    """
    print(f"Required confirmations for an error probability of {error_probability}:")
    for fraction in malicious_fraction_scenarios:
        confirmations = calculate_required_confirmations(error_probability, fraction)
        print(f"  - {fraction*100:.0f}% malicious nodes: {confirmations} confirmations")

if __name__ == '__main__':
    scenarios = [0.1, 0.2, 0.3, 0.4, 0.49]
    simulate_finality_under_attack(scenarios)
