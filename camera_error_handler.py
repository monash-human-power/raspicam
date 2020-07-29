class CameraErrorHandler:
    def __enter__(self):

    def __exit__(self, type, value, traceback):


if __name__ == '__main__':
    with CameraErrorHandler():
        raise Exception("Test error")