from flask import request, jsonify
from . import db
from .models import User


def register_routes(app):
    @app.route("/")
    def home():
        return jsonify({"message": "Welcome to the Authentication App!"})

    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            return jsonify({"message": "Login successful!"}), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @app.route("/reset-password", methods=["POST"])
    def reset_password():
        data = request.get_json()
        email = data.get("email")
        new_password = data.get("new_password")

        user = User.query.filter_by(email=email).first()

        if user:
            user.password_hash = bcrypt.generate_password_hash(new_password).decode(
                "utf-8"
            )
            db.session.commit()
            return jsonify({"message": "Password reset successful"}), 200

        return jsonify({"error": "User not found"}), 404
