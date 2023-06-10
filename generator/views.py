import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, FileResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, UpdateView
from .models import *
from .forms import *
from faker import Faker
import csv


# Create your views here.

class DataSchemasView(LoginRequiredMixin, TemplateView):
    template_name = 'generator/data_schemas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Data Schemas'
        context['schemas'] = SchemaModel.objects.filter(user=self.request.user)
        return context


class DataSetsView(FormView):
    template_name = 'generator/data_sets.html'
    form_class = GenerateFile
    success_url = reverse_lazy('data_schemas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Data Sets'
        context['schema'] = SchemaModel.objects.get(pk=self.kwargs['pk'])
        context['columns'] = SchemaColumn.objects.filter(model_id=self.kwargs['pk'])
        context['data_sets'] = DataSetModel.objects.filter(schema_id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        rows = self.request.POST['rows']
        fake = Faker()

        data = []
        data_type = [i.data_type for i in context['columns']]
        names = [i.name for i in context['columns']]
        order = [i.order for i in context['columns']]

        for i in range(0, int(rows)):
            row = []
            for j in range(len(data_type)):
                if data_type[j] == 'Full name':
                    row.append(str(fake.name()))
                elif data_type[j] == 'Phone number':
                    row.append(fake.phone_number())
                elif data_type[j] == 'Company name':
                    row.append(str(fake.company()))
                elif data_type[j] == 'Job':
                    row.append(str(fake.job()))
                elif data_type[j] == 'Date':
                    row.append(str(fake.date()))
            data.append(row)

        headers = [i.name for i in context['columns']]
        print(headers)

        file_name = f"data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        # Записываем данные в файл
        if context['schema'].string_character == '"':
            writer = csv.writer(response, delimiter=context['schema'].column_sep, quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC)
        else:
            writer = csv.writer(response, delimiter=context['schema'].column_sep, quotechar="'",
                                quoting=csv.QUOTE_NONNUMERIC)

        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

        # Сохраняем файл на сервере
        with open(f"media/files/{file_name}", "w") as file:
            file.write(response.content.decode("utf-8"))

        file_model = DataSetModel(file=f"files/{file_name}", schema_id=context['schema'].pk,
                                  user=self.request.user)
        file_model.save()

        return response


def download_file(request, pk):
    data_set = DataSetModel.objects.get(pk=pk)
    response = HttpResponse(data_set.file)
    response['Content-Disposition'] = f'attachment; filename="{data_set.file.name}"'
    return response


def delete_schema(request, pk):
    SchemaModel.objects.get(pk=pk).delete()
    return redirect('data_schemas')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = 'data_schemas'


class SchemaCreateView(CreateView):
    model = SchemaModel
    form_class = SchemaForm
    template_name = 'generator/new_schema.html'
    success_url = reverse_lazy('data_schemas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_column_form'] = ColumnsForm()
        if self.request.POST:
            context['schema_column_formset'] = ColumnFormSet(self.request.POST)
        else:
            context['schema_column_formset'] = ColumnFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        column = context['schema_column_formset']
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = form.save()
        if column.is_valid():
            column.instance = self.object
            column.save()
        return super().form_valid(form)


class SchemaUpdateView(UpdateView):
    model = SchemaModel
    form_class = SchemaForm
    template_name = 'generator/test.html'
    success_url = reverse_lazy('data_schemas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_column_form'] = ColumnsForm()
        context['pk'] = self.kwargs['pk']
        print(self.kwargs['pk'])
        if self.request.POST:
            context['schema_column_formset'] = ColumnFormSet(self.request.POST)
        else:
            context['schema_column_formset'] = ColumnFormSet(instance=self.object)
            context['header'] = self.object
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        column = context['schema_column_formset']
        self.object.save()
        if column.is_valid():
            column.instance = self.object
            column.save()
        return super().form_valid(form)


class AddColumn(View):

    def post(self, request, pk):
        form = ColumnsForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.model = SchemaModel.objects.get(pk=pk)
            obj.save()
        return redirect('show_schema', pk)


def delete_column(request, pk):
    column = SchemaColumn.objects.get(pk=pk)
    parent = column.model.pk
    column.delete()
    return redirect('show_schema', parent)
