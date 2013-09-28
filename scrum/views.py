from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from .models import Project, Story, Task, Sprint, SprintTasks
from django.http import HttpResponseNotFound, HttpResponse
import string
import json

class WhiteBoardView(TemplateView):
    template_name = 'scrum/whiteboard.html'


class WhiteBoardView(DetailView):
    template_name = 'scrum/whiteboard.html'
    model = Project
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WhiteBoardView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        project = kwargs.get('object')
        project_stories = Story.objects.filter(project=project)
        project_tasks = Task.objects.filter(story__in=project_stories)
        project_tasks_backlog = project_tasks.filter(status='BACKLOGS')
        
        context['stories'] = project_stories
        context['tasks'] = project_tasks
        context['tasks_backlog'] = project_tasks_backlog
        
        return context
    
def add_story(request):
    
    if request.method == 'POST':
        url = request.META.get('PATH_INFO')[1:]
        project_id = url[:url.find('/')]
        
        story_title = request.POST.get('title')
        story_time = request.POST.get('time')
        story_project = Project.objects.get(pk=project_id)
        
        new_story = Story.objects.create(title = story_title,
                                         project = story_project ,
                                         estimated_time = story_time)

        response_data = {}
        response_data['story_pk'] = new_story.pk
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    else:
        return HttpResponseNotFound('<h1> Not Found </h1>')
    #return response
    
    
    