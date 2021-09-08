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
        filename = filename.replace('/', '\\')
        pathfile = os.path.join(os.getcwd(), filename)
    
    return pathfile


