from django.db import models
from django.contrib.auth.models import User


class Trainee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, null=False)


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20, null=False)
    experience = models.FloatField(null=False)
    expertise = models.CharField(null=False, max_length=30)


class Training(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=30, null=False, blank=False)
    document = models.FileField(upload_to='tasks_uploads/', null=True)
    duration = models.DurationField(null=True)


class AssignedTraining(models.Model):
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee_id = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    status = models.BooleanField(null=False, blank=False, default=False)


class Task(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=30, null=False, blank=False)
    assignment_file_path = models.FileField(upload_to='tasks_uploads/', null=True)
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee_id = models.ForeignKey(Trainee, on_delete=models.CASCADE)


class Assignment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    due_date = models.DurationField(null=True)
    remarks = models.CharField(max_length=30, null=True)
    score = models.FloatField(null=True)
    assignment_submission_path = models.FileField(upload_to='solution_uploads/', null=True)