from datetime import datetime

from flask import render_template, request, redirect, url_for, flash, session
from www.project.main import main
from www.project.models import Query, UserQueries, User
from www.project import db
from www.project import login_required

@main.route('/')
@main.route("/addquery/<string:new_query>")
@login_required
def index(new_query=None):
    query = db.session.query(Query).all()
    context = {'queries': query}

    if new_query:
        query = Query(query=new_query, timestamp=datetime.now().strftime("%d-%m-%Y"))
        db.session.add(query)
        db.session.commit()

        author = db.session.query(User).filter(User.public_id == session.get('public_id')).first()
        print(f'::::::::::::: queryID: {query.id}, authorID: {author.id}')
        userquery = UserQueries(userID=author.id, queryID=query.id)
        db.session.add(userquery)
        db.session.commit()

        flash(f"nowe zapytanie — [{new_query}] — dodane do bazy")
        return redirect(url_for('main.index'))

    return render_template('queries.html', **context)