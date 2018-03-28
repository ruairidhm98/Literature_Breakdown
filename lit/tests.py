from django.test import TestCase
from lit.models import Article,UserProfile,Category
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.

def create_user_prof(username='test',password='test',name='test'):
    user = User(username=username, password=password)
    user.save()

    user_prof = UserProfile(name=name, user=user)
    user_prof.save()

    return user_prof

def add_art(title='test',views=1,author='test_admin',book='test',date='01/03/18',rating=0,category = 'Fiction'):
    a = Article.objects.get_or_create(title=title,author=author,category=category)[0]
    a.views = views
    a.book = book
    a.date = date
    a.rating = rating
    a.save()

    return a

def add_cat(name,slug):
    c = Category.objects.get_or_create(name=name)[0]
    c.slug = slug
    c.save()

    return c

class CategoriesTest(TestCase):
    def test_ensure_fiction_category_is_displayed_for_fiction(self):
        """
         test_ensure_fiction_category_is_displayed should only return true if article of category
         fiction is in response
        """

        add_cat('Fiction','fiction')


        user_prof = create_user_prof(username='Fiction')

        add_art(title='Fiction',author=user_prof,category='Fiction')


        response = self.client.get(reverse('show_category',kwargs={'category_name_slug' : 'fiction'}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Fiction')

    def test_ensure_fiction_category_is_displayed_for_short_story(self):
        """
         test_ensure_fiction_category_is_displayed should only return true if article of category
         short story is in response
        """

        add_cat('Short Story','short-story')


        user_prof = create_user_prof(username='Short')

        add_art(title='Short Story',author = user_prof,category='Short Story')

        response = self.client.get(reverse('show_category',kwargs={'category_name_slug' : 'short-story'}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'Short Story')

    def test_ensure_fiction_category_is_displayed_for_scripture(self):
        """
         test_ensure_fiction_category_is_displayed should only return true if article of category
         scripture is in response
        """

        add_cat('Scripture','scripture')

        user_prof = create_user_prof(username='Scrip')

        add_art(title='Scripture',author = user_prof,category='Scripture')

        response = self.client.get(reverse('show_category',kwargs={'category_name_slug' : 'scripture'}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'Scripture')

    def test_ensure_fiction_category_is_displayed_for_philosophy(self):
        """
         test_ensure_fiction_category_is_displayed should only return true if article of category
         philosophy is in response
        """

        add_cat('Philosophy','philosophy')

        user_prof = create_user_prof(username='Phil')

        add_art(title='Philosophy',author= user_prof, category = 'Philosophy')

        response = self.client.get(reverse('show_category',kwargs={'category_name_slug' : 'philosophy'}))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'Philosophy')

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

class NewArticleTest(TestCase):
    def test_ensure_newest_articles_displayed(self):
        """
        test_ensure_newest_articles_displayed should return new if trending articles are there
        """

        user_prof = create_user_prof(username="new")

        add_art(title='new1', author=user_prof, date='09/03/2018')
        add_art(title='new2', author=user_prof, date='08/03/2018')
        add_art(title='new3', author=user_prof, date='07/03/2018')
        add_art(title='new4', author=user_prof, date='06/03/2018')
        add_art(title='new5', author=user_prof, date='05/03/2018')
        add_art(title='new6', author=user_prof, date='04/03/2018')
        add_art(title='new7', author=user_prof, date='03/03/2018')

        response = self.client.get(reverse('new'))
        self.assertEquals(response.status_code,200)
        self.assertContains(response, 'new1')
        self.assertContains(response, 'new2')
        self.assertContains(response, 'new3')
        self.assertContains(response, 'new4')
        self.assertContains(response, 'new5')


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
