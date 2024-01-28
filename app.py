from website import create_app
from website.views import home

if __name__ == "__main__" :
    app = create_app()
    app.add_url_rule('/', view_func=home)
    app.run(debug=True)
