from app import app, db
from app.models import User, Image

@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Image": Image}

if __name__ == '__main__':
    app.run(ssl_context=("cert.pem", "key.pem"), debug= False)