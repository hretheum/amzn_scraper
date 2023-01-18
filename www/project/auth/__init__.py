from flask import Blueprint, render_template

auth_bp = Blueprint('auth_endpoints', __name__, url_prefix='/auth')

from www.project.auth import routes