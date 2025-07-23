import requests
from flask import Blueprint, jsonify

from server.config import Config

report_bp = Blueprint('report', __name__)

AUTH_URL = f'https://login.microsoftonline.com/{Config.TENANT_ID}/oauth2/v2.0/token'
POWER_BI_API = 'https://api.powerbi.com/v1.0/myorg'


def get_access_token():
    """
    Retrieve Power BI Access Token.
    """
    data = {
        'grant_type': 'client_credentials',
        'client_id': Config.CLIENT_ID,
        'client_secret': Config.CLIENT_SECRET,
        'scope': 'https://analysis.windows.net/powerbi/api/.default',
        # "scope": "https://graph.microsoft.com/.default",
        # "resource": "https://analysis.windows.net/powerbi/api"
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(AUTH_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Failed to get access token: {response.text}')

    return response.json().get('access_token')


@report_bp.route('/get-embed-url', methods=['GET'])
def get_embed_url():
    """
    Fetch Power BI Embed URL.
    """
    token = get_access_token()
    headers = {'Authorization': f'Bearer {token}'}
    report_url = (
        f'{POWER_BI_API}/groups/{Config.WORKSPACE_ID}/reports/{Config.REPORT_ID}'
    )
    # response = requests.get(report_url, headers=headers)
    # embed_url = response.json().get("embedUrl")

    try:
        response = requests.get(report_url, headers=headers)

        # Check for empty response
        if response.text.strip() == '':
            return jsonify({'error': 'Power BI API returned an empty response'}), 500

        data = response.json()
        return jsonify({'embedUrl': data.get('embedUrl'), 'accessToken': token})
    except requests.exceptions.RequestException as e:
        return jsonify(
            {'error': 'Request to Power BI API failed', 'details': str(e)}
        ), 500

    # return jsonify({"embedUrl": embed_url, "accessToken": token})
