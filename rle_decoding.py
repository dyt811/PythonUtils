from typing import List
from collections import namedtuple
import numpy as np
from PIL import ImageDraw, Image
from pathlib import Path
# Run Length Decoding.
# This is a specialized module to make it less PITA.
import cv2

class RLE_decoding:  # Rune Length Encoding
    @staticmethod
    def parse_order_length_string(order_length: str):
        """
        A method to quickly parse the string of order and length and then return a list of order and a list of length
        :param order_length:
        :return:
        """
        list_order_length = order_length.split()

        # Must be pleural
        assert (len(list_order_length) % 2 == 0)
        # Filter the list of order length for:
            # First element is the index
            # Second element is the content.
        # This will be a list of tuple.
        # We do not need the first element, remove it via.
        enumerated_order = list(filter(lambda x: x[0] % 2 == 0, enumerate(list_order_length)))
        order = list(map(lambda x: int(x[1]), enumerated_order))
        enumerated_length = list(filter(lambda x: x[0] % 2 == 1, enumerate(list_order_length)))
        length = list(map(lambda x: int(x[1]), enumerated_length))
        return order, length





    def __init__(
        self,
        order: List[int],
        length: List[int],
        x_max=1600,
        y_max=256,
        y_encoded_first=True,
    ):
        """
        Establish the assumption before decoding.
        Take a RLE string, parse to order and length,
        Save as an image.


        :param order: the Nth pixel count.
        :param length: the number of pixels to include (inclusive both ends)
        :param x_max: max x values (items per row)
        :param y_max: max y values (number of rows)
        :param y_encoded_first:
        """
        self.y_encoded_first = (
            y_encoded_first
        )  # assuming Y direction is incremented first before incrementing X in terms of pixel indexing.
        self.y_max = y_max
        self.x_max = x_max
        self.list_order = order
        self.list_length = length
        assert len(self.list_length) == len(self.list_order)

    def decode(self) -> List[tuple]:
        """
        Decode a list of order length pixel style marker to the more humane list of x y coordinate
        :param list_orderlength:a list of pixel order (n-th pixel) and length of the commit
        :return: list of tuple(x,y)
        """
        # Check to ensure the length are matching up.
        assert len(self.list_length) == len(self.list_order)

        # Get a list of run and length.
        list_run_length = list(zip(self.list_order, self.list_length))

        total_xy = []
        for (length, order) in list_run_length:
            total_xy.append(self.decode_OrderLength_to_listxy(length,  order, self.y_max))
        return total_xy

    @staticmethod
    def decode_OrderLength_to_listxy(order: int, length: int, y_max=None) -> List[tuple]:
        list_xy = []
        for index in range(order, order + length):
            list_xy.append(RLE_decoding.decode_order_to_xy(index, y_max))
        return list_xy

    @staticmethod
    def decode_order_to_xy(pixel_order: int, y_max) -> tuple:
        """
        Take an order integer in a 1600 x 255 images, convert it to xy coordinate in the form of a Pixel object
        :param pixel_order: integer order of the pixel
        :return: Pixel object
        """
        x = (
            pixel_order - 1
        ) // y_max + 1  # had to offset pixel order because orders are 1 based.
        y = (pixel_order - 1) % y_max + 1  #
        return (x, y)

    def get_mask(self):
        # Skip          Drawing if the         EncodedPixels         are         empty in the         DataFrame.
        if self.list_order == [] or self.list_length == []:
            return

        # Create the black image.
        image_mask = Image.new("L", size=(self.x_max, self.y_max))

        # Instantiate the drawing object.
        draw = ImageDraw.Draw(image_mask)

        # Get coordinates to draw.
        list_xy = self.decode()

        # Actually drawing white on the mask
        for area in list_xy:
            # Draw the coordinates provided with value of 1 for BINARY mask.
            draw.point(area, fill=255)

        return image_mask


    def save_mask(self, path_mask:Path or str):
        """
        Take a numpy data matrix and convert it to 4 separate iamges.
        :param path_numpy:
        :return:
        """
        path_mask = Path(path_mask)

        image_mask = Image.new("L", size=(self.x_max, self.y_max))



        # Skip          Drawing if the         EncodedPixels         are         empty in the         DataFrame.
        if self.list_order == [] or self.list_length == []:
            return

        # Draw white on the mask.
        draw = ImageDraw.Draw(image_mask)

        # Get coordinates to draw.
        list_xy = self.decode()

        for area in list_xy:
            # Draw the coordinates provided with value of 1 for BINARY mask.
            draw.point(area, fill=255)

        image_mask.save(path_mask)

if __name__ == "__main__":
    alpha = RLE_decoding([255, 1231], [5, 12])
    print(alpha.decode())
