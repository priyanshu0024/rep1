from flask import Flask, render_template,request, jsonify
from config import DevelopmentConfig
from models import db, User, Role
from flask_security import SQLAlchemyUserDatastore, Security, auth_required

datastore = SQLAlchemyUserDatastore(db, User, Role)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
security = Security(app, datastore)



@app.get('/')
def home():
    return render_template('index.html')

@app.post('/user')
def create_user():
    data = request.json
    datastore.create_user(**data)
    db.session.commit()
    return jsonify({"msg":"User Created"})

@app.get('/profile')
@auth_required('token')
def profile():
    return jsonify({"name":"work"})

@app.get('/login')
def login():
    return jsonify({"name":"work"})



@app.before_first_request
def create_db():
    db.create_all( )


if __name__ == "__main__":
    app.run(debug=True)