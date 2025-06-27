"""
MasterBlog API - Backend Application

This module initializes a Flask app with a simple API
that returns a list of blog posts and supports deleting posts by ID.
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

    Returns:
        JSON list of all posts.
    """
    return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Handle DELETE request to delete a post by its ID.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        JSON message confirming deletion or error message if not found.
    """
    # Find the post by ID
    post = next((p for p in POSTS if p["id"] == post_id), None)

    if post is None:
        # Post not found: return 404 error
        return jsonify({"message": f"Post with id {post_id} not found."}), 404

    # Remove the post from the list
    POSTS.remove(post)

    # Return success message
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


if __name__ == '__main__':
    # Run the Flask app on port 5002 for development
    app.run(host="0.0.0.0", port=5002, debug=True)
