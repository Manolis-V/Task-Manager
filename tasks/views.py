from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializers import TaskSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

class TaskListCreate(APIView):
    def get(self, request):
        # Only get tasks that belong to the authenticated user
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create task without requiring the 'user' field in the request
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Save task with user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)  # Get task by primary key and user
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)  # Validate and serialize data
        if serializer.is_valid():
            serializer.save()  # Save updated task
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class TaskDetail(APIView):
#     def get(self, request, pk):
#         try:
#             task = Task.objects.get(pk=pk, user=request.user)  # Fetch task by ID for the authenticated user
#             serializer = TaskSerializer(task)
#             return Response(serializer.data)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         try:
#             task = Task.objects.get(pk=pk, user=request.user)  # Ensure the task belongs to the user
#             serializer = TaskSerializer(task, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Task.DoesNotExist:
#             return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
class TaskDetailUpdateDelete(APIView):
    def get(self, request, pk):
        # Get the task with the given primary key (pk) for the authenticated user
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Update the task with the given primary key (pk) for the authenticated user
        task = get_object_or_404(Task, pk=pk, user=request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # Delete the task with the given primary key (pk) for the authenticated user
        try:
            task = get_object_or_404(Task, pk=pk, user=request.user)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            raise PermissionDenied("You do not have permission to delete this task.")
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Homepage view for '/'
def homepage(request):
    return HttpResponse("<h1>Welcome to the Task Manager API</h1>")


class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists. Please choose a different one.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create new user
            user = User(username=username, password=make_password(password))
            user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access': access_token,
                'refresh': refresh_token
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)