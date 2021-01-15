#  solving Riddler Classic @ https://fivethirtyeight.com/features/can-you-hunt-for-the-mysterious-numbers/

from functools import reduce
from itertools import permutations, product
from math import prod


rows = (294, 216, 135, 98, 112, 84, 245, 40)
cols = (8890560, 156800, 55566)
n_rows = len(rows)
n_cols = len(cols)


def factorize(n):
    """yield all factors of integer n"""
    res = []
    while n > 1:
        for i in range(2, n + 1):
            if n % i == 0:
                n //= i
                res.append(i)
                break
    return res


def n_sums(num, n):
    """list all n-elements sets of non-negative integers that sum up to positive integer num"""
    if n == 1:
        return set([(num,)])
    res = set()
    for first_addend in range(0, num + 1):
        for s in n_sums(num - first_addend, n - 1):
            res.add(tuple(sorted(list(s) + [first_addend], reverse=True)))
    return sorted(res, reverse=True)


def n_factorizations_1_9(num, n):
    """list all possible ways to factorize positive integer in n digits between 1 and 9"""
    res = set()
    factors = factorize(num)
    sums = n_sums(len(factors), n)
    for p in permutations(factors):
        for s in sums:
            index = 0
            partition = []
            acceptable = True
            for a in s:
                factor = prod(p[index:index + a])
                if factor > 9:
                    acceptable = False
                    break
                partition.append(factor)
                index += a
            if acceptable:
                res.add(tuple(sorted(partition, reverse=True)))
    return sorted(res, reverse=True)


# derive a constraint on the last digit based on the possible factorizations of the last and smallest column number
possible_last_digits = set()
for x in n_factorizations_1_9(cols[-1], n_rows):
    possible_last_digits = possible_last_digits.union(set(x))
print(f'Possibile last digits:\n{sorted(possible_last_digits)}\n')


def acceptable_row_factorizations(row):
    """list all possible factorizations of the given row (positive integer) compatibly with all known constraints"""
    n = n_cols
    factors = factorize(row)
    sums = n_sums(len(factors), n)
    res = set()
    for p in permutations(factors):
        for s in sums:
            index = 0
            partition = []
            acceptable = True
            for a in s:
                factor = prod(p[index:index + a])
                if factor > 9:
                    acceptable = False
                    break
                partition.append(factor)
                index += a
            if acceptable and set(partition).intersection(possible_last_digits):
                res.add(tuple(sorted(partition, reverse=True)))
    return sorted(res, reverse=True)


def acceptable_row_numbers(row):
    """list all possible row numbers based on the given row (positive integer) compatibly with all known constraints"""
    res = set()
    for f in acceptable_row_factorizations(row):
        for p in permutations(f):
            if p[-1] in possible_last_digits:
                res.add(tuple(p))
    return sorted(res, reverse=True)


def valid_solution(solution, rows, cols):
    """return True if and only if the solution is correct; used as a double-check"""
    if len(solution) != len(rows) or any([len(row) != len(cols) for row in solution]):
        return False
    valid = True
    for sol_row, row in zip(solution, rows):
        if prod(sol_row) != row:
            valid = False
            break
    if not valid:
        return False
    for c in range(len(cols)):
        if prod([sol_row[c] for sol_row in solution]) != cols[c]:
            valid = False
            break
    return valid


row_decompositions = {row: acceptable_row_numbers(row) for row in rows}
for row, decomps in row_decompositions.items():
    print(f'\nPossibile decompositions of {row}:\n' + '\n'.join([str(d) for d in decomps]))
n_row_decompositions = {row: len(decomps) for row, decomps in row_decompositions.items()}
print(f'\nTotal number of possibilities to check: {prod(n_row_decompositions.values())}\n')
solutions = []
for possibility in product(*row_decompositions.values()):
    result = tuple([prod([p[i] for p in possibility]) for i in range(n_cols)])
    if result == cols and valid_solution(possibility, rows, cols):
        solutions.append(possibility)
n_solutions = len(solutions)
if n_solutions == 0:
    print('\nThere are no solutions.\n')
else:
    if n_solutions == 1:
        print('\nThere is only one solution.\n')
    else:
        print(f'\nThere are {n_solutions} solutions.\n')
    for i, solution in enumerate(solutions, 1):
        print(f'Solution nr. {i}:   {", ".join(["".join([str(digit) for digit in n]) for n in solution])}')
        for n in solution:
            print(' '.join([str(digit) for digit in n]))
