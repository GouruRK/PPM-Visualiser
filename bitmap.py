import fltk


class Bitmap:
    """Object representing an PPM file picture"""

    def __init__(self, infos: dict, pixel_size: int, rotate: int):
        """Initialisation

        :param infos: dictionnary representing the images propreties
        :type infos: dict
        :param pixel_size: zoom degree (1 pixel = 1 pixel size)
        :type pixel_size: int
        :param rotate: The rotation angle (only 0, 90, 180, 270)
        :type rotate: int
        """
        self.infos = infos
        self.picture = infos["picture"]
        self.pixel_size = pixel_size
        self.width, self.height = infos["size"]
        self.rotate = rotate
        if rotate not in {0, 90, 180, 270}:
            raise ValueError

    def build(self):
        """Build the window to represent the ppm image"""
        width, height = self.width, self.height
        if self.rotate in {90, 270}:
            width, height = self.height, self.width
        fltk.cree_fenetre(width * self.pixel_size, height * self.pixel_size)

        for y in range(height):
            for x in range(width):
                if self.rotate == 0:
                    r_x, r_y = x, y
                elif self.rotate == 180:
                    r_x, r_y = width - x - 1, height - y - 1
                elif self.rotate == 90:
                    r_x, r_y = y, x
                elif self.rotate == 270:
                    r_x, r_y = height - y - 1, width - x - 1

                cell = self.picture[r_y][r_x]
                color = self.list_to_hex(cell)

                fltk.rectangle(
                    x * self.pixel_size,
                    y * self.pixel_size,
                    (x + 1) * self.pixel_size,
                    (y + 1) * self.pixel_size,
                    couleur=color,
                    remplissage=color,
                )

        tev = None
        re_open = False
        while tev != "Quitte":
            ev = fltk.donne_ev()
            tev = fltk.type_ev(ev)
            if tev == "Touche":
                touche = fltk.touche(ev)
                if touche == "r" or touche == "R":
                    if self.rotate == 270:
                        self.rotate = 0
                    else:
                        self.rotate += 90
                    re_open = True
                    tev = "Quitte"
            fltk.mise_a_jour()
        fltk.ferme_fenetre()
        if re_open:
            self.build()

    def int_to_hex(self, nb: int):
        """Convernt an integer value to it's hexadecimal value

        :param nb: the number to convert
        :type nb: int
        :param max_value: maximum value, defaults to 1
        :type max_value: int, optional
        :return: the hex number
        :rtype: str

        >>> int_to_hex(0)
        '0'
        >>> int_to_hex(40)
        '28'
        >>> int_to_hex(255)
        'ff'
        """
        nb = hex(nb)[2:]
        if len(nb) == 1:
            nb = "0" + nb
        return nb

    def list_to_hex(self, lst: list[int]):
        return "#" + "".join([self.int_to_hex(n) for n in lst])
