import base64
import os.path
import urllib.parse
import urllib.request
from io import BytesIO
from flask import Markup
import logging
import requests
from PIL import Image
import json


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

API_URL = "https://api.wolframalpha.com/v2/query"
API_SIGNUP_PAGE = "https://developer.wolframalpha.com"
KEY = "V2WJ46-EEXEV95WXG"


def raw(text):
    """
    Returns a raw string representation of text
    """
    escape_dict = {
        "\a": "\\a",
        "\b": "\\b",
        "\f": "\\f",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\v": "\\v",
    }
    for k, v in escape_dict.items():
        text = text.replace(k, v)

    return text


def to_mathml(text_mml):
    """
    Return the correct mathml visualization of the expression returned from wolfram|alpha
    """
    symbols_dict = {"integral": "&int;"}

    for k, v in symbols_dict.items():
        text_mml = text_mml.replace(k, v)

    return text_mml


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
        self.response_format = "json"

        if self.key is None:
            raise NoAPIKeyException(
                "Warning: Missing API Key. Please visit "
                + API_SIGNUP_PAGE
                + " to register for a key."
            )

    def full_results(
        self, response_format=None, key=None, query=None, pods_format="mathml"
    ):
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
            return "Sorry, I did not get your question."
        else:
            query = raw(query)
            url = (
                "%s?input=%s&podstate%s&output=%s&appid=%s&format=%s,image"
                % (
                    API_URL,
                    urllib.parse.quote(query),
                    "Result__Step-by-step+solution",
                    self.response_format,
                    key,
                    pods_format,
                )
            )

            r = requests.get(url)
            r = r.json()
            return r["queryresult"]


class ExpressionException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Expression(object):
    def __init__(
        self,
        query,
        results,
        id_equation=None,
        dir_plots=None,
        pods_format="mathml",
        output_result="default",
    ):
        """
        Initializes the Expression class with a results from Wolfram Alpha API.

        Arguments:
            query (str): expression query
            results (dict): results of query from Wolfram Alpha API
            dir_plots (str, optional): dir where to save plots
            id_equation (int, optional): identifier of expression
            pods_format (str, optional): pod format. It can be mathml or plaintext
            output_results (str, optional): Output default result or full results. It can be default or full
        """

        if query is None:
            raise ExpressionException("Sorry, there is no expression query")
        if dir_plots is None:
            dir_plots = "plot_images"
        if results is None:
            raise ExpressionException(
                "Sorry, there are no results to examinate"
            )

        self.query = query
        self.success = results["success"]
        self.execution_time = results["timing"]
        self.plots = []
        self.alternate_forms = []
        self.solutions = []
        self.symbolic_solutions = []
        self.results = []
        self.limits = []
        self.partial_derivatives = []
        self.integral = []

        if self.success:
            if output_result == "default":
                for pod in results["pods"]:
                    try:
                        # print(pod['id'])
                        if "Plot" in pod["id"] or "Parallelogram" in pod["id"]:
                            if isinstance(pod["subpods"], list):
                                for subpod in pod["subpods"]:
                                    src_plot = subpod["img"]["src"]
                                    self.plots.append(
                                        base64.b64encode(
                                            requests.get(src_plot).content
                                        ).decode("utf-8")
                                    )
                            else:
                                src_plot = pod["subpods"]["img"]["src"]
                                self.plots.append(
                                    base64.b64encode(
                                        requests.get(src_plot).content
                                    ).decode("utf-8")
                                )

                        if "AlternateForm" in pod["id"]:
                            self.alternate_forms.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if (
                            "Solution" in pod["id"]
                            and "SolutionForTheVariable" not in pod["id"]
                            and "SymbolicSolution" not in pod["id"]
                        ):
                            self.solutions.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if "SymbolicSolution" in pod["id"]:
                            self.symbolic_solutions.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if "Result" in pod["id"]:
                            self.results.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if "Limit" in pod["id"]:
                            self.limits.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if "Derivative" in pod["id"]:
                            self.partial_derivatives.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )
                        if "Integral" in pod["id"]:
                            self.integral.extend(
                                self.extract_mathml(pod=pod)
                                if pods_format == "mathml"
                                else self.extract_plaintext(pod=pod)
                            )

                    except BaseException:
                        print("Error in extraction:", pod["id"])
            elif output_result == "full":
                self.compute_full_result(results)

        if id_equation is not None:
            self.save_plots(id_equation, dir_plots)

    def compute_full_result(self, results, output="plaintext"):
        for pod in results["pods"]:
            subpods = []
            if isinstance(pod["subpods"], list):
                for subpod in pod["subpods"]:
                    if subpod["title"] != "":
                        subpods.append({subpod["title"]: subpod[output]})
                    else:
                        subpods.append(subpod[output])
            else:
                if pod["subpods"]["title"] != "":
                    subpods.append({pod["subpods"]["title"]: subpod[output]})
                else:
                    subpods.append(pod["subpods"][output])
            if pod["id"] != "Plot":
                setattr(self, "" + pod["id"] + "", subpods)

    def extract_plaintext(self, pod):
        """
        Extract plaintext field from subpods
        """
        plaint_text = []
        if isinstance(pod["subpods"], list):
            for subpod in pod["subpods"]:
                plaint_text.append(subpod["plaintext"])
        else:
            plaint_text.append(pod["subpods"]["plaintext"])
        return plaint_text

    def extract_mathml(self, pod):
        """
        Extract mathml field from subpods
        """
        mathml = []
        if isinstance(pod["subpods"], list):
            for subpod in pod["subpods"]:
                ml = subpod["mathml"]
                ml = ml.replace("\n", "")
                ml = to_mathml(ml)
                ml = Markup(ml)
                mathml.append(ml)
        else:
            ml = pod["subpods"]["mathml"]
            ml = ml.replace("\n", "")
            ml = to_mathml(ml)
            ml = Markup(ml)
            mathml.append(ml)
        return mathml

    def save_plots(self, id_equation, dir_plots):
        """
        Save image plots in dir_plots
        """
        for i in range(len(self.plots)):
            filename_img = str(id_equation) + "_" + str(i) + ".png"
            path_img = os.path.join(dir_plots, filename_img)

            img_base64 = bytes(self.plots[i], "utf-8")
            im = Image.open(BytesIO(base64.b64decode(img_base64)))
            im.save(path_img, "PNG")

            self.plots[i] = path_img

    def print_expression(self):
        """
        Print content of the expression.
        """
        logging.info("\nExpression information")
        logging.info("Success: {}".format(self.success))
        logging.info("Query: {}".format(raw(self.query)))
        logging.info("Execution time: {}".format(self.execution_time))
        logging.info("Plots: {}".format(self.plots))
        logging.info("Alternate forms: {}".format(self.alternate_forms))
        logging.info("Results: {}".format(self.results))
        logging.info("Solutions: {}".format(self.solutions))
        logging.info("Symbolic Solutions: {}".format(self.symbolic_solutions))
        logging.info("Limit: {}".format(self.limits))
        logging.info(
            "Partial derivatives: {}".format(self.partial_derivatives)
        )
        logging.info("Integral: {}".format(self.integral))

    def to_json(self):
        """
        Convert expression object to json
        """
        expression = {}
        expression['success'] = self.success
        expression['query'] = self.query
        expression['execution_time'] = self.execution_time
        expression['plots'] = json.dumps(self.plots)
        expression['alternate_forms'] = json.dumps(self.alternate_forms)
        expression['results'] = json.dumps(self.results)
        expression['solutions'] = json.dumps(self.solutions)
        expression['symbolic_solutions'] = json.dumps(self.symbolic_solutions)
        expression['limits'] = json.dumps(self.limits)
        expression['partial_derivatives'] = json.dumps(self.partial_derivatives)
        expression['integral'] = json.dumps(self.integral)

        return json.dumps(expression)



def compute_expression(
    query,
    key=KEY,
    id_equation=None,
    dir_plots=None,
    response_format=None,
    pods_format="mathml",
    output_result="default",
):
    """
    Returns an Expression object containing the query results

    Arguments:

    query (str): expression query
    key (str, optional): key to use Wolfram Alpha API
    id_equation (int, optional): identifier to rename plot images
    dir_plots (str, optional): directory where to save plot images
    pods_format (str, optional): output for results: mathml or plaintext

    Expression examples:
        x^3 - y^2 = 23
        x^3 + x^2 y + x y^2 + y^3
        3x^3 + 2x^2 - 4ax +2 = 0
        \frac{x^2-1}{x^2+1}
        \cos{\frac{\arcsin{x}}{2}}
        2x+17y=23,x-y=5,\int_{0}^{x} x dx
        \int x^2 dx
    """
    client_api = waAPI(key)
    query = "\left( " + query + "\right)"
    results_json = client_api.full_results(
        response_format=response_format, query=query, pods_format=pods_format
    )
    obj_expression = Expression(
        query=query,
        results=results_json,
        id_equation=id_equation,
        dir_plots=dir_plots,
        pods_format=pods_format,
        output_result=output_result,
    )
    return obj_expression
