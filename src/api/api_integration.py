import os
import json
import threading
import time
from http.client import HTTPSConnection
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

# App details, statics
CLIENT_ID = "649d60d3998f0adad30ce53e"
CLIENT_SECRET = "TumbK6X1YW42PmsnM8GqnO5hkluOY2ef56fVsB"
REDIRECT_URI = "http://localhost:8080/auth/callback"
SCOPE = "read_station"
STATE = "NetatmoDashboardState"
SERVER_ADDRESS = ("localhost", 8080)
USER_FILE = "user_data.json"


class User:
    USER = None  # Should be used in other places as current user

    def __init__(self, access_token=None, refresh_token=None, expiration_time=None, new=False):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiration_time = expiration_time
        self.is_authenticated = True
        if new:
            self.is_authenticated = False
            self.authenticate()
        elif self.expiration_time < time.time():
            self.refresh()
        self.save()
        User.USER = self

    # Should be used to create new user or load existing one, if there is one
    @classmethod
    def load(cls):
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as file:
                data = json.load(file)
                access_token = data.get("access_token")
                refresh_token = data.get("refresh_token")
                expiration_time = data.get("expiration_time")
                if (refresh_token is not None) and (access_token is not None) and (expiration_time is not None):
                    return cls(access_token, refresh_token, expiration_time)
        return cls(new=True)

    # Saves user's data to json file
    def save(self):
        data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expiration_time": self.expiration_time
        }
        with open(USER_FILE, "w") as file:
            json.dump(data, file, indent=4)

    # First part of authentication
    # Sends user to netatmo's website to confirm access for app
    # Continuation (if successful) in authentication_2
    def authenticate(self):
        conn = HTTPSConnection("api.netatmo.com")
        payload = ""
        headers = {}

        # Starts local server to handle GET request
        server = HTTPServer(SERVER_ADDRESS, lambda *args, **kwargs: CallbackHandler(self, *args, **kwargs))

        server.user_event = threading.Event()
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Redirects the user to Netatmo OAuth2 dialog
        conn.request("POST",
                     f"/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&state={STATE}",
                     payload, headers)
        res = conn.getresponse()
        res.read()
        print(f"Redirect the user to the following URL and wait for the callback:\n{res.getheader('Location')}")

        server.user_event.wait()

    # Second part of authentication
    # Extracts code from api request, and sets tokens for user
    def authenticate_code(self, authorization_code):
        # Retrieves the access token with the authorization code
        conn = HTTPSConnection("api.netatmo.com")
        payload = f"grant_type=authorization_code&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={authorization_code}&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn.request("POST", "/oauth2/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response_json = json.loads(data)

        if "access_token" in response_json:
            self.access_token = response_json["access_token"]
            self.refresh_token = response_json["refresh_token"]
            self.expiration_time = int(time.time()) + response_json["expires_in"]
            self.is_authenticated = True
            self.save()
            print("Authentication successful!")
        else:
            self.is_authenticated = False
            error = response_json["error"]
            print(f"Authentication failed: {error}")

        CallbackHandler.user_event.set()

    # Refreshes user's token, doesn't require any user interaction
    def refresh(self):
        # Sends API request to Netatmo with user's refresh token
        conn = HTTPSConnection("api.netatmo.com")
        payload = f"grant_type=refresh_token&refresh_token={self.refresh_token}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn.request("POST", "/oauth2/token", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        response_json = json.loads(data)

        # Changes user's tokens if successful
        if "access_token" in response_json:
            self.access_token = response_json["access_token"]
            self.refresh_token = response_json["refresh_token"]
            self.expiration_time = int(time.time()) + response_json["expires_in"]
            self.save()
            print("Token Refreshed successfully!")
        else:
            error = response_json["error"]
            error_description = response_json["error_description"]
            print(f"Token Refresh failed: {error} - {error_description}")


# Class for handling confirmation request from netatmo API
class CallbackHandler(BaseHTTPRequestHandler):
    user_event = threading.Event()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def do_GET(self):
        query = urlparse(self.path).query
        query_params = parse_qs(query)

        if hasattr(self, 'authenticated') and self.authenticated:
            # User already authenticated, no further processing needed
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head><title>Already Authenticated</title></head>")
            self.wfile.write(b"<body><h1>Already Authenticated!</h1></body></html>")
            return

        if "code" in query_params:
            authorization_code = query_params["code"][0]
            self.user.authenticate_code(authorization_code)
            self.user.is_authenticated = True

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><head><title>Authentication Successful</title></head>")
            self.wfile.write(b"<body><h1>Authentication Successful!</h1></body></html>")
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication Failed!</h1></body></html>")


# Returns json data from weather station, requires access token from netatmo
def get_station_data(access_token: str) -> dict:
    conn = HTTPSConnection("api.netatmo.com")
    payload = ""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    conn.request("GET", "/api/getstationsdata?get_favorites=false", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    return data
