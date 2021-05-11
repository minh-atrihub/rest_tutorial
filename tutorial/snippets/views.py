from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# from django.http import Http404
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
#
#
# class SnippetList(APIView):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     # Serialize
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         # Serialize queryset into Python native datatype
#         serializer = SnippetSerializer(snippets, many=True)
#         # Render data into JSON
#         return Response(serializer.data)
#
#     # De-serialize
#     def post(self, request, format=None):
#         # request.data can handle different formats, including json
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
#
#     def get(self, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, many=True)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, pk, format=None):
#         snippet = Snippet.objects.get(pk=pk)
#         snippet.delete()
