import requests
import dropbox
import os
from dotenv import load_dotenv
from pathlib import Path
import logging


class DropboxAPI:
    def __init__(self):
        env_path = Path(__file__).resolve().parent.parent.parent / '.env'
        load_dotenv(dotenv_path=env_path)
        self.logger = logging.getLogger("dropbox")
        
        # Get app credentials and tokens from .env
        self.client_id = os.getenv("DROPBOX_API_APP_ID")
        self.client_secret = os.getenv("DROPBOX_API_APP_SECRET")
        self.access_token = os.getenv("DROPBOX_API_TOKEN_ACCESS")
        self.refresh_token = os.getenv("DROPBOX_API_TOKEN_REFRESH")
        self.auth_code = os.getenv("DROPBOX_API_AUTHORIZATION_CODE")
        
        # Log the loaded values for debugging
        self.logger.debug(f"*********** Loaded from .env at {env_path}")
        self.logger.debug(f"*********** Client ID: {self.client_id[5:]}")
        self.logger.debug(f"*********** Client Secret: {self.client_secret[5:]}")
        self.logger.debug(f"*********** Current Token: {self.access_token[5:]}")
        self.logger.debug(f"*********** Refresh Token: {self.refresh_token[5:]}")
        self.logger.debug(f"*********** Authorization Code: {self.auth_code[5:]}")

        # Validate required credentials
        if not self.client_id or not self.client_secret:
            self.logger.error("Missing required Dropbox app credentials (client_id or client_secret)")
            self.logger.error("Please set DROPBOX_API_APP_ID and DROPBOX_API_APP_SECRET in .env")
            self.dbx = None
            return

        # if not self.refresh_token:
        #     self.logger.error("No refresh token found. Please add DROPBOX_API_TOKEN_REFRESH to .env")
        #     self.dbx = None
        #     return
            
        # Initialize Dropbox client
        self.dbx = None
        
        # Always try to get a valid access token using the refresh token
        self.logger.info(f"Attempting to get valid access token. Access token: {self.access_token}")
        self.access_token = self.get_valid_access_token(
            self.access_token,
            self.refresh_token,
            self.client_id,
            self.client_secret 
        )
        
        if self.access_token:
            try:
                self.dbx = dropbox.Dropbox(self.access_token)
                # Test the connection
                self.dbx.users_get_current_account()
                self.logger.info("Successfully connected to Dropbox")
            except dropbox.exceptions.AuthError:
                self.logger.error("Invalid Dropbox access token")
                self.dbx = None
            except Exception as e:
                self.logger.error(f"Error connecting to Dropbox: {e}")
                self.dbx = None
        else:
            self.logger.error("Failed to obtain valid Dropbox access token")
                
    def is_token_valid(self, access_token):
        """Check if the access token is valid by calling Dropbox's account endpoint."""
        if not access_token:
            self.logger.error("No access token provided for validation")
            return False
        url = "https://api.dropboxapi.com/2/users/get_current_account"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            self.logger.error(f"Token validation failed. Status: {response.status_code}, Response: {response.text}")
        return response.status_code == 200

    def renew_access_token(self, refresh_token, client_id, client_secret) -> str:
        """Refresh the Dropbox access token using the refresh token."""
        if not refresh_token:
            self.logger.error("No refresh token provided for access token refresh. Authorizing another refresh token.")
            refresh_token, access_token = self.authorize_refresh_token(client_id, client_secret, self.auth_code)
            if not refresh_token or not access_token:
                self.logger.error("Failed to authorize refresh token")  
                return None
            else:
                return access_token
        
        url = "https://api.dropbox.com/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        self.logger.debug(f"Attempting to renew access token using refresh token: {refresh_token[:5]}...")
        response = requests.post(url, data=data, auth=(client_id, client_secret))
        if response.status_code == 200:
            new_token = response.json().get("access_token")
            if new_token:
                self._update_env_token("DROPBOX_API_TOKEN_ACCESS", new_token)
                self.logger.info("New access token acquired and stored")
            return new_token
        
        else:
            self.logger.error("Failed to renew access token. Authorizing another refresh token.")
            refresh_token, access_token = self.authorize_refresh_token(client_id, client_secret, self.auth_code)
            if not refresh_token or not access_token:
                self.logger.error(f"Failed to refresh access token. Status: {response.status_code}, Response: {response.text}")
                return None
            else:
                return access_token


    def authorize_refresh_token(self, client_id, client_secret, auth_code):

        redirect_uri = "https://lexicon.systems/"   # Must match the one registered with your Dropbox app
        token_url = "https://api.dropbox.com/oauth2/token"
        data = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        self.logger.info(f"Attempting to authorize refresh token with code: {auth_code}")
        # Using HTTP Basic Auth to send client credentials securely
        response = requests.post(token_url, data=data, auth=(client_id, client_secret))

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            print("Access token:", access_token)
            print("Refresh token:", refresh_token)
            if refresh_token:
                self._update_env_token("DROPBOX_API_TOKEN_REFRESH", refresh_token)
                self.logger.info("New refresh token acquired and stored")
            if access_token:
                self._update_env_token("DROPBOX_API_TOKEN_ACCESS", access_token)
                self.logger.info("New access token acquired and stored")               
            return refresh_token, access_token
        self.logger.error(f"Failed to authorize refresh token. Status: {response.status_code}, Response: {response.text}")
        return None




    # def refresh_refresh_token(self, refresh_token, client_id, client_secret):
    #     """Refresh the refresh token using the OAuth2 flow."""
    #     if not refresh_token:
    #         self.logger.error("No refresh token provided for refresh token refresh")
    #         return None
            
    #     url = "https://api.dropbox.com/oauth2/token"
    #     data = {
    #         "grant_type": "refresh_token",
    #         "refresh_token": refresh_token,
    #         "client_id": client_id,
    #         "client_secret": client_secret,
    #         "include_refresh_token": "true"  # This is required to get a new refresh token
    #     }
    #     self.logger.debug(f"Attempting to refresh refresh token with current refresh token: {refresh_token[:5]}...")
    #     response = requests.post(url, data=data)
    #     if response.status_code == 200:
    #         response_data = response.json()
    #         new_refresh_token = response_data.get("refresh_token")
    #         if new_refresh_token:
    #             self._update_env_token("DROPBOX_API_TOKEN_REFRESH", new_refresh_token)
    #             self.logger.info("New refresh token acquired and stored")
    #             return new_refresh_token
    #         else:
    #             self.logger.error("No refresh token in response")
    #     self.logger.error(f"Failed to refresh refresh token. Status: {response.status_code}, Response: {response.text}")
    #     return None

    def _update_env_token(self, token_name: str, new_token: str):
        """Update a token in the .env file."""
        try:
            env_path = Path(__file__).resolve().parent.parent.parent / '.env'
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            with open(env_path, 'w') as f:
                for line in lines:
                    if line.startswith(f'{token_name}='):
                        f.write(f'{token_name}={new_token}\n')
                    else:
                        f.write(line)
        except Exception as e:
            self.logger.error(f"Error updating {token_name} in .env: {e}")

    def get_valid_access_token(self, access_token, refresh_token, client_id, client_secret):
        """Get a valid access token, refreshing if necessary."""
        # if not refresh_token:
        #     self.logger.error("No refresh token provided for token validation")
        #     return None
        self.logger.info(f"Checking access token: {access_token}")
        if self.is_token_valid(access_token):
            self.logger.info("Access token is valid")
            return access_token
        self.logger.info("Access token is invalid")
            
        # If current token is invalid, try to refresh
        self.logger.info("Attempting to refresh access token")
        new_token = self.renew_access_token(refresh_token, client_id, client_secret)
        if new_token and self.is_token_valid(new_token):
            self.logger.info("Successfully refreshed access token")
            return new_token
        self.logger.warning("Failed to refresh access token")
            
        # If refresh failed, try to refresh the refresh token
        self.logger.info("Attempting to refresh refresh token")
        new_refresh_token = "" #self.refresh_refresh_token(refresh_token, client_id, client_secret)
        if not new_refresh_token:
            self.logger.warning("Failed to refresh refresh token")
            
        self.logger.error("All token refresh attempts failed")
        return None

    def get_initial_tokens(self, client_id, client_secret):
        """Get initial access token using refresh token."""
        if not client_id or not client_secret:
            self.logger.error("Missing required Dropbox app credentials")
            return False
                  
        if not self.refresh_token:
            self.logger.error("No refresh token provided")
            return False
            
        # Get access token using refresh token
        token_url = "https://api.dropbox.com/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        try:
            self.logger.info("Attempting to get access token using refresh token")
            response = requests.post(token_url, data=data, auth=(client_id, client_secret))
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access_token")
                
                if not access_token:
                    self.logger.error("No access token found in the response")
                    return False
                    
                # Update .env with new access token
                self._update_env_token("DROPBOX_API_TOKEN_ACCESS", access_token)
                self.logger.info("Successfully obtained and stored access token")
                return True
            else:
                self.logger.error(f"Error obtaining access token: {response.content}")
                return False
        except Exception as e:
            self.logger.error(f"Error getting access token: {e}")
            return False

    def oauth_callback():
        # Step 2: Retrieve the authorization code from Dropbox
        code = requests.args.get('code')
        if not code:
            self.logger.error("No authorization code received")
