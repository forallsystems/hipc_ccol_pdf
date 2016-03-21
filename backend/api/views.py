from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from wsgiref.util import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from api.models import *
from api.serializers import *
import urllib2

class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)
    ordering = ('name',)

class FlyerViewSet(viewsets.ViewSet):
    queryset = Flyer.objects.all()
    
    @detail_route(methods=['post'])
    def unsubscribe(self, request, pk):
        flyer = Flyer.objects.get(pk=pk)
        flyer.delete()
        
        return Response({'status': 'ok'})
    
    @list_route(methods=['post'])
    def subscribe(self, request):
        #ToDo
        return Response({'status': 'ok'})
    
    @list_route(methods=['post'])
    def sample(self, request):
        #Dummy code for now
        req = urllib2.Request("https://forallschools.s3.amazonaws.com/media/files/4b_Instructional_Protocol-Blank.pdf")
        response = urllib2.urlopen(req)
        response = HttpResponse(response.read(),  content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
        
        
    