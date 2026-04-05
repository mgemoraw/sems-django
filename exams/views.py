from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ExamResponse
from .serializers import ExamResponseSerializer


# Create your views here.

class ExamResponseViewSet(viewsets.ModelViewSet):
    queryset = ExamResponse.objects.all()
    serializer_class = ExamResponseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # automatically assign the current user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        response = self.get_object()

        if response.user != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        if response.status == 'submitted':
            return Response({'detail': 'Already submitted'}, status=status.HTTP_400_BAD_REQUEST)

        response.submit()  # calculate score + save answers_json
        return Response({'detail': 'Exam submitted', 'score': response.score})