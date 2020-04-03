"""
Main script that creates the Flask server.
"""


from whyemetl import create_app, db_url

if __name__ == "__main__":
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url()
    app.run(debug=False, host="0.0.0.0")
