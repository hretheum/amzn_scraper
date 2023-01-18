
from flask import request, jsonify
from www.project.models import Query, Offer, UserQueries, q2o
from www.project.update import update_bp
from www.project import db, login_required


@update_bp.route('/update', methods=['POST'])
@login_required
def update_price():
    field_name = request.form['field_name']
    field_value = request.form['field_value']
    offer_id = request.form['offer_id']

    offer = db.session.query(Offer)\
        .filter(Offer.id == offer_id)\
        .first()

    if offer:
        setattr(offer, field_name, field_value)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})


