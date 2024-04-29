from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic  import DeleteView, ListView, DetailView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.http import JsonResponse

from .models import Task
from authentication.models import User
from contacts.models import Contact
from deals.models import Deal
from projects.models import Project
from organizations.models import Company
from leads.models import Lead
from crm_admin.models import Customer

class BaseTaskView(LoginRequiredMixin): #base class
    model = Task
    login_url = 'authentication:login'
    template_name = 'tasks/tasks.html'
    error404 = reverse_lazy('authentication:error404')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.warning(request, 'Invalid user.')
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    

class TaskCreateView(BaseTaskView, CreateView): # For creating task.
    model = Task
    fields="__all__"
    success_url = reverse_lazy('tasks:list')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        assigned_to = request.POST.get('assigned_to')
        try:
            assigned_to = get_object_or_404(User, pk = assigned_to)
        except Http404:
            messages.error(self.request,'Invalid user selected!')
            return HttpResponseRedirect(reverse('tasks:list'))
        category = request.POST.get('category')
        due_date = request.POST.get('due_date')
        start_date = request.POST.get('start_date')
        reminder_date = request.POST.get('reminder_date')
        progress = request.POST.get('progress')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        related_to = request.POST.get('related_to')
        description = request.POST.get('description')
        try:
            created_by = get_object_or_404(User, pk = self.request.user.pk)
            organization_id = self.request.user.organization_id
        except Http404:
            messages.error(self.request,'Unauthorized user!')
            return HttpResponseRedirect(reverse('tasks:list'))
        Task.objects.create(
            name = name,
            assigned_to = assigned_to,
            category = category,
            due_date = due_date,
            start_date = start_date,
            reminder_date = reminder_date,
            progress = progress,
            priority = priority,
            status = status,
            related_to = related_to,
            description = description,
            created_by = created_by,
            organization_id = organization_id
        )
        messages.success(self.request,"New task created")
        return redirect(self.success_url)    
    
    def form_invalid(self, form):        
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")

        messages.error(self.request, "Failed to create task.")
        return super().form_invalid(form)

    
class CloneTaskView(BaseTaskView, View):
    def get(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk)
            Task.objects.create(
                name=task.name,
                assigned_to=task.assigned_to,
                category=task.category,
                due_date=task.due_date,
                start_date=task.start_date,
                reminder_date=task.reminder_date,
                progress=task.progress,
                priority=task.priority,
                status=task.status,
                related_to=task.related_to,
                description=task.description,
                task_owner=task.record_owner,
                organization_id=task.organization_id
            )
            return redirect('tasks:list')
        except Http404:
            return redirect(self.error404)


class TaskUpdateView(BaseTaskView, UpdateView): # For updating task.
    fields=[
        'name',
        'assigned_to',
        'category',
        'due_date',
        'start_date',
        'reminder_date',
        'progress',
        'priority',
        'status',
        'related_to',
        'description',
        'task_visibility',
        'created_by'
    ]
    query_pk_and_slug = 'pk'
    success_url = reverse_lazy('tasks:list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Task updation successfull.')
        return response    


class TaskOwnerUpdateView(BaseTaskView, UpdateView):
    fields = ["record_owner"]
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        messages.success(self.request, 'Successfully updated task owner.')
        return super().form_valid(form)


class TaskCompletionView(BaseTaskView, UpdateView):
    fields = ["status"]
    success_url = reverse_lazy('tasks:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()        
        self.object.status = "Completed"
        self.object.save()
        messages.success(self.request, "Task completed successfully.")
        return redirect(self.get_success_url())
    

class TaskCompletionAndCloningView(BaseTaskView, UpdateView):
    fields = ["status"]
    success_url = reverse_lazy('tasks:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        Task.objects.create(
                name=self.object.name,
                assigned_to=self.object.assigned_to,
                category=self.object.category,
                due_date=self.object.due_date,
                start_date=self.object.start_date,
                reminder_date=self.object.reminder_date,
                progress=self.object.progress,
                priority=self.object.priority,
                status=self.object.status,
                related_to=self.object.related_to,
                description=self.object.description,
                task_owner=self.object.record_owner,
                organization_id=self.object.organization_id
            )
        self.object.status = "Completed"
        self.object.save()
        messages.success(self.request, "Task completed and cloned successfully.")
        return redirect(self.get_success_url())

class TaskListView(BaseTaskView, ListView): # To list tasks.
    context_object_name = 'tasks'

    def get_queryset(self, **kwargs):
        return Task.objects.filter(organization_id = self.request.user.organization_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "users": User.objects.all().exclude(username='admin'),
            "contacts": Contact.objects.all(),
            "deals": Deal.objects.all(),
            "projects": Project.objects.all(),
            "organizations": Company.objects.all(),
            "leads": Lead.objects.all(),
        })
        try:
            customer = get_object_or_404(Customer, organization_id = self.request.user.organization_id)
            context['customer'] = customer
        except Http404:
            print("Customer not found.")

        return context

class CompletedTaskListView(TaskListView):

    def get_queryset(self, *kwargs):
        return Task.objects.filter(status="Completed", organization_id=self.request.user.organization_id).order_by('created')

class TaskDetailView(BaseTaskView, DetailView): # For providing a detail of a single task. 
    model = Task
    query_pk_and_slug = 'pk'

    def render_to_response(self, context, **response_kwargs):
        task = context['object']

        serialized_data = {}

        for field in task._meta.fields:
            field_name = field.name
            field_value = getattr(task, field_name)
            print(field_name, ": " , field_value)
            if field_value:
                if field_name in ("assigned_to", "record_owner", "created_by", "record_owner"):
                    if field_value.last_name:
                        serialized_data.update({
                            field_name: f"{field_value.first_name} {field_value.last_name}",
                            field_name + '_id': field_value.pk,
                        })
                    else:
                        serialized_data.update({
                            field_name: field_value.first_name,
                            field_name + '_id': field_value.id,
                            })
                
                elif field_name in ["assigned_to", "created_by"]:
                    if field_value.last_name:
                        serialized_data[field_name] = f"{field_value.first_name} {field_value.last_name}"
                        print(field_value.last_name)
                    else:
                        serialized_data[field_name] = field_value.first_name
                
                elif field_name in ("created", "updated"):
                    serialized_data[field_name] = field_value.strftime("%d %b %Y %I:%M %p")
                else:
                    serialized_data[field_name] = field_value

        return JsonResponse(serialized_data)
    

class TaskDeleteView(BaseTaskView, View):
    def get(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk)
            task.delete()
            messages.success(request, "Task Deleted.")
            return redirect('tasks:list')
        except Http404:
            return HttpResponse("invalid object")

    