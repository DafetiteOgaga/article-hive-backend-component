from django.shortcuts import render

def custom_error_view(request, exception=None, status_code=500):
    error_messages = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Page Not Found",
        500: "Internal Server Error",
    }
    error_message = error_messages.get(status_code, "Error")
    error_description = {
        400: "The request could not be understood by the server due to malformed syntax.",
        401: "You must be logged in to view this page.",
        403: "You do not have permission to access the requested resource.",
        404: "The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.",
        500: "The server encountered an internal error and was unable to complete your request.",
    }.get(status_code, "An unexpected error occurred.")

    context = {
        'pgname': error_message,
        'error_code': status_code,
        'error_message': error_message,
        'error_description': error_description,
    }
    return render(request, 'errors/error_page.html', context, status=status_code)