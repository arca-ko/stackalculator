import connexion

app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yml")


@app.route("/")
def index():
        return "Home Page"

if __name__ == "__main__":
        app.run()
