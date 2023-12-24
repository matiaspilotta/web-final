from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import PostForm, CommentForm, RegistrationForm, EditionFormulario, AvatarFormulario
from .models import UserProfile, Post, Comment, Avatar
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post, UserProfile
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .forms import CommentForm




def home(request):
    avatar_url = ""
    
    if request.user.is_authenticated:
        usuario = request.user
        avatar = Avatar.objects.filter(user=usuario).last()
        
        if avatar and avatar.imagen:
            avatar_url = avatar.imagen.url

    return render(request, "home.html", context={"avatar_url": avatar_url})


def nosotros(request):
    return render(request, "nosotros.html")

def contactos(request):
    return render(request, "contactos.html")



###############POST,COMENTARIOS#################



def post(request):
    posts = Post.objects.all().order_by('-created_at')
    users = UserProfile.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter(Q(user__username__icontains=query) | Q(caption__icontains=query))

    comment_form = CommentForm()

    return render(request, 'post.html', {'posts': posts, 'users': users, 'query': query, 'comment_form': comment_form})






@login_required
def upload_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)

        if post_form.is_valid() and comment_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            messages.success(request, 'Publicación y comentario cargados exitosamente.')
            return redirect('home')
        else:
            messages.error(request, 'Hubo un error al procesar el formulario. Por favor, corrige los errores.')
    else:
        post_form = PostForm()
        comment_form = CommentForm()

    return render(request, 'upload_post.html', {'post_form': post_form, 'comment_form': comment_form})





@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Tu comentario fue agregado con éxito.')
        else:
            messages.error(request, 'Hubo un error al agregar tu comentario.')
    return redirect("post")



@login_required
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if post.user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                messages.success(request, 'Publicación editada correctamente.')
                return redirect('home')
        else:
            form = PostForm(instance=post)
        
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        messages.error(request, 'No tienes permisos para editar esta publicación.')
        return redirect('home')


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.user == request.user:
        post.delete()
        messages.success(request, 'Publicación eliminada exitosamente.')
    else:
        messages.error(request, 'No tienes permisos para eliminar esta publicación.')
    return redirect('home')


########################### Registro,Login,Logout,############################
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(
                request,
                "registro_exitoso.html",
                {"mensaje": f"Usuario creado: {user}"}
            )
    else:
        form = RegistrationForm()
    return render(request, 'registro.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if user.is_staff:
                   
                    return redirect('admin_dashboard')
                else:
                    
                    messages.success(request, '¡Inicio de sesión exitoso!')
                    return redirect('mi_cuenta')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})




def user_logout(request):
    logout(request)
    return redirect('home')


##############################PERFIL###########################


@login_required
def editar_perfil(request):
    usuario = request.user
    avatar = Avatar.objects.filter(user=usuario).last()
    avatar_url = avatar.imagen.url if avatar and avatar.imagen else ""

    if request.method == "POST":
        formulario = EditionFormulario(request.POST, instance=usuario)
        avatar_formulario = AvatarFormulario(request.POST, request.FILES, instance=avatar)

        if formulario.is_valid() and avatar_formulario.is_valid():
            formulario.save()
            avatar_formulario.save()
            return redirect("mi_cuenta")  # Ajusta esto a la URL correcta
    else:
        formulario = EditionFormulario(instance=usuario)
        avatar_formulario = AvatarFormulario(instance=avatar)

    return render(
        request,
        "editar_perfil.html",
        context={"form": formulario, "avatar_form": avatar_formulario, "usuario": usuario, "avatar_url": avatar_url}
    )


@login_required
def crear_avatar(request):

    usuario = request.user

    if request.method == "GET":
        formulario = AvatarFormulario()
        return render(
            request,
            "core/crear_avatar.html",
            context={"form": formulario, "usuario": usuario}
        )
    else:
        formulario = AvatarFormulario(request.POST, request.FILES)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Avatar(user=usuario, imagen=informacion["imagen"])
            modelo.save()
            return redirect("core:inicio")


def mi_cuenta(request):
    return render(request, 'mi_cuenta.html')

@login_required
def perfil(request):
    perfil_user = UserProfile.objects.get(user=request.user)
    return render(request, 'perfil.html', {'perfil_user': perfil_user})



#######################ADMIN###############################
def admin_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_required)
def admin_dashboard(request):
    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard.html', {'posts': posts, 'comments': comments, 'usuarios': usuarios})

@user_passes_test(admin_required)
def admin_delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'El post ha sido borrado exitosamente.')
    return redirect('admin_dashboard')

@user_passes_test(admin_required)
def admin_delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'El comentario ha sido borrado exitosamente.')
    return redirect('admin_dashboard')

@user_passes_test(admin_required)
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'El usuario ha sido borrado exitosamente.')
    return redirect('admin_dashboard')
