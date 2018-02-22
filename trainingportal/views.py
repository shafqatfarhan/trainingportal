from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
#from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
#from django.core.files.storage import FileSystemStorage

#import pdb
import json

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import permissions, generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.reverse import reverse
from rest_framework import renderers

from .serializers import SnippetSerializer, SnippetModelSerializer, UserSerializer, GroupSerializer
from .models import Training, Snippet, AssignedTraining, Trainee, Trainer, Task, Assignment
from .forms import LoginForm, ProfileForm, UserForm, AddTrainingForm, AssignmentForm, TaskForm, \
    EvaluateAssignmentForm, SubmitAssignmentForm
from django.http import QueryDict


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
# class SnippetViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#
#     Additionally we also provide an extra `highlight` action.
#     """
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

#
# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes((permissions.AllowAny,))
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

def home(request):
    data ={}

    if request.user.id:
        user_instance = User.objects.get(pk=request.user.id)
        if (user_instance.is_staff):
            trainer = Trainer.objects.get(user_id=user_instance.id)
            assigned_trainings = AssignedTraining.objects.filter(trainer_id=trainer.id)
            trainee_ids = [training.trainee_id.id for training in assigned_trainings]
            trainees = Trainee.objects.filter(id__in=trainee_ids)
            trainee_user_ids = [trainee.user_id for trainee in trainees]
            trainees_user = User.objects.filter(id__in=trainee_user_ids)

            if assigned_trainings:
                trainings = []
                for training in assigned_trainings:
                    assigned_training = {
                        'trainee_id': training.trainee_id.id,
                        'trainee_name': get_trainee_name(trainees_user, training),
                        'training_name': training.training_id.title,
                        'training_due_date': training.training_id.due_date,
                        'status': 'Completed' if training.status else 'In Progress',
                    }
                    trainings.append(assigned_training)

                data['assigned_trainings'] = trainings
            else:
                data['no_trainee'] = 'No trainees assigned.'
        else:
            trainee = Trainee.objects.get(user_id=user_instance.id)
            assigned_trainings = AssignedTraining.objects.filter(trainee_id=trainee.id)

            if assigned_trainings:
                trainings = []
                for training in assigned_trainings:
                    assigned_training = {
                        'id': training.id,
                        'trainee_id': training.trainee_id.id,
                        'trainer_id': training.trainer_id.id,
                        'training_id': training.training_id.id,
                        'training_description': training.training_id.description,
                        'training_name': training.training_id.title,
                        'training_due_date': training.training_id.due_date,
                        'status': 'Completed' if training.status else 'In Progress',
                    }
                    trainings.append(assigned_training)

                data['assigned_trainings'] = trainings
            else:
                data['no_training'] = 'No enrolled trainings.'
    return render(request, 'trainingportal/home.html', data)


def logout_view(request):
    logout(request)
    return redirect(home)


class LoginView(View):
    """ handles requests for login form and redirection """

    template_name = 'trainingportal/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        login_form = self.form_class()
        return render(request, self.template_name, {'login_form': login_form})

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        data = {
            'failure_message': 'Login Failed',
        }
        if login_form.is_valid():
            try:
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user:
                    login(request, user)
                    data['redirect_path'] = '/home/'
                    data.pop('failure_message', None)
                    return HttpResponse(json.dumps(data))
                else:
                    return HttpResponse(json.dumps(data))

            except PermissionDenied:
                return HttpResponse(json.dumps(data))

        return render(request, self.template_name, {'login_form': login_form})


def register(request):
    """ handles requests for registration form and its submission """
    data = {}
    user_form = None
    profile_form = None

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # user = UserRegistration(
            #     first_name=form.cleaned_data['firstname'],
            #     last_name=form.cleaned_data['lastname'],
            #     password=form.cleaned_data['password'],
            #     designation=form.cleaned_data['designation'],
            #     email_id=form.cleaned_data['email']
            # )
            user = User.objects.create_user(
                user_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password']
            )
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            profile_form.save(user=user)
            try:
                login_user = authenticate(
                    request,
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password']
                )
                if login_user:
                    login(request, login_user)
                return redirect(home)
            except PermissionDenied:
                return redirect(home)
    data["user_form"] = user_form or UserForm()
    data["profile_form"] = profile_form or ProfileForm()

    return render(request, 'trainingportal/registration.html', data)


