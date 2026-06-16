from django.shortcuts import redirect

def role_required(allowed_roles = []):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            role = get_user_role(request)
            if role not in allowed_roles:
                return redirect('login')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

def get_user_role(request):
    return request.session.get('role', 'Гость')