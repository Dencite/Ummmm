import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijk2NTNlNjIxLWJmNTQtNDIyNS05ZDk4LWM3ZWQxMWQ4NWVmYiIsImlhdCI6MTc1MTcwNzUxOSwic3ViIjoiZGV2ZWxvcGVyLzQ3MTBkOGUwLTY0ZjYtYzA2Ny0xZTI4LTQwOGU1OTA5YzQ0YiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NC4yMjYuMTIyLjMiXSwidHlwZSI6ImNsaWVudCJ9XX0.3XxD8sWhUn5-76rrkkqQh5wPAf0CwsGJrZgUTx3632bP2ZrD0U1FDyFw6_1Gky6u6Xlc817iQnPcmwr0aiW4Zw"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

@app.route("/get_deck", methods=["GET"])
def get_deck():
    medal_count = request.args.get("medals", type=int)
    if not medal_count:
        return jsonify({"error": "Invalid medals value"}), 400

    res = requests.get("https://api.clashroyale.com/v1/rankings/global/pathOfLegend", headers=HEADERS)
    if res.status_code != 200:
        return jsonify({"error": "Failed to fetch leaderboard"}), 500

    leaderboard = res.json().get("items", [])
    for player in leaderboard:
        try:
            trophies = player["pathOfLegendStatistics"]["seasonResult"]["trophies"]
            if trophies == medal_count:
                tag = player["tag"].replace("#", "%23")
                log = requests.get(f"https://api.clashroyale.com/v1/players/{tag}/battlelog", headers=HEADERS)
                if log.status_code == 200:
                    battles = log.json()
                    for b in battles:
                        if b["type"] == "pathOfLegend":
                            deck = [c["name"] for c in b["team"][0]["cards"]]
                            return jsonify({"name": player["name"], "tag": player["tag"], "deck": deck})
        except:
            continue

    return jsonify({"error": "No player found with this exact medal count"}), 404

@app.route("/")
def home():
    return "Clash Royale UC Deck Finder is live!"
