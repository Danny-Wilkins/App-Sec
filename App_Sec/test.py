from app import app, db
from app.models import User, Image
import logging

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Image": Image}

if __name__ == '__main__':
    logging.basicConfig(filename="error.log", level=logging.INFO)
    app.run(ssl_context=("cert.pem", "key.pem"), debug=False)