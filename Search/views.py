from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from . import client


class SearchListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        tag = request.GET.get("tag") or None
        if not query:
            return Response({""}, status=status.HTTP_400_BAD_REQUEST)
        results = client.perform_search(query, tags=tag)
        return Response(results)
