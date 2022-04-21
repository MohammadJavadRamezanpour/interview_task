from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()

    @property
    def rating(self) -> float:
        """
            this calculates the average rating of a post
            Returns(float): the average
        """
        
        # first we aggregate the average of scores to the queryset and then we get dict_values using .values()
        # since dict_values are not subscriptable, we need to convert them into a list
        # to be able to get the first index
        average = list(self.ratings.aggregate(Avg('score')).values())[0]

        # floats have some rounding issues in python, so for now we just want one digit after .
        # we do it with the help of f strings in python 
        # by the way, average can be None if this post has no rating in that case we return 0.0
        return float(f'{average:.1f}') if average is not None else 0.0

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        # we dont want a user to have two ratings on one post
        unique_together = ['user', 'post']

