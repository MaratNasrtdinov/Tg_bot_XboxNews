import environ


env = environ.Env(
    TOKEN=(str),
)

TOKEN = env('TOKEN')