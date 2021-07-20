import moviepy.editor as mpy, os, PIL

vcodec = "libx264"
videoquality = "24"
compression = "slow"

def start():
    
    print("Title: ")
    title = input()

    bgpath = './tru.png'

    audiopaths = ['3']

    """ def receiveAudio(): 
        print("Aud Path: ")
        audio = input()
        audiopaths.append(audio)

    add = True

    while add:
        receiveAudio()
        print(audiopaths)
        print('Add more?')
        uinput = input()
        if uinput.upper() == 'N':
            add = False; """
     
    
    def getAudio(audio):
        clip = mpy.AudioFileClip(f'.\\{audio}.wav')
        duration = clip.duration

        return {"clip": clip, "duration": duration}

    audios = []

    for audio in audiopaths:
        audios.append(getAudio(audio))


    def getTotalLength():
        length = 0

        for audio in audios:
            length += audio['duration']
    
        return length

    length = getTotalLength()

    info = [title, bgpath, audiopaths, audios, length]

    # convert sec to min
    def getMinSec(time):
        minutes = round(time // 60)
        seconds = round(time % 60)

        return [minutes, seconds]

    # return timestamp and pad with 0s
    def timestamp(timestamp):
        stamp = ''
        first = True

        for time in timestamp:
            if time < 10:
                stamp += f'0{str(time)}'
            else:
                stamp += str(time)

            if first == True:
                stamp += ':'
                first = False

        return stamp 
        
    # writing timestamps 
    with open('timestamps.txt', 'a') as f:
        n = 0
        t = n + 1
        f.write(title + '\n\n')

        curtime = 0

        for audio in audios:
            # timestamp to min
            mtimestamp = getMinSec(curtime)

            # song length from seconds to min
            slength = audios[n]['duration']
            mlength = getMinSec(slength)

            # writing track info
            f.write(f'{t} - {audiopaths[n]} - {mlength[0]}m{mlength[1]}s - {timestamp(mtimestamp)}\n')
            
            # counter increment
            n += 1

            # timestamp increment
            curtime += slength

        mlength = getMinSec(length)
        
        f.write(f'\nTotal Length: {mlength[0]}m{mlength[1]}s' )

    ### Video
    ## Background
    # getting size from img
    img = PIL.Image.open(f'.\\{bgpath}')
    width, height = img.size

    # setting bg
    bg = mpy.ImageClip(f'.\\{bgpath}')

    # length of all songs
    bg = bg.set_duration(length)

    videoroll = [bg]

    ## Captions
    n = 0
    # 3 seconds delay caption
    curtime = 3
    for audio in audios:
        t = n + 1
        txt = mpy.TextClip(f'{t} - {audiopaths[n]}', 
            font='Calibri', fontsize=75, color='white')
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
    final.write_videofile(f'{title}.mp4', threads=4, fps=24, codec="mpeg4")


start();