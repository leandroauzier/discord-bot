import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SECRET_KEY_DJANGO = os.getenv('SECRET_KEY_DJANGO')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
