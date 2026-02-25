## Setup Instructions

1. Create virtual environment:
   python -m venv venv

2. Activate environment:
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run server:
   uvicorn main:app --reload
   
   ## Notes

- The current implementation uses an in-memory dictionary (fake_db).
- In production, this will be replaced with a real database.