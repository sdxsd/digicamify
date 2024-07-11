#!/usr/bin/env python3

# DIGICAMIFY IS LICENSED UNDER THE GNU GPLv3
# Copyright (C) 2024 Will Maguire

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# The definition of Free Software is as follows:
# 	- The freedom to run the program, for any purpose.
# 	- The freedom to study how the program works, and adapt it to your needs.
# 	- The freedom to redistribute copies so you can help your neighbor.
# 	- The freedom to improve the program, and release your improvements
#   - to the public, so that the whole community benefits.

# A program is free software if users have all of these freedoms.

import os
from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from . import process_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif'}

def create_app():
    digicamify = Flask(__name__)
    digicamify.config.from_mapping(
        UPLOAD_FOLDER="digicamify/static/uploads/",
        PROCESSED_FOLDER="digicamify/static/processed/"
    )

    @digicamify.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'file' not in request.files:
                # flash('No file given.')
                return (redirect(request.url))
            file = request.files['file']
            if file.filename == '':
                # flash('No selected file.')
                return (redirect(request.url))

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(digicamify.config['UPLOAD_FOLDER'], filename))
                print(os.path.join(digicamify.config['UPLOAD_FOLDER'], filename))
                process_image.process_and_save_image(filename, digicamify.config['UPLOAD_FOLDER'], digicamify.config['PROCESSED_FOLDER'])
                os.remove(os.path.join(digicamify.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('view_file', name=filename))

        return render_template('index.html')

    @digicamify.route('/view/<name>')
    def view_file(name):
        dir = os.path.abspath(digicamify.config['PROCESSED_FOLDER'])
        return render_template('image.html', img=("processed/" + name))

    return digicamify

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
