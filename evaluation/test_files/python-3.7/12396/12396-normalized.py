def create(self, request):
    """
        Change password for logged in django staff user
        """
    password_form = PasswordChangeForm(request.user, data=request.data)
    if not password_form.is_valid():
        raise serializers.ValidationError(password_form.errors)
    password_form.save()
    update_session_auth_hash(request, password_form.user)
    return Response(status=status.HTTP_204_NO_CONTENT)