from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vuln_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    published_date = db.Column(db.String(20), nullable=False)
    source_link = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Vulnerability {self.title}>"
