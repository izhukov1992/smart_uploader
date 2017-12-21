from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from uploader.models import StorageFile
from uploader.forms import StorageFileForm
from uploader.utils import getSHA1Digest
from .models import UserFile


class BaseView(TemplateView):
    """Base template view
    """

    # Define context dictionary
    context = {}

    def get(self, request):
        """Handle GET-query. Render template. Return HTML-page
        """

        return render(request, self.template_name, self.context)


class IndexView(BaseView):
    """User storage view
    """
    
    template_name = 'account/index.html'

    def get(self, request):
        """Handle GET
        """

        if request.user.is_anonymous:
            return redirect('account:login')

        # Find all files in user storage 
        files = UserFile.objects.filter(user=request.user)
        # Create file uploading form
        form = StorageFileForm()

        # Update context
        self.context.update({'files': files, 'form': form})

        # Call GET handler of base class
        return super(IndexView, self).get(request)


class UploadView(BaseView):
    """File uploading view
    """
    
    template_name = 'account/upload.html'

    def post(self, request):
        """Handle POST
        """

        if request.user.is_anonymous:
            # Redirect to login page if anonymous
            return redirect('account:login')

        if UserFile.objects.filter(user=request.user).count() > 99:
            # If user has more than 99 files in storage return limitation alert
            self.context.update({'limit': True})
            return super(UploadView, self).get(request)

        # Extract data from form
        form = StorageFileForm(request.POST, request.FILES)
        if not form.is_valid():
            # If data is not valid return errors alerts
            self.context.update({'form': form})
            return super(UploadView, self).get(request)

        # Clean context
        self.context = {}

        # Get uploaded file
        file_uploaded = request.FILES['file']
        # Generate SHA-1 hash
        digest = getSHA1Digest(file_uploaded)
        try:
            # Try to find duplicates of uploaded file by hash
            file_duplicate = StorageFile.objects.get(sha1=digest)
            # Remember duplicate if exists
            file_new = file_duplicate
        except Exception:
            # File is unique
            file_duplicate = None
            # Create new physical file entry
            file_new = StorageFile(file=file_uploaded, sha1=digest)
            file_new.save()

        # Create mirror of file in user storage
        file_user = UserFile(user=request.user, file=file_new, display_name=file_uploaded)
        file_user.save()
        self.context.update({'file_new': file_user})

        if file_duplicate:
            # Find all mirrors of physical file in users storages if file in not unique.
            # Exclude new mirror from list
            file_duplicates = UserFile.objects.filter(file=file_duplicate).exclude(pk=file_user.pk)
            self.context.update({'file_duplicates': file_duplicates})

        return super(UploadView, self).get(request)


class DeleteView(BaseView):
    """File deleting view
    """
    
    template_name = 'account/delete.html'

    def get(self, request, file_id):
        """Handle GET
        """

        if request.user.is_anonymous:
            # Redirect to login page if anonymous
            return redirect('account:login')

        # Find link of file in users storages by ID
        file_user = UserFile.objects.get(pk=file_id)
        if file_user.file.userfile_set.count() < 2:
            # If there is only one link, delete physical file
            file_user.file.file.delete()
            # Delete entry from databse
            file_user.file.delete()
        # Delete link
        file_user.delete()

        return super(DeleteView, self).get(request)


class JoinView(BaseView):
    """User registration view
    """
    
    template_name = 'account/join.html'

    def get(self, request):
        """Handle GET
        """

        if request.user.is_authenticated:
            # Redirect to dashboard page if authenticated
            return redirect('account:index')

        # Create user registration form
        form = UserCreationForm()
        self.context.update({'form': form})

        return super(JoinView, self).get(request)

    def post(self, request):
        """Handle POST
        """

        if request.user.is_authenticated:
            # Redirect to dashboard page if authenticated
            return redirect('account:index')

        # Extract user registration form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            # If data is valid create user
            form.save()
            # ... then login
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            # ... then redirect to dashboard
            return redirect('account:index')

        # If data is not valid return error alerts
        self.context.update({'form': form})

        return super(JoinView, self).get(request)


class LoginView(BaseView):
    """User login view
    """
    
    template_name = 'account/login.html'

    def get(self, request):
        """Handle GET
        """

        if request.user.is_authenticated:
            # Redirect to dashboard page if authenticated
            return redirect('account:index')

        # Create user login form
        form = AuthenticationForm()
        self.context.update({'form': form})

        return super(LoginView, self).get(request)

    def post(self, request):
        """Handle POST
        """

        if request.user.is_authenticated:
            # Redirect to dashboard page if authenticated
            return redirect('account:index')

        # Extract user login form
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # If data is valid login
            login(request, form.get_user())
            # ... then redirect to dashboard
            return redirect('account:index')

        # If data is not valid return error alerts
        self.context.update({'form': form})

        return super(LoginView, self).get(request)


def logout(request):
    """User logout view
    """

    # Logout user
    auth.logout(request)
    
    # Redirect to login page
    return redirect('account:login')
