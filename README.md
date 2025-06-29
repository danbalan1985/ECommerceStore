# Here are your Instructions
🚀 Local Setup Instructions
Prerequisites

# Install these first:
- Python 3.8+ 
- Node.js 16+ and npm/yarn
- MongoDB (local installation or MongoDB Atlas)
- Git

1. Clone and Setup Project

git clone <your-github-repo-url>
cd <your-project-folder>

2. Backend Setup (FastAPI)

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

3. Backend Environment Configuration

Create /backend/.env file:

MONGO_URL="mongodb://localhost:27017"
DB_NAME="ecommerce_db"

If using MongoDB Atlas (cloud):

MONGO_URL="mongodb+srv://username:password@cluster.mongodb.net/"
DB_NAME="ecommerce_db"

4. Frontend Setup (React)

# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# OR if you prefer yarn:
yarn install

5. Frontend Environment Configuration

Create /frontend/.env file:

REACT_APP_BACKEND_URL=http://localhost:8000

6. Database Setup

Option A: Local MongoDB

# Install MongoDB locally
# Windows: Download from mongodb.com
# macOS: brew install mongodb-community
# Linux: sudo apt install mongodb

# Start MongoDB service
# Windows: Start MongoDB service from Services
# macOS/Linux: sudo systemctl start mongod

Option B: MongoDB Atlas (Cloud)

    Create account at mongodb.com/atlas
    Create cluster and get connection string
    Use connection string in backend/.env

7. Run the Applications

Terminal 1 - Backend:

cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

Terminal 2 - Frontend:

cd frontend
npm start
# OR
yarn start

8. Access Your Application

    Frontend: http://localhost:3000
    Backend API: http://localhost:8000
    API Documentation: http://localhost:8000/docs

🔧 Troubleshooting
Common Issues:

1. MongoDB Connection Error:

# Check if MongoDB is running
sudo systemctl status mongod
# OR check MongoDB Atlas connection string

2. Backend Dependencies:

# If bcrypt installation fails on Windows:
pip install --only-binary=all bcrypt

3. Frontend Build Issues:

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

4. CORS Issues:

    Make sure backend is running on port 8000
    Frontend .env should point to http://localhost:8000

5. Port Conflicts:

# If ports are busy, change them:
# Backend: uvicorn server:app --port 8001
# Frontend: Add PORT=3001 to frontend/.env

📱 Testing Your Local Setup

    Register a new user at http://localhost:3000
    Browse products - should show 15 electronic items
    Search products - try "iPhone" or "MacBook"
    Add to cart and verify cart functionality
    API Testing - Visit http://localhost:8000/docs for Swagger UI

🗂️ Project Structure

your-project/
├── backend/
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   └── .env
└── README.md

Your app should now be running locally! Let me know if you encounter any issues during setup.
