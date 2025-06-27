"""
MasterBlog API - Backend Application

This module initializes a Flask app with a simple in-memory
blog post API supporting GET and POST requests.
"""

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory mock database for blog posts
POSTS = [
    {"id": 1, "title": "First Post", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Handle GET requests to fetch all blog posts.

    Returns:
        JSON list of all posts.
    """
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """
    Handle POST requests to add a new blog post.

    Expects JSON with 'title' and 'content' fields.

    Returns:
        The created post as JSON with status 201.
        If missing fields, returns 400 with error message.
    """
    data = request.get_json()

    # Check if JSON body exists and has required fields
    missing_fields = []
    if not data:
        missing_fields = ['title', 'content']
    else:
        if 'title' not in data:
            missing_fields.append('title')
        if 'content' not in data:
            missing_fields.append('content')

    if missing_fields:
        return (
            jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}),
            400,
        )

    # Generate new ID by incrementing the max existing ID
    new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content'],
    }
    POSTS.append(new_post)

    return jsonify(new_post), 201


if __name__ == '__main__':
    # Run the Flask app on port 5002 for development
    app.run(host="0.0.0.0", port=5002, debug=True)
