from rest_framework import serializers
from .models import Post, Rating

class PostSerializer(serializers.ModelSerializer):
    
    # this keeps your vote, only if you voted, it wont exist if you didnt
    your_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'rating', 'voted_users_count', 'your_rating')
        extra_kwargs = {
            # because you didnt say to show posts body, so we make it write_only.
            # it doesnt make sense to me, but that's what I was asked for.
            'body': {'write_only': True}
        }


    def get_your_rating(self, post):
        try:
            # get user from serializers context if you can
            user = self.context['request'].user

            # get users reviews if you can
            return post.ratings.get(user=user).score
        except:
            # if somthing wrong happend, return None, 
            # it will be deleted in 'to_representation' method
            return None

    def to_representation(self, post):
        """
            we need to stop showing users vote on the posts he didnt vote for
            so with overriding this we delete 'your_rating' field from json output
        """

        # get the original representation
        representaiton = super().to_representation(post)

        # rename request for simplicity
        request = self.context['request']

        # get user from serializers context, set it None if he is not authenticated
        user = request.user if request.user.is_authenticated else None

        # if user didnt vote, delete your_rating field
        if not post.ratings.filter(user=user):
            representaiton.pop('your_rating')
            
        return representaiton 


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['id', 'post', 'score']

    def validate_score(self, value):
        """
            in this validation method we check if the score is between 0 and 5
        """
        if not 0 <= value <= 5:
            raise serializers.ValidationError("score should be between 0 and 5")
        return value
    
    def save(self, **kwargs):
        """
            we eigther create the rating record, or update it if already exists
        """

        # extract data we need from validated data and context
        score = self.validated_data['score']
        post = self.validated_data['post']
        user = self.context['request'].user

        # update the score or create it if doesnt exist
        # it returns the final object and a boolean representing
        # wether the object is created or opdated in a tuple
        # we unpacked it in obj and _
        obj, _ = Rating.objects.update_or_create(
            user=user, post=post,
            defaults={'score': score},
        )

        # return the object
        return obj