from flask import Flask
from auth.routes import auth_bp
from pages.routes import pages_bp
from admin.routes import admin_bp
from content.routes import content_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(content_bp)

@app.route("/")
def home():
    return {"message": "Temple Admin API is running"}

if __name__ == "__main__":
    app.run(debug=True)