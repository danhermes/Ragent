Dropbox OAuth

Two tokens: Long-term Refresh Token and short-term Access Token.  Use Auth Code to get Refresh Token. Access Token authorizes access to the Dropbox API.

1. User Authorization:

Redirect the user to Dropbox’s OAuth URL with token_access_type=offline.
 https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://example.com
 User logs in and authorizes your app.

2. Exchange Authorization Code:

 Receive the authorization code at your redirect URI.
 Use the authorization code (with grant type authorization_code) along with your App Key/Client ID and App Secret/Client Secret to get an access token (and a refresh token if requested).

3. Using Tokens:

 Access Token: Use this for API calls.



 Refresh Token: When the access token expires, exchange it (using grant type refresh_token) along with your client credentials for a new access token(#1 & 2).


CODEZ

1. User Authorization:

 https://www.dropbox.com/oauth2/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=https://lexicon.systems/
 Find Auth Code in resulting URL.


2. Exchange Authorization Code:


import requests

# Replace these with your actual Dropbox app details
client_id = "YOUR_APP_KEY"         # Also known as App Key or Client ID
client_secret = "YOUR_APP_SECRET"    # Also known as App Secret or Client Secret
code = "YOUR_AUTHORIZATION_CODE"     # The code you received after user authorization
redirect_uri = "YOUR_REDIRECT_URI"   # Must match the one registered with your Dropbox app

token_url = "https://api.dropbox.com/oauth2/token"
data = {
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
}

# Using HTTP Basic Auth to send client credentials securely
response = requests.post(token_url, data=data, auth=(client_id, client_secret))

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    print("Access token:", access_token)
    print("Refresh token:", refresh_token)
else:
    print("Error:", response.status_code, response.text)

3. Using Tokens:


import os
import requests

# Retrieve the refresh token from an environment variable.
DROPBOX_REFRESH_TOKEN = os.environ.get("DROPBOX_REFRESH_TOKEN")
if not DROPBOX_REFRESH_TOKEN:
    raise Exception("No refresh token found. Please set the DROPBOX_REFRESH_TOKEN environment variable.")

def refresh_access_token(refresh_token, client_id, client_secret):
    """Refresh the Dropbox access token using the provided refresh token."""
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        new_token = response.json().get("access_token")
        return new_token
    else:
        raise Exception(f"Error refreshing token: {response.content}")

# Replace these with your actual Dropbox app credentials.
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Now, refresh the access token without any UI prompts.
access_token = refresh_access_token(DROPBOX_REFRESH_TOKEN, client_id, client_secret)
print("Your new access token is:", access_token)
