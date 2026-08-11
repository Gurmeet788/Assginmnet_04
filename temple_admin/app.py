import os

from flask import Flask
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/")
def home():
    return {"message": "Temple Admin API is running"}


if __name__ == "__main__":
    app.run(debug=True)