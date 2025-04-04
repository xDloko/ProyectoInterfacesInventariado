from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import sales
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#dashboard view with class based view
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/sales_dashboard.html'
    model = sales
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context