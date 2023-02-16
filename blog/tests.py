from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client=Client()

    def test_post_list(self):
        response=self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, '남승현의 홈페이지')

        navbar=soup.nav

        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        self.assertEqual(Post.objects.count(), 0)

        main_area=soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        post_001=Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world',
        )

        post_002=Post.objects.create(
            title='en 번째 포스트입니다.',
            content='Hello World.',
        )
        self.assertEqual(Post.objects.count(), 2)

        response=self.client.get('/blog/')
        soup=BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        main_area=soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)


        self.assertNotIn('아직 게시물이 없습니다', main_area.text)





