from flask import Flask, render_template_string, request
import logging

logging.basicConfig(filename="/var/log/app/app.log", level=logging.INFO)
app = Flask(__name__, static_folder="./", static_url_path="/")

with open("index.html", "r") as f:
    index_html = f.read()


@app.get("/")
def index():
    q = request.args.get("q")
    
    if not q:
        template = index_html.replace("$CONTEXT", "''")
        return render_template_string(template)
    else:
        template = index_html.replace("$CONTEXT", q)
        return render_template_string(template)
