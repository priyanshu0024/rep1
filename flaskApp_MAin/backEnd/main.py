import datetime
from flask import Flask, render_template,request, jsonify
from config import DevelopmentConfig
from models import db, User, Role, Posts, Like, Comment, Follow_unfollow
from flask_security import SQLAlchemyUserDatastore, Security, auth_required, current_user
from flask_cors import CORS

datastore = SQLAlchemyUserDatastore(db, User, Role)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
db.init_app(app)
security = Security(app, datastore)




## ------- Create User ----------##
@app.post('/register')
def create_user():
    data = request.json
    datastore.create_user(**data)
    db.session.commit()
    return jsonify({"msg":"User Created"})
    

## ------- Get User ----------##
@app.get("/getuser/<string:email>")
def get_user(email):
    user = User.query.filter_by(email = email).first()
    id1 = user.id
    return jsonify({"id":id1})


## ------- User Dashboard ----------##
@app.get('/dashboard/<int:id>')
def dashboard(id):
    user = User.query.get(id)
    user_data = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'city': user.city,
        'join_date': user.join_date,
        "posts": len([post.id for post in user.posts]),
        "followers" : len([follower.id for follower in user.followers]),
        "followeds" : len([follow.id for follow in user.followed]),
        'profile_pic': user.profile_pic
    }
    return jsonify(user_data), 200





@app.route('/users/search/<string:str>', methods=['GET'])
def search_users(str):
    name = str
    if not name:
        return jsonify({'error': 'Name parameter is required'}), 400
    
    # Query the database to find users whose name contains the search term
    users = User.query.filter(User.name.ilike(f'%{name}%')).all()
    
    # Serialize the search results to JSON
    serialized_users = [{'id': user.id, 'name': user.name, 'username': user.username,
                         'email': user.email, 'city': user.city, 'join_date': user.join_date.strftime('%Y-%m-%d'),
                         'profile_pic': user.profile_pic} for user in users]
    
    return jsonify(serialized_users)







# @app.route('/users', methods=['GET'])
# def get_users():
#     users = User.query.all()
#     data = []
#     for user in users:
#         item = {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "city": user.city,
#             "followers": [follower.id for follower in user.followers],
#             "followeds": len([follow.id for follow in user.followed]),
#         }
#         data.append(item)
#     return jsonify(data)



@app.route('/users')
def get_users():
    users = User.query.all()
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'followers': user.followers.count(),
            'followed': user.followed.count(),
        }
        users_data.append(user_data)
    return jsonify(users_data)









## ------- Create Post ----------##
@app.post('/add/post')
@auth_required('token')
def create_post():
    data = request.json
    post = Posts(title = data['title'], content=data['content'], author_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"msg":"Post Created"})



## ------- Get Post ----------##
# @app.get("/getpost/<int:id>")
# @auth_required('token')
# def get_post(id):
#     post = Posts.query.get(id)
#     if post:
#         data = {
#             "id": post.id,
#             "title": post.title,
#             "key_note": post.key_note,
#             "content": post.content,
#             "author_id": post.author_id
#         }
#         return jsonify(data)
#     else:
#         return jsonify({"message": "Post not found"}), 404





## ------- Delete Post ----------##
@app.delete('/deletepost/<int:id>')
@auth_required('token')
def delete_post(id):
    post = Posts.query.get(id)
    user_id = post.author_id
    if user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg":"post deleted"})
    else:
        return jsonify({"msg":"You are not Authorised to delete this post"})

    


## ------- Update Post ----------##
@app.post('/updatepost/<int:id>')
@auth_required('token')
def update_post(id ):
    data = request.json
    post = Posts.query.get(id)
    if not post:
        return jsonify({'error': 'Post not found.'}), 404
    
    if post.author_id != data.get('author_id'):
        return jsonify({'error': 'You do not have permission to edit this post.'}), 403
    post.title = data.get('title', post.title)
    post.key_note = data.get('key_note', post.key_note)
    post.content = data.get('content', post.content)
    db.session.commit()
    return jsonify({"msg":"Post Updated"})





@app.route("/getallposts")
@auth_required('token')
def get_posts():
    posts = Posts.query.all()
    data = []
    for post in posts:
        item = {
            "id": post.id,
            "title": post.title,
            "key_note": post.key_note,
            "content": post.content,
            "date_posted": post.date_posted,
            "author_id": post.author_id,
            "comments": [comment.id for comment in post.comments],
            "likes": len([like.id for like in post.likes]),
        }
        data.append(item)
    return jsonify(data)





# # Get a post by id
@app.get("/getpost/<int:id>")
@auth_required('token')
def get_post(id):
    post = Posts.query.get_or_404(id)
    item = {
        "id": post.id,
        "title": post.title,
        "key_note": post.key_note,
        "content": post.content,
        "date_posted": post.date_posted,
        "author_id": post.author_id,
        "comments": [comment.id for comment in post.comments],
        "likes": [like.id for like in post.likes],
    }
    return jsonify(item)





# Get all comments for a post by post id
@app.get("/post/<int:id>/comments")
@auth_required('token')
def get_comments(id):
    post = Posts.query.get_or_404(id)
    comments = post.comments
    data = []
    for comment in comments:
        item = {
            "id": comment.id,
            "text": comment.text,
            "date_posted": comment.date_posted,
            "author_id": comment.author,
            "post_id": comment.post_id,
        }
        data.append(item)
    return jsonify(data)

# Get all likes for a post by post id
@app.get("/post/<int:id>/likes")
def get_likes(id):
    post = Posts.query.get_or_404(id)
    likes = post.likes
    data = []
    for like in likes:
        item = {
            "id": like.id,
            "date_posted": like.date_posted,
            "author_id": like.author,
            "post_id": like.post_id,
        }
        data.append(item)
    return jsonify(data)

# Create a comment for a post by post id
@app.post("/post/<int:id>/comments")
@auth_required('token')
def create_comment(id):
    post = Posts.query.get_or_404(id)
    data = request.json
    comment = Comment(text=data["text"], author=current_user.id, post_id=post.id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"msg": "Comment Created"})





@app.post("/post/<int:id>/like")
@auth_required('token')
def like_post(id):
    post = Posts.query.get_or_404(id)
    like = Like.query.filter_by(author=current_user.id, post_id=post.id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        liked = False
    else:
        like = Like(author=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit() 
        liked = True
    likes_count = len(post.likes)
    item = {
        "id": post.id,
        "title": post.title,
        "key_note": post.key_note,
        "content": post.content,
        "date_posted": post.date_posted,
        "author_id": post.author_id,
        "comments": [comment.id for comment in post.comments],
        "likes": likes_count,
        "liked": liked,
    }
    return jsonify(item)




# Follow a user by user id
# @app.post("/user/<int:id>/follow")
# @auth_required('token')
# def follow_user(id):
#     user = User.query.get_or_404(id)
#     follow = Follow_unfollow(follower_id=current_user.id, followed_by_id=user.id)
#     db.session.add(follow)
#     db.session.commit()
#     return jsonify({"msg": "User Followed"})

# Unfollow a user by user id
# @app.post("/user/<int:id>/unfollow")
# @auth_required('token')
# def unfollow_user(id):
#     user = User.query.get_or_404(id)
#     follow = Follow









## ------- DataBase Create ----------##
@app.before_first_request
def create_db():
    db.create_all( )


if __name__ == "__main__":
    app.run(debug=True)
