# conda environment flask
# python version 3.11.2
# plan to deploy on raspberry pi
# will use the following tools:
#   flask back end
#   gunicorn to serve the flask app
#   nginx on pi for reverse proxy
#   self signed ssl for local development

from flask import Flask
from routes.routes import routes_bp

app = Flask(__name__, 
            template_folder="templates", 
            static_folder="static")
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)