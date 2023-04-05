import environ

env = environ.Env()
environ.Env.read_env()

BEARER_TOKEN = env('BEARER_TOKEN')
ORG_ID = env('ORG_ID')