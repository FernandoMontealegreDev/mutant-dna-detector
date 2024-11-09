from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
import hashlib
import json

class DNASequence(Base):
    """
    Represents a DNA sequence record in the database.

    Attributes:
        id (int): Unique identifier for the DNA sequence.
        sequence_hash (str): SHA256 hash of the DNA sequence.
        is_mutant (bool): Flag indicating whether the DNA sequence belongs to a mutant.

    Methods:
        calculate_hash(dna_sequence): Calculates a unique hash for the given DNA sequence.
    """
    __tablename__ = "dna_sequences"

    id = Column(Integer, primary_key=True, index=True)
    sequence_hash = Column(String(255), unique=True, index=True)
    is_mutant = Column(Boolean)

    @staticmethod
    def calculate_hash(dna_sequence):
        """
        Calculate a unique hash for the DNA sequence.

        This method ensures that the same DNA sequence in different row orders 
        will have the same hash value by sorting the sequence before hashing.

        Args:
            dna_sequence (List[str]): A list representing the DNA sequence.

        Returns:
            str: A SHA256 hash of the DNA sequence.
        """
        # Sort the DNA sequence to ensure consistency for sequences in different orders
        sequence_str = json.dumps(sorted(dna_sequence))
        return hashlib.sha256(sequence_str.encode()).hexdigest()