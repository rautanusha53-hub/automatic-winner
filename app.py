
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from flask import Flask, request, Response

app = Flask(__name__)

UPSTREAM_API = "https://api-info-tz3o.vercel.app/api/player"
API_KEY = "HNTH"


@app.route("/api/player", methods=["GET"])
def player():
    uid = request.args.get("uid", "").strip()

    if not uid or not uid.isdigit():
        return Response(
            json.dumps({"error": "A valid numeric UID is required"}),
            status=400,
            mimetype="application/json"
        )

    params = urlencode({"uid": uid, "key": API_KEY})
    req = Request(
        f"{UPSTREAM_API}?{params}",
        headers={"Accept": "application/json"},
        method="GET"
    )

    try:
        with urlopen(req, timeout=15) as upstream:
            body = upstream.read()
            content_type = upstream.headers.get(
                "Content-Type", "application/json"
            )
            return Response(
                body,
                status=upstream.status,
                content_type=content_type
            )

    except HTTPError as exc:
        body = exc.read()
        return Response(
            body,
            status=exc.code,
            content_type=exc.headers.get(
                "Content-Type", "application/json"
            )
        )

    except (URLError, TimeoutError):
        return Response(
            json.dumps({"error": "Unable to connect to the player API"}),
            status=502,
            mimetype="application/json"
        )
