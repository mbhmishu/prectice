# blog/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostTests(APITestCase):
    def setUp(self):
        self.post1 = Post.objects.create(title="Test Post 1", content="Content for test post 1")
        self.post2 = Post.objects.create(title="Test Post 2", content="Content for test post 2")
        self.comment1 = Comment.objects.create(post=self.post1, author="Test Author 1", text="Comment for test post 1")
        self.comment2 = Comment.objects.create(post=self.post1, author="Test Author 2", text="Another comment for test post 1")
        self.comment3 = Comment.objects.create(post=self.post2, author="Test Author 3", text="Comment for test post 2")

    def test_get_all_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_post(self):
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.get(url)
        post = Post.objects.get(id=self.post1.id)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'Content for new post'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post(self):
        url = reverse('post-detail', args=[self.post1.id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        url = reverse('post-detail', args=[self.post1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTests(APITestCase):
    def setUp(self):
        self.post1 = Post.objects.create(title="Test Post 1", content="Content for test post 1")
        self.comment1 = Comment.objects.create(post=self.post1, author="Test Author 1", text="Comment for test post 1")
        self.comment2 = Comment.objects.create(post=self.post1, author="Test Author 2", text="Another comment for test post 1")

    def test_get_all_comments(self):
        url = reverse('comment-list')
        response = self.client.get(url)
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_comment(self):
        url = reverse('comment-detail', args=[self.comment1.id])
        response = self.client.get(url)
        comment = Comment.objects.get(id=self.comment1.id)
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'post': self.post1.id, 'author': 'New Author', 'text': 'New comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_comment(self):
        url = reverse('comment-detail', args=[self.comment1.id])
        data = {'text': 'Updated comment'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        url = reverse('comment-detail', args=[self.comment1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
