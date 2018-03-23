from django.test import TestCase
from lit.models import Article,UserProfile
from django.contrib.auth.models import User
# Create your tests here.

class ArticleMethodTest(TestCase):
    def test_ensure_view_are_positive(self):
        """

        ensure_views_are_positive should results True fo
        where views are zero or positive
        :return:
        """

        user = User(username='test1',password='test1')
        user.save()

        user_prof = UserProfile(name='test1',user=user)
        user_prof.save()

        art = Article(title='test1',views=-1,author=user_prof)
        art.save()
        self.assertEqual((art.views>=0),True)

