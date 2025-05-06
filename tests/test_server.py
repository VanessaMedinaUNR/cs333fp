import unittest
from app import app, db, Todo
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone


class WebsiteTestCase(unittest.TestCase):

    #set up test client and a test task in db
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

    #after test cleaner
    def tearDown(self):
        
        with app.app_context():
            db.session.remove()
            db.drop_all()

    #testing if homepage is up
    def test_homepage(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)

    #testing if update with valid id gets correctly redirected
    def test_update_redirect(self):
        response = self.app.get(f'/update/{self.task_id}')

        self.assertEqual(response.status_code, 200)
    
    #testing if the task if correctly updated 
    def test_update_task(self):
        response = self.app.post(f'/update/{self.task_id}', data={'content': 'Updated Task'}, follow_redirects=True)
        with app.app_context():
            updated_task = db.session.get(Todo, self.task_id)
            self.assertEqual(updated_task.content, 'Updated Task')

    #testing deleting a task and if success
    def test_delete_redirect(self):
        response = self.app.get(f'/delete/{self.task_id}', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    #testing if the task deleted is no longer in db
    def test_delete_task(self):
        response = self.app.get(f'/delete/{self.task_id}', follow_redirects=True)
        with app.app_context():
            deleted_task = db.session.get(Todo, self.task_id)
            self.assertIsNone(deleted_task)

    #adding a task test 
    def test_create_task(self):
        response = self.app.post('/', data={'content': 'New Task'}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Task', response.data)
    
    #error tests
    def test_index_error(self):
        response = self.app.post('/', follow_redirects=True)

        self.assertEqual(response.status_code, 400)
    
    def test_delete_error(self):
        response = self.app.get('/delete/9999', follow_redirects=True)

        self.assertIn(b'There was a problem deleting that task', response.data)
    
    def test_update_error(self):
        response = self.app.get('/update/9999', follow_redirects=True)

        self.assertIn(b'There was an issue updating your task', response.data)

    #unit tests
    #test to see if self rep of todo in todo model is accurate
    def test_repr_method(self):
        todo = Todo(id=42, content="Example task")
        self.assertEqual(repr(todo), '<Task 42>')
    
    #test datetime library is not returning none
    def test_default_date_created(self):
        with app.app_context():
            todo = Todo(content='Sample')
            db.session.add(todo)
            db.session.flush()  # Triggers default value
            self.assertIsInstance(todo.date_created, datetime)

    #testing db by mocking it and adding a task
    @patch('app.db.session')
    def test_add_task_success(self, mock_session):
        todo = Todo(content="Mocked task")
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        try:
            db.session.add(todo)
            db.session.commit()
        except Exception:
            self.fail("Add task raised Exception unexpectedly")
    
    #testing db, mock exception
    @patch('app.db.session')
    def test_add_task_failure(self, mock_session):
        todo = Todo(content="Bad task")
        mock_session.add.side_effect = Exception("DB error")

        with self.assertRaises(Exception):
            db.session.add(todo)
            db.session.commit()
    
    #testing getting task
    def test_get_task_by_id(self):
        with app.app_context():
                task = Todo.query.get(self.task_id)  # Ensure we're inside the app context
                self.assertIsNotNone(task)  # Check that the task exists
                self.assertEqual(task.content, 'Test task')


    

    

if __name__ == '__main__':
    unittest.main()
