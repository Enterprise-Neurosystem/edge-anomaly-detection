from os import walk


class DataFileManager:
    """
    This class provided static methods to deal with data files on the server.
    """

    @staticmethod
    def get_file_names_in_path(path):
        """Get file names
        Get all the file names in the given path.
        :param path The relative path to the file directory. eg 'static/data'
        :type: string
        :return: List of filenames in the given path.  Ignores any subdirectories in the given path.
        :type: list
        """
        file_names = []
        for(dirpath, dirnames, filenames) in walk(path):
            file_names.extend(filenames)
            break  # Stop after first directory has been found and do not walk any deeper
        return file_names
