from pdb import set_trace
from app.api.authentication.models import User
from rest_framework import status, generics
from rest_framework.serializers import ValidationError
from ..helpers.renderers import RequestJSONRenderer
from .serializers import SocialSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Social


class UserFollowAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)#Helps to arrange the json on postman front end.
    serializer_class = SocialSerializer
    def post(self, request):
        """
        Handles following
        """
        follow = request.data#user from browser sending request
        serializer = self.serializer_class(data=follow)
        serializer.is_valid(raise_exception=True)
        followee_id=request.data['followee']
        followee = User.objects.get(pk=followee_id)
        serializer.save(follower=request.user, followee=followee)#user is a method in class request, and one currently logged in.
        #the tokens generated was unique depeding with who is logged in.
        data = serializer.data

        return_message = {
            "message":"followed followee successfully",
            "data": data
        }
        return Response(return_message, status=status.HTTP_201_CREATED)


    def get(self, request):#querrying social model social=Social.objects.all() think follower as social for description
        follower = Social.objects.all()
    def post(self, request):
        """
        Handles following
        """
        follow = request.data#user from browser sending request
        serializer = self.serializer_class(data=follow)
        serializer.is_valid(raise_exception=True)
        followee_id=request.data['followee']
        followee = User.objects.get(pk=followee_id)
        serializer = self.serializer_class(followee, many=False)
        return_message = {
            "message":"All followers retrieved successfully",
            "data":serializer.data
        }
        return Response(return_message, status=status.HTTP_200_OK)


class UserUnfollowApiView(generics.CreateAPIView):
    #always use this class provided methods
    permission_classes = (IsAuthenticated,)#Here user currently authenticated is taken dynamically.
    renderer_classes = (RequestJSONRenderer,)#Helps to arrange the json on postman front end.
    serializer_class = SocialSerializer

    def post(self, request, followee_id):
        # followee_id is the id passed at postman,also can be a unique username dankama231
        try:
            follower = Social.objects.filter(followee=followee_id, follower=request.user)
        except Social.DoesNotExist:
            raise ValidationError(
                "The follower you want to delete does not exist"
            )
        follower.delete()
        return_message = {
            "message": "You have successfully unfollowed"
        }

        return Response(return_message, status=status.HTTP_200_OK)
