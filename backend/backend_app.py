"""
MasterBlog API - Backend Application

This module provides endpoints to list, update, delete, search, and sort blog posts.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

# Create the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing for all routes
CORS(app)

# In-memory mock database for blog posts
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Alpha post", "content": "This is an alpha post."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Handle GET requests to fetch and optionally sort blog posts.

    Query Parameters:
        sort (str, optional): Field to sort by ('title' or 'content').
        direction (str, optional): 'asc' or 'desc' (default is ascending).

    Returns:
        JSON list of posts, sorted if parameters are valid.
    """
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc')

    # Validate sort field if provided
    if sort_field and sort_field not in ['title', 'content']:
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    # Validate direction if provided
    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    result_posts = POSTS.copy()

    # Apply sorting if sort field is specified
    if sort_field:
        reverse = direction == 'desc'
        result_posts.sort(key=lambda post: post[sort_field].lower(), reverse=reverse)

    return jsonify(result_posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Handle DELETE request to delete a post by its ID.
    """
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"message": f"Post with id {post_id} not found."}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Handle PUT request to update a blog post.
    """
    data = request.get_json()
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        return jsonify({"message": f"Post with id {post_id} not found."}), 404

    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Handle GET request to search blog posts by title or content.
    """
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    results = [
        post for post in POSTS
        if (title_query in post["title"].lower() or content_query in post["content"].lower())
    ]

    return jsonify(results)


if __name__ == '__main__':
    # Run the Flask app on port 5002 for development
    app.run(host="0.0.0.0", port=5002, debug=True)
