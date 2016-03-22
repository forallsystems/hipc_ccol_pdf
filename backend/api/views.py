from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from wsgiref.util import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from api.models import *
from api.serializers import *
import urllib2
import xmltodict
import xhtml2pdf.pisa as pisa
try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO
import cgi

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
    
    @list_route(methods=['post','get'])
    def sample(self, request):
        return FlyerViewSet._generatePDF()
        
    @staticmethod
    def _generatePDF(title="Latest CCOL Events", school_id="", grade="", subject=""):        
        events = Event.objects.all().order_by('-start_date')[:6]

        context_dict = {'events':events,
                        'title':title}
        
        template = get_template("flyer_pdf.html")
        context = Context(context_dict)
        html  = template.render(context)
        result = StringIO()
        pdf = pisa.pisaDocument(StringIO( "{0}".format(html) ), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
    
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
