from flask import Flask, request, json, render_template
from model import Model

# Create a flask app and configure it
app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET'])
def course_search():
    '''Get the list of courses and their information '''
    course_id =  request.args.get('select_course')
    model = Model()

    if course_id is None:
        # Extract list of all courses
        courses = model.get_available_courses()
        return render_template("index.html", courses = courses, course_info = None)
    else:
        # Get list of available classes, cost and description
        course_info = model.get_course_info(course_id)
        return render_template('index.html', course_info = course_info)

@app.route('/', methods=['POST'])
def enrollment():
    '''Enroll student to a specific class'''
    model = Model()

    student_UIN = request.form.get('UIN')
    course = request.form.get('course_id')
    schdule = request.form.get('schedule_id')
    return model.enroll_student(student_UIN, course, schdule)

if __name__ == '__main__':
    app.run(debug=True)