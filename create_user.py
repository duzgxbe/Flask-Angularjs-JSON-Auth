from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError

from app import create_app
from app.users.models import Users, db

app = create_app('config')

name='Leo'
email='leo@techarena51.com'
password=generate_password_hash('password')
is_enabled=True
user=Users(email, name,password, is_enabled)

def db_commit():
    try:
          db.session.commit()
          print("{} was added successfully".format(email))
          return True
    except SQLAlchemyError as e:
          reason=str(e)
          print (reason)
          return False

with app.app_context():   
        db.session.add(user)
        db_commit()
