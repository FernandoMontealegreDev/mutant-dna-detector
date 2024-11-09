"""
Test suite for the DNA Mutant Detection System.
"""

import unittest
from typing import List
from mutant_detector import is_mutant, DNAValidationError


class TestMutantDetector(unittest.TestCase):
    """Test cases for the mutant detector functionality."""
    
    def test_valid_no_mutant(self):
        """Test case for a valid non-mutant DNA sequence."""
        no_mutant = [
            "ATGCGA",
            "CAGTGC",
            "TTATTT",
            "AGACGG",
            "GCGTCA",
            "TCACTG"
        ]
        self.assertFalse(is_mutant(no_mutant))
    
    def test_valid_mutant(self):
        """Test case for a valid mutant DNA sequence."""
        mutant = [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
        self.assertTrue(is_mutant(mutant))
    
    def test_valid_mutant_diagonal(self):
        """Test case for a valid mutant DNA sequence with diagonal pattern."""
        mutant_diagonal = [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGT",
            "CCCCTC",
            "TCACTG"
        ]
        self.assertTrue(is_mutant(mutant_diagonal))
    
    def test_invalid_empty_sequence(self):
        """Test case for an empty DNA sequence."""
        with self.assertRaises(ValueError):
            is_mutant([])
    
    def test_invalid_characters(self):
        """Test case for invalid characters in DNA sequence."""
        invalid_dna = [
            "ATGCGA",
            "CAGTGC",
            "TTATZT",  # Invalid character 'Z'
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
        with self.assertRaises(DNAValidationError):
            is_mutant(invalid_dna)
    
    def test_non_square_matrix(self):
        """Test case for non-square DNA matrix."""
        non_square = [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA"  # Missing one row
        ]
        with self.assertRaises(DNAValidationError):
            is_mutant(non_square)


if __name__ == '__main__':
    unittest.main(verbosity=2)