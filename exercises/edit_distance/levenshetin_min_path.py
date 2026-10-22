#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Title: levenshetin_min_path.py
Version: 1.0.0
Description:
    Implementation of Levenshetin Edit Distance Calculation to determine a shortest path
    between two strings. 
    See Jerofsky, Fig 2.20 https://web.stanford.edu/~jurafsky/slp3/ed3book_aug26.pdf

Author: Shane Hussey
Create Date: 2026-10-21
Licence: MIT
Usage:
	python levenshetin_min_path.py --source "intention" --target "execution" --verbose

"""


import argparse


class Entry:
    def __init__(self, value):
        self.value = value
        self.pointer_up = None
        self.pointer_left = None
        self.pointer_diag = None


def print_matrix_D(D):
    """
    Helper function to print Entry matrix values and pointers
    """

    # look at the matrix values
    for row in D:
        print([entry.value for entry in row])
    
    print("\n")

    # look at the pointers
    new_d = [[None for _ in range(len(D[0]))] for _ in range(len(D))]
    for n in range(len(D)):
        for m in range(len(D[0])):
            string = ""
            if D[n][m].pointer_up:
                string += "U"
            if D[n][m].pointer_left:
                string += "L"
            if D[n][m].pointer_diag:
                string += "D"
            new_d[n][m] = string
    for row in new_d:
        print([entry for entry in row])


def levenshetin_distance(source: str, target: str, verbose: bool) -> tuple[list[str], list[str]]:
    """
    Function to calculate the levenshetin (edit) distance between a source
    and a target string and prints out the minimum cost and a 
    minimum-distance path 

    here im implementing the version of the algormithm using the
    min from Jurafsky page 62 figure 2.20
    # citation - https://web.stanford.edu/~jurafsky/slp3/ed3book_aug26.pdf
    and focusing backtrace so the minimum-distance path matches the 
    slides from lecture 3.4

    :source: str: source string
    :target: str: target string
    """

    # initialize our matrix of entries 
    n = len(source)
    m = len(target)
    D = [[Entry(None) for _ in range(m + 1)] for _ in range(n + 1)]
    D[0][0].value = 0

    # first row and column 
    for l in range(1, n + 1):
        D[l][0].value = D[l-1][0].value + 1
        D[l][0].pointer_up = D[l-1][0]
    
    for l in range(1, m + 1):
        D[0][l].value = D[0][l-1].value + 1
        D[0][l].pointer_left = D[0][l-1]
    
    

    # Compute the del, insertion and substitution costs and populate pointers
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            
            # Calculate costs for each option (See Jerofsky, fig 2.20)
            del_cost = D[i-1][j].value + 1
            ins_cost = D[i][j-1].value + 1
            if source[i - 1] == target[j - 1]:
                sub_cost = D[i-1][j-1].value
            else:
                sub_cost = D[i-1][j-1].value + 2
                
            # Update entry with the minimum cost of all change options
            min_cost = min(del_cost, sub_cost, ins_cost)
            D[i][j].value = min_cost

            # Update the entry with pointer entry
            ## double checked pointers -> same as slides
            if min_cost == del_cost:
                D[i][j].pointer_up = D[i-1][j]
            if min_cost == sub_cost:
                D[i][j].pointer_diag = D[i-1][j-1]
            if min_cost == ins_cost:
                D[i][j].pointer_left = D[i][j-1]
        
    # Backtrace shortest path
    source_alignment = []
    target_alignment = []
    min_path = []

    i, j = n, m
    entry = D[-1][-1]
    while entry:
        # Add entry value to min_path 
        min_path.insert(0, entry.value)

        # Find the movement that minimizes value
        options = {}
        if entry.pointer_diag:
            source_alignment.insert(0, source[i-1])
            target_alignment.insert(0, target[j-1])
            entry = entry.pointer_diag
            i, j = i - 1, j - 1
        elif entry.pointer_left:
            source_alignment.insert(0, "-")
            target_alignment.insert(0, target[j-1])
            entry = entry.pointer_left
            j -= 1
        elif entry.pointer_up:
            source_alignment.insert(0, source[i-1])
            target_alignment.insert(0, "-")
            entry = entry.pointer_up
            i -= 1
        else:
            break
        
             
    if verbose:
        print(f"levenshetin distance:")
        print(f"source: {source} (rows)")
        print(f"target: {target} (columns)\n")
        print_matrix_D(D)
        print(f"minimum edit distance: {D[-1][-1].value}")
        print(f"minimum path : {min_path}")
        print(f"Alignment")
    
    return source_alignment, target_alignment


def main():
    """Calculates Levenshetin Distance and returns a minimum path"""
    parser = argparse.ArgumentParser(
                        prog="Levenshetin Edit Distance Minimum Path",
                        description="""Implementation of Levenshetin Edit Distance \
                        Calculation to determine a shortest path between two strings.""")
    parser.add_argument('--source',
                        default="intention",
                        type=str, 
                        help='source string')
    parser.add_argument('--target',
                        default="execution",
                        type=str, 
                        help='target string')
    parser.add_argument('--verbose',
                        action="store_true",
                        help='Prints dynamic programming steps for learning purposes.')
    
    args = parser.parse_args()

    source_alignment, target_alignment = levenshetin_distance(
                                                    source=args.source,
                                                    target=args.target,
                                                    verbose=args.verbose)
    
    print(source_alignment)
    print(target_alignment)

if __name__ == '__main__':
	main()
	