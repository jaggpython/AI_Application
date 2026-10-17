Step 1: Open your Git repository in VS Code

git clone https://github.com/jaggpython/AI_Application

Step 2: Create a Python virtual environment

python3 -m venv venv

Activate it on macOS:

source venv/bin/activate

Step 3: Install project dependencies

pip install -r requirements.txt

Step 4: Install and configure Ollama

https://ollama.com/download

ollama --version

ollama pull llama3.2:3b

ollama list

ollama serve

Step 5: Run Backend and Frontend server

uvicorn backend.main:app --reload --port 8000   

streamlit run frontend/app.py






