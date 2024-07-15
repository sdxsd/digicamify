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

from flask import Blueprint, request, redirect, render_template, abort, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from jinja2 import TemplateNotFound
from faircam.db import get_db
from . import utils

posts = Blueprint('posts', __name__, template_folder='templates/posts')

@posts.route('/posts/')
def view_posts():
    return (render_template('posts.html'))

@posts.route('/create_post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No image uploaded...')
            return redirect(request.url)
        image = request.files['file']
        if image.filename == '' or image.filename == None or not utils.allowed_file(image.filename):
            flash('Invalid or No image uploaded...')
            return redirect(request.url)

        title = request.form['title']
        filename = secure_filename(image.filename)
        deletion_pass = request.form['deletion_pass']
        if not title:
            flash('No title given...')
            redirect(request.url)

        db = get_db()
        try:
            if not deletion_pass:
                db.execute("INSERT INTO post (title, filename, posted) VALUES (?, ?, ?)",
                       (title, filename, datetime.now(timezone.utc)))
            else:
                db.execute("INSERT INTO post (title, filename, posted, deletion_pass) VALUES (?, ?, ?, ?)",
                           (title, filename, datetime.now(timezone.utc), generate_password_hash(deletion_pass)))
            db.commit()
        except db.IntegrityError:
            error = "Post with the same name or filename already exists."
            flash(error)
        else:
            return (redirect(url_for('posts.view_posts')))
    return render_template('create_post.html')
