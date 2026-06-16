def user_info(request):
    return {
        'username': request.session.get('username', 'Гость'),
        'user_role': request.session.get('role', 'Гость'),
    }