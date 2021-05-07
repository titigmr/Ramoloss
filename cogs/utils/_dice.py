import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image


matplotlib.use('Agg')

REF_COLORS = {'green': (186, 242, 184),
              'magenta': (227, 129, 222),
              'red': (176, 62, 62),
              'white': (255, 255, 255),
              'black': (0, 0, 0)}


class DiceGenerator:
    """
    Dice Image Generator
    """
    def __init__(self, pt1=(30, 70), pt2=(70, 30),
                 thinkness=5, shape=(100, 100, 3),
                 xy=(50, 52), crop=(200, 200), directory='_img_dices'):
        """
        Usage example:
        TODO
        """
        self.pt1 = pt1
        self.pt2 = pt2
        self.thinkness = thinkness
        self.shape = shape
        self.xy = xy
        self.crop = crop
        self.directory = self.get_path(directory)


    def create_lauch_dice(self, inputs_dice: list, colors='green', line_return: int = 3, save=True):
        """
        Draw a dice or multiple dices side by side with a value number and a color.

        Params:
        ------
        - input_dice: list of values, e.g `['0', '10', '9']`
        - color: str or list, default is 'green'. All dices are green. e.g `['green', 'black', 'magenta']`
                NOTE: All avalaible colors are in `REF_COLOR`
        - line_return: int, default 3, break the line at the number of dice.
        - save: bool, default True, save the image into .png file

        Return:
        ------
            PIL Image
        """
        list_img = []
        list_lines = []
        last = len(inputs_dice) - 1

        list_colors = self.convert_colors(colors, inputs_dice)

        if len(list_colors) != len(inputs_dice):
            raise ValueError('Colors and dice numbers must be in the same size')

        for (n, i), c in zip(enumerate(inputs_dice), list_colors):
            if (n % line_return == 0) and (n != 0):
                line_img = self.create_side_by_side(
                    list_img, how='horizontal', save=False)
                list_lines.append(line_img)
                list_img = []

            img = self.create_image_dice(value=i,
                                    size=50,
                                    color=c,
                                    border=1, save=False)
            list_img.append(img)
            if n == last:
                line_img = self.create_side_by_side(
                    list_img, how='horizontal', save=False)
                list_lines.append(line_img)

        output_img = self.create_side_by_side(list_lines, how='vertical', save=False)
        if save:
            path = os.path.join(self.directory, 'out.png')
            output_img.save(path)
        return output_img

    @staticmethod
    def get_color(color):
        if len(color) == 3 and isinstance(color, tuple):
            return color
        return REF_COLORS[color]

    @staticmethod
    def get_path(directory):
        if directory is None:
            return '.'
        path_cf = os.path.dirname(os.path.realpath("__file__"))
        path = os.path.join(path_cf, directory)
        return path

    def create_image_dice(self, value, size=50,
                          color='magenta', border=1,
                          color_b=(0, 0, 0),
                          font='sans',
                          weight=1000,
                          save=False):

        path = os.path.join(self.directory, f'{value}.png')
        color = self.get_color(color)
        size = self.reformat_size(value, size)
        img = self.write_white_img(self.shape)
        rect_border = cv2.rectangle(img,
                                    (self.pt1[0] - border, self.pt1[1] + border),
                                    (self.pt2[0] + border, self.pt2[1] - border),
                                    color_b,
                                    self.thinkness)

        rect = cv2.rectangle(img, self.pt1, self.pt2, color, -1)
        rect_center = cv2.rectangle(img, self.pt1, self.pt2,
                                    color, self.thinkness)
        fontcolor = 'black'

        if color == (0, 0, 0):
            fontcolor = 'white'

        plt.imshow(rect_center)
        plt.annotate(value, xy=self.xy, size=size, ha='center', color=fontcolor,
                     va='center', fontname=font, weight=weight)
        plt.axis('off')
        plt.savefig(path)
        plt.close()
        img_f = self.white_to_transparency_gradient(Image.open(path))
        img_f = self.crop_center(img_f, *self.crop)
        if save:
            img_f.save(path)
        else:
            os.remove(path)
        return img_f

    @staticmethod
    def reformat_size(value, size):
        """
        Rescale the fontsize number on the dice drawed.
        """
        resize = len(value) - 2

        if resize > 0:
            size -= resize * 10
        return size

    @staticmethod
    def white_to_transparency_gradient(img):
        """
        Remove white to transparency
        """
        x = np.asarray(img.convert('RGBA')).copy()
        x[:, :, 3] = (255 - x[:, :, :3].mean(axis=2)).astype(np.uint8)
        return Image.fromarray(x)

    @staticmethod
    def write_white_img(shape):
        """
        Create a white image with a specified shape
        """
        img = np.full(fill_value=255, shape=shape, dtype="uint8")
        return img

    @staticmethod
    def crop_center(pil_img, crop_width, crop_height, slide_x=0, slide_y=15):
        """
        Crop to center a PIL image with possibility
        to slide vertically and horizontally
        """
        img_width, img_height = pil_img.size
        return pil_img.crop((((img_width - crop_width) // 2) + slide_x,
                            (img_height - crop_height) // 2,
                            ((img_width + crop_width) // 2) + slide_y,
                            (img_height + crop_height) // 2))

    def create_side_by_side(
            self, list_img: list, name='line', how='horizontal', save=False, saved_images=False):
        """Concatenate multiple PIL images verticaly or horizontaly"""

        if saved_images:
            images = [Image.read(x) for x in list_img]
        else:
            images = list_img
        widths, heights = zip(*(i.size for i in images))

        if how == 'horizontal':
            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', size=(total_width, max_height), color=(255, 255, 255))

            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset, 0))
                x_offset += im.size[0]

        if how == 'vertical':
            max_width = max(widths)
            total_height = sum(heights)

            new_im = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))

            y_offset = 0
            for im in images:
                new_im.paste(im, (0, y_offset))
                y_offset += im.size[1]

        img_f = self.white_to_transparency_gradient(new_im)
        if save:
            path = os.path.join(self.directory, f'{name}.png')
            img_f.save(path)
        return img_f

    @staticmethod
    def convert_colors(input_color, input_dice):
        """ Convert a list of color with the same size at the list input dice"""
        if isinstance(input_color, list):
            colors = [REF_COLORS[c] for c in input_color if c in REF_COLORS.keys()]
            if len(input_color) != len(colors):
                raise ColorError
        else:
            colors = [REF_COLORS[input_color] for i in input_dice]
        return colors


class ColorError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'Available colors are {list(REF_COLORS.keys())}, or list of colors'


if __name__ == '__main__':
    dg = DiceGenerator(crop=(200, 200))
    dg.create_lauch_dice(["0", '10', '30'], colors='magenta')
