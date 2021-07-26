from .forms import SignupForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

class SignupFormView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(SignupFormView, self).form_valid(form)