from fabric.api import *
import fabric.contrib.project as project
import os
import re
import sys
import glob
import datetime
import SimpleHTTPServer
import SocketServer
from jinja2 import Environment, FileSystemLoader

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'


def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))


def build():
    local('pelican -s pelicanconf.py')


def rebuild():
    clean()
    build()


def regenerate():
    local('pelican -r -s pelicanconf.py')


def serve():
    os.chdir(env.deploy_path)

    PORT = 8000

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        ('', PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()


def reserve():
    build()
    serve()


def preview():
    local('pelican -s publishconf.py')


def cf_upload():
    rebuild()
    local('cd {deploy_path} && '
          'swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
          '-U {cloudfiles_username} '
          '-K {cloudfiles_api_key} '
          'upload -c {cloudfiles_container} .'.format(**env))


@hosts(production)
def publish():
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )


def new_post(title, slug=None, tags='', categories='',
             summary='', author='dongweiming', overwrite="no"):
    if slug is None:
        slug = slugify(title)

    now = datetime.datetime.now()
    month_part = now.strftime("%Y-%m")
    post_date = now.strftime("%Y-%m-%d")

    params = get_params(title, slug, tags, categories, summary, author,
                        post_date)

    out_file = "content/{}/{}.md".format(month_part, slug)
    local("mkdir -p '{}' || true".format(os.path.dirname(out_file)))
    if not os.path.exists(out_file) or overwrite.lower() == "yes":
        render(out_file, **params)
    else:
        print("{} already exists. Pass 'overwrite=yes' to destroy it.".
              format(out_file))


def slugify(text):
    normalized = "".join([c.lower() if c.isalnum() else "-"
                          for c in text])
    no_repetitions = re.sub(r"--+", "-", normalized)
    clean_start = re.sub(r"^-+", "", no_repetitions)
    clean_end = re.sub(r"-+$", "", clean_start)
    return clean_end


def render(destination, **kwargs):
    env = Environment(loader=FileSystemLoader(['.', 'tmpl']))
    template = env.get_template('post.tmpl')
    text = template.render(**kwargs)
    puts("Rendering: {}".format(template, destination))
    with open(destination, "w") as output:
        output.write(text.encode("utf-8"))


def get_params(title, slug, tags, categories, summary, author, post_date):
    params = dict(
        date=post_date,
        modified_date=post_date,
        title=title,
        slug=slug,
        categories=categories,
        summary=summary,
        author=author
    )
    return params


def import_ipynb(filepath, title, slug=None, tags='', categories='',
                 summary='', author='dongweiming', overwrite="no"):
    if slug is None:
        slug = slugify(title)
    now = datetime.datetime.now()
    month_part = now.strftime("%Y-%m")
    post_date = now.strftime("%Y-%m-%d")

    params = get_params(title, slug, tags, categories, summary, author,
                        post_date)

    out_file = "content/{}/{}.ipynb".format(month_part, slug)
    filepath = os.path.expanduser(filepath)
    local("mkdir -p '{}' || true".format(os.path.dirname(out_file)))
    if not os.path.exists(filepath):
        print("Error: {} not exists!".format(filepath))
        return
    if not os.path.exists(out_file) or overwrite.lower() == "yes":
        local("cp {} {}".format(filepath, out_file))
        render(out_file + '-meta', **params)
    else:
        print("{} already exists. Pass 'overwrite=yes' to destroy it.".
              format(out_file))


def edit(article):
    article_files = glob.glob('content/*/{}.*'.format(article))
    if not article_files:
        print("Error: article {} not exists!".format(article))
        return

    if article_files[0].endswith(('md', 'markdown')):
        open_file = article_files[0]
    elif article_files[0].endswith('ipynb'):
        open_file = article_files[1]
    else:
        print("Error: article type[only support markdown/ipynb")
        return
    local("$PELICAN_EDITOR {}".format(open_file))
