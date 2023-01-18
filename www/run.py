from project import create_app, db

app = create_app()

@app.cli.command()
def create_db():
    db.create_all()