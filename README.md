
# DNA Mutant Detection System

This project implements a DNA mutant detection system using Python and FastAPI, with endpoints for detecting mutants and fetching statistics about verified DNA sequences. 

## Algorithm Folder

The `Algorithm` folder contains the core logic for detecting mutants in DNA sequences.

### mutant_detector.py

This file contains the logic to detect mutant DNA sequences. A mutant DNA sequence contains more than one sequence of four identical letters arranged horizontally, vertically, or diagonally in a matrix.

The system provides a function `is_mutant(dna: List[str])` to detect if the input DNA sequence contains mutant patterns. The DNA sequence is validated before the check is performed, ensuring that only valid sequences are processed.

### Functions in `mutant_detector.py`:

- **`validate_dna_sequence(dna: List[str]) -> None`**: Validates the DNA sequence to ensure that it is a square matrix and contains only valid bases ('A', 'T', 'C', 'G').
- **`is_mutant(dna: List[str]) -> bool`**: Detects if the DNA sequence corresponds to a mutant by checking for multiple sequences of four identical letters in any direction.
- **`get_dna_sequence() -> List[str]`**: Prompts the user to input a DNA sequence matrix.
- **`main()`**: The entry point of the script that executes the mutant detection system.

### test_mutant_detector.py

This file contains unit tests for the mutant detection system using `unittest`.

### Test cases:

- **`test_valid_no_mutant`**: Tests a valid non-mutant DNA sequence.
- **`test_valid_mutant`**: Tests a valid mutant DNA sequence.
- **`test_valid_mutant_diagonal`**: Tests a valid mutant DNA sequence with a diagonal mutant pattern.
- **`test_invalid_empty_sequence`**: Tests for an empty DNA sequence.
- **`test_invalid_characters`**: Tests for invalid characters in the DNA sequence.
- **`test_non_square_matrix`**: Tests for a non-square DNA matrix.

## mutant_api Folder

The `mutant_api` folder contains the FastAPI application for the mutant detection API.

### Requirements

Before running the application, you need to create a Python virtual environment and install dependencies:

1. Create and activate the virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scriptsctivate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the `mutant_api` folder with the following content:

```bash
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
DB_NAME=mutant_dna
```

### Database Setup

Create the `mutant_dna` database with the following SQL query:

```sql
CREATE DATABASE mutant_dna CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then, apply the migrations:

```bash
alembic upgrade head
```

### Running the API Locally

Run the API locally using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

### Endpoints

- **POST /mutant/**: Detects whether a DNA sequence belongs to a mutant.

Example request:

```json
POST - /mutant/
{
    "dna": ["ATCGGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
}
```

- **GET /stats/**: Returns statistics about the verification of DNA sequences.

Example response:

```json
{
    "count_mutant_dna": 0,
    "count_human_dna": 0,
    "ratio": 0.0
}
```

### Deploying to Render

The API is deployed to Render and can be accessed at:

- [Mutant Detection API](https://mutant-dna-detector.onrender.com/)
- [Mutant Detection Endpoint](https://mutant-dna-detector.onrender.com/mutant/)
- [Stats Endpoint](https://mutant-dna-detector.onrender.com/stats/)