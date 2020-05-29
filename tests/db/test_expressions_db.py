import mongomock
import unittest
from bson.objectid import ObjectId

unittest.TestLoader.sortTestMethodsUsing = None

class TestExpressionDb(unittest.TestCase): 
    def setUp(self): 
        self.database = mongomock.MongoClient().sciq_mongo 
        self.collection = self.database['users'] 
        
    def test__connection(self): 
        self.assertEqual("Database(mongomock.MongoClient('localhost', 27017), 'sciq_mongo')", repr(self.database)) 
        self.assertEqual("Collection(Database(mongomock.MongoClient('localhost', 27017), 'sciq_mongo'), 'users')", repr(self.collection)) 
    
    def test__default_collection(self): 
        id_user = 'test_user'
        
        test_data = {
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
        
        self.database.users.insert_one(test_data) 
        result_obj = self.database.users.find_one(filter = test_data) 
        self.assertEqual(test_data, result_obj) 

    def test__test_collection(self): 
        id_user = 'test_user'
        name = 'testCollection'
        info = 'Testing collection.'

        test_data = {
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
        
        self.database.users.insert_one(test_data) 
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$set': {'collections.'+name+'.info' : info, 'collections.'+name+'.ids' : [] } }
        )

        collection_exist=False
        for doc in list(self.database.users.find( {'id_user' : id_user} )):
            for collection in doc["collections"]:
                if collection == name:
                    collection_exist=True

        self.assertTrue(collection_exist)

    def test__delete_collection(self): 
        id_user = 'test_user'
        name = 'testDeleteCollection'
        info = 'Testing collection.'

        test_data = {
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
        
        self.database.users.insert_one(test_data) 
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$set': {'collections.'+name+'.info' : info, 'collections.'+name+'.ids' : [] } }
        )

        self.database.users.update_one( {'id_user': id_user},{'$unset': {'collections.'+name : 1 }} )

        collection_exist=True
        for doc in list(self.database.users.find( {'id_user' : id_user} )):
            for collection in doc["collections"]:
                if collection == name:
                    collection_exist=False

        self.assertTrue(collection_exist)

    def test__save_expression(self):
        id_user = 'test_user'
        name = 'testCollection'
        info = 'Testing collection.'
        id_obj =  ObjectId()

        json_obj = {'query': '\\sum_{i = 1}^{n} i^{3} = \\left(\\frac{n \\left(n + 1\\right)}{2}\\right)^{2}', 
                   'success': 'true', 
                   'execution_time': '1.279', 
                   'plots': [], 
                   'alternate_forms': [], 
                   'solutions': [], 
                   'symbolic_solutions': [], 
                   'results': ["<math xmlns='http://www.w3.org/1998/Math/MathML'    mathematica:form='StandardForm'    xmlns:mathematica='http://www.wolfram.com/XML/'> <mi>True</mi></math>"], 
                   'limits': [], 
                   'partial_derivatives': [], 
                   'integral': [], 
                   '_id': id_obj, 
                   'public': 'false'}

        test_data = {
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
        
        self.database.users.insert_one(test_data)
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$set': {'collections.'+name+'.info' : info, 'collections.'+name+'.ids' : [] } }
        )

        self.database.users.update_one(
            { 'id_user' : id_user },
            { '$addToSet': {'expressions': json_obj } }
        )
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$addToSet': {'collections.default.ids' : id_obj } }
        )
        self.database.users.update_one( 
            {'id_user' : id_user}, 
            {'$addToSet': {'collections.' + name + ".ids": id_obj}} 
        )

        expression_id = self.database.users.find({"id_user": id_user}, { 'expressions': { '$elemMatch': { '_id': id_obj } } })[0]['expressions'][0]['_id']
        default_expression_id = self.database.users.find({"id_user": id_user}, { 'collections.default.ids':1 } )[0]['collections']['default']['ids'][0]
        collection_expression_id = self.database.users.find({"id_user": id_user}, { 'collections.'+name+'.ids':1 } )[0]['collections'][name]['ids'][0]

        self.assertEqual(id_obj, ObjectId(expression_id))
        self.assertEqual(id_obj, ObjectId(default_expression_id))
        self.assertEqual(id_obj, ObjectId(collection_expression_id))

    def test__delete_expression(self):
        id_user = 'test_user'
        name = 'testCollection'
        info = 'Testing collection.'
        id_obj =  ObjectId()

        json_obj = {'query': '\\sum_{i = 1}^{n} i^{3} = \\left(\\frac{n \\left(n + 1\\right)}{2}\\right)^{2}', 
                   'success': 'true', 
                   'execution_time': '1.279', 
                   'plots': [], 
                   'alternate_forms': [], 
                   'solutions': [], 
                   'symbolic_solutions': [], 
                   'results': ["<math xmlns='http://www.w3.org/1998/Math/MathML'    mathematica:form='StandardForm'    xmlns:mathematica='http://www.wolfram.com/XML/'> <mi>True</mi></math>"], 
                   'limits': [], 
                   'partial_derivatives': [], 
                   'integral': [], 
                   '_id': id_obj, 
                   'public': 'false'}

        test_data = {
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
        
        self.database.users.insert_one(test_data)
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$set': {'collections.'+name+'.info' : info, 'collections.'+name+'.ids' : [] } }
        )

        self.database.users.update_one(
            { 'id_user' : id_user },
            { '$addToSet': {'expressions': json_obj } }
        )
        self.database.users.update_one(
            { 'id_user' : id_user},
            { '$addToSet': {'collections.default.ids' : id_obj } }
        )
        self.database.users.update_one( 
            {'id_user' : id_user}, 
            {'$addToSet': {'collections.' + name + ".ids": id_obj}} 
        )

        self.database.users.update( {'id_user': id_user},{'$pull': {'expressions':{'_id' : id_obj  }}}, 'false','true' )
        self.database.users.update( {'id_user': id_user},{'$pull': {'collections.default.ids' : id_obj }}, 'false','true' )
        self.database.users.update( {'id_user': id_user},{'$pull': {'collections.'+name+'.ids' : id_obj }}, 'false','true' )
        try:
            expression_id = self.database.users.find({"id_user": id_user}, { 'expressions': { '$elemMatch': { '_id': id_obj } } })[0]['expressions'][0]['_id']
            default_expression_id = self.database.users.find({"id_user": id_user}, { 'collections.default.ids':1 } )[0]['collections']['default']['ids'][0]
            collection_expression_id = self.database.users.find({"id_user": id_user}, { 'collections.'+name+'.ids':1 } )[0]['collections'][name]['ids'][0]
        except:
            expression_id = None
            default_expression_id = None
            collection_expression_id = None
            pass

        self.assertNotEqual(id_obj, ObjectId(expression_id))
        self.assertNotEqual(id_obj, ObjectId(default_expression_id))
        self.assertNotEqual(id_obj, ObjectId(collection_expression_id))



if __name__ == '__main__': 
    unittest.main()