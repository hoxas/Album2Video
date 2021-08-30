"""
album2video

Usage:
    album2video [options] [URL...]

Options:
    -h --help               Show this screen
    -v --version            Show version
    -d --debug              Verbose logging
    -n --notxt              Don't output timestamps.txt
    --title=TITLE           Set title beforehand


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
"""

import os, docopt, logging
import moviepy.editor as mpy

from PathTool import getPath

appversion = '0.0.1'

arguments = docopt.docopt(__doc__, version=f"Album2Video {appversion}")

vcodec = "libx264"
videoquality = "24"
compression = "slow"

log = logging.getLogger(__name__)

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



imgext = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
audext = ('.wav', '.mp3', '.flac', '.m4a')






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
                    if file.lower().endswith(imgext):
                        bgpath = getPath(file)
                    
                    elif file.lower().endswith(audext):
                        songs.append(getPath(file))

            ### If path is file... parse by extension
            elif os.path.isfile(path):
                file = path
                if file.lower().endswith(imgext):
                    bgpath = getPath(file)
                    
                elif file.lower().endswith(audext):
                    songs.append(getPath(file))

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

    audios = []

    ### Parse each song and append to audios[]
    for song in songs:
        audios.append(getAudio(song))


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
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    tracknames = []
    for song in songs:
        trackname = os.path.basename(song)
        for ext in audext:
            trackname = trackname.replace(ext, '')
        
        if trackname[0] in num and trackname[1:4] in '.-':
            arguments['--debug'] and log.debug('Track number parsing.')
            try:
                trackname = trackname.split('.', 1)
                print(trackname)
            except IndexError:
                pass

            


        tracknames.append(trackname)

        
    ### If --notxt == False write txt
    if not arguments['--notxt']:
        # writing timestamps.txt
        with open('timestamps.txt', 'a') as f:
            n = 0
            t = n + 1
            f.write(title + '\n\n')

            curtime = 0

            for audio in audios:
                # creating timestamp[minutes(int), seconds(int)] from curtime
                current = getMinSec(curtime)

                # getting track length in seconds(float)
                slength = audios[n]['duration']
                # song length from seconds(float) to mlength[minutes(int), seconds(int)]
                mlength = getMinSec(slength)
                
                # writing track info
                f.write(f'{t} - {tracknames[n]} - {mlength[0]}m{mlength[1]}s - {timestampformat(current)}\n')
                
                # counter increment
                n += 1
                t = n + 1
                # timestamp increment
                curtime += slength

            # Getting and writing total length
            mlength = getMinSec(length)
            f.write(f'\nTotal Length: {mlength[0]}m{mlength[1]}s')

            log.debug('Txt file written!')

    ### Video
    ## Background
    # getting size from img
    ''' img = PIL.Image.open(f'.\\{bgpath}')
    width, height = img.size '''

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
        txt = mpy.TextClip(f'{t} - {tracknames[n]}', 
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
    def setAudio():
        setlist = []
        curtime = 0

        for audio in audios:
            setlist.append(audio['clip'].set_start(curtime))
            curtime += audio['duration']
        
        print(setlist)
        return setlist
    
    # mixing it all up
    finalvideo = mpy.CompositeVideoClip(videoroll)
    songmix = mpy.CompositeAudioClip(setAudio())
    final = finalvideo.set_audio(songmix)
    print(final)

    

    ''' final.write_videofile(f'{title\}.mp4', threads=4, fps=1, codec="mpeg4") '''

if __name__ == '__main__':
    main()