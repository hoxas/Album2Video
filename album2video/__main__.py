"""
album2video

Usage:
    album2video [options] [URL...]

Options:
    -h --help               Show this screen
    -v --version            Show version
    -d --debug              Verbose logging
    -n --notxt              Don't output timestamps.txt
    -t --test               Run program without writing videofile (for test purposes)
    --title=TITLE           Set title beforehand
    --imgmagick=PATH        Set path to ImageMagick & exit



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
"""

import os, pkg_resources, docopt, re, logging
log = logging.getLogger(__name__)

# hiding pil debug logs
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

__version__ = pkg_resources.require('album2video')[0].version

arguments = docopt.docopt(__doc__, version=f"Album2Video {__version__}")

from pathlib import Path
from .PathTool import getPath
from .config import parsing

cfg = parsing()

if arguments['--debug']:
    LOG_FORMAT = "\n%(levelname)s | %(asctime)s §\n%(message)s\n"
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT)

    def listItems(itemlist):
        itemstring = '-'*32+'\n'
        for item in itemlist:
            itemstring += f"{item}\n"
        itemstring += '-'*32+'\n'
        return itemstring
    
    log.debug(f'Docopt:\n {arguments}')

    def listDict(dict: dict):
        itemstring = '-'*32+'\n'
        for key, value in dict.items():
            itemstring += f"{key}: {value} - type: {type(value)}\n"
        itemstring += '-'*32+'\n'
        return itemstring
    
    log.debug(f'Config:\n {listDict(cfg)}')


if arguments['--imgmagick']:
    import moviepy

    # moviepy.__file__ points to moviepy\__init__.py
    # so we split '__init__.py' from pathname
    moviepy_path = os.path.split(moviepy.__file__)[0]
    # join it with the config filename
    moviepy_config = os.path.join(moviepy_path, 'config_defaults.py')

    arguments['--debug'] and log.debug('MoviePyConfig: ' + moviepy_config)

    # assign imgmagick path variable
    imgmagick = getPath(arguments['--imgmagick'])
    
    # line with imagemagick_binary found starts false
    found = False

    with open(moviepy_config, 'r') as f:
        lines = f.readlines()
    
    with open(moviepy_config, 'w') as f:
        for index, line in enumerate(lines):
            if line.startswith('IMAGEMAGICK_BINARY'):
                arguments['--debug'] and log.debug(f'Setting IMAGEMAGICK_BINARY path to: {imgmagick}')
                lines[index] = f"IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', '{imgmagick}')"
                found = True
        
        if found == False:
            arguments['--debug'] and log.debug(f'Creating IMAGEMAGICK_BINARY = {imgmagick}')
            lines.append(f"IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', '{imgmagick}')")

        f.writelines(lines)
    
    print('ImgMagick set... exiting\n')
    exit()

try:
    from moviepy import editor as mpy
except OSError as e:
    print(e)
    print('\nSet proper imagemagick_binary path with: album2video --imgmagick path/to/binary\n')
    exit()



