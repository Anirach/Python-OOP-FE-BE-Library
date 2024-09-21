# PythonLibraryProject
The small Python Example of OOP FrontEnd - Back-End and Database 
PythonLibraryProject/
├── backend/
│   ├── backend.py         # FastAPI backend code
│   ├── database.py        # Database connection and operations
│   └── requirements.txt   # Python dependencies for both backend and frontend
├── frontend/
│   ├── frontend.py        # Flask frontend code
│   ├── templates/
│   │   ├── index.html     # List books (Frontend HTML)
│   │   ├── create.html    # Create a new book (Frontend HTML)
│   │   ├── book.html      # Book details (Frontend HTML)
│   │   └── edit.html      # Edit book (Frontend HTML)
│   └── static/
│       └── styles.css     # CSS styles for the frontend
└── requirements.txt       # Combined requirements for the project (both backend and frontend)

# To run the project

# Step 1: Set up a virtual environment (Optional)
cd project/
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start the FastAPI backend
cd backend/
uvicorn backend:app --reload

# Step 4: Start the Flask frontend (in a new terminal)
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd frontend/
python frontend.py

# Access the frontend at http://127.0.0.1:5000
# Access the backend at http://127.0.0.1:8000/docs
