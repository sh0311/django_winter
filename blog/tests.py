from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client=Client()
        self.user_alice=User.objects.create_user(username='alice', password='somepassword')
        self.user_Derek=User.objects.create_user(username='Derek', password='somepassword')
        self.category_food=Category.objects.create(name='food', slug='food')
        self.category_study=Category.objects.create(name='study',slug='study')


    def navbar_test(self, soup):
        navbar=soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn=navbar.find('a', text='Alicesh')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn=navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn=navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn=navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
            categories_card=soup.find('div', id='categories-card')
            self.assertIn('Categorys', categories_card.text)
            self.assertIn(f'{self.category_food.name} ({self.category_food.post_set.count()})', categories_card.text)
            self.assertIn(f'{self.category_study.name} ({self.category_study.post_set.count()})', categories_card.text)
            self.assertIn(f'미분류(1)', categories_card.text)
    def test_post_list(self):
        #포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup=BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area=soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        post_001_card=main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        self.assertIn(self.user_alice.username.upper(), main_area.text)
        self.assertIn(self.user_Derek.username.upper(), main_area.text)

        #텍스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response=self.client.get('/blog/')
        soup=BeautifulSoup(response.content, 'html.parser')
        main_area=soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    def test_category_page(self):
        response=self.client.get(self.category_food.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup=BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_food.name, soup.h1.text)

        main_area=soup.find('div', id='main-area')
        self.assertIn(self.category_food.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)





























