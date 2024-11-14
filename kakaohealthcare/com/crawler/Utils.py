import os


class Utils:


    def __init__(self):
        pass

    @staticmethod
    def dir_path():
        """
        작업중인 디렉토리 확인
        :return:
        """
        return os.path.dirname(os.getcwd())