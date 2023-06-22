from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))




# Create a follow/unfollow model 
class Follow_unfollow(db.Model):
    __tablename__ = 'follow_unfollow'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    followed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)



# Create a blog user model 
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    city = db.Column(db.String, nullable = False)
    join_date = db.Column(db.DateTime, default = datetime.utcnow)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    profile_pic = db.Column(db.String(), nullable = True)
    posts = db.relationship('Posts', backref = "poster")
    comments = db.relationship('Comment', backref = "user", passive_deletes = True)
    likes = db.relationship('Like', backref = "user", passive_deletes = True)
    followed = db.relationship('Follow_unfollow',
                               foreign_keys=[Follow_unfollow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic')
    followers = db.relationship('Follow_unfollow',
                            foreign_keys=[Follow_unfollow.followed_by_id],
                            backref=db.backref('followed', lazy='joined'),
                            lazy='dynamic')
    about_user = db.Column(db.String, nullable = True)
    
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    is_following = False

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.city}')"



# Create a blog role model 
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    
    
    
    
    
# Create a blog post model 
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    key_note = db.Column(db.String)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    comments = db.relationship('Comment', backref = "post", passive_deletes = True)
    likes = db.relationship('Like', backref = "post", passive_deletes = True)




# Create a comment model 
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable = False)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete = "CASCADE"), nullable = False)






# Create a like model 
class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete = "CASCADE"), nullable = False)
    
    
    
    


