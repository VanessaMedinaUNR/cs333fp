import unittest
from app import app, db, Todo

class WebsiteTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
        self.app = app.test_client()

       
        with app.app_context():
            db.create_all()
            task = Todo(content='Test task')
            db.session.add(task)
            db.session.commit()
            self.task_id = task.id

    def tearDown(self):
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = self.app.get(f'/update/{self.task_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.app.get(f'/delete/{self.task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.app.post('/', data={'content': 'New Task'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Task', response.data)

if __name__ == '__main__':
    unittest.main()
