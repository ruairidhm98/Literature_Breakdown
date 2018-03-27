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

def add_art(title='test',views=1,author='test_admin',book='test',date='01/03/18',rating=0):
    a = Article.objects.get_or_create(title=title,author=author)[0]
    a.views = views
    a.book = book
    a.date = date
    a.rating = rating
    a.save()

    return a

class TrendingArticleTest(TestCase):
    def test_ensure_top_trending_articles_appear(self):
        """
         test_ensure_top_trending_articles_appear should return positive if trending articles are there
        """

        user_prof = create_user_prof(username="trending")

        add_art(title='trend1', author=user_prof, rating=5)
        add_art(title='trend2', author=user_prof, rating=4)
        add_art(title='trend3', author=user_prof, rating=3)
        add_art(title='trend4', author=user_prof, rating=2)
        add_art(title='trend5', author=user_prof, rating=1)

        response = self.client.get(reverse('trending'))
        self.assertEquals(response.status_code,200)
        self.assertContains(response, 'trend1')
        self.assertContains(response, 'trend2')
        self.assertContains(response, 'trend3')
        self.assertContains(response, 'trend4')
        self.assertContains(response, 'trend5')


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

    def test_ensure_search_returns_true_if_query_matches_known_article_or_user(self):
        """
         test_ensure_search_returns_true_if_query_matches_known_article should only retun true
         if we attempt to search for an article and user that we know exists and it is present in results
        """

        user_prof = create_user_prof(username='queryfind')

        add_art(title='test article query',author=user_prof)

        response = self.client.post(reverse('search'), data={'query': "test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'test article query')
        self.assertContains(response,'queryfind')

    def test_ensure_search_returns_nothing_if_query_searches_for_artilce_or_user_that_is_not_there(self):
        """
         test_ensure_search_returns_nothing_if_query_searches_for_artilce_or_user_that_is_not_there
         should return true for no findings of either a user or article with an incorrect search
        """

        user_prof = create_user_prof(username='nofindings')

        add_art(title='nofindings',author =user_prof)

        response = self.client.post(reverse('search'), data={'query': "a"})
        self.assertEqual(response.status_code, 200)

        num_art = len(response.context['result_list_articles'])
        num_user = len(response.context['result_list_users'])

        self.assertEqual(num_art,0)
        self.assertEqual(num_user,0)


class ArticleMethodTest(TestCase):
    def test_ensure_view_are_positive(self):
        """
        ensure_views_are_positive should results True for
        where views are zero or positive
        """

        user_prof = create_user_prof()

        art = Article(title='test',views=-1,author=user_prof)
        art.save()
        self.assertEqual((art.views>=0),True)

    def test_ensure_rating_are_positive(self):
        """
        test_ensure_rating_are_positive should results True for
        where rating is zero or positive
        """
        user_prof = create_user_prof()

        art = Article(title='test',rating=-1,author=user_prof)
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
