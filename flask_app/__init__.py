from flask import Flask
from decouple import config

app = Flask (__name__)

app.secret_key = config('secret_key')