def main():
    """
    Main Program
    """
    songs = []
    bgpath = ''
    
    ### Checking args and parsing again
    if arguments['URL']:
        for path in arguments['URL']:
            path = getPath(path)
            
            ### If path is directory list it
            if os.path.isdir(path):
                folder = path
                print(f'Searching folder -> {folder}')

                foldercontent = os.listdir(folder)

                arguments['--debug'] and log.debug(f'Folder content:\n{listItems(foldercontent)}')

                ### For file in directory... parse by extension
                for file in foldercontent:
                    if file.lower().endswith(cfg['imgext']):
                        bgpath = getPath(file)
                    
                    elif file.lower().endswith(cfg['audext']):
                        songs.append(getPath(file))

            ### If path is file... parse by extension
            elif os.path.isfile(path):
                file = path
                if file.lower().endswith(cfg['imgext']):
                    bgpath = getPath(file)
                    
                elif file.lower().endswith(cfg['audext']):
                    songs.append(getPath(file))
    ### If no URL given exit
    else:
        return
    
    ### If no img given exit
    if bgpath == '':
        print('No img given!\nExiting...')
        return 
    
    def getAudio(song):
        """
        Parse songpath (str)

        return: dict containing: 
                            - clip: (mpy.AudioFileClip)
                            - duration: float   
        """

        clip = mpy.AudioFileClip(song)

        duration = clip.duration

        return {"clip": clip, "duration": duration}

    ### Parse each song and append to audios[]
    audios = [getAudio(song) for song in songs]


    def getTotalLength(audios):
        """
        Add every audio['duration'] in audios list

        return: total length of audios (float)
        """
        length = 0

        for audio in audios:
            length += audio['duration']
    
        return length

    length = getTotalLength(audios)
    
    if arguments['--debug']:
        _infos = [bgpath, songs, audios, length]      

        informatized = f'''
        BackgroundPath({type(bgpath)}):\n {bgpath}\n 
        Songs({type(songs[0])}):\n {listItems(songs)}
        Audios({type(audios[0])}):\n {listItems(audios)}
        Total Length({type(length)}): {length}
        '''
        log.debug(informatized)

    ### Check for title if not given ask for input
    if arguments['--title']:
        title = arguments['--title']
    else:
        print("Title (outputname): ")
        title = input()

    arguments['--debug'] and log.debug(f"Title: '{title}'")

    # convert sec to min
    def getMinSec(time):
        """
        Get time(float) in seconds and convert to minutes(int) and seconds(int)

        return: list[minutes(int), seconds(int)] 
        """

        minutes = round(time // 60)
        seconds = round(time % 60)

        return [minutes, seconds]

    # return timestamp and pad with 0s
    def timestampformat(timestamp):
        """
        Receives timestamp(list) = [minutes, seconds]

        return: padded timestamp(string)
        """

        stamp = ''
        first = True

        for time in timestamp:
            # if time < 10 pad with 0
            if time < 10:
                stamp += f'0{str(time)}'
            else:
                stamp += str(time)

            if first == True:
                stamp += ':'
                first = False

        return stamp 

    # getting tracknames
    def getTrackName(song):
        trackname = os.path.basename(song)
        for ext in cfg['audext']:
            trackname = trackname.replace(ext, '')
        
        arguments['--debug'] and cfg['show_search_result'] and log.debug('Separator search range:' + trackname[1:cfg['ssr']])

        ### Parse tracknames
        if trackname[0] in [str(i) for i in range(10)] and any(separator in trackname[1:cfg['ssr']] for separator in cfg['separator']):
            try:
                trackname = re.split(cfg['separator'], trackname)[1].lstrip()
            except IndexError:
                pass

        return trackname

    tracknames = [getTrackName(song) for song in songs]

    arguments['--debug'] and log.debug(f'Tracknames:\n{listItems(tracknames)}')
        
    ### If --notxt == False write txt
    if not arguments['--notxt']:
        # writing timestamps.txt
        with open('timestamps.txt', 'w') as f:
            n = 0
            t = n + 1
            lines = [f'{title}\n\n']

            curtime = 0

            for audio in audios:
                # creating timestamp[minutes(int), seconds(int)] from curtime
                current = getMinSec(curtime)

                # getting track length in seconds(float)
                slength = audios[n]['duration']
                # song length from seconds(float) to mlength[minutes(int), seconds(int)]
                mlength = getMinSec(slength)
                
                # writing track info
                lines.append(f'{t} - {tracknames[n]} - {mlength[0]}m{mlength[1]}s - {timestampformat(current)}\n')
                
                # counter increment
                n += 1
                t = n + 1
                # timestamp increment
                curtime += slength

            # Getting and writing total length
            mlength = getMinSec(length)
            lines.append(f'\nTotal Length: {mlength[0]}m{mlength[1]}s')

            f.writelines(lines)

            log.debug('Txt file written!')

    ### Video
    ## Background
    # setting bg
    bg = mpy.ImageClip(bgpath)

    # set img duration = length of all songs added
    bg = bg.set_duration(length)

    videoroll = [bg]

    ## Captions
    n = 0
    # 3 seconds delay caption
    curtime = 3
    for audio in audios:
        t = n + 1
        txt = mpy.TextClip(txt=f'{t} - {tracknames[n]}', 
            font='Calibri', fontsize=30, color='white')
        txt = txt.set_position(('center', 0.80), relative=True)
        txt = txt.set_start((curtime))
        txt = txt.set_duration(8)
        txt = txt.crossfadein(0.6)
        txt = txt.crossfadeout(0.6)

        videoroll.append(txt)

        curtime += audio['duration']
        n += 1

    # Iterate through every audio file
    def setAudio(audios):
        
        curtime = 0
        def setIterator(audio):
            nonlocal curtime
            audio['clip'] = audio['clip'].set_start(curtime)
            curtime += audio['duration']
            return audio['clip']

        setlist = [setIterator(audio) for audio in audios]     
        
        arguments['--debug'] and log.debug(f'Setlist:\n{listItems(setlist)}\n\nCurrenttime:\n{curtime}')
        return setlist
    
    # mixing it all up
    finalvideo = mpy.CompositeVideoClip(videoroll)
    songmix = mpy.CompositeAudioClip(setAudio(audios))
    final = finalvideo.set_audio(songmix)
    
    arguments['--debug'] and log.debug(f'Final object:\n{final}')

    # if --test == False then write videofile
    if not arguments['--test']:
        # if path given and folder doesn't exist create it
        Path(title).mkdir(parents=True, exist_ok=True)
        if title.endswith(cfg['outext']):
            title.replace(cfg['outext'], '')
        final.write_videofile(title + cfg['outext'], threads=cfg['threads'], fps=cfg['fps'], codec=cfg['codec'])

if __name__ == '__main__':
    main()