from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

REQUIRED_POST_FIELDS = ["title", "content"]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


def get_next_id(blog_posts: list[dict]) -> int:
    """
    Generate a new ID for the next blog post (maximum existing ID + 1).

    Args:
        blog_posts: List with blog posts.

    Returns:
        ID for the next blog post.
    """
    ids = [blog_post['id'] for blog_post in blog_posts]
    return max(ids, default=0) + 1


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()

    missing_fields = []
    for field in REQUIRED_POST_FIELDS:
        if not data.get(field):
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400

    new_post = {"id": get_next_id(POSTS)}
    for field in REQUIRED_POST_FIELDS:
        new_post[field] = data[field]

    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
