# coding: utf-8
"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    # Remember, the arguments for a GET request are a set of key/value pairs that
    # the user can send to the web server via the URL. An example URL with GET
    # request arguments would look like this:
    # http://127.0.0.1:5000/?key1=val1&key2=val2
    # A question mark after a URL tells the server that the remainder of the line is
    # not part of the URL. It indicates that anything that follows is a set of
    # key-value pairs in the form of key=val, with each pair separated by an
    # ampersand. In Flask, the set of pairs gets transformed into a dictionary
    # which is an attribute on a Request Object.
    # For GET requests, this dictionary is called args. If you were to examine
    # request.args from inside the handler that responds to the above URL, the
    # dictionary would be the following: {'key1': 'val1', 'key2': 'val2'}
    # We’ll use this to collect the student’s GitHub username from the user. The
    # request.args variable acts like a dictionary. To be safe, just in case they
    # don’t enter anything, we’ll use the familiar dictionary .get() method
    # (no relation to GET request).
    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form to search for a student."""
    # Recall that the action in the student_search.html file tells the browser
    # where to send the form values when the user clicks submit. Here it sends
    # the data to the first handler we built earlier. That handler expects the
    # student's GitHub username in the form of a key-value pair. The value is
    # obviously whatever the user types into the text-field of the search.
    # Remember the key for a value input is stored on the HTML element as the
    # name attribute in the student_search.html where it says:
    # <input type="text" name="github">
    return render_template("student_search.html")

@app.route('/student-add', methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    student_github = request.form.get('github')
    hackbright.make_new_student(first_name,last_name, student_github)

    return render_template("student_info.html",
                           first=first_name,
                           last=last_name,
                           github=student_github)
    

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
