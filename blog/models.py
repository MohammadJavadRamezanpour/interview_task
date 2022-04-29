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

        # we get _rating from the annotation in the PostView, this is much more
        # optimized and sends less query to database
        if hasattr(self, '_rating') and self._rating is not None:
            return self._rating
        
        # we get here if _rating is not annotated in to the queryset
        # so we have to calculate it manually
        # note that in this demo we annotated it, so the queryset is optimized
        # and previous if condition is always True
        # so why do we write the following code?
        # in future we migth have more views that do not have _rating annotated
        # so we should calculate the rating for them manually

        average = list(self.ratings.aggregate(Avg('score')).values())[0]

        # floats have some rounding issues in python, so for now we just want one digit after dot
        # we do it with the help of f strings in python 
        # by the way, average can be None if this post has no rating in that case we return 0
        return float(f'{average:.1f}') if average is not None else 0

    @property
    def voted_users_count(self) -> int:
        """
            this works like rating property
            it returns _voted_users_count
            which was annotated in view
        """

        # we get this (_voted_users_count) from the annotation in the view
        # this is more optimized and sends less query to database
        if hasattr(self, '_voted_users_count') and self._voted_users_count is not None:
            return self._voted_users_count

        # we get here if _voted_users_count is not annotated in to the queryset
        # so we have to calculate it manually
        # note that in this demo we annotated it, so the queryset is optimized
        # and previous if condition is always True
        # so why do we write the following code?
        # in future we migth have more views that do not have _voted_users_count annotated
        # so we should calculate the count for them manually
        return self.ratings.all().count()

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        # we dont want a user to have two ratings on one post
        unique_together = ['user', 'post']
