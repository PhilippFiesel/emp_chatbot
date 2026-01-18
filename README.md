
# Setup & Installation Guide

Follow the steps below to set up and run the application locally.

## 1. Clone the Repository
```
git clone <your-repository-url>
cd <your-repository-folder>
```
## 2. Configure Environment Variables

Rename the example environment file ".env.example" to ".env.local"

## 3. Add API Keys

Open .env.local and enter all required API keys.
For LiveKit Room ID and LiveKit API keys, sign in to the LiveKit dashboard and create a project.

## 4. Create a Virtual Environment (or Install uv)

Create a virtual environment
```
python -m venv .venv
```
Activate it (Windows):
```
.venv\Scripts\Activate.ps1
```
## 5. Install Project Dependencies
```
pip install .
```
 or
```
uv sync
```
## 6. Install Plugins
```
pip install -r requirements.txt
```
## 7. Download Required Models
```
python agent.py download-files
```
## 8. Start the Application

Run the following command inside the virtual environment:
```
python agent.py console
```
## 9. Open the Web Interface
```
http://localhost:8000/web/web_client.html
```
## 10. Access from a Mobile Device

Replace localhost in the URL with your host machine’s local IP address.
Your phone must be connected to the same network as the host PC.

⚠️Note:
This does not work on university networks due to firewall restrictions.

 





