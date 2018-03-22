from django.test import TestCase
from lit.models import Article,UserProfile
# Create your tests here.

class ArticleMethodTest(TestCase):
    def test_ensure_view_are_positive(selfs):
        """

        ensure_views_are_positive should results True fo
        where views are zero or positive
        :return:
        """

        art = Article(title='test',views=-1)
        art.save()
        seld.assertEqual((art.views>=0),True)