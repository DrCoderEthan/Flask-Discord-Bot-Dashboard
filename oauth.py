from email import header
from wsgiref import headers
from flask import request
import requests
from dotenv import load_dotenv
import os


load_dotenv()

class Oauth:
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    redirect_uri = os.environ['REDIRECT_URI']
    scope = os.environ['SCOPE']
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id=817419214679703612&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foauth%2Fdiscord&response_type=code&scope=identify%20guilds"
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"

    @staticmethod
    def get_access_token(code):
        payload = {
            "client_id":Oauth.client_id,
            "client_secret":Oauth.client_secret,
            "grant_type": "authorization_code",
            "code":code,
            "redirect_uri":Oauth.redirect_uri,
            "scope":Oauth.scope
        }

        access_token = requests.post(url=Oauth.discord_token_url, data=payload).json()
        return access_token.get("access_token")
    
    @staticmethod
    def get_user_json(access_token):
        url = f'{Oauth.discord_api_url}/v6/users/@me'
        headers = {"Authorization":f"Bearer {access_token}"}
        user_object = requests.get(url=url, headers = headers).json()
        return user_object
    
    @staticmethod
    def get_user_guild(access_token):
        response = requests.get(url=f'{Oauth.discord_api_url}/v6/users/@me/guilds', headers={"Authorization":f"Bearer {access_token}"})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_bot_guilds():
        bot_token = os.environ['BOT_TOKEN']
        url = (f'{Oauth.discord_api_url}/v6/users/@me/guilds')
        headers = {"Authorization":f"Bot {bot_token}"}
        bot_guild_object = requests.get(url=url, headers=headers)
        return bot_guild_object.json()
    
    @staticmethod
    def get_mutual_guilds(user_guilds :list, bot_guilds :list):
        return [guild for guild in user_guilds if guild['id'] in map(lambda i: i['id'], bot_guilds) and (guild['permissions'] & 0x20) == 0x20]
    
    @staticmethod
    def get_guild_data(guild_id:int, token:str):
        bot_token = os.environ['BOT_TOKEN']
        response = requests.get(f'{Oauth.discord_api_url}/v6/guilds/{guild_id}', headers={"Authorization":f"Bot {bot_token}"})
        response.raise_for_status()
        return response.json()