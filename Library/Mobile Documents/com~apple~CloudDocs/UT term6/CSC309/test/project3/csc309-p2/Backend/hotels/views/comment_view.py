from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from rest_framework.pagination import PageNumberPagination
from ..serializers import CommentSerializer, CommentAddSerializer
from ..models import Comment, Notification, Hotel
import sys

sys.path.append("...")
from accounts.models import MyUser


# Create your views here.


class AddComment(CreateAPIView):
    serializer_class = CommentAddSerializer
    permission_class = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        return Response(user.get_map(), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # regular operation
        comment = request.data
        user = request.user
        content_type = comment["content_type"]
        print("content_type", content_type)

        if content_type == '7' or content_type == 7:  # comment on a hotel
            hotel_id = comment["object_id"]
            try:
                hotel = Hotel.objects.get(pk=hotel_id)
            except:
                return Response({"error": "the hotel does not exist"}, status=status.HTTP_403_FORBIDDEN)
            # check if the user has ever finished living in the hotel
            try:
                reservation = Reservation.objects.get(guest=user, hotel=hotel, STATUS='F')
            except:
                return Response({"error": "the user has not finished the living in the hotel"}, status=status.HTTP_403_FORBIDDEN)

            # find out the property owner
            hotel_owner = hotel.owner
            # print("hotel owner", hotel_owner)

            if 'author' in comment and comment['author'] != '':
                author = comment['author']
            else:
                author = request.user.id

            # check if I have commented on this hotel?
            my_comments = Comment.objects.filter(author=request.user, content_type=7)
            for my_comment in my_comments:
                if my_comment.object_id == hotel_id:
                    return Response(
                        {"error", "you have commented on this property with comment_id: " + str(my_comment.id)},
                        status=status.HTTP_403_FORBIDDEN)

            # create a comment

            ordinary_dict = {'content_type': comment['content_type'],
                             'object_id': comment['object_id'],
                             'rating': comment['rating'],
                             'detail': comment['detail'],
                             'author': author}

            QueryDict('', mutable=True).update(ordinary_dict)

            serializer = self.get_serializer(data=ordinary_dict)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # create a notification
            notif = Notification.objects.create(receiver=hotel_owner,
                                                message="comment on your property: " + str(hotel_id))
            hotel_owner.get_notified()
        elif content_type == '6' or content_type == 6:  # comment on an user
            user_id = comment['object_id']
            try:
                commented_user = MyUser.objects.get(pk=user_id)
            except:
                return Response({"error": "the user you are commenting does not exist"}, status=status.HTTP_403_FORBIDDEN)

            # create a comment
            if 'author' in comment and comment['author'] != '':
                author = comment['author']
            else:
                author = request.user.id
            ordinary_dict = {'content_type': comment['content_type'],
                             'object_id': comment['object_id'],
                             'rating': comment['rating'],
                             'detail': comment['detail'],
                             'author': author}

            QueryDict('', mutable=True).update(ordinary_dict)

            serializer = self.get_serializer(data=ordinary_dict)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # create a notification
            notif = Notification.objects.create(receiver=commented_user, message="comment on yourself: " + str(user_id))
            commented_user.get_notified()
        else:
            return Response({"error": "no choice for content_type"}, status=status.HTTP_403_FORBIDDEN)

        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetComments(ListAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        print(Comment.objects.filter(author=user))
        return Comment.objects.filter(author=user)


class GetComment(ListAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.request.get_full_path().split('/')[-2]
        print(comment_id)

        # check if the comment_id belongs to the logined user
        user = self.request.user
        user_comments = Comment.objects.filter(author=user)
        for comment in user_comments:
            if comment.id == comment_id:
                return comment
        return Response({"error": "not allowed"}, status.HTTP_403_FORBIDDEN)

# host reply to the public comment about his property.
# class FollowComment1(CreateAPIView):
#     pass
#
# # guest reply to the host's comment
# class FollowComment2(CreateAPIView):
#     pass


class DeleteComment(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        comment_id = kwargs['pk']
        try:
            comment_to_delete = Comment.objects.get(pk=comment_id, author=request.user.id)
        except:
            return Response({"error": "You cannot delete other people comments or this comment does not exist"},
                            status=status.HTTP_403_FORBIDDEN)
        comment_to_delete.delete()
        return Response({"delete_sucess": "The comment has been deleted"},
                            status=status.HTTP_200_OK)
