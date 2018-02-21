from django.db import models
from django.contrib.auth.models import User

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)


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
    due_date = models.DateField(null=True)


class AssignedTraining(models.Model):
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee_id = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    status = models.BooleanField(null=False, blank=False, default=False)


class Task(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=30, null=False, blank=False)
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    trainer_id = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    trainee_id = models.ForeignKey(Trainee, on_delete=models.CASCADE)


class Assignment(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False, blank=False, default=" ")
    description = models.CharField(max_length=30, null=False, blank=False, default=" ")
    due_date = models.DateField(null=True)
    remarks = models.CharField(max_length=30, null=True)
    score = models.FloatField(null=True)
    assignment_submission_path = models.FileField(upload_to='solution_uploads/', null=True)
    assignment_file_path = models.FileField(upload_to='tasks_uploads/', null=True)