@login_required
def training(request):
    """ handles requests for registration form and its submission """
    training_form = None
    data = {
        'failure_message': 'Failed to add training.',
    }
    if request.method == 'POST':
        training_form = AddTrainingForm(request.POST, request.FILES)
        if training_form.is_valid():
            training_form.save()
            data.pop('failure_message', None)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    trainings = Training.objects.all()
    data["training_form"] = training_form or AddTrainingForm()
    data['trainings'] = trainings
    return render(request, 'trainingportal/trainings.html', data)


@login_required
def edit_training(request, training_id):
    """ handles requests for registration form and its submission """
    data = {}
    training_form = None
    data = {
        'failure_message': 'Error in form.',
        'delete_path': '/delete_training/'
    }
    training = Training.objects.get(pk=training_id)
    if request.method == 'POST':
        training_form = AddTrainingForm(request.POST, request.FILES, instance=training)
        if training_form.is_valid():
            training_form.save()
            data.pop('failure_message', None)
            data['redirect_path'] = '/trainings/'
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    data["training_form"] = training_form or AddTrainingForm(instance=training)
    data["training_id"] = training_id
    return render(request, 'trainingportal/edit_training.html', data)


@login_required
def delete_training(request):
    """ handles requests for deletion of a training """
    data = {}
    if request.method == 'DELETE':
        request.DELETE = QueryDict(request.body)
        training_id = request.DELETE['training_id']
        print(training_id)
        training = Training.objects.get(pk=training_id)
        if training:
            training.delete()

    data['success_message'] = 'Training deleted.'
    data['redirect_path'] = '/trainings/'
    return HttpResponse(json.dumps(data))


@login_required
def trainees(request):
    """ handles requests for populating trainees """
    data = {}
    trainer_id = request.user.id

    assigned_trainings = AssignedTraining.objects.filter(trainer_id=trainer_id)

    if assigned_trainings:
        #training_ids = [training.training_id.id for training in assigned_trainings]
        trainee_ids = [training.trainee_id.id for training in assigned_trainings]
        trainees = Trainee.objects.filter(id__in=trainee_ids)
        trainee_user_ids = [trainee.user_id for trainee in trainees]
        print(trainee_user_ids)
        trainees_user = User.objects.filter(id__in=trainee_user_ids)

        trainees_training = []
        for training in assigned_trainings:
            assigned_training = {
                'id': training.id,
                'training_id': training.training_id.id,
                'trainee_id': training.trainee_id.id,
                'trainer_id': training.trainer_id.id,
                'trainee_name': get_trainee_name(trainees_user, training),
                'training_name': training.training_id.title,
                'status': 'Completed' if training.status else 'In Progress',
            }
            trainees_training.append(assigned_training)

        data['assigned_trainings'] = trainees_training
    else:
        data['no_trainee'] = 'No trainees assigned.'
    return render(request, 'trainingportal/trainees.html', data)


def get_trainee_name(trainees_user, training):
    return "{} {}".format(trainees_user.get(pk=training.trainee_id.user_id).first_name,
                    trainees_user.get(pk=training.trainee_id.user_id).last_name)


@login_required
def update_training_status(request):
    """ handles requests for populating trainees """

    data = {
        'failure_message': 'Error Occured.',
    }
    if request.method == 'POST':
        training_id = request.POST['training_id']
        print(training_id)
        training = AssignedTraining.objects.get(pk=training_id)
        if training:
            training.status = True
            training.save()
            data['success_message'] = 'Status Updated.'
            data.pop('failure_message', None)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))


@login_required
def tasks(request):
    """ handles requests for populating tasks """

    task_form = None
    data = {
        'failure_message': 'Failed to add Task.',
        'training_id': request.GET.get('training_id'),
        'trainer_id': request.GET.get('trainer_id'),
        'trainee_id': request.GET.get('trainee_id'),
    }

    if request.method == 'POST':
        training = Training.objects.get(pk=data['training_id'])
        trainee = Trainee.objects.get(pk=data['trainee_id'])
        trainer = Trainer.objects.get(pk=data['trainer_id'])

        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.training_id = training
            task.trainee_id = trainee
            task.trainer_id = trainer
            task.save()
            data.pop('failure_message', None)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    tasks = Task.objects.filter(training_id=data['training_id'])
    data["task_form"] = task_form or TaskForm()

    if tasks:
        data['tasks'] = tasks
    else:
        data['no_tasks'] = 'No tasks assigned.'

    user_instance = User.objects.get(pk=request.user.id)

    if (user_instance.is_staff):
        data['is_staff'] = 'Trainer'

    return render(request, 'trainingportal/tasks.html', data)


