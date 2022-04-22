from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

# Create your views here.
class PostView(ListCreateAPIView):
    # we use prefetch_related for optimization
    # cause we assume we have a huge number of reviews for each post
    # prefetch_related does a separate lookup for each relationship, and performs the joining in python

    queryset = Post.objects.prefetch_related('ratings').all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly] # admins can create post, users can just watch and rate

    def get_serializer_context(self):
        return {'request': self.request}


class RatingView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can vote

    def get_serializer_context(self):
        return {'request': self.request}