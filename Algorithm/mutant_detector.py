"""
DNA Mutant Detection System
--------------------------
This module provides functionality to detect mutant DNA sequences based on specific patterns.
A mutant DNA sequence contains more than one sequence of four identical letters
arranged horizontally, vertically, or diagonally in a matrix.
"""

from typing import List
import re


class DNAValidationError(Exception):
    """Custom exception for DNA validation errors."""
    pass


def validate_dna_sequence(dna: List[str]) -> None:
    """
    Validates the DNA sequence matrix according to specified rules.
    
    Args:
        dna (List[str]): List of strings representing DNA sequences
        
    Raises:
        DNAValidationError: If the DNA sequence is invalid
        ValueError: If the input is empty or malformed
    """
    if not dna:
        raise ValueError("DNA sequence cannot be empty")
        
    n = len(dna)
    if not all(len(row) == n for row in dna):
        raise DNAValidationError("DNA matrix must be square (NxN)")
        
    valid_bases = set('ATCG')
    for row in dna:
        if not set(row).issubset(valid_bases):
            raise DNAValidationError(
                "Invalid DNA sequence. Only A, T, C, G letters are allowed"
            )


def is_mutant(dna: List[str]) -> bool:
    """
    Detects if a DNA sequence corresponds to a mutant.
    A mutant has more than one sequence of 4 identical letters in any direction.
    
    Args:
        dna (List[str]): List of strings representing the DNA matrix
        
    Returns:
        bool: True if mutant (has more than one sequence), False otherwise
        
    Raises:
        DNAValidationError: If the DNA sequence is invalid
    """
    # Validate input
    validate_dna_sequence(dna)
    
    n = len(dna)
    sequences_found = 0
    
    def check_sequence(sequence: str) -> bool:
        """Helper function to check if a sequence contains 4 consecutive identical letters."""
        return bool(re.search(r'([ATCG])\1{3}', sequence))
    
    # 1. Horizontal sequences
    for row in dna:
        if check_sequence(row):
            sequences_found += 1
            if sequences_found > 1:
                return True
    
    # 2. Vertical sequences
    for col in range(n):
        vertical = ''.join(dna[row][col] for row in range(n))
        if check_sequence(vertical):
            sequences_found += 1
            if sequences_found > 1:
                return True
    
    # 3. Main diagonals (top-left to bottom-right)
    for i in range(n - 3):
        for j in range(n - 3):
            diagonal = ''.join(dna[i + k][j + k] for k in range(4))
            if len(set(diagonal)) == 1:
                sequences_found += 1
                if sequences_found > 1:
                    return True
    
    # 4. Secondary diagonals (top-right to bottom-left)
    for i in range(n - 3):
        for j in range(3, n):
            diagonal = ''.join(dna[i + k][j - k] for k in range(4))
            if len(set(diagonal)) == 1:
                sequences_found += 1
                if sequences_found > 1:
                    return True
    
    return False


def get_dna_sequence() -> List[str]:
    """
    Prompts the user to input a DNA sequence matrix.
    
    Returns:
        List[str]: List of DNA sequences
        
    Raises:
        DNAValidationError: If the input is invalid
    """
    print("Enter DNA sequence (one row per line, empty line to finish):")
    dna_sequence = []
    while True:
        line = input().strip().upper()
        if not line:
            break
        dna_sequence.append(line)
    return dna_sequence


def main():
    """Main function to run the DNA mutant detection system."""
    try:
        # Get DNA sequence from user
        dna = get_dna_sequence()
        
        # Check if it's a mutant
        result = is_mutant(dna)
        
        # Print result
        print("\nResult:", "Mutant detected!" if result else "No mutant detected")
        
    except (DNAValidationError, ValueError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()