from typing import List
from collections import namedtuple

# Run Length Decoding.
# This is a specialized module to make it less PITA.

class RLE: # Rune Length Encoding
    def __init__(self,
                 order:List[int],
                 length:List[int],
                 x_max=1600,
                 y_max=256,
                 y_encoded_first=True):
        """
        Establish the assumption before encoding and decoding.
        :param order: the Nth pixel count.
        :param length: the number of pixels to include (inclusive both ends)
        :param x_max: max x values (items per row)
        :param y_max: max y values (number of rows)
        :param y_encoded_first:
        """
        self.y_encoded_first = y_encoded_first # assuming Y direction is incremented first before incrementing X in terms of pixel indexing.
        self.y_max = y_max
        self.x_max = x_max
        self.list_order = order
        self.list_length = length
        assert len(self.list_length) == len(self.list_order)

    def decode(self) -> List[tuple]:
        """
        Decode a list of order length pixel style marker to the more human list of x y coordinate
        :param list_orderlength:a list of pixel order (n-th pixel) and length of the commit
        :return: list of tuple(x,y)
        """
        # Check to ensure the length are matching up.
        assert len(self.list_length) == len(self.list_order)

        total_xy = []

        # Send each RLE
        for index, length in enumerate(self.list_length):

            # Run-Length i.e. Order + Length pair return a list of pixels
            list_xy = self.decode_OrderLength_to_listxy(self.list_order[index], length )

            # Append to the total pixels.
            total_xy = total_xy + list_xy

        return total_xy

    def decode_OrderLength_to_listxy(self, order: int, length: int) -> List[tuple]:
        list_xy = []
        for index in range(order,order+length):
            list_xy.append(self.decode_order_to_xy(index))
        return list_xy

    def decode_order_to_xy(self, pixel_order:int) -> tuple:
        """
        Take an order integer in a 1600 x 255 images, convert it to xy coordinate in the form of a Pixel object
        :param pixel_order: integer order of the pixel
        :return: Pixel object
        """
        x = (pixel_order - 1) // self.y_max + 1 # had to offset pixel order because orders are 1 based.
        y = (pixel_order - 1) % self.y_max + 1 #
        return (x, y)

if __name__=="__main__":
    alpha = RLE([255, 1231], [5, 12])
    print(alpha.decode())
