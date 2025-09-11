from flask_dance.contrib.azure import azure


def fetch_user_info():
    """Fetch user info from Azure."""
    response = azure.session.get("/v1.0/me")
    if response.ok:
        return response.json()
    return None
