from typing import List, Set, Optional
from dataclasses import dataclass
from . import models
from sqlalchemy.orm import Session
import hashlib

@dataclass
class DNAValidationResult:
    """
    Data class to represent the result of a DNA validation and mutation check.

    Attributes:
        is_valid (bool): Indicates if the DNA sequence passed validation.
        error_message (str): Error message if validation fails.
        sequence_hash (str): SHA256 hash of the DNA sequence.
        is_mutant (Optional[bool]): Flag indicating if the DNA sequence is mutant (if checked).
        is_processed (bool): Indicates if the DNA sequence has already been processed.
    """
    is_valid: bool
    error_message: str = ""
    sequence_hash: str = ""
    is_mutant: Optional[bool] = None
    is_processed: bool = False

class DNAService:
    """Centralized service for DNA sequence validation and mutation detection."""
    
    VALID_BASES: Set[str] = set('ATCG')

    @classmethod
    def calculate_hash(cls, dna: List[str]) -> str:
        """
        Calculate a SHA256 hash of the DNA sequence.

        Args:
            dna (List[str]): List of DNA string sequences.

        Returns:
            str: SHA256 hash of the concatenated DNA sequence.
        """
        concatenated_dna = "".join(dna)
        return hashlib.sha256(concatenated_dna.encode()).hexdigest()

    @classmethod
    def validate_and_check_existence(cls, dna: List[str], db: Session) -> DNAValidationResult:
        """
        Validate the DNA sequence format and check if it has been processed before.

        Args:
            dna (List[str]): List of DNA string sequences.
            db (Session): SQLAlchemy database session for querying previous records.

        Returns:
            DNAValidationResult: Object containing validation results, 
            including existence check and mutation status if previously processed.
        """
        
        # Check if the DNA sequence is empty
        if not dna:
            return DNAValidationResult(False, "DNA sequence cannot be empty")

        # Ensure the DNA sequence is a square matrix (NxN)
        n = len(dna)
        if not all(len(row) == n for row in dna):
            return DNAValidationResult(False, "DNA matrix must be square (NxN)")

        # Validate that each base in the DNA sequence is one of the valid bases (A, T, C, G)
        for row in dna:
            invalid_bases = set(row) - cls.VALID_BASES
            if invalid_bases:
                return DNAValidationResult(
                    False,
                    f"DNA sequence contains invalid characters: {', '.join(invalid_bases)}"
                )

        # Calculate the hash of the DNA sequence
        sequence_hash = cls.calculate_hash(dna)

        # Check if the DNA sequence already exists in the database
        if db:  # Only query the database if a session is provided
            db_sequence = db.query(models.DNASequence).filter(
                models.DNASequence.sequence_hash == sequence_hash
            ).first()

            # If found, return existing data with mutation status
            if db_sequence:
                return DNAValidationResult(
                    is_valid=True,
                    sequence_hash=sequence_hash,
                    is_mutant=db_sequence.is_mutant,
                    is_processed=True
                )

        # Return validation result for new DNA sequence
        return DNAValidationResult(
            is_valid=True,
            sequence_hash=sequence_hash,
            is_processed=False
        )