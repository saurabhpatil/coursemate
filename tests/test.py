import model
import unittest 
import requests

class AppTestCases(unittest.TestCase):
    def setUp(self):
        self.con = model.connect_database()

    def tearDown(self):
        self.con.close()

    ###------------------ TEST CASES FOR MODEL -----------------------###
    def test_get_courses(self):
        cursor = self.con.cursor()
        
        insert_query = "INSERT INTO courses(name) VALUES('TEST COURSE - STAT 651')"
        cursor.execute(insert_query)

        sql_query = "SELECT id, name FROM courses"
        cursor.execute(sql_query)
        patient_profile_id = cursor.fetchall()
        self.assertIsNotNone(patient_profile_id)

        delete_query = "DELETE FROM courses WHERE name = 'TEST COURSE - STAT 651'"
        cursor.execute(delete_query)
        self.con.commit()

    def test_get_course_info(self):
        cursor = self.con.cursor()
        
        insert_query = "INSERT INTO courses(name, cost, desc) VALUES('TEST COURSE - STAT 651', 2600, 'DEMO Class')"
        cursor.execute(insert_query)

        sql_query = "SELECT id FROM courses WHERE name='TEST COURSE - STAT 651'"
        cursor.execute(sql_query)
        course_id = int(cursor.fetchone()[0])
        self.assertIsNotNone(course_id)

        sql_query = "SELECT name, cost, desc FROM courses WHERE id='{}'".format(course_id)
        cursor.execute(sql_query)
        course_info = cursor.fetchone()
        self.assertIsNotNone(course_info)
        self.assertTupleEqual(course_info,('TEST COURSE - STAT 651', 2600, 'DEMO Class'))

        insert_query = "INSERT INTO availability(id, professor, schedule) VALUES({}, 'Dr. Paul', 'MW 10:00-11:10')".format(course_id)
        cursor.execute(insert_query)



        insert_query = "INSERT INTO availability(id, professor, schedule) VALUES({}, 'Dr. Matt', 'THF 11:20-12:30')".format(course_id)
        cursor.execute(insert_query)
        sql_query = "SELECT id, professor, schedule FROM availability WHERE course_id={}".format(course_id)
        cursor.execute(sql_query)
        classes = cursor.fetchall()
        self.assertIsNotNone(classes)

        self.con.commit()

    ###------------------ TEST CASES FOR VIEWS -----------------------###
    def test_course_search(self):
        resp = requests.get('http://localhost:5000/')
        result = resp.json()
        self.assertTrue(result['success'])
        self.assertTrue(len(result['courses']) != 0)

if __name__ == '__main__':
  unittest.main()