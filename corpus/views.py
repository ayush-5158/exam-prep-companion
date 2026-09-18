from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 

from .models import Subject,SourceDocument
from .serializers import SubjectSerializer,SourceDocumentSerializer


class SubjectListView(APIView):

    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)

    def post(self,request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class SubjectDetailView(APIView):

    def put(self, request, pk):
        subject = get_object_or_404(Subject,id=pk)
        serializer = SubjectSerializer(subject, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        subject = get_object_or_404(Subject,id=pk)

        serializer = SubjectSerializer(
            subject,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def get(self,request,pk):
        subject = get_object_or_404(Subject,id=pk)
        serializer = SubjectSerializer(subject)

        return Response(serializer.data)
    
    def delete(self, request, pk):
        subject = get_object_or_404(Subject,id=pk)

        subject.delete()

        return Response(status=204)

class SourceDocumentListView(APIView):

    def post(self, request):
        serializer = SourceDocumentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    def get(self,request):
        documents = SourceDocument.objects.all()
        serializer = SourceDocumentSerializer(documents,many=True)

        return Response(serializer.data)