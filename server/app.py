from flask import Flask

def server_run():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "1"
    
    app.run(host='0.0.0.0', port=8082)
