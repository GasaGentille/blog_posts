from app.models import Writer,Post,Comment
from app import db
import unittest

class CommentModelTest(unittest.TestCase):

    def setUp(self):
        self.new_writer = Writer(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_post = Post(post_title='Test',post_content='Posts test')
        self.new_comment = Comment(id=1,comment='Test comment',writer=self.new_writer)

    def test_password_setter(self):
        self.assertTrue(self.new_writer.pass_secure is not None)

    def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_writer.password

    def test_password_verification(self):
        self.assertTrue(self.new_writer.verify_password('potato'))

        # self.new_comment.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Test comment')
        self.assertEquals(self.new_comment.writer,self.new_writer)
      
