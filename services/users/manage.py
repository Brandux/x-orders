# services/users/manage.py

import unittest

import coverage # new

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()


from flask.cli import FlaskGroup

from project import create_app, db # new
from project.api.models import User # new

app = create_app() # new
cli = FlaskGroup(create_app=create_app) # new

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Ejecutar los tests sin covertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

# nueva era
@cli.command('seed_db')
def seed_db():
    """Sembrado en la base de datos"""
    db.session.add(User(username='Brandux JUarez', email= 'branduxjuarez@upeu.edu.pe', password='greaterthaneight'))
    db.session.add(User(username='Didier', email= 'didi@upeu.edu.pe', password='greaterthaneight'))
    db.session.commit()

# nuevo -> de covertura
@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con coverage"""
    tests   = unittest.TestLoader().discover('project/tests')
    result  = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de cobertura')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()
