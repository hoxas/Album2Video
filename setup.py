from setuptools import setup, find_packages
    
appversion = '0.0.1'


setup(
    name = 'album2video',
    version = appversion,
    description = 'album2video creates an albumvideo(with img as bg) from tracks w/ timestamp output',
    long_description = open('README.rst').read(),
    url = 'http://github.com/hoxas/Album2Video',
    download_url = 'https://github.com/hoxas/Album2Video/archive/refs/tags/v0.0.1.tar.gz',
    author = 'hoxas',
    author_email = 'hoxas@live.com',
    license = 'unlicense',
    classifiers = [
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: Public Domain',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.9'
    ],
    keywords = ['audio', 'album', 'video', 'music', 'cli', 'albums', 'edit', 'timestamp', 'youtube'],
    python_requires = '>=3.6',
    install_requires = [
        'docopt==0.6.2',
        'moviepy==1.0.3'
    ],
    packages = find_packages(exclude="tests"),
    entry_points = {
        'console_scripts': [
            'album2video = album2video.__main__:main'
        ]
    }
)
