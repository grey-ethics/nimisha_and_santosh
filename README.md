Clone/Download this repo into your local


Backend (terminal 1) -->
1) open vs-code terminal, cd into your backend folder and create new venv with the name "venv" and activate it
2) run the command "pip cache purge" to clear cache, and then install 'requirements.txt' with the command "pip install -r requirements.txt"
3)  - start/run postgres in your local pc
    - then open powershell from PC and run the command "psql -U postgres -h localhost -p 5432" (if you get environment variable error, then first fix this by adding new 'postgres environment variable' in your windows)
    - then run the command "CREATE USER nimisha_user WITH PASSWORD 'StrongPassword123';"
    - then run the command "CREATE DATABASE nimisha_santosh_db;"
    - then run the command "ALTER DATABASE nimisha_santosh_db OWNER TO nimisha_user;"
    - then run the command "GRANT ALL PRIVILEGES ON SCHEMA public TO nimisha_user;"
    - then run the command "ALTER USER nimisha_user CREATEDB;"
    - then run the command "GRANT USAGE, CREATE ON SCHEMA public TO nimisha_user;"
    - close powershell terminal
4) create ".env" file and copy paste data from ".env.example" inside it
5) run the command "python create_tables.py"
6) run the command "uvicorn app.main:app --reload" to start the app
7) go to "http://127.0.0.1:8000/docs" to access the app


Frontend (terminal 2) -->
1) open frontend and run the command "npm install"
2) run the command "npm run dev" to start the app
3) open "http://localhost:5173/" to access the app


Phone = "+919876543210"
Password = "SuperPassword@123"
Admin's Name = "Super Admin"