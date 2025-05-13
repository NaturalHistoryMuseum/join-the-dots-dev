from flask import Flask, jsonify, redirect, url_for, session, request
from flask_cors import CORS
import mysql.connector
import requests
#Microsoft Authentication Library
from msal import ConfidentialClientApplication
import uuid
import os

from flask_dance.contrib.azure import make_azure_blueprint
from dotenv import load_dotenv
from flask_dance.contrib.azure import azure
from flask_dance.consumer import oauth_authorized
load_dotenv()

# Allow insecure transport for testing purposes (for SSO) - DO NOT USE IN PRODUCTION!!
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from your Vue frontend

app.secret_key = os.urandom(24)

# Database configuration
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

# Create a connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Route to fetch data
@app.route('/api/category', methods=['GET'])
def get_data():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Fetch data from the database
    cursor.execute("SELECT * FROM category")
    result = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    # Return the result as JSON
    return jsonify(result)

@app.route('/api/unit-department', methods=['GET'])
def get_units_and_departments():
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Fetch data from the database
    cursor.execute("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name
                   FROM jtd_live.collection_unit AS unit 
                    LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
                    LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
                   """)
    result = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    # Return the result as JSON
    return jsonify(result)

@app.route('/api/unit/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Fetch data from the database
    cursor.execute("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.*
                   FROM jtd_live.collection_unit AS unit 
                    LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
                    LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
                    WHERE  unit.collection_unit_id = %u
                   """ % int(unit_id))
    result = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    # Return the result as JSON
    return jsonify(result)

@app.route('/api/section-units/<sectionId>', methods=['GET'])
def get_section_units(sectionId):
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Fetch data from the database
    cursor.execute("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, section.section_name, unit.*
                   FROM jtd_live.collection_unit AS unit 
                    LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
                    LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
                    WHERE  section.section_id = %i
                   """ % int(sectionId))
    result = cursor.fetchall()
    # Close connection
    cursor.close()
    connection.close()
    # Return the result as JSON
    return jsonify(result)


# Azure AD OAuth
azure_blueprint = make_azure_blueprint(
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
    tenant=os.getenv("AZURE_TENANT_ID"),
    redirect_url=os.getenv("AZURE_REDIRECT_URI"),
    # redirect_to="auth_callback"
)
app.register_blueprint(azure_blueprint, url_prefix="/api/auth/login")


@app.route("/api/auth/callback")
def auth_callback():
    # Check if user is authorized
    if not azure.authorized:
        return jsonify({"error": "User not authorized"}), 401
    # Fetch user info
    resp = azure_blueprint.session.get("/v1.0/me")
    if not resp.ok:
        return jsonify({"error": "Failed to fetch user info"}), 500
    # Set user info from response
    user_info = resp.json()

    # Save user info in session
    session["user"] = {
        "email": user_info.get("userPrincipalName"),
        "name": user_info.get("displayName"),
    }
    # Redirect to home page
    return redirect("http://localhost:5173/")

@app.route("/api/auth/logout")
def logout():
    session.clear()
    return {"message": "Logged out"}


@app.route("/check_authorization")
def check_authorization():
    if azure.authorized:
        return "User is authorized! v2"
    else:
        return "User is not authorized. v2", 401



if __name__ == '__main__':
    app.run(debug=True)
