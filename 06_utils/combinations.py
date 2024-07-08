
'''
Standalone script that takes
1. X lists
2. Y inputs per list

and generates all possible combinations of electrode montages. 

To be used later for general TI optimization.

Ido Haber
May 2024
'''



from itertools import product

def generate_combinations(E1_plus, E1_minus, E2_plus, E2_minus):
    combinations = []
    for e1p, e1m in product(E1_plus, E1_minus):
        for e2p, e2m in product(E2_plus, E2_minus):
            combinations.append(((e1p, e1m), (e2p, e2m)))
    return combinations

# Example lists
E1_plus = ['x', 'y', 'z']
E1_minus = ['a', 'b', 'c']
E2_plus = ['p', 'q', 'r']
E2_minus = ['u', 'v', 'w']

# Generate all combinations
all_combinations = generate_combinations(E1_plus, E1_minus, E2_plus, E2_minus)

# Print combinations
for combo in all_combinations:
    print(combo)

# Print the number of combinations
print(f'Total number of combinations: {len(all_combinations)}')