@login_required
def assignments(request):
    """ handles requests for populating assignments """

    assignment_form = None
    data = {
        'failure_message': 'Failed to add Task.',
        'task_id': request.GET.get('task_id'),
    }

    if request.method == 'POST':
        task = Task.objects.get(pk=data['task_id'])

        assignment_form = AssignmentForm(request.POST, request.FILES)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.task_id = task
            assignment.save()
            data.pop('failure_message', None)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    assignments = Assignment.objects.filter(task_id=data['task_id'])
    data["assignment_form"] = assignment_form or AssignmentForm()

    if assignments:
        data['assignments'] = assignments
    else:
        data['no_assignments'] = 'No assignments assigned.'

    user_instance = User.objects.get(pk=request.user.id)

    if (user_instance.is_staff):
        data['is_staff'] = 'Trainer'

    return render(request, 'trainingportal/assignments.html', data)


@login_required
def evaluate_assignment(request, assignment_id):

    assignment_form = None
    data = {
        'failure_message': 'Failed to add Task.',
        'assignment_id': assignment_id
    }
    assignment = Assignment.objects.get(pk=assignment_id)
    print("\n\nID:")
    print(assignment.task_id.id)
    if request.method == 'POST':
        assignment_form = EvaluateAssignmentForm(request.POST, request.FILES, instance=assignment)
        if assignment_form.is_valid():
            assignment_form.save()
            data.pop('failure_message', None)
            data["redirect_path"] = '/assignments/?task_id={}'.format(assignment.task_id.id)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    data["assignment_form"] = assignment_form or EvaluateAssignmentForm(instance=assignment)

    return render(request, 'trainingportal/evaluate_assignment.html', data)


@login_required
def submit_assignment(request, assignment_id):

    assignment_form = None
    data = {
        'failure_message': 'Failed to add Task.',
        'assignment_id': assignment_id
    }
    assignment = Assignment.objects.get(pk=assignment_id)
    print("\n\nID:")
    print(assignment.task_id.id)
    if request.method == 'POST':
        assignment_form = SubmitAssignmentForm(request.POST, request.FILES, instance=assignment)
        if assignment_form.is_valid():
            assignment = assignment_form.save(commit=False)
            assignment.status = True
            assignment.save()
            data.pop('failure_message', None)
            data["redirect_path"] = '/assignments/?task_id={}'.format(assignment.task_id.id)
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))

    data["assignment_form"] = assignment_form or SubmitAssignmentForm(instance=assignment)

    return render(request, 'trainingportal/submit_assignment.html', data)


@login_required
def enroll_training(request):
    """ handles requests for registration form and its submission """
    data = {
        'failure_message': 'Failed to add training.',
    }
    if request.method == 'POST':
        selected_training_id = request.POST.get('training')
        selected_trainer_id = request.POST.get('trainer')
        training = Training.objects.get(pk=selected_training_id)
        trainer = Trainer.objects.get(user_id=selected_trainer_id)
        trainee = Trainee.objects.get(user_id=request.user.id)

        if AssignedTraining.objects.filter(trainee_id=trainee.id, training_id=training.id).exists():
            data['already_enrolled'] = "You are already enrolled in this training."
        else:
            assigned_training = AssignedTraining (
                training_id=training,
                trainer_id=trainer,
                trainee_id=trainee
            )
            assigned_training.save()
            return redirect(home)

    trainings = Training.objects.all()
    data['trainings'] = trainings

    trainers = User.objects.filter(is_staff=True)
    data['trainers'] = trainers
    return render(request, 'trainingportal/enroll_training.html', data)


@login_required
def contact_us(request):
    return render(request, 'trainingportal/contact.html')