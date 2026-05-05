"""Frontend application for reading, updating, adding and deleting blog posts."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Render the blog homepage.

    Returns:
        Rendered index.html template.
    """
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
