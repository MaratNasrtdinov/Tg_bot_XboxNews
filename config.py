import environ

environ.Env.read_env()

env = environ.Env(
    TOKEN=(str),
)

TOKEN = env('TOKEN')