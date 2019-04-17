from app import app
import unittest
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloglytest'
app.config['TESTING'] = True
connect_db(app)


class BloglyAppTest(unittest.TestCase):

    def setUp(self):

        # Create all tables
        db.create_all()

        # Add pets
        user_1 = User(first_name='Test1', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
        user_2 = User(first_name='Test2', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
        user_3 = User(first_name='Test3', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
        user_4 = User(first_name='Test4', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')
        user_5 = User(first_name='Test5', last_name="last1", image_url='http://dummyimage.com/261x224.png/ff4444/ffffff')

        # Add new objects to session, so they'll persist
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(user_3)
        db.session.add(user_4)
        db.session.add(user_5)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.client = app.test_client()
    
    def tearDown(self):

        db.drop_all(bind=None)

    def test_root_redirect(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)
    
    def test_landing(self):
        result = self.client.get('/users')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Users', result.data)

    def test_new_user_page(self):
        result = self.client.get('/users/new')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'New User', result.data)
    
    def test_new_user_page_processing(self):
        result = self.client.post('/users', data={
            "first-name": "TESTTT_first",
            "last-name": "TESTTT_last",
            "img-url": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/SupermanRoss.png/250px-SupermanRoss.png",
         }, follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'TESTTT_first', result.data)
        self.assertIn(b'TESTTT_last', result.data)
    
    def test_render_user_details(self):

        result = self.client.get('/users/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Test1', result.data)
    
    # def test_process_edit_user_request(self):

    #     result = self.client.post('/users', data={
    #         "first-name": "TESTTT_first",
    #         "last-name": "TESTTT_last",
    #         "img-url": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/SupermanRoss.png/250px-SupermanRoss.png",
    #      }, follow_redirects=True)

    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'TESTTT_first', result.data)
    #     self.assertIn(b'TESTTT_last', result.data)
