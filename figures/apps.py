from django.apps import AppConfig

class FiguresConfig(AppConfig):
    # This is standard for modern Django projects
    default_auto_field = 'django.db.models.BigAutoField'
    
    # This is the critical line: it tells Django the name of the app
    # which must match the directory name 'figures'.
    name = 'figures'