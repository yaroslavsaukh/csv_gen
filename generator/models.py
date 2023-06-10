from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse


class SchemaModel(models.Model):
    SEPARATORS = (
        (',', ','),
        (';', ';')
    )
    STRING_CHARACTER = (
        ("'", "'"),
        ('"', '"')
    )
    name = models.CharField(max_length=255)
    column_sep = models.CharField(max_length=10, choices=SEPARATORS)
    string_character = models.CharField(max_length=10, choices=STRING_CHARACTER)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_schema', kwargs={'pk': self.pk})


class SchemaColumn(models.Model):
    DATA_TYPES = (
        ('Full name', 'Full name'),
        ('Phone number', 'Phone number'),
        ('Company name', 'Company name'),
        ('Job', 'Job'),
        ('Date', 'Date')
    )

    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=100, choices=DATA_TYPES)
    order = models.IntegerField(default=1)
    model = models.ForeignKey(SchemaModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DataSetModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/')
    schema = models.ForeignKey(SchemaModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



