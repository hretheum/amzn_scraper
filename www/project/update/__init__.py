from flask import Blueprint, render_template

update_bp = Blueprint('update', __name__)

from www.project.update import routes