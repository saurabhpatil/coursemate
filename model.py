from config import *
import MySQLdb as mdb
import json

def connect_database():
    '''Returns a connection to database'''
    try:
        con = mdb.connect(os.environ.get('SQL_DATABASE_URI'), SQL_DATABASE_USER, \
                          SQL_DATABASE_PASS, SQL_DATABASE_SCHEMA, \
                          use_unicode=True, charset='utf8')
        return con
    except Exception as e:
        return None

class Model:
    '''This class handles all data related operations.
        It performs information retrieval and insertion and returns JSON objects as required'''
    def __init__(self):
        '''Initialize connection to database'''
        self.con = connect_database()
        self.cursor = self.con.cursor

    def __del__(self):
        '''Close the active database connection'''
        self.con.commit()
        self.cursor.close()

    def get_available_courses(self):
        '''Get the entire list of available courses'''
        result = dict()
        result['courses'] = list()

        try:
            # Get search results based on doctor type and city
            sql_query = '''SELECT id,  name FROM courses'''
            self.cursor.execute(sql_query)
            course_iterator = self.cursor.fetchall()

            # construct a json for all of the search result-set
            for course in course_iterator:
                course_dict = dict()
                course_dict['course_id'] = int(course[0])
                course_dict['course_name'] = str(course[1])
                result['courses'].append(course_dict)
            result['success'] = True
            return json.dumps(result)

        except Exception as e:
            # Return the error information in JSON result
            result['error'] = e
            result['success'] = False
            return json.dumps(result)

    def get_course_info(self, course_id):
        '''Get the information(cost, description, classes) related to a particular course'''
        result = dict()

        try:
            # Get course cost and description
            sql_query = '''SELECT name, cost, desc FROM courses WHERE id = {}'''.format(course_id)

            self.cursor.execute(sql_query)
            course_info = self.cursor.fetchone()

            result['course'] = course_info[0]
            result['cost'] = course_info[1]
            result['description'] = course_info[2]

            # Get the list of all available classes
            sql_query = '''SELECT id, professor, schedule FROM availability WHERE course_id = {}'''.format(course_id)
            self.cursor.execute(sql_query)
            schedule_iterator = self.cursor.fetchall()

            # Append the list to JSON object
            result['availability'] = list()
            for schedule in schedule_iterator:
                schedule_dict = dict()
                schedule_dict['id'] = int(schedule[0])
                schedule_dict['professor'] = int(schedule[1])
                schedule_dict['weekly_schedule'] = str(schedule[2])
                result['availability'].append(schedule_dict)
            result['success'] = True
            return json.dumps(result)

        except Exception as e:
            result['error'] = e
            result['success'] = False
            return json.dumps(result)

    def enroll_student(self, student_UIN, course_id, schedule_id):
        '''Process student enrollment for classes'''
        result = dict()

        try:
            # Add the student and class information to enrollment table
            sql_query = '''INSERT IGNORE INTO enrollment(UIN, course, schedule) VALUES({}, {}, {})''' \
                .format(student_UIN, course_id, schedule_id)
            self.cursor.execute(sql_query)

            result['success'] = True
            return json.dumps(result)

        except Exception as e:
            result['error'] = e
            result['success'] = False
            return json.dumps(result)