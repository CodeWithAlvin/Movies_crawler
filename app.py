from flask import Flask, request, render_template
from crawler import Hdhub4u # custom scraper class

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])  
def index():
    if request.method == "POST":
        query = request.form["query"]
        try:
        	hd = Hdhub4u()
        	search = hd.search(query)
        	movies = hd.movies
        except Exception as e:
        	print(e)
        	movies = {f"Nothing Matching  : {query}":"#"}

        return render_template("results.html", movies=movies)

    return render_template("index.html")

if __name__ == "__main__":
   app.run()