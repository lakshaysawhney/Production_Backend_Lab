from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs.api.serializers import (
    JobCreateSerializer,
    JobSerializer,
)
from jobs.models import Job
from jobs.services import create_job


class JobListCreateAPIView(APIView):

    def get(self, request):
        # Fetching top 100 latest jobs
        jobs = Job.objects.order_by("-created_at")[:100] # Pagination to be implemented for this soon
        
        serializer = JobSerializer(
            jobs,
            many=True,
        )

        return Response(serializer.data) # implicit/default HTTP 200 Staus code returned here no need of explicit mention


    def post(self, request):
        # Creating input serializer using incoming data
        input_serializer = JobCreateSerializer(
            data=request.data # request.data gives us the data/json sent by client to backend (just data/json not metadata and headers that's why we want to do request.data)
        )

        # Validating the input_serializer created using the input API contract specified in corresponding serializers.py 
        input_serializer.is_valid(
            raise_exception=True
        )
        # if sucess -> `input_serializer.validated_data` exists
        # else if fails -> DRF raises ValidationError with HTTP 400 (Bad Request)

        job = create_job(
            **input_serializer.validated_data # **validated_data unpacks unpacks dictionary keyword arguments.
        )

        # Creating output serializer by converting the job object into our public API representation
        output_serializer = JobSerializer(job)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class JobDetailAPIView(APIView):

    def get(self, request, job_id):
        job = get_object_or_404(
            Job,
            id=job_id,
        )

        serializer = JobSerializer(job)

        return Response(serializer.data)