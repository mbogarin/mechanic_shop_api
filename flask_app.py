from app import create_app
from app.models import db


app = create_app("ProductionConfig")
    
    
# Create tables in DB:
with app.app_context():
    # db.drop_all() # ! reset test data *
    db.create_all()


# if __name__ == '__main__':
#     app.run(debug=True) # remove for production.