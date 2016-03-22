from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from wsgiref.util import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from api.models import *
from api.serializers import *
import urllib2
import xmltodict

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
        
    @staticmethod
    def _generatePDF(title, school_id, grade, subject):
        pass
    
#A cron job will call this once a day/week, to update the events from the CCOL rss feed    
def update_events(request):
    rss_url = "https://lw6qqcgvzf.execute-api.us-east-1.amazonaws.com/prod/rss"
    
    file = urllib2.urlopen(rss_url)
    data = file.read()
    file.close()
    
    Event.objects.all().delete()

    for item in xmltodict.parse(data)['rss']['channel']['item']:
        event = Event(name=item['event_name'],
                      description=item['event_description'],
                      organizer=item['event_organizer'],
                      website=item['event_website'],
                      start_date=item['event_start_date'],
                      end_date=item['event_end_date'],
                      start_time=item['event_start_time'],
                      end_time=item['event_end_time'],
                      cost=item['event_cost'],
                      venue_name=item['venue_name'],
                      venue_street_address=item['venue_street_address'],
                      venue_city=item['venue_city'],
                      venue_state=item['venue_state'],
                      venue_zipcode=item['venue_zipcode'])
        event.save()
        
    return HttpResponse('')
