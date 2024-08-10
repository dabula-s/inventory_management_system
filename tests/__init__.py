import os

from dotenv import load_dotenv

envs_path = {
    'local': '.env.test.local',
    'docker': '.env.test',
}
load_dotenv(envs_path[os.getenv('ENVIRONMENT', 'local')], override=True)
