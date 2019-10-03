
from app.models import Comment,Writer,Post
from app import db
import unittest

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.user_James = Writer(username = 'James',password = 'potato', email = 'james@ms.com')
        self.new_post = Post(post_title='Test',post_content='Post test')
        self.new_comment = Comment(id=1,comment='Test comment',writer=self.user_James)

    

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Test comment')
        self.assertEquals(self.new_comment.writer,self.user_James)
        