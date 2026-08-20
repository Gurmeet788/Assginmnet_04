from flask import Flask, render_template
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

@app.route("/admin/login")
def admin_login_page():
    return render_template("admin/login.html")

@app.route("/admin/signup")
def admin_signup_page():
    return render_template("admin/signup.html")

@app.route("/admin/dashboard")
def admin_dashboard_page():
    return render_template("admin/dashboard.html")

if __name__ == "__main__":
    app.run(debug=True,port=3000)