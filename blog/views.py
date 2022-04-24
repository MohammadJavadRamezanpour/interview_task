from .models import Post, Rating
from .serializers import PostSerializer, RatingSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from django.db.models import Avg


# Create your views here.
class PostView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly] # admins can create post, users can just watch and rate

    def get_queryset(self):
        """
          we use prefetch_related for optimization
          cause we assume we have a huge number of reviews for each post
          prefetch_related does a separate lookup for each relationship, and performs the joining in python
          we annotate the _rating to the queryset and send it from model to the serializer
          i think this is much more faster and optimized, because you said we have a huge number of reviews
        """
        return Post.objects.prefetch_related('ratings').all().annotate(_rating=Avg('ratings__score'))
    
    def get_serializer_context(self):
        return {'request': self.request}


class RatingView(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can vote

    def get_serializer_context(self):
        return {'request': self.request}