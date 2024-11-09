"""
DNA Mutant Detection System
--------------------------
This module provides functionality to detect mutant DNA sequences based on specific patterns.
A mutant DNA sequence contains more than one sequence of four identical letters
arranged horizontally, vertically, or diagonally in a matrix.
"""

from typing import List
import re
from .dna_service import DNAService  # Changed from DNAValidator to DNAService

class DNAValidationError(Exception):
    """Custom exception for DNA validation errors."""
    pass

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
    # Validate input using service (without DB check)
    validation_result = DNAService.validate_and_check_existence(dna, db=None)
    if not validation_result.is_valid:
        raise DNAValidationError(validation_result.error_message)
    
    n = len(dna)
    sequences_found = 0
    
    def check_sequence(sequence: str) -> bool:
        """Helper function to check if a sequence contains 4 consecutive identical letters."""
        return bool(re.search(r'([ATCG])\1{3}', sequence))
    
    # 1. Check horizontal sequences
    for row in dna:
        if check_sequence(row):
            sequences_found += 1
            if sequences_found > 1:
                return True
    
    # 2. Check vertical sequences
    for col in range(n):
        vertical = ''.join(dna[row][col] for row in range(n))
        if check_sequence(vertical):
            sequences_found += 1
            if sequences_found > 1:
                return True
    
    # 3. Check main diagonals (top-left to bottom-right)
    for i in range(n - 3):
        for j in range(n - 3):
            diagonal = ''.join(dna[i + k][j + k] for k in range(4))
            if len(set(diagonal)) == 1:
                sequences_found += 1
                if sequences_found > 1:
                    return True
    
    # 4. Check secondary diagonals (top-right to bottom-left)
    for i in range(n - 3):
        for j in range(3, n):
            diagonal = ''.join(dna[i + k][j - k] for k in range(4))
            if len(set(diagonal)) == 1:
                sequences_found += 1
                if sequences_found > 1:
                    return True
    
    return False