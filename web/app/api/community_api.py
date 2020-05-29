import logging
import os
from datetime import datetime

from flask import (
    jsonify,
    render_template,
    request,
)
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    get_jwt_identity
)
import pickle
from bson import ObjectId
from bson.json_util import dumps, loads, RELAXED_JSON_OPTIONS

from web.app import mongo

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def get_all_post(username=None):
    posts = mongo.db.posts
    _posts = []

    if not username:
        for post in posts.find(sort=[('data', -1)]):

            _posts.append({ 'id':       str(post['_id']),
                            'author':   post['author'],
                            'title':    post['title'] if 'title' in post else "",
                            'text':     post['text'],
                            'topic':    post['topic']    
            })
        
        return _posts
    else:
        for post in posts.find(filter={'author': username}, sort=[('data', -1)]):

            _posts.append({ 'id':       str(post['_id']),
                            'author':   post['author'],
                            'title':    post['title'] if 'title' in post else "",
                            'text':     post['text'],
                            'topic':    post['topic']    
            })
        
        return _posts        

def posts():

    _posts = get_all_post()

    return render_template('community.html', posts=_posts)

@jwt_required
def get_posts():

    username = get_jwt_identity()['username']

    _posts = get_all_post(username)

    return render_template('user_post.html', posts=_posts)

@jwt_required
def post():

    posts = mongo.db.posts
    
    if request.method == 'POST':

        _author = get_jwt_identity()['username']
        _text = request.json['text']
        _title = request.json['title']
        _data = datetime.now()
        _topic = request.json['topic']

        logging.info(_text)

        payload = {
            'author': _author,
            'text': _text,
            'title': _title,
            'comment': [],
            'data': _data,
            'topic': _topic
        }

        _ = posts.insert_one(document=payload)

        return jsonify(result='success')
        
    # delete a post
    if request.method == 'DELETE':
        _id = request.json['id']

        posts.delete_one({'_id': ObjectId(_id)})

        return jsonify(result='success')

def get_post(id):

    posts = mongo.db.posts

    if request.method == 'GET':

        _post = []

        res = posts.find_one({'_id': ObjectId(id)})
        res['_id'] = id
        _post.append(res)
        
        return render_template('post.html', posts=_post)

@jwt_required
def comment():
    posts = mongo.db.posts

    if request.method == 'POST':
        _id = request.json['id_post']
        _author = get_jwt_identity()['username']
        _text = request.json['text'] 

    logging.info(_id)
    logging.info(_text)
    
    op = {
            '$push': {
                "comment": {   
                    '$each': [
                        {
                            'author': _author, 
                            'text': _text,
                            'data': datetime.now()
                        }
                    ],
                    '$sort': {
                        "data": -1
                    }
                }
            }
        }

    posts.update_many(  filter  =   {'_id': ObjectId(_id)}, 
                        update  =   op
    )
        
    return jsonify(result='success')