from flask import Flask
from application.database import db
app=None
def create_app():
    app = Flask(__name__)
    app.debug= True
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///placement-p.sqlite3'
    db.init_app(app)
    with app.app_context():
        
        from application.models import User, Student, Company, PlacementDrive, Application
        db.create_all() 
        Admin=User.query.filter_by(role="admin").first()
        if Admin is None:
            Admin=User(username="admin1",password="admin123", role="admin" )
            db.session.add(Admin)
            db.session.commit()
    return app


app= create_app()

if __name__ == "__main__":
    app.run()


