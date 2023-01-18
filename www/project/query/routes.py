from flask import render_template, redirect
from www.project.models import Query, Offer, q2o
from www.project.query import query_bp
from www.project import db


@query_bp.route('/<int:query>')
def query(query):

    offers = find_item_by_query(query, True)
    print(f":::: gdzie te oferty: {offers}")
    context = {'offers': offers, 'query': query, 'hidden': False}
    return render_template('tab-visible.html', **context )

@query_bp.route('/<int:query>/hidden')
def query_hidden(query):
    context = {'offers': find_item_by_query(query, False), 'query': query, 'hidden': True}
    return render_template('tab-hidden.html', **context)


@query_bp.route('/<int:query>/record/<int:record_id>/hide')
def hide_record(query, record_id):
    record = db.session.query(q2o) \
        .filter(
        q2o.columns.offerID == record_id,
        q2o.columns.queryID == query
    ).update({q2o.columns.visible: not db.session.query(q2o.columns.visible).filter(
        q2o.columns.offerID == record_id,
        q2o.columns.queryID == query
    ).scalar()})
    db.session.commit()

    return redirect(f'/q/{query}')

@query_bp.route('/<int:query>/record/<int:record_id>/show')
def show_record(query, record_id):
    record = db.session.query(q2o) \
        .filter(
        q2o.columns.offerID == record_id,
        q2o.columns.queryID == query
    ).update({q2o.columns.visible: not db.session.query(q2o.columns.visible).filter(
        q2o.columns.offerID == record_id,
        q2o.columns.queryID == query
    ).scalar()})
    db.session.commit()

    return redirect(f'/q/{query}/hidden')


def find_item_by_query(query: int, visible: bool):
    return db.session.query(Offer)\
        .join(q2o, Offer.id == q2o.c.offerID)\
        .join(Query, Query.id == q2o.c.queryID)\
        .filter(Query.id == query, q2o.c.visible == visible) \
        .all()

def find_item_by_id(record_id: int):
    return db.session.query(Offer)\
        .select_from(Offer)\
        .filter(Offer.id == record_id)\
        .all()



def lorem(offers, query):
    for offer in offers:
        offer.category = []
        results = db.session.query(q2o).filter(q2o.offerID == offer.id,
                                                                   q2o.queryID == query).all()
        # results = db.session.execute("SELECT * FROM query2offer WHERE queryID = :query AND offerID = :offer",
        #                              {"query": query, "offer": offer.id, }).fetchall()
        for result in results:
            if result.category:
                offer.category.append(result.category)

    return offers

