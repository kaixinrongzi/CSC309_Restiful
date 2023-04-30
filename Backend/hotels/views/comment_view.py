from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404, \
    RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from ..serializers import CommentSerializer, CommentAddSerializer, NotificationSerializer
from ..models import Comment, Notification, Hotel, Reservation
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
        print(request.data)
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
                reservations = Reservation.objects.filter(guest=user, hotel=hotel, state='F')
            except Exception as e:
                print(e)
                return Response({"error": "the user has not finished the living in the hotel"}, status=status.HTTP_403_FORBIDDEN)

            # find out the property owner
            hotel_owner = hotel.owner
            # print("hotel owner", hotel_owner)

            if 'author' in comment and comment['author'] != '':
                author = comment['author']
            else:
                author = request.user.id
            if 'content_type' in comment and comment['content_type'] != '':
                content_type = comment['content_type']
            else:
                content_type = ''
            if 'object_id' in comment and comment['object_id'] != '':
                object_id = comment['object_id']
            else:
                object_id=''
            if 'rating' in comment and comment['rating'] != '':
                rating = comment['rating']
            else:
                rating=''
            if 'detail' in comment and comment['detail'] != '':
                detail = comment['detail']
            else:
                detail = ''

            # check if I have commented on this hotel?
            try:
                my_comment = get_object_or_404(Comment, author=request.user, content_type=7, object_id=hotel_id)
                print(my_comment)
                return Response(
                    {"error", "you have commented on this property with comment_id: " + str(my_comment.id)},
                    status=status.HTTP_403_FORBIDDEN)
            except:
                print('no comment before')

            # create a comment

            ordinary_dict = {'content_type': content_type,
                             'object_id': object_id,
                             'rating': rating,
                             'detail': detail,
                             'author': author,
                             'receiver': hotel_owner.id}

            QueryDict('', mutable=True).update(ordinary_dict)

            serializer = self.get_serializer(data=ordinary_dict)
            serializer.is_valid(raise_exception=True)
            comment_obj = serializer.save()
            print('98', comment_obj)
            # self.perform_create(serializer)

            # create a notification
            notif_data={'receiver' : hotel_owner.id,
                        'message': "comment on your property: " + str(hotel_id),
                        'content_type': 11,
                        'object_id': comment_obj.id}

            notif_serializer = NotificationSerializer(data=notif_data)
            if notif_serializer.is_valid(raise_exception=True):
                notif_serializer.save()

            hotel_owner.get_notified()
        elif content_type == '6' or content_type == 6:  # comment on an user
            user_id = comment['object_id']
            try:
                commented_user = MyUser.objects.get(pk=user_id)
                print(commented_user)
            except:
                return Response({"error": "the user you are commenting does not exist"}, status=status.HTTP_403_FORBIDDEN)

            # # check if the commented_user has ever lived in your hotel
            # reservations = Reservation.objects.filter(guest=commented_user, hotel=request.data['hotel_id'])
            # if not reservations:
            #     return Response({'error': 'the user has never lived in your hotel'})

            # create a comment
            if 'author' in comment and comment['author'] != '':
                author = comment['author']
            else:
                author = request.user.id
            ordinary_dict = {'content_type': comment['content_type'],
                             'object_id': comment['object_id'],
                             'rating': comment['rating'],
                             'detail': comment['detail'],
                             'author': author,
                             'receiver': commented_user.id}

            QueryDict('', mutable=True).update(ordinary_dict)

            serializer = self.get_serializer(data=ordinary_dict)
            serializer.is_valid(raise_exception=True)
            comment_obj = serializer.save()
            print('137', comment_obj.receiver)

            # create a notification
            notif_data = {'receiver': commented_user.id,
                          'message': "comment on you",
                          'content_type': 11,
                          'object_id': comment_obj.id}

            notif_serializer = NotificationSerializer(data=notif_data)
            if notif_serializer.is_valid(raise_exception=True):
                notif_serializer.save()

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
        comment_id = self.kwargs['pk']
        print(comment_id)

        # check if the comment_id belongs to the logined user
        user = self.request.user
        user_comments = Comment.objects.filter(author=user.id)
        return user_comments

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


class GetCommentsforHotel(ListAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        hotel_id = self.request.get_full_path().split('/')[-4]
        comments = Comment.objects.filter(content_type=ContentType.objects.get(model='hotel'), object_id=hotel_id)
        return comments


class GetCommentsforMyself(ListAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        model = self.request.query_params.get('content_type')
        print(229, model)
        comments = Comment.objects.filter(receiver=self.request.user.id, content_type=ContentType.objects.get(model=model))
        return comments


class GetCommentforMyself(RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_class = [IsAuthenticated]

    def get_object(self):
        comment = get_object_or_404(Comment, id=self.kwargs['pk'])
        return comment
