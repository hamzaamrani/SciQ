# autopep8 --in-place --aggressive --aggressive waAPI.py
# Wolfram|Alpha Show Steps API Reference:
# https://products.wolframalpha.com/show-steps-api/documentation/

import requests
import urllib.parse
import json
import base64
import xmltodict
import urllib.request
import pickle

API_URL = 'https://api.wolframalpha.com/v2/query'
API_SIGNUP_PAGE = 'https://developer.wolframalpha.com'
KEY = 'V2WJ46-EEXEV95WXG'


class NoAPIKeyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class waAPI(object):
    def __init__(self, key=None):
        """
        Initializes the booksAPI class with a developer key. Raises an exception if a key is not given.

        Request a key at https://developer.wolframalpha.com

        :param key: Wolfram Alpha App ID Developer Key

        """
        self.key = key
        self.response_format = 'json'

        if self.key is None:
            raise NoAPIKeyException(
                'Warning: Missing API Key. Please visit ' +
                API_SIGNUP_PAGE +
                ' to register for a key.')

    def full_results(self,
                     response_format=None,
                     key=None,
                     query=None):
        """
        Calls the API and returns a dictionary of the search results

        :param response_format: the format that the API uses for its response,
                                includes JSON (.json) and XML.
                                Defaults to '.json'.

        :param key: a developer key. Defaults to key given when the waAPI class was initialized.

        :**kwargs examples:
                        query = 'How many megabytes are in a gigabyte'
        """
        if key is None:
            key = self.key
        if response_format is None:
            response_format = self.response_format
        if query is None:
            return 'Sorry, I did not get your question.'
        else:
            url = '%s?input=%s&podstate%s&output=%s&appid=%s' % (API_URL, urllib.parse.quote(
                query), 'Result__Step-by-step+solution', 'xml', key)

            r = urllib.request.urlopen(url)
            result = xmltodict.parse(r, dict_constructor=dict)['queryresult']
            return result


class Expression(object):
    def __init__(self, query, results):
        """
        Initializes the Expression class with a results from Wolfram Alpha API.

        Request a query.
        Request a JSON results.

        :param results: Results of query from Wolfram Alpha App
        :param results: Results of query from Wolfram Alpha App

        """

        self.query = query
        self.execution_time = None
        self.plots = []
        self.alternate_forms = []
        self.solutions = []
        #self.steps = []

        self.execution_time = results['@timing']

        for pod in results['pod']:
            print(pod['@id'])
            if pod['@id'].find("Plot") >= 0:
                if isinstance(pod['subpod'], list):
                    for subpod in pod['subpod']:
                        src_plot = subpod['img']['@src']
                        self.plots.append(
                            base64.b64encode(
                                requests.get(src_plot).content))
                else:
                    src_plot = pod['subpod']['img']['@src']
                    self.plots.append(
                        base64.b64encode(
                            requests.get(src_plot).content))

            if pod['@id'].find("AlternateForm") >= 0:
                if isinstance(pod['subpod'], list):
                    for subpod in pod['subpod']:
                        self.alternate_forms.append(subpod['plaintext'])
                else:
                    self.alternate_forms.append(pod['subpod']['plaintext'])

            if pod['@id'].find("Solution") >= 0:
                if isinstance(pod['subpod'], list):
                    for subpod in pod['subpod']:
                        self.solutions.append(subpod['plaintext'])
                else:
                    self.solutions.append(pod['subpod']['plaintext'])

    def print_expression(self):
        """
        Print content of the expression.

        """
        print("\nExpression info")
        print("Query: ", self.query)
        print("Execution time: ", self.execution_time)
        print("Plots (base64): ", len(self.plots))
        print("Alternate forms: ", self.alternate_forms)
        print("Solutions: ", self.solutions)


if __name__ == "__main__":
    '''
    Query examples:
        int e^x^2 dx
        x^3 + x^2 y + x y^2 + y^3
        (x^2-1)/(x^2+1)
        cos(arcsin(x)/2)
        
    '''
    query = 'cos(arcsin(x)/2)'

    api = waAPI(KEY)
    results = api.full_results(query=query)

    # filehandler = open("pick","wb")
    # pickle.dump(results,filehandler)
    # filehandler.close()

    # file = open("pick",'rb')
    # results = pickle.load(file)
    # file.close()

    obj = Expression(query, results)
    obj.print_expression()
