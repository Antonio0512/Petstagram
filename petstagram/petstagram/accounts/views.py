from django.contrib.auth import views as auth_views, login, authenticate
from django.core.paginator import Paginator
from django.views import generic as views
from django.urls import reverse_lazy
from ..accounts.forms import PetstagramUserCreateForm
from ..accounts.models import PetstagramUser


class UserRegisterView(views.CreateView):
    form_class = PetstagramUserCreateForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('page-home')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"]
        )
        login(self.request, user)

        return to_return


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'


class UserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('page-login')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = PetstagramUser

    def get_photos_page(self):
        return self.request.GET.get('page', 1)

    def get_paginated_photos(self):
        page = self.get_photos_page()
        photos = self.object.photo_set.all()
        paginator = Paginator(photos, 2)
        return paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_likes_count = self.object.like_set.count()
        total_pets_count = self.object.pet_set.count()
        total_photos_count = self.object.photo_set.count()

        context['is_owner'] = self.request.user == self.object
        context['total_likes_count'] = total_likes_count
        context['total_pets_count'] = total_pets_count
        context['total_photos_count'] = total_photos_count
        context['paginated_photos'] = self.get_paginated_photos()
        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = PetstagramUser
    fields = ['first_name', 'last_name', 'email', 'profile_picture', 'gender']

    def get_success_url(self):
        return reverse_lazy('profile-page', kwargs={
            'pk': self.request.user.pk
        })


class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = PetstagramUser
    success_url = reverse_lazy('page-home')
