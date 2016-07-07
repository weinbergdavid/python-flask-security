
from flask import *
from flask_security import http_auth_required, auth_token_required, Security, RoleMixin, UserMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'something_super_secret_change_in_production'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_MAX_AGE'] = 365*24*60*60*1000


db = SQLAlchemy(app)
# A base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('auth_user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('auth_role.id')))


class Role(Base, RoleMixin):
    __tablename__ = 'auth_role'
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base, UserMixin):
    __tablename__ = 'auth_user'
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    # Why 45 characters for IP Address ?
    # See http://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address/166157#166157
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password='test123')
        db.session.commit()



from flask_security import auth_token_required
from flask import jsonify

@app.route('/dummy-api-http/', methods=['GET'])
@http_auth_required
def dummyAPIHttpAuth():
    ret_dict = {
        "Type": "Http",
        "Email": g.identity.user.email
    }
    return jsonify(items=ret_dict)

@app.route('/dummy-api-token/', methods=['GET'])
@auth_token_required
def dummyAPITokenAuth():
    ret_dict = {
        "Type": "Token",
        "Email": g.identity.user.email
    }
    return jsonify(items=ret_dict)

@app.route('/dummy-api-anonymous/', methods=['GET'])
def index():
    ret_dict = {
        "Type": "Anonymous",
        "Email": None
    }
    return jsonify(items=ret_dict)


app.run(port=5001)

