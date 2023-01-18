from flask import request, jsonify
from www.project.livesearch import livesearch_bp
from www.project.models import Query
from www.project import db
from www.project import login_required


@livesearch_bp.route("/livesearch",methods=["POST","GET"])
@login_required
def livesearch():
    searchbox = request.form.get("text")
    query = (
        Query.query.like("%" + searchbox + "%")
    )
    result = db.session.query(Query).filter(query).all()

    dict = []

    for query in result:
        dict.append({'id': query.id, 'query': query.query})
    return jsonify(dict)