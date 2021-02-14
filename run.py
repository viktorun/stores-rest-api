from app import app
from db import db

db.init_app(app)  # This will do the same as __main__ in app.py

# However we will need to move the decorator from app.py. Note we will need to ensure this is running in uwsgi.ini
# hence it is run in Heroku
@app.before_first_request
def create_tables():
    db.create_all()
