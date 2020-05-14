import logging
import os

from flask import (
    current_app,
    flash,
    jsonify,
    render_template,
    request,
)
from werkzeug.utils import secure_filename

from web.app.services.api_wolfram.waAPI import compute_expression
from web.app.services.parser.const import asciimath_grammar
from web.app.services.parser.parser import ASCIIMath2Tex

from web.app.services.api_wolfram.waAPI import Expression
import pickle

from bson import ObjectId

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def collections():
    logging.info("Collections")

    collections_names,collections_infos = get_collections_names()

    return render_template(
        "collections.html",
        collections_names=collections_names,
        collections_infos=collections_infos
    )

def get_idUser():
    return "001"

# COLLECTIONS HANDLE
def save_expression_to_db():

    # logging.info(request.form["name_collection"])

    with open('tmp_expression', 'rb') as f:
        expression_obj = pickle.load(f)
    os.remove('tmp_expression')

    from web.app import mongo
    users = mongo.db.users

    id_user = get_idUser()

    logging.info("Saving current expression to db...")

    # Check if user collection exists
    # logging.info(users.find({ 'id_user': id_user } ).count())
    if users.find({ 'id_user': id_user } ).count() == 0:
        logging.info( "Creating collection for user: " + id_user )
        printer = {
                    'id_user' : id_user,
                    'expressions' : [],
                    'collections' :
                        {
                            'default' : {
                                'info' : "Default collection for expressions.",
                                'ids' : []
                            }

                        }
                }

        users.insert_one(printer)
        users.createIndex( { 'id_user' : id_user, 'collections.default':1 }, { 'unique': 'true' } )

    
    id_obj = ObjectId()
    json_obj = expression_obj.to_json()
    json_obj['_id'] = id_obj
    json_obj['public'] = request.form["public"]

    
    # Add current expression and add to default collection
    users.update(
        { 'id_user' : id_user },
        { '$addToSet': {'expressions': json_obj } }
    )

    # Save current expression's id in default collection
    users.update(
        { 'id_user' : id_user},
        { '$addToSet': {'collections.default.ids' : id_obj } }
    )

    # Save current expression's id in personalized collection

    if not( request.form["name_collection"] == "default"):
        collection = 'collections.' + request.form["name_collection"] + ".ids"
        users.update( 
            {'id_user' : '001'}, 
            {'$addToSet': {collection: id_obj}} 
        )
    
    logging.info("Saving expression to db has been completed with success!")

    return "okk"

def get_collections_names():
    from web.app import mongo
    users = mongo.db.users

    id_user = get_idUser()
    collections_names = []
    collections_infos = []

    for doc in users.find( {'id_user' : id_user} ):
        for collection in doc["collections"]:
            collections_names += [collection]
            collections_infos += [doc["collections"][collection]['info']]
    
    if not collections_names:
        collections_names = ['default']
        collections_infos = ['Default collection for expressions.']
    
    return collections_names,collections_infos

def get_expressions(collection_name):
    from web.app import mongo
    users = mongo.db.users

    logging.info("Get expressions")

    id_user = get_idUser()
    user = users.find( {'id_user' : id_user} )[0]
    collection_ids = user["collections"][collection_name]["ids"]

    collection_expressions = []
    for collection_id in collection_ids:
        tmp = users.find({"id_user":"001"}, { 'expressions': { '$elemMatch': { '_id': collection_id } } })[0]
        collection_expressions += [tmp]
    
    return collection_expressions

def create_collection():
    from web.app import mongo
    users = mongo.db.users
    
    id_user = get_idUser()
    name = request.form["name_collection"]
    info = request.form["info_collection"]

    users.update(
        { 'id_user' : id_user},
        { '$set': {'collections.'+name+'.info' : info, 'collections.'+name+'.ids' : [] } }
    )
    users.createIndex( { 'id_user' : id_user, 'collections.default':1 }, { 'unique': 'true' } )
    
    logging.info("User " + id_user + ": created collection " + name + "!"  )

def delete_collection():
    from web.app import mongo
    users = mongo.db.users
    
    id_user = get_idUser()
    name = request.form["name_collection"]

    users.update( {'id_user':'001'},{'$unset': {'collections.'+name : 1 }} )
    
    logging.info("User " + id_user + ": deleted collection " + name + "!"  )