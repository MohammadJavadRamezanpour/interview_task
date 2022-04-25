from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from django.db.models import Avg, Count


# Create your views here.
class PostView(ListCreateAPIView):
    """
    this route lists all posts for anyone
    fields:
        id: posts id
        title: posts title
        voted_users_count: number of users who had voted for this post
        rating: the rating of this post, the average of all votes
        your_rating: the score you gave to this post, available only if you voted
    to create a post you have to be admin
    in order to vote, head over to /rate
    to create a post, post 'title' and 'body' to this route as admin
    """

    # we use prefetch_related for optimization
    # cause we assume we have a huge number of reviews for each post
    # prefetch_related does a separate lookup for each relationship, and performs the joining in python
    # we annotate the _rating to the queryset and send it from model to the serializer
    # i think this is much more faster and optimized, because you said we have a huge number of reviews
    queryset = Post.objects.prefetch_related('ratings').all().annotate(_rating=Avg('ratings__score'), _voted_users_count=Count('ratings'))
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly] # admins can create post, users can just watch and rate
    

    def get_serializer_context(self):
        return {'request': self.request}


class RatingView(CreateAPIView):
    """
    this route lets you vote!
    only authenticated users can make post request to this
    to vote send these:
    post: post id as an integer
    score, an integer number between 0 to 5
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can vote

    def get_serializer_context(self):
        return {'request': self.request}