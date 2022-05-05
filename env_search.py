import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
SECRET_KEY_DJANGO = os.getenv('SECRET_KEY_DJANGO')
BEARER_PUBLIC_API= os.getenv('BEARER_PUBLIC_API')
DB_STRING= os.getenv('DB_STRING')