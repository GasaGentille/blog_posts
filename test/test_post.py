from app.models import Comment,Writer,Post
from app import db
import unittest

class PostModelTest(unittest.TestCase):

        def setUp(self):
                self.new_writer = Writer(id=1, username = 'James',password = 'potato', email = 'james@ms.com')
                self.new_post = Post(id=1249,writer_id=self.new_writer.id, post_title='Test',post_content='Posts test')



        def test_check_instance_variables(self):
                self.assertEquals(self.new_post.id,1249)
                self.assertEquals(self.new_post.post_title,'Test')
                self.assertEquals(self.new_post.post_content,'Posts test')
                self.assertEquals(self.new_post.writer_id,self.new_writer.id)

        def test_save_post(self):
                self.new_post.save_post()
                self.assertTrue(len(Post.query.all())>0)

