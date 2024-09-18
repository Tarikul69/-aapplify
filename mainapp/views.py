from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .models import Service
from django.shortcuts import render, get_object_or_404

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html')

class BlogView(View):
    def get(self, request):
        return render(request, 'pages/blog.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html')

class FAQView(View):
    def get(self, request):
        return render(request, 'pages/faq.html')

class ServiceView(View):
    def get(self, request, service_id=None):
        if service_id:
            # Show details for a specific service
            service = get_object_or_404(Service, id=service_id)
            print(service)
            return render(request, 'pages/service_detail.html', {'service': service})

        # List all services
        services = Service.objects.all()
        return render(request, 'pages/services.html', {'services': services})

# class ServiceListView(ListView):
#     model = Service
#     template_name = 'service_list.html'
#     context_object_name = 'services'

# class ServiceDetailView(DetailView):
#     model = Service
#     template_name = 'service_detail.html'
#     context_object_name = 'service'

# class ServiceCreateView(CreateView):
#     model = Service
#     form_class = ServiceForm
#     template_name = 'service_form.html'
#     success_url = reverse_lazy('service-list')

# class ServiceUpdateView(UpdateView):
#     model = Service
#     form_class = ServiceForm
#     template_name = 'service_form.html'
#     success_url = reverse_lazy('service-list')

# class ServiceDeleteView(DeleteView):
#     model = Service
#     template_name = 'service_confirm_delete.html'
#     success_url = reverse_lazy('service-list')