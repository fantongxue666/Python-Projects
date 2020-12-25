def newRoute(app):
    @app.route("/test")
    def test():
        return 'test test'