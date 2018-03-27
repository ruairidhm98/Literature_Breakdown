from django.test import TestCase
from lit.models import Article,UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.

def create_user_prof(username='test',password='test',name='test'):
    user = User(username=username, password=password)
    user.save()

    user_prof = UserProfile(name=name, user=user)
    user_prof.save()

    return user_prof

def add_art(title='test',views=1,author='test_admin',book='test',date='01/03/18',rating=4):
    c = Article.objects.get_or_create(author=author)[0]
    c.views = views
    c.title = title
    c.book = book
    c.date = date
    c.rating =rating
    c.save()

    return c

class SearchMethondTest(TestCase):
    def test_ensure_search_with_no_query_posts_all_possible_results(self):
        """
         test_ensure_search_with_no_query_posts_all_possible_results should return true
         if all possible articles and users are shown when no query is entered
        """

        user_prof = create_user_prof(username='querytest',name='query')

        add_art(title='querytitle',author=user_prof)

        response = self.client.post(reverse('search'),data={'query':""})
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'querytest')
        self.assertContains(response, 'querytitle')

    def test_ensure_search_returns_true_if_query_matches_know_article(self):
        """
         
        """

class ArticleMethodTest(TestCase):
    def test_ensure_view_are_positive(self):
        """
        ensure_views_are_positive should results True for
        where views are zero or positive
        :return:
        """

        user_prof = create_user_prof()

        art = Article(title='test',views=-1,author=user_prof)
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

        user_prof = create_user_prof()

        add_art(title='test',author=user_prof)
        add_art(title='temp',author=user_prof)
        add_art(title='tmp',author=user_prof)
        add_art(title='tmp test temp',author=user_prof)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"tmp test temp")

        num_art = len(response.context['articles_trending'])
        self.assertEqual(num_art, 4)