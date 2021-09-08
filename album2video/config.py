import os
from configparser import ConfigParser
import logging
log = logging.getLogger(__name__)

def parsing():
    # default values
    cfg = {
        'imgext': '.png, .jpg, .jpeg, .tiff, .bmp, .gif', 
        'audext': '.wav, .mp3, .flac, .m4a', 
        'separator': '-, .', 
        'ssr': '6', 
        'show_search_result': '0', 
        'codec': 'mpeg4', 
        'outext': '.mp4', 
        'threads': '4', 
        'fps': '1'
    }

    file = os.path.join(os.path.dirname(__file__), 'config.ini')
    if os.path.exists(file):
        pass
    else:
        lines = [
            "[extensions]",
            "; image extensions",
            "imgext = .png, .jpg, .jpeg, .tiff, .bmp, .gif",
            "; Audio extensions",
            "audext = .wav, .mp3, .flac, .m4a",
            "\n",
            "; parsing tracknumber options",
            "[parsing]",
            "; separators:",
            "separator = -, .",
            "; separator_search_range:",
            "ssr = 6",
            "; show separator_search_result on debug mode (0 false 1 true):" ,
            "show_search_result = 0",
            "\n",
            "[output]",
            "; output codec:",
            "codec = mpeg4",
            "; output extension:",
            "outext = .mp4",
            "; output threads:", 
            "threads = 4",
            "; output fps:",
            "fps = 1"
        ]
        with open(file, 'w') as w:
            w.write('\n'.join(line for line in lines))

        
    parser = ConfigParser()
    parser.read(file)

    # unpacking sections
    sections = [*parser.sections()]

    for section in sections:
        for key in parser[section]:
            if key in ['imgext', 'audext']:
                cfg[key] = tuple(value.strip() for value in cfg[key].split(','))
            elif key == 'separator':
                ## separator: '-, .' on dict
                cfg[key] = parser[section][key].split(',')
                cfg[key] = [i.strip() for i in cfg[key]]
                if any(separator in '.' for separator in cfg[key]):
                    cfg[key] = [i.replace('.', '\.') for i in cfg[key]] 
                
                cfg[key] = '|'.join(i for i in cfg[key])
            elif key in ['ssr', 'show_search_result', 'threads', 'fps']:
                cfg[key] = int(parser[section][key]) 
            else: 
                cfg[key] = parser[section][key]
            
    log.debug(f'Config:\n {cfg}')

    return cfg