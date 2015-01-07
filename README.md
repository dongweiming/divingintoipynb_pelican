pelican_blog
============

a pelican blog that use ipython notebook format

Run it
-----

    cd
    git clone --recursive https://github.com/dongweiming/divingintoipynb_pelican
    git clone https://github.com/dongweiming/diving_into_ipynb
    cd divingintoipynb_pelican
    # create post
    fab new_post:post_title # title is `post_title`
    fab new_post:post_title2,slug=with_other_slug # title is `post_title2`, but filename is `content/2015-01/with_other_slug.md`
    fab new_post:post_title,overwrite=yes # overwrite the `content/2015-01/post_title.md`

    # 1. use liquid_tags.notebook
    # edit `content/2015-01/post_title.md` and add content like this:
    `{% notebook xx/path/yy.ipynb %}`
    # 2. use the pure ipynb
    fab import_ipynb:~/diving_into_ipynb/python_2/highchart.ipynb,"ipynb title"
    # edit `content/2015-01/ipynb-title.ipynb-meta`. also you can use `fab edit:article`
    export PELICAN_EDITOR='emacsclient'
    # fab edit:double11
