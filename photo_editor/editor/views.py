from email.mime import image

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import ImageUploadForm

from django.contrib.auth.decorators import login_required
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Image
from django.utils.decorators import method_decorator

from .models import Image



def edit_image(request, image_id):
    # Retrieve image from database using image_id
    # Pass the image data to the template
    return render(request, 'editor/edit_image.html', {'image': image})

def download_image(request, image_id):
    # Retrieve edited image from database using image_id
    # Serve the image for download
    pass

class HomeView(View):
    def get(self, request):
        return render(request, 'editor/home.html')

class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging line
            user = form.save()
            print(f"User {user.username} created")  # Debugging line
            login(request, user)
            return redirect('home')
        else:
            print("Form is not valid")  # Debugging line
            print(form.errors)  # Debugging line
        return render(request, 'registration/signup.html', {'form': form})



@login_required
@csrf_exempt
def save_edited_image(request):
    if request.method == 'POST':
        data_url = request.POST.get('image')
        if data_url:
            format, imgstr = data_url.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'edited_image.{ext}'
            file_data = ContentFile(base64.b64decode(imgstr), name=file_name)

            # Save the file to the server
            with open(f'media/{file_name}', 'wb') as f:
                f.write(file_data.read())

            # At this point, you need to update your database entry
            # Example assuming you have Image model with edited_image field:
            edited_image = Image.objects.create(
                user=request.user,
                edited_image=f'images/edited/{file_name}'  # adjust path if necessary
            )

            return JsonResponse({'status': 'success', 'file_name': file_name})
        return JsonResponse({'status': 'failed', 'message': 'No image data'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user  # Assign the logged-in user
            instance.save()
            return redirect('image_list')  # Redirect to image list page
    else:
        form = ImageUploadForm()
    return render(request, 'editor/upload_image.html', {'form': form})



@login_required
def image_list(request):
    images = Image.objects.filter(user=request.user)
    return render(request, 'editor/image_list.html', {'images': images})

@login_required
def download_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    file_path = image.original_image.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/jpeg')  # Adjust content_type based on image type
        response['Content-Disposition'] = 'attachment; filename=' + image.original_image.name
        return response