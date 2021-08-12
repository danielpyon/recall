from .forms import SignupForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# mixin for preventing authenticated users from accessing views
class AnonOnlyMixin:
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('app'))
        return super(AnonOnlyMixin, self).get(request, *args, **kwargs)

class SignupFormView(AnonOnlyMixin, FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(SignupFormView, self).form_valid(form)
