<p align="center">
 <h1>XboxNews bot</h1>
</p>



## About
Telegram bot on aiogram using parsing (Beautifulsoup4 and requests) and MySQL database.
The bot parses the news site and, when news appears, sends the name, description and link to the news on the Xbox topic to the user.

P.S.The bot was made a long time ago, when I was not very experienced, so the code may not look very nice and with a small number of comments :(

## Installation

1. Сreate and activate a new virtual environment:
   ```bash
   python3.9 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Install the libraries:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
