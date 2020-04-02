# autopep8 --in-place --aggressive --aggressive waAPI.py
# Wolfram|Alpha Show Steps API Reference:
# https://products.wolframalpha.com/show-steps-api/documentation/
# test con pytest

import requests
import urllib.parse
import urllib.request
import json
import base64
import pickle
import os.path
from PIL import Image
from io import BytesIO
import unittest


API_URL = 'https://api.wolframalpha.com/v2/query'
API_SIGNUP_PAGE = 'https://developer.wolframalpha.com'
KEY = 'V2WJ46-EEXEV95WXG'


def raw(text):
    """
    Returns a raw string representation of text
    """
    escape_dict = {'\a': '\\a',
                   '\b': '\\b',
                   '\f': '\\f',
                   '\n': '\\n',
                   '\r': '\\r',
                   '\t': '\\t',
                   '\v': '\\v'}
    for k, v in escape_dict.items():
        text = text.replace(k, v)

    return text


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
                                Defaults to '.xml'.

        :param key: a developer key. Defaults to key given when the waAPI class was initialized.

        """
        if key is None:
            key = self.key
        if response_format is None:
            response_format = self.response_format
        if query is None:
            return 'Sorry, I did not get your question.'
        else:
            query = raw(query)
            url = '%s?input=%s&podstate%s&output=%s&appid=%s&format=mathml,image' % (API_URL, urllib.parse.quote(
                query), 'Result__Step-by-step+solution', self.response_format, key)
            
            #r = urllib.request.urlopen(url)
            #result = xmltodict.parse(r, dict_constructor=dict)['queryresult']
            #return result

            r = requests.get(url)
            r = r.json()
            return r['queryresult']


class Expression(object):
    def __init__(
            self,
            query,
            results,
            id_equation=None,
            dir_plots='plot_images'):
        """
        Initializes the Expression class with a results from Wolfram Alpha API.

        Request a query.
        Request a JSON results.

        :param query: expression query
        :param results: results of query from Wolfram Alpha App
        :param dir_plots: rir where to save plots
        :param id_equation: identifier of expression
        """

        self.query = query
        self.success = results['success']
        self.execution_time = results['timing']
        self.plots = []
        self.alternate_forms = []
        self.solutions = []
        self.symbolic_solutions = []
        self.results = []
        self.limits = []
        self.partial_derivatives = []
        self.integral = []


        if self.success == True:
            for pod in results['pods']:
                try:
                    # print(pod['id'])
                    if 'Plot' in pod['id']:
                        if isinstance(pod['subpods'], list):
                            for subpod in pod['subpods']:
                                src_plot = subpod['img']['src']
                                self.plots.append(
                                    base64.b64encode(
                                        requests.get(src_plot).content))
                        else:
                            src_plot = pod['subpods']['img']['src']
                            self.plots.append(
                                    base64.b64encode(
                                        requests.get(src_plot).content))

                    if 'AlternateForm' in pod['id']:
                        self.alternate_forms.extend(self.extract_mathml(pod=pod))
                    if 'Solution' in pod['id'] and not 'SolutionForTheVariable' in pod['id'] and not 'SymbolicSolution' in pod['id']:
                        self.solutions.extend(self.extract_mathml(pod=pod))
                    if 'SymbolicSolution' in pod['id']:
                        self.symbolic_solutions.extend(self.extract_mathml(pod=pod))
                    if 'Result' in pod['id']:
                        self.results.extend(self.extract_mathml(pod=pod))
                    if 'Limit' in pod['id']:
                        self.limits.extend(self.extract_mathml(pod=pod))
                    if 'Derivative' in pod['id']:
                        self.partial_derivatives.extend(self.extract_mathml(pod=pod))
                    if 'Integral' in pod['id']:
                        self.integral.extend(self.extract_mathml(pod=pod))

                except BaseException:
                    print("Error in extraction:", pod['id'])

        if id_equation is not None:
            self.save_plots(id_equation, dir_plots)

    def extract_plaintext(self, pod):
        """
        Extract plaintext field from subpods
        """
        plaint_text = []
        if isinstance(pod['subpod'], list):
            for subpod in pod['subpod']:
                plaint_text.append(subpod['plaintext'])
        else:
            plaint_text.append(pod['subpod']['plaintext'])
        return plaint_text

    def extract_mathml(self, pod):
        """
        Extract mathml field from subpods
        """
        mathml = []
        if isinstance(pod['subpods'], list):
            for subpod in pod['subpods']:
                ml = subpod['mathml']
                ml = ml.replace("\n","")
                mathml.append(ml)
        else:
            ml = pod['subpods']['mathml']
            ml = ml.replace("\n","")
            mathml.append(ml)
        return mathml

    def save_plots(self, id_equation, dir_plots):
        """
        Save image plots in dir_plots
        """
        for i in range(len(self.plots)):
            filename_img = str(id_equation) + '_' + str(i) + '.png'
            path_img = os.path.join(dir_plots, filename_img)

            im = Image.open(BytesIO(base64.b64decode(self.plots[i])))
            im.save(path_img, 'PNG')

            self.plots[i] = path_img

    def print_expression(self):
        """
        Print content of the expression.
        """
        print("\nExpression information")
        print("Success: ", self.success)
        print("Query: ", raw(self.query))
        print("Execution time: ", self.execution_time)
        print("Plots: ", self.plots)
        print("Alternate forms: ", self.alternate_forms)
        print("Results: ", self.results)
        print("Solutions: ", self.solutions)
        print("Symbolic Solutions: ", self.symbolic_solutions)
        print("Limit: ", self.limits)
        print("Partial derivatives: ", self.partial_derivatives)
        print("Integral: ", self.integral)

class TestStringMethods(unittest.TestCase): 
      
    def setUp(self): 
        pass
  


if __name__ == "__main__":
    """
    Expression examples:
        x^3 - y^2 = 23
        x^3 + x^2 y + x y^2 + y^3
        3x^3 + 2x^2 - 4ax +2 = 0
        \frac{x^2-1}{x^2+1}
        \cos{\frac{\arcsin{x}}{2}}
        2x+17y=23,x-y=5,\int_{0}^{x} x dx
        \int x^2 dx
    """
    query = '2x+17y=23,x-y=5,\int_{0}^{x} x dx'
    api = waAPI(KEY)
    results = api.full_results(query=query)

    # filehandler = open("pick","wb")
    # pickle.dump(results,filehandler)
    # filehandler.close()

    # file = open("pick",'rb')
    # results = pickle.load(file)
    # file.close()

    id_equation = '001'
    obj = Expression(query=query, results=results, id_equation=id_equation)
    obj.print_expression()