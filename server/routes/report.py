from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
import requests
import os

report_bp = Blueprint('report', __name__)

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
REPORT_ID = os.getenv("REPORT_ID")

print(CLIENT_ID, CLIENT_SECRET, TENANT_ID, WORKSPACE_ID, REPORT_ID)

AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
POWER_BI_API = "https://api.powerbi.com/v1.0/myorg"

def get_access_token():
    """Retrieve Power BI Access Token"""
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
        # "scope": "https://graph.microsoft.com/.default",
        # "resource": "https://analysis.windows.net/powerbi/api"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(AUTH_URL, data=data, headers=headers)
    print("Token Response:", response.text)  # Debugging

    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")

    return response.json().get("access_token")

@report_bp.route("/get-embed-url", methods=["GET"])
def get_embed_url():
    """Fetch Power BI Embed URL"""
    print("Get Embed URL")
    token = get_access_token()
    print("Access Token:", token)
    headers = {"Authorization": f"Bearer {token}"}
    print("Headers:", headers)
    report_url = f"{POWER_BI_API}/groups/{WORKSPACE_ID}/reports/{REPORT_ID}"
    print("Report URL:", report_url)
    # response = requests.get(report_url, headers=headers)
    # print("Response:", response.json())
    # embed_url = response.json().get("embedUrl")

    # print("Embed URL:", embed_url)

    try:
        response = requests.get(report_url, headers=headers)
        print("HTTP Status Code:", response.status_code)  # Debugging
        print("Raw API Response:", response.text)  # Debugging

        # Check for empty response
        if response.text.strip() == "":
            return jsonify({"error": "Power BI API returned an empty response"}), 500

        data = response.json()
        return jsonify({"embedUrl": data.get("embedUrl"), "accessToken": token})
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))  # Debugging
        return jsonify({"error": "Request to Power BI API failed", "details": str(e)}), 500
    
    # return jsonify({"embedUrl": embed_url, "accessToken": token})

