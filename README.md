
1. Clone this repo
2. rename .env.example to .env.local
3. Enter all API keys. For livekit room id and api keys sign in to livekit. 
5. Create a virtual env or  install uv
   a. python -m venv .venv
   b. .venv\Scripts\Activate.ps1
6. pip install .  or  uv sync
7. Plugins installieren mit pip install -r requirements.txt 
8. Modell herunterladen: "python agent.py download-files"
8. In der virtuellen Umgebung folgenden Befehl ausführen, um alles zu starten:  python agent.py console
9. Webseite unter folgendem Link aufrufen: http://localhost:8000/web/web_client.html
10. Auf dem Handy die URL bei “localhost” mit eigener IP-Adresse austauschen. Achtung: Handy muss im gleichen Netz wie Host-PC sein. Allerdings funktioniert dies aufgrund von Firewallpolicies nicht im Hochschulnetz 

 

