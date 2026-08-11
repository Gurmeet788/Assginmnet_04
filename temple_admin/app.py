from flask import Flask
from auth.routes import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"message": "Temple Admin API is running"}


if __name__ == "__main__":
    app.run(debug=True)