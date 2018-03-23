from django.test import TestCase
from lit.models import Article,UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.

def add_art(name, views, author):
    c = Article.objects.get_or_create(author=author)[0]
    c.views = views
    c.name = name
    c.save()
    return c

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

class IndexViewTests(TestCase):

    def test_index_view_with_no_articles(self):
        """
        If no articles exist, an appropriate message should be displayed.
        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories to show.")
        self.assertQuerysetEqual(response.context['articles_new'], [])

    def test_index_view_with_articles(self):
        """
        Check to make sure that the index has articles displayed
        """

        user = User(username='test2', password='test2')
        user.save()

        user_prof = UserProfile(name='test2', user=user)
        user_prof.save()

        add_art('test',1,user_prof)
        add_art('temp',1,user_prof)
        add_art('tmp',1,user_prof)
        add_art('tmp test temp',1,user_prof)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response.context['articles_new'],"tmp test temp")

        num_art = len(response.context['articles_new'])
        self.asserEqual(num_art, 4)