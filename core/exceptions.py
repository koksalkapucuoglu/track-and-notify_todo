from rest_framework.exceptions import APIException, ValidationError


class ExceptionHandler(ValidationError):
    default_code = ''
    default_detail = 'INVALID DATA'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)


class WrongOldPasswordException(ExceptionHandler):
    default_code = 1001
    default_detail = 'Old password is wrong'


class ShortNewPasswordException(ExceptionHandler):
    default_code = 1002
    default_detail = 'New password must be least 8 character'


class PasswordsDoNotMatchException(ExceptionHandler):
    default_code = 1003
    default_detail = 'Passwords do not match'


class UserDoesNotExistWithEmailException(ExceptionHandler):
    default_code = 1004
    default_detail = 'User with this email does not exist'


class ResetPasswordTokenHasExpiredException(ExceptionHandler):
    default_code = 1005
    default_detail = 'Reset password link has expired'


class InvalidResetPasswordTokenException(ExceptionHandler):
    default_code = 1004
    default_detail = 'Invalid reset password token'


def prettier_exc(errors=None, message_text=None):
    message = {
        'detail': []
    }
    if errors is None:
        message['detail'] = message_text
        return message

    if isinstance(errors, dict):
        for key, value in errors.items():
            message['detail'] = value[0]
    return message
