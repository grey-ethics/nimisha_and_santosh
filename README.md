Clone/Download this repo into your local

Backend (terminal 1) -->
1) open backend and create new venv with the name "venv" and activate it
2) install requirements.txt
3) start/run postgres in your local pc, and then run the command "python create_tables.py"
4) create ".env" file and copy paste data from ".env.example" inside it
5) run the command "uvicorn app.main:app --reload" to start the app
6) go to "http://127.0.0.1:8000/docs" to access the app

Frontend (terminal 2) -->
1) open frontend and run the command "npm install"
2) run the command "npm run dev" to start the app
3) open "http://localhost:5173/" to access the app