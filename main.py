from flask import *
from oauth import Oauth
from dotenv import load_dotenv
import os

load_dotenv()

# Creating and Configuring the app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']

# Server
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/oauth/discord')
def oauth():
    # Authorization 
    code = request.args.get("code")
    token = Oauth.get_access_token(code)
    session['token'] = token
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'token' not in session:
        return redirect("https://discord.com/api/oauth2/authorize?client_id=817419214679703612&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foauth%2Fdiscord&response_type=code&scope=identify%20guilds")

    user_data = Oauth.get_user_json(session.get('token'))
    user_guilds_data  = Oauth.get_user_guild(session.get('token'))
    bot_guilds = Oauth.get_bot_guilds()
    mutual_bot_guilds = Oauth.get_mutual_guilds(user_guilds_data, bot_guilds)
    return jsonify(mutual_bot_guilds)





    

# Server Runner
if __name__ == "__main__":
    app.run(
        debug=True
    )

