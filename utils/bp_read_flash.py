import serial


class FlashChip:

    def __init__(self, total_size, num_pages, page_size, **kwargs):
        self.total_size = total_size
        self.num_pages = num_pages
        self.page_size = page_size
        self._kwargs = kwargs

    