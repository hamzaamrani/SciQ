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


def submit_expression():
    expression = request.form["symbolic_expression"]

    parsed = parse_2_latex(expression)
    response_obj = compute_expression(parsed)

    with open('tmp_expression', 'wb') as f:
        pickle.dump(response_obj, f)
    collections_names,collections_infos = get_collections_names()

    return render_template(
        "show_results.html",
        alert=False,
        query=expression,
        response_obj=response_obj,
        collections_names=collections_names,
        collections_infos=collections_infos
    )


def parse_2_latex(expression):
    parser = ASCIIMath2Tex(
        asciimath_grammar, inplace=True, parser="lalr", lexer="contextual"
    )
    return parser.asciimath2tex(expression)


def send_file():
    logging.info("Current working location is = " + os.getcwd())
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    logging.info("Save path is = " + save_path)
    fileob.save(save_path)
    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    flash("File uploaded succesfully!")
    return "200"


# GET NAMES OF UPLOADED FILES
def get_filenames():
    logging.info("Current working location is = " + os.getcwd())
    filenames = os.listdir(current_app.config["UPLOAD_FOLDER"])

    def modify_time_sort(file_name):
        file_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], file_name
        )
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time

    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)

# COLLECTIONS HANDLE
def save_expression_to_db():

    # logging.info(request.form["name_collection"])

    with open('tmp_expression', 'rb') as f:
        expression_obj = pickle.load(f)
    os.remove('tmp_expression')

    from web.app import mongo
    users = mongo.db.users

    id_user = "001" # qui id_user andrà letto dai token

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
                            },
                            'prova' : {
                                'info' : "Collezione di prova.",
                                'ids' : []
                            } 

                        }
                }

        users.insert_one(printer)
    
    id_obj = ObjectId()
    json_obj = expression_obj.to_json()
    json_obj['_id'] = id_obj
    # logging.info( id_obj )
    
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

    id_user = "001" # qui id_user andrà letto dai token
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

    id_user = "001" # qui id_user andrà letto dai token
    user = users.find( {'id_user' : id_user} )[0]
    collection_ids = user["collections"][collection_name]["ids"]

    collection_expressions = []
    for collection_id in collection_ids:
        tmp = users.find({"id_user":"001"}, { 'expressions': { '$elemMatch': { '_id': collection_id } } })[0]
        collection_expressions += [tmp]
    
    return collection_expressions