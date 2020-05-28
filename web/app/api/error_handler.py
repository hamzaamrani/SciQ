import logging

from flask import jsonify, render_template, request
from user_agents import parse

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def reached_limit_requests(error):
    _ = request.stream.read()
    user_agent = parse(request.headers.get("User-Agent"))
    if user_agent.is_pc and "api" not in request.full_path:
        logging.info("handler limit request")
        return (
            render_template(
                "math.html",
                alert=True,
                error="Limit reached for a not logged user",
            ),
            429,
        )
    else:
        return jsonify({"error": "limit request"}), 429
