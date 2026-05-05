"""RESTful API for reading, updating, adding and deleting blog posts."""
import copy

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)  # This will enable CORS for all routes

INITIAL_POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

posts = copy.deepcopy(INITIAL_POSTS)

REQUIRED_POST_FIELDS = ["title", "content"]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Get all posts in the blog.

    Returns:
        JSON object with all posts.
    """
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """
    Get the post with a given ID.

    Returns:
        JSON object and a status code. The blog post with status code 200
        in case of success, error message with status code 404 if the post
        with a given ID was not found.
    """
    for post in posts:
        if post["id"] == post_id:
            return jsonify(post), 200
    return jsonify({"error": f"Post with id {post_id} does not exist."}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts by query string. A post matches if any provided field contains
    the corresponding value (case-insensitive substring match).

    Returns:
        JSON object with all posts matching the query.
    """
    search_query = request.args
    query_keys = [key for key in REQUIRED_POST_FIELDS if search_query.get(key)]
    filtered_posts = posts[:]
    if query_keys:
        filtered_posts = [post for post in posts if
                          any(search_query[key].lower() in post[key].lower()
                              for key in query_keys)]
    return jsonify(filtered_posts)


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
    """
    Add a new blog post.

    Request Body (JSON):
        title (str): Title of the new post.
        content (str): Content of the new post.

    Returns:
        JSON object and a status code. The new blog post with status code
        201 in case of success, error message with status code 400 in case
        of failure.
    """
    data = request.get_json(silent=True) or {}

    missing_fields = []
    for field in REQUIRED_POST_FIELDS:
        if not data.get(field):
            missing_fields.append(field)

    if missing_fields:
        return jsonify({"error": f"Missing field(s): {', '.join(missing_fields)}"}), 400

    new_post = {"id": get_next_id(posts)}
    for field in REQUIRED_POST_FIELDS:
        new_post[field] = data[field]

    posts.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Delete the post with a given ID.

    Args:
        post_id: ID of the post to delete.

    Returns:
        JSON object and a status code. Success message with a status code
        200 or error message with a status code 404 if the post with a given
        ID was not found.
    """
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            return jsonify({"message": f"Post with id {post_id} has been deleted "
                                       f"successfully."}), 200
    return jsonify({"error": f"Post with id {post_id} does not exist."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Update the post with a given ID.

    Request Body (JSON):
        title (str): New title of the post.
        content (str): New content of the post.

    Returns:
        JSON object and a status code. The updated blog post with status
        code 200 in case of success, error message with status code 404
        if the post with a given ID was not found.
    """
    data = request.get_json(silent=True) or {}

    for post in posts:
        if post["id"] == post_id:
            for field in REQUIRED_POST_FIELDS:
                if data.get(field):
                    post[field] = data[field]
            return jsonify(post), 200
    return jsonify({"error": f"Post with id {post_id} does not exist."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
