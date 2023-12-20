from functools import reduce
from operator import or_

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q

from common.views import TitleMixin
from todo.models import Todo
from todo.forms import Form, EditForm


class IndexView(TitleMixin, TemplateView):
    template_name = 'todo/index.html'
    tittle = 'Home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Todo.objects.all()
        return context


def delete_record(request, pk):
    record = Todo.objects.get(pk=pk)
    record.delete()
    return redirect('index')


class EditRecordView(UpdateView):
    template_name = 'todo/edit_record.html'
    model = Todo
    form_class = Form
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return get_object_or_404(Todo, pk=self.kwargs['pk'])


class AddRecordView(View):
    template_name = 'todo/add_record.html'
    succsess_url = 'todo/index.html'

    def get(self, request):
        form = Form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = Form(request.POST)
        if form.is_valid():
            # Создаем запись в основной таблице
            Todo.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                completed=form.cleaned_data['completed'],
            )

            return redirect('index')
        return render(request, self.template_name, {'form': form})


class SearchView(View):
    template_name = 'todo/search.html'
    results_template_name = 'todo/search_result.html'

    def get(self, request, *args, **kwargs):
        form = Form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = Form(request.POST)

        if form.is_valid():
            # Создаем список Q-объектов для фильтрации записей
            q_filters = []

            # Добавляем условия в список, только если соответствующее поле заполнено
            for field_name, field_value in form.cleaned_data.items():
                if field_value:
                    q_filters.append(Q(**{field_name: field_value}))

            # Исключаем результаты, если хотя бы одно условие не выполняется
            search_results = Todo.objects.all()

            if q_filters:
                # Используем оператор | для объединения Q-объектов с условием "или"
                combined_q_filters = Q()

                for q_filter in q_filters:
                    combined_q_filters |= q_filter

                search_results = search_results.filter(combined_q_filters)

            # Проверяем, есть ли результаты поиска
            if not search_results.exists():
                return render(request, self.results_template_name, {'no_results': True})

            # Возвращаем результаты поиска в шаблон
            return render(request, self.results_template_name, {'results': search_results})

        # Возвращаем форму с ошибками, если форма не прошла валидацию
        return render(request, self.template_name, {'form': form})
