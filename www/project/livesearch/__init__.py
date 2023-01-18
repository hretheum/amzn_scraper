from flask import Blueprint, render_template

livesearch_bp = Blueprint('livesearch', __name__)

from www.project.livesearch import routes