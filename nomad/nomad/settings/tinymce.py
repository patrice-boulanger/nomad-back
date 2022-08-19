TINYMCE_DEFAULT_CONFIG = {
    'height': 400,
    'width': 1080,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
       textcolor save link image media preview codesample contextmenu
       table code lists fullscreen insertdatetime nonbreaking
       contextmenu directionality searchreplace wordcount visualblocks
       visualchars code fullscreen autolink lists charmap print hr
       anchor pagebreak
    ''',
    'toolbar1': '''
       fullscreen preview bold italic underline | fontselect,
       fontsizeselect | forecolor backcolor | alignleft alignright |
       aligncenter alignjustify | indent outdent | bullist numlist table |
       | link image media | codesample |
    ''',
    'toolbar2': '''
       visualblocks visualchars |
       charmap hr pagebreak nonbreaking anchor | code |
    ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
