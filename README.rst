album2video
===============

receives tracks and img and outputs albumvideo with tracknames subtitle & timestamps.txt

Description
-----------

**album2video** is a CLI to create album videos with img as bg & tracknames subtitles (useful for uploading albumvideos to yt)

**Python 3.9**

Installation
------------

From PyPI
~~~~~~~~~

``pip3 install album2video``

OR w/ pipx (recommended)

``pipx install album2video``

From Source
~~~~~~~~~~~

1. Clone the project or `download and extract the zip <https://github.com/hoxas/Album2Video/archive/master.zip>`_
2. ``cd`` to the project directory containing the ``setup.py``
3. ``python setup.py install`` or ``pipx install .``

Details
-------

::

    Usage:
    album2video [options] [URL...]

    Arguments:
        URL                     Path to folder w/ tracks & img 
                                            or
                                    folderpath + img path
                                            or
                                individual trackpaths + img path

    Examples:
        album2video --help
        album2video path/to/folder
        album2video --title TheAlbumTitle path/to/mp3 path/to/mp3 path/to/img 

* Requires path to img or path to folder with img

(Needs ImageMagick installed)
Windows users will have to define magick.exe filepath with album2video --imgmagick path/to/magick.exe

Options
-------

::

    Options:
        -h --help               Show this screen
        -v --version            Show version
        -d --debug              Verbose logging
        -n --notxt              Don't output timestamps.txt
        -t --test               Run program without writing videofile (for test purposes)
        --title=TITLE           Set title beforehand
        --imgmagick=PATH        Set path to ImageMagick & exit


