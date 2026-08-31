from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import init_db, db_session
from seed_data import seed_database
from routes.profile_routes import profile_bp
from routes.opportunity_routes import opportunity_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(profile_bp)
    app.register_blueprint(opportunity_bp)

    # Health check route
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy", "service": "Smart Internship & Job Finder API"}), 200

    # Ensure DB session is cleared on teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

if __name__ == "__main__":
    init_db()
    seed_database()
    app = create_app()
    print("[INFO] Smart Finder Backend API starting on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
