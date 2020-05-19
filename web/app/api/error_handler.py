from flask import request, render_template, jsonify
from user_agents import parse
import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def reached_limit_requests(error):
    _ = request.stream.read()
    user_agent = parse(request.headers.get("User-Agent"))
    logging.info(request.full_path)
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