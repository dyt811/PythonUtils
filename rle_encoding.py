from typing import List
import numpy as np
from collections import namedtuple

# Run Length Decoding.
# This is a specialized module to make it less PITA.
#

class RLE_encoding:  # Rune Length Encoding process from a mask to RLE
    def __init__(
        self,
        mask: np.array,  # a 2d nmumpy matrix array
        mask_value=1,  # default assume the mask is 0 for background and 1 for mask value.
        background_value=0,  # default assume the mask is 0 for background and 1 for mask value.
        mask_value_higher=True
    ):
        """
        Establish the assumption before encoding.
        :param order: the Nth pixel count.
        :param length: the number of pixels to include (inclusive both ends)
        :param x_max: max x values (items per row)
        :param y_max: max y values (number of rows)
        :param y_encoded_first:
        """
        self.mask = mask

        self.mask_value = mask_value
        self.background_value = background_value
        self.mask_value_higher = mask_value_higher

        self.list_order = []
        self.list_length = []
        self.list_order_length = []
        self.encode()

    def get(self):
        """
        Return the List of Order Length
        :return:
        """
        return self.list_order_length

    def encode(self):
        """
        Return a string representation of POSITION & Length pair.
        Encode the image into a string.

        Source inspired by: https://www.kaggle.com/paulorzp/rle-functions-run-lenght-encode-decode
        :param list_orderlength:a list of pixel order (n-th pixel) and length of the commit
        :return: list of tuple(x,y)
        """

        # Flatten into 1D array.
        mask_1d = self.mask.flatten()

        # Do check a few simple assumptions about values.
        if self.mask_value_higher:
            assert max(mask_1d) <= self.mask_value
            assert min(mask_1d) == self.background_value
        else:
            assert max(mask_1d) == self.background_value
            assert min(mask_1d) >= self.mask_value

        # Append 0 to both end to accommodate the upcoming shift.
        mask_1d_padded_both = np.concatenate([[self.background_value], mask_1d, [self.background_value]])
        mask_1d_padded_left = mask_1d_padded_both[:-1]  # skipped right pad
        mask_1d_padded_right = mask_1d_padded_both[1:]  # skipped left pad

        # Determine where non-continuity occcur:  e.g. 0 & 1 at the same position in the left and right shifted version
        # e.g. [Pad, 0, 1, 1, 0] & [0, 1, 1, 0, Pad]
        # Compare the above two, where they are not the same. 0 & 1

        # np.where return tuples, only first element matters
        boundaries = np.where(mask_1d_padded_left != mask_1d_padded_right)[0]

        # +1 because index are 1 based in the final CSV report for pixel wise counting.
        # i.e. there is no 0th pixel.
        boundaries = boundaries + 1

        # every other element is where 0 starts (since they are continuous).
        boundaries_background = boundaries[1::2]
        # every other element is where 1 starts (since they are continuous).
        boundaries_mask = boundaries[::2]


        run_length = []
        # Compute the length part before adding Run/Length couple to the output list.
        for index, element in enumerate(boundaries_mask):
            # Element: is the place where 1 start
            run = element
            self.list_order.append(run)

            # Length is the differences between where 0 starts and where proceeding 0 starts.
            length = boundaries_background[index] - element
            self.list_length.append(length)

            self.list_order_length.append((run, length))

if __name__ == "__main__":
    alpha = RLE_encoding(np.array([1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0]))
    print(alpha.encode())
