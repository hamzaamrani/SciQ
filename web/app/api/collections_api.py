import logging

from bson import ObjectId
from flask import Markup, jsonify, render_template, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from user_agents import parse
from web.app.services.utils.utils import raw

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


@jwt_required
def collections():
    logging.info("Collections")

    collections_names, collections_infos = get_collections()
    expressions_by_collection = []

    for collection_name in collections_names:
        expressions = get_expressions(collection_name)
        expressions_by_collection.append(expressions)

    user_agent = parse(request.headers.get("User-Agent"))
    if user_agent.is_pc:
        return render_template(
            "collections.html",
            collections_names=collections_names,
            collections_infos=collections_infos,
            expressions_by_collection=expressions_by_collection,
        )


@jwt_required
def get_idUser():
    return str(get_jwt_identity()["id_user"])


# COLLECTIONS HANDLE
def save_expression_to_db():
    logging.info("Saving expression to db...")

    json_obj = request.get_json()
    logging.info(json_obj)

    from web.app import mongo

    users = mongo.db.users

    id_user = get_idUser()
    id_obj = ObjectId()
    json_obj["response"]["_id"] = id_obj
    json_obj["response"]["public"] = json_obj["public"]
    json_obj["response"]["query"] = raw(json_obj["response"]["query"])

    # Add current expression and add to default collection
    users.update(
        {"id_user": id_user},
        {"$addToSet": {"expressions": json_obj["response"]}},
    )

    # Save current expression's id in default collection
    users.update(
        {"id_user": id_user},
        {"$addToSet": {"collections.default.ids": id_obj}},
    )

    # Save current expression's id in personalized collection

    if not (json_obj["name_collection"] == "default"):
        collection = "collections." + json_obj["name_collection"] + ".ids"
        users.update({"id_user": id_user}, {"$addToSet": {collection: id_obj}})

    logging.info("Saving expression to db has been completed with success!")

    return jsonify({"result": "expression saved in collection"})


def create_default_collection(id_user):
    from web.app import mongo

    users = mongo.db.users

    # id_user = get_idUser()

    logging.info("Saving current expression to db...")

    # Check if user collection exists
    # logging.info(users.find({ 'id_user': id_user } ).count())
    if users.find({"id_user": id_user}).count() == 0:
        logging.info("Creating collection for user: " + id_user)
        printer = {
            "id_user": id_user,
            "expressions": [],
            "collections": {
                "default": {
                    "info": "Default collection for expressions.",
                    "ids": [],
                }
            },
        }

        users.insert_one(printer)


def get_collections():
    from web.app import mongo

    users = mongo.db.users

    id_user = get_idUser()
    collections_names = []
    collections_infos = []

    for doc in users.find({"id_user": id_user}):
        for collection in doc["collections"]:
            collections_names += [collection]
            collections_infos += [doc["collections"][collection]["info"]]

    if not collections_names:
        collections_names = ["default"]
        collections_infos = ["Default collection for expressions."]

    return collections_names, collections_infos


def dict2obj(d):
    if isinstance(d, list):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d

    class C(object):
        pass

    o = C()
    for k in d:
        o.__dict__[k] = dict2obj(d[k])
    return o


def get_expressions(collection_name):
    from web.app import mongo

    users = mongo.db.users

    logging.info("Get expressions")

    id_user = get_idUser()
    collection_expressions = []

    try:
        user = users.find({"id_user": id_user})[0]
        collection_ids = user["collections"][collection_name]["ids"]

        for collection_id in collection_ids:
            try:
                expression = users.find(
                    {"id_user": id_user},
                    {"expressions": {"$elemMatch": {"_id": collection_id}}},
                )[0]["expressions"][0]
                expression_obj = dict2obj(expression)
                collection_expressions.append(expression_obj)
            except Exception:
                pass
    except Exception:
        pass

    return collection_expressions


def create_collection():
    from web.app import mongo

    users = mongo.db.users

    id_user = get_idUser()
    name = request.form["name_collection"]
    info = request.form["info_collection"]

    users.update(
        {"id_user": id_user},
        {
            "$set": {
                "collections." + name + ".info": info,
                "collections." + name + ".ids": [],
            }
        },
    )
    """
    users.createIndex(
        {"id_user": id_user, "collections.default": 1}, {"unique": "true"}
    )
    """
    """
    users.create_index([("id_user"),("collections.default")], unique=True)
    """

    logging.info("User " + id_user + ": created collection " + name + "!")

    return jsonify({"result": "collection created"})


def delete_collection():
    from web.app import mongo

    users = mongo.db.users

    id_user = get_idUser()
    name = request.form["name_collection"]

    logging.info("User " + id_user + ": deliting collection " + name + "...")

    users.update({"id_user": id_user}, {"$unset": {"collections." + name: 1}})

    logging.info("User " + id_user + ": deleted collection " + name + "!")

    return jsonify({"result": "collection deleted"})


def show_expression():
    id_expr = request.form["id_expr"]

    from web.app import mongo

    users = mongo.db.users
    id_user = get_idUser()

    exp = users.find(
        {"id_user": id_user},
        {"expressions": {"$elemMatch": {"_id": ObjectId(id_expr)}}},
    )[0]["expressions"][0]

    exp_keys = [
        "alternate_forms",
        "solutions",
        "symbolic_solutions",
        "results",
        "limits",
        "partial_derivatives",
        "integral",
    ]

    for key in exp_keys:
        exp[key] = [Markup(x) for x in exp[key]]

    exp_obj = dict2obj(exp)

    return render_template(
        "show_results.html",
        alert=False,
        query=exp_obj.query,
        response_obj_json=jsonify({}),
        response_obj=exp_obj,
        collections_names=[],
        collections_infos=[],
    )


def delete_expression():
    id_expr = request.form["id_expr"]

    from web.app import mongo

    users = mongo.db.users
    id_user = get_idUser()

    collections_names, collections_infos = get_collections()

    users.update(
        {"id_user": id_user},
        {"$pull": {"expressions": {"_id": ObjectId(id_expr)}}},
        "false",
        "true",
    )

    for collection_name in collections_names:
        users.update(
            {"id_user": id_user},
            {
                "$pull": {
                    "collections."
                    + collection_name
                    + ".ids": ObjectId(id_expr)
                }
            },
            "false",
            "true",
        )
