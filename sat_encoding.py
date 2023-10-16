### Made by Haris Rasul
### Oct 15th 2023
### Purpose: SAT Encodings
# sat_encoding.py
from pysat.formula import CNF
from pysat.solvers import Solver

# A dictionary to store the mapping between (prefix, t, j) tuples and unique variable indices
var_mapping = {}
current_index = 1

def choose_one_feature_at_branching(TB, F):
    """
    Encode that exactly one feature is chosen at each branching node.

    Parameters:
    - TB (list): List of branching nodes.
    - F (list): List of features.

    Returns:
    - CNF: A CNF formula encoding the decision tree logic for choosing one feature at branching.
    """
    
    formula = CNF()

    # Eq. (1): Ensuring that two different features aren't chosen for the same branching node.
    for t in TB:
        for j in F:
            for j_prime in F:
                if j != j_prime:
                    formula.append([-1 * get_var_index('a', t, j), -1 * get_var_index('a', t, j_prime)])
    
    # Eq. (2): Guaranteeing that at least one feature is chosen for every branching node.
    for t in TB:
        clause = [get_var_index('a', t, j) for j in F]
        formula.append(clause)
    
    return formula

# all contsraint variable information on nodes 
def get_var_index(prefix, t, j):
    """
    Helper function to get the variable index for the SAT solver.

    Parameters:
    - prefix (str): Prefix of the variable type (e.g., 'a' for at,j).
    - t (int): Index of the branching node.
    - j (int): Index of the feature.

    Returns:
    - int: Unique variable index.
    """
    global current_index
    key = (prefix, t, j)
    
    # If the key hasn't been seen before, assign it a new unique index
    if key not in var_mapping:
        var_mapping[key] = current_index
        current_index += 1
    
    return var_mapping[key]

# {O_ij} list for feature ordering 
def compute_ordering(X, j):
    """
    Compute the ordering Oj for feature j based on dataset X.
    
    Parameters:
    - X (list): List of data points.
    - j (int): Index of the feature.

    Returns:
    - list: A list of consecutive pairs in the ordering.
    """
    sorted_indices = sorted(range(len(X)), key=lambda i: X[i][j])
    return [(sorted_indices[i], sorted_indices[i+1]) for i in range(len(X)-1)]

# O_ij clause
def enforce_ordering_at_branching(TB, F, X):
    """
    Encode the direction of data points based on feature values.

    Parameters:
    - TB (list): List of branching nodes.
    - F (list): List of features.
    - X (list): List of data points.

    Returns:
    - CNF: A CNF formula encoding the decision tree logic.
    """
    formula = CNF()
    
    for j in F:
        Oj = compute_ordering(X, j)
        for t in TB:
            for (i, i_prime) in Oj:
                # Clause (3)
                formula.append([-1 * get_var_index('a', t, j), get_var_index('s', i, t), -1 * get_var_index('s', i_prime, t)])
                # Clause (4)
                if X[i][j] == X[i_prime][j]:
                    formula.append([-1 * get_var_index('a', t, j), -1 * get_var_index('s', i, t), get_var_index('s', i_prime, t)])
                    
    return formula


# Simple testings 
if __name__ == "__main__":
    # Example usage
    TB = [1, 2, 3]  # Example branching nodes
    F = [1, 2]  # Example features

    formula = choose_one_feature_at_branching(TB, F)
    with Solver(name="glucose4") as solver:
        solver.append_formula(formula)
        print(solver.solve())