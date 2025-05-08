from django.shortcuts import render, redirect
from .models import SiteInfo, Testimonial
from .forms import TestimonialForm

from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def about_view(request):
    site_info = SiteInfo.objects.first()
    testimonials = Testimonial.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = TestimonialForm(request.POST)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.user = request.user
                testimonial.save()
                return redirect('info:info')
        else:
            return redirect('login')
    else:
        form = TestimonialForm()

    return render(request, 'info/about.html', {
        'site_info': site_info,
        'testimonials': testimonials,
        'form': form,
    })


