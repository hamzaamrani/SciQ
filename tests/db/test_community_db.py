import mongomock
import unittest
from datetime import datetime
from bson.objectid import ObjectId
import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

unittest.TestLoader.sortTestMethodsUsing = None

class TestExpressionDb(unittest.TestCase): 
    def setUp(self): 
        self.database = mongomock.MongoClient().sciq_mongo 
        self.collection = self.database['posts'] 
        
    def test__connection(self): 
        self.assertEqual("Database(mongomock.MongoClient('localhost', 27017), 'sciq_mongo')", repr(self.database)) 
        self.assertEqual("Collection(Database(mongomock.MongoClient('localhost', 27017), 'sciq_mongo'), 'posts')", repr(self.collection)) 

    def test_add_post(self):
        payload = {
            'author': 'test_author',
            'text': 'test_text',
            'title': 'test_title',
            'comment': [],
            'data': datetime.now(),
            'topic': 'test_topic'
        }

        self.collection.insert_one(document=payload)
        result_obj = self.collection.find_one(filter = payload) 
        self.assertEqual(payload, result_obj) 


    def test_delete_post(self):
        payload1 = {
            'author': 'test_author1',
            'text': 'test_text_1',
            'title': 'test_title',
            'comment': [],
            'data': datetime.now(),
            'topic': 'test_topic'
        }

        self.collection.insert_one(document=payload1)

        payload2 = {
            'author': 'test_author2',
            'text': 'test_text_2',
            'title': 'test_title',
            'comment': [],
            'data': datetime.now(),
            'topic': 'test_topic'
        }

        self.collection.insert_one(document=payload2)

        self.collection.delete_one(filter=payload1)
        result_obj = self.collection.find()
        for doc in result_obj:
            self.assertEqual(payload2, doc) 


    def test_add_comment(self):

        comment1 = {
            'author': 'author1', 
            'text': 'text1',
            'data': 'data_mock'
        }
        comment2 = {
            'author': 'author2', 
            'text': 'text2',
            'data': 'data_mock'
        }

        comments = [comment1, comment2]

        payload = {
            'author': 'test_author1',
            'text': 'test_text_1',
            'title': 'test_title',
            'comment': comments,
            'data': datetime.now(),
            'topic': 'test_topic'
        }

        self.collection.insert_one(document=payload)

        res = self.collection.find_one(filter=payload)

        for comment, true_comment in zip(res['comment'], comments):
            self.assertEqual(true_comment, comment)

if __name__ == '__main__': 
    unittest.main()

