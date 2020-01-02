import os
import secrets
from PIL import Image
from flaskblog import app
from datetime import timezone
from bleach import clean
from markupsafe import Markup
import re

def thread_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    i = Image.open(form_picture)
    width, height = i.size
    if width <= 250:
        size = width,width
    else:
        size = 250,250
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg',quality=95)
    return picture_fn

def post_save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    thumb_path = os.path.join(app.root_path, 'static/thumbs', random_hex)
    i = Image.open(form_picture)
    width,height = i.size
    if width <= 125:
        size = width,width
    else:
        size = 125,125
    i.save(picture_path)
    t = Image.open(form_picture).convert('RGB')
    t.thumbnail(size, Image.ANTIALIAS)
    t.save(thumb_path,'jpeg',quality=95)
    return picture_fn

def utc_to_local(utc_d):
    return utc_d.replace(tzinfo=timezone.utc).astimezone()

# functions for white listing html tags in jinja templates
def do_clean(text, **kw):
    """Perform clean and return a Markup object to mark the string as safe.
    This prevents Jinja from re-escaping the result."""
    return Markup(clean(text, **kw))

# regex and replace for greentexting
def greentext(m):
    return f'<span class="greentext">{m.group(0)}</span>'

def greenregex(content):
    return re.sub(r'^>.*',greentext,content,flags=re.MULTILINE)

# regex and replace for href jumping
def href(m):
    jump = int(m.group(0)[2:]) - 1
    if jump < 1:
        jump = 1
    str(jump)
    return f'<a href=#{jump}>{m.group(0)}</a>'

def hrefregex(content):
    return re.sub(r'>>[0-9]*',href,content)

# jijnja filter for moment.js for converting datetime to client timezone
def moment(date):
    return Markup(f'<script>document.write(moment("{str(date)}"+"Z").format("DD/MM/YY(ddd)HH:mm:ss"))</script>')
