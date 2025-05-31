import os

def getPath(filename):
    """
    Clean up/format path string(filename)

    :rtype: str
    :return: path string
    """

    if os.path.isabs(filename):
        pathfile = filename
    else:
        filename = filename.lstrip('/\.')
        pathfile = os.path.join(os.getcwd(), filename)
    
    if pathfile.endswith('/'):
        pathfile.rstrip('/')
    
    return pathfile


