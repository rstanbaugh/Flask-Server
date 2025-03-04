from flask import Blueprint, render_template, jsonify, url_for
from sensors.tempest import get_weather  # Import correct function


routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
def index():
    return render_template("first_template.html")

@routes_bp.route("/about")
def about():
    return render_template("profile.html", name="About Us")

@routes_bp.route("/api/weather")
def api_weather():
    """API endpoint to fetch and return weather data."""
    weather_data = get_weather()
    return jsonify(weather_data)

@routes_bp.route("/weather")
def weather_page():
    """Render the weather page with live data."""
    weather_data = get_weather()  # Get latest weather data
    if not weather_data:
        weather_data = {"error": "No weather data available"}  # Fallback message
    return render_template("weather.html", weather=weather_data)


@routes_bp.route("/profile/<username>")
def show_profile(username):
    return render_template("profile.html", name=username)

@routes_bp.route("/product/<name>")
def product(name):
    return f"<h3>Product: {name}</h3>"

@routes_bp.route("/courses/<int:course_id>")
def course_detail(course_id):
    """Displays details for a specific course."""
    courses = {
        1: {"title": "AI Coding", "description": "Learn AI programming.", "image_url": "https://cdn.pixabay.com/photo/2019/04/10/08/37/artificial-intelligence-4116432_1280.jpg"},
        2: {"title": "Machine Learning for Everyone", "description": "Understand machine learning concepts.", "image_url": "https://cdn.pixabay.com/photo/2018/05/08/08/44/artificial-intelligence-3382507_1280.jpg"},
        3: {"title": "Wall Street Coder", "description": "Master financial coding.", "image_url": "https://cdn.pixabay.com/photo/2015/12/04/14/05/code-1076536_1280.jpg"}
    }
    
    course = courses.get(course_id)
    if not course:
        return "Course not found", 404

    return render_template("course_detail.html", course=course)
  
@routes_bp.route("/api/courses")
def api_courses():
    """ Returns the courses with static image URLs """
    courses_with_urls = [
        {
            "id": 1,
            "title": "AI Coding",
            "image_url": url_for("static", filename="images/image-1.jpeg", _external=True)
        },
        {
            "id": 2,
            "title": "Machine Learning for Everyone",
            "image_url": url_for("static", filename="images/image-ai.jpeg", _external=True)
        },
        {
            "id": 3,
            "title": "Wall Street Coder",
            "image_url": url_for("static", filename="images/image-code.jpeg", _external=True)
        }
    ]
    return jsonify({"courses": courses_with_urls, "status": "success"})

@routes_bp.route("/courses")
def courses():
    """ Renders courses using images from Pixabay CDN """
    courses_with_cdn_urls = [
        {
            "id": 1,
            "title": "AI Coding",
            "image_url": "https://cdn.pixabay.com/photo/2019/04/10/08/37/artificial-intelligence-4116432_1280.jpg"
        },
        {
            "id": 2,
            "title": "Machine Learning for Everyone",
            "image_url": "https://cdn.pixabay.com/photo/2018/05/08/08/44/artificial-intelligence-3382507_1280.jpg"
        },
        {
            "id": 3,
            "title": "Wall Street Coder",
            "image_url": "https://cdn.pixabay.com/photo/2015/12/04/14/05/code-1076536_1280.jpg"
        }
    ]
        
    return render_template("all_courses.html", courses=courses_with_cdn_urls)
