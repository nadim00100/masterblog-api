"""
MasterBlog API - Backend Application

This module provides endpoints to list, update, delete, and search blog posts.
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
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Handle GET requests to fetch all blog posts.
    """
    return jsonify(POSTS)


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

    Query Parameters:
        title (str, optional): Search term for post title.
        content (str, optional): Search term for post content.

    Returns:
        List of posts that match the search terms.
    """
    title_query = request.args.get("title", "").lower()
    content_query = request.args.get("content", "").lower()

    # Filter posts based on title/content match (case-insensitive)
    results = [
        post for post in POSTS
        if (title_query in post["title"].lower() or content_query in post["content"].lower())
    ]

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
