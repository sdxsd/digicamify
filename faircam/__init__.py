#!/usr/bin/env python3

# FAIRCAM IS LICENSED UNDER THE GNU GPLv3
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

from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from faircam.posts import posts
from flask_moment import Moment
from . import process_image
from . import utils
from . import db
import tomllib
import os

moment = Moment()

def create_app():
    faircam = Flask(__name__, instance_relative_config=True)
    faircam.config.from_mapping(
        SECRET_KEY='dev', # FIXME: Must be changed before live!
        MASTER_DELETION_PASS='devpass',
        UPLOAD_FOLDER="faircam/static/uploads/",
        PROCESSED_FOLDER="faircam/static/processed/",
        DATABASE=os.path.join(faircam.instance_path, 'posts.sqlite')
    )
    moment.init_app(faircam)
    db.init_app(faircam)

    # Blueprints.
    faircam.register_blueprint(posts)
    @faircam.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'file' not in request.files:
                return (redirect(request.url))
            file = request.files['file']
            if file.filename == '':
                return (redirect(request.url))

            if file and utils.allowed_file(file.filename):
                process_image.process_and_save_image(file, faircam.config['PROCESSED_FOLDER'])
                return redirect(url_for('view_file', name=secure_filename(file.filename)))

        return render_template('faircam/index.html')

    @faircam.route('/view/<name>')
    def view_file(name):
        dir = os.path.abspath(faircam.config['PROCESSED_FOLDER'])
        return render_template('faircam/image.html', img=("processed/" + name))

    return faircam
