from flask import Blueprint, render_template, request, jsonify

from app.models import Goods

# Initialize a Blueprint for form-related routes
form_bp = Blueprint('form_bp', __name__)


@form_bp.route('/form', methods=['GET', 'POST'])
def form():
    """
    Route to display a form and handle its submission.
    On GET request: Renders a form for the user to fill out.
    On POST request: Processes the submitted form data.

    :return: On GET request, renders the 'form.html'. On POST request, can perform data processing and then may render a template or redirect.
    """
    if request.method == 'POST':
        # Example of handling the form data
        print(request.form)  # Printing form data to the console for demonstration
        # Here you can add your logic to process form data (e.g., saving to database, sending an email, etc.)
    return render_template('form.html')  # Render the form template on both GET and POST requests


@form_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    """
    Route to handle autocomplete suggestions.
    Fetches goods names from the database that match the user's search query and returns them in a JSON format suitable for autocomplete functionalities.

    :return: A JSON response containing matching results, each with an "id" and "name" derived from goods names in the database.
    """
    search = request.args.get('q')  # Get the search query parameter 'q' from the URL
    results = Goods.query.filter(Goods.good_name.like(f'%{search}%')).limit(
        10).all()  # Query the database for goods names that contain the search term
    # Prepare and return the JSON response with the search results
    return jsonify(matching_results=[{"id": item.good_name, "name": item.good_name} for item in results])
