import os


def export_vars(request):
    return {
        'OAUTH_CLIENT_ID': os.getenv('OAUTH_CLIENT_ID'),
        'OAUTH_CLIENT_SECRET': os.getenv('OAUTH_CLIENT_SECRET'),
    }
