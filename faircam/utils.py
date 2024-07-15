#!/usr/bin/env python3

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
