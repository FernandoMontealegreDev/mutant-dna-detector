from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .dna_service import DNAService
from .mutant_detector import is_mutant, DNAValidationError

# Initialize the database tables
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI application
app = FastAPI(
    title="Mutant Detection API",
    description="API for detecting mutant DNA sequences",
    version="1.0.0"
)

@app.post("/mutant/", status_code=200)
async def analyze_dna(
    dna_sequence: schemas.DNASequence,
    db: Session = Depends(get_db)
):
    """
    Analyze a DNA sequence to detect if it belongs to a mutant.
    
    This endpoint validates and processes a DNA sequence for mutant detection. 
    If the sequence has been processed previously, it returns the stored result; 
    otherwise, it analyzes and stores the result in the database.

    Args:
        dna_sequence (schemas.DNASequence): The DNA sequence data in JSON format.
        db (Session): SQLAlchemy session dependency.

    Returns:
        JSONResponse: Response indicating if the DNA is mutant or not, 
        along with conflict status if it was previously processed.
    """
    try:
        # Validate DNA and check if it already exists in the database
        validation_result = DNAService.validate_and_check_existence(dna_sequence.dna, db)
        
        if not validation_result.is_valid:
            raise DNAValidationError(validation_result.error_message)
            
        if validation_result.is_processed:
            return JSONResponse(
                status_code=409, 
                content={
                    "message": "DNA sequence already processed",
                    "sequence_hash": validation_result.sequence_hash,
                    "is_mutant": validation_result.is_mutant
                }
            )

        # Detect mutant status if DNA is new
        result = is_mutant(dna_sequence.dna)
        
        # Store the DNA analysis result in the database
        db_sequence = models.DNASequence(
            sequence_hash=validation_result.sequence_hash,
            is_mutant=result
        )
        db.add(db_sequence)
        db.commit()
        
        return JSONResponse(
            status_code=200 if result else 403, 
            content={"is_mutant": result}
        )
        
    except DNAValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stats/", response_model=schemas.Stats)
async def get_stats(db: Session = Depends(get_db)):
    """
    Retrieve statistics of analyzed DNA sequences.

    This endpoint returns the count of mutant and human DNA sequences analyzed,
    along with the mutant-to-human ratio.

    Args:
        db (Session): SQLAlchemy session dependency.

    Returns:
        dict: A dictionary with counts of mutant and human DNA sequences and their ratio.
    """
    # Count mutant and human DNA sequences in the database
    mutant_count = db.query(models.DNASequence).filter(
        models.DNASequence.is_mutant == True
    ).count()
    
    human_count = db.query(models.DNASequence).filter(
        models.DNASequence.is_mutant == False
    ).count()
    
    # Calculate the mutant-to-human DNA ratio
    ratio = mutant_count / human_count if human_count > 0 else 0
    
    return {
        "count_mutant_dna": mutant_count,
        "count_human_dna": human_count,
        "ratio": round(ratio, 2)
    }