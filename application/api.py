from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from application.database import db
from application.models import User, Post, Comment
from application.validation import NotFoundError, BusinessValidationError
from flask import Blueprint, jsonify, request, current_app
import bcrypt

current_user = None

login_fields = {
    "email": fields.String,
    "password": fields.String
}

user_fields = {"username" : fields.String,
                "name" : fields.String,
                "email" : fields.String,
                "bio" : fields.String,
                "profile_photo" : fields.String
}

only_usernames = {"username" : fields.String}

comment_fields = {"comment_id": fields.Integer,
                    "post_id": fields.Integer,
                    "body": fields.String,
                    "user": fields.Nested(user_fields),
                    "commenter": fields.String

}

post_fields = {"post_id": fields.Integer,
                "title" : fields.String,
                "description" : fields.String,
                "username" : fields.String,
                "likes": fields.Integer,
                "post_photo": fields.String,
                "user": fields.Nested(user_fields),
                "comments": fields.Nested(comment_fields)
}

class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self,username):
        if username == "*":
            username = current_user
        user = db.session.query(User).filter(User.username == username).first()
        if user:
            print(current_user)
            return user
        else:
            raise NotFoundError(status_code=404)

    def post(self):
        args = request.get_json()
        username = args.get("username")
        name = args.get("name")
        bio = args.get("bio")  
        profile_photo= args.get("profile_photo") 
        email =   args.get("email")    
        password = args.get("password").encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        new_user = User(username = username, name = name, bio = bio, email = email, password = hashed, profile_photo = profile_photo)
        db.session.add(new_user)
        db.session.commit()
        return "",201

    def put(self):
        args = request.get_json()
        modify_user = db.session.query(User).filter(User.username == current_user).first()
        if not modify_user:
            return {"status": "Not Found"}, 404
        print(modify_user)
        modify_user.name = args.get("name", None)
        modify_user.email = args.get("email", None)
        modify_user.bio = args.get("bio", None)
        passw = args.get("password", None).encode('utf-8')
        hashed = bcrypt.hashpw(passw, bcrypt.gensalt()).decode('utf-8')
        modify_user.password = hashed
        modify_user.profile_photo = args.get("profile_photo",None)
        db.session.commit()
        return "", 200

    def delete(self, username):
        delete_user = db.session.query(User).filter(User.username == username).first()
        db.session.delete(delete_user)
        db.session.commit()
        return "",204

#-----------------#-----#-----------------

class PostAPI(Resource):
    @marshal_with(post_fields)
    def get(self,username):
        post = db.session.query(Post).filter(Post.username == username).all()
        if post:
            return post
        else:
            raise NotFoundError(status_code=404)
        

    def post(self):
        args = request.get_json()
        print(args)
        title = args.get("title")
        description = args.get("description")
        post_photo= args.get("post_photo") 
        username = args.get("username") 
        likes = 0
        new_post = Post(username = username, title = title, description = description, post_photo = post_photo, likes=likes)
        db.session.add(new_post)
        db.session.commit()
        return "",201

    def put(self, post_id):
        print(post_id)
        args = request.get_json()
        modify_post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if not modify_post:
            return {"status": "Not Found"}, 404
        print(modify_post)
        modify_post.title = args.get("title", None)
        modify_post.description = args.get("description", None)
        db.session.commit()
        return "", 200

    def delete(self, post_id):
        delete_post = db.session.query(Post).filter(Post.post_id == post_id).first()
        db.session.delete(delete_post)
        db.session.commit()
        return "",204

#-----------------#-----#-----------------

class CommentAPI(Resource):
    @marshal_with(comment_fields)
    def get(self,id):
        comment = db.session.query(Comment).filter(Comment.post_id == id).all()
        if comment:
            return comment
        else:
            raise NotFoundError(status_code=404)
        

    def post(self, id):
        args = request.get_json()
        print(args)
        commenter = args.get("commenter")
        body = args.get("body")
        new_comment = Comment(commenter = commenter, post_id = id, body = body)
        db.session.add(new_comment)
        db.session.commit()
        return "",201

    def put(self, id):
        args = request.get_json()
        modify_comment = db.session.query(Comment).filter(Comment.comment_id == id).first()
        if not modify_comment:
            return {"status": "Not Found"}, 404
        modify_comment.body = args.get("body", None)
        db.session.commit()
        return "", 200

    def delete(self, id):
        delete_comment = db.session.query(Comment).filter(Comment.comment_id == id).first()
        db.session.delete(delete_comment)
        db.session.commit()
        return "",204

#-----------------#-----#-----------------

class IndividualPostAPI(Resource):
    @marshal_with(post_fields)
    def get(self,post_id):
        post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if post:
            return post
        else:
            raise NotFoundError(status_code=404)

#-----------------#-----#-----------------

class CurrentUserAPI(Resource):
    @marshal_with(post_fields)
    def get(self,post_id):
        post = db.session.query(Post).filter(Post.post_id == post_id).first()
        if post:
            return post
        else:
            raise NotFoundError(status_code=404)

test_api_resource_fields = {
    'msg': fields.String,
}

#-----------------#-----#-----------------

class AllUsersAPI(Resource):
    @marshal_with(only_usernames)
    def get(self):
        users = db.session.query(User).all()
        if users:
            return users
        else:
            raise NotFoundError(status_code=404)

#-----------------#-----#-----------------

class LoginAPI(Resource):
    @marshal_with(login_fields)
    def post(self):
        global current_user
        args = request.get_json()
        email = args.get("email")
        password = args.get("password")
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), bytes(user.password, 'utf-8')):
                current_user = user.username
                print(current_user)
                return "",200
            else:
                print("Incorrect Data")
        else:
            raise NotFoundError(status_code=404)

#-----------------#-----#-----------------

class LogoutAPI(Resource):
    def get(self):
        global current_user
        current_user = None
        return "",200

test_api_resource_fields = {
    'msg': fields.String,
}

class TestAPI(Resource):
    def get(self):
        return jsonify({"msg":"Hi Mom"})