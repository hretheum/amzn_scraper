from flask import Blueprint, render_template

query_bp = Blueprint('query_endpoints', __name__, url_prefix='/q')

from www.project.query import routes