from pydantic import BaseModel, Field, validator
from typing import List
from .dna_service import DNAService

class DNASequence(BaseModel):
    """Model for the DNA sequence input."""
    dna: List[str] = Field(..., description="List of strings representing the DNA matrix.")

    @validator('dna')
    def validate_dna_sequence(cls, v):
        """
        Validator to ensure the DNA sequence is valid using DNAService.
        
        Args:
            v (List[str]): The DNA sequence to be validated.

        Raises:
            ValueError: If the DNA sequence is invalid or contains errors.
            
        Returns:
            List[str]: The validated DNA sequence if valid.
        """
        validation_result = DNAService.validate_and_check_existence(v, db=None)
        if not validation_result.is_valid:
            raise ValueError(validation_result.error_message)
        return v

class Stats(BaseModel):
    """Model for returning statistics about analyzed DNA sequences."""
    count_mutant_dna: int = Field(..., description="Count of mutant DNA sequences.")
    count_human_dna: int = Field(..., description="Count of human DNA sequences.")
    ratio: float = Field(..., description="Ratio of mutant to human DNA sequences.")