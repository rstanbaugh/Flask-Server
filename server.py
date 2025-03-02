# conda environment flask
# python version 3.11.8

from flask import Flask
from routes.routes import routes_bp

app = Flask(__name__, 
            template_folder="templates", 
            static_folder="static")
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(port=8000, debug=True)