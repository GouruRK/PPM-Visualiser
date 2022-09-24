class Parser:
    """Parser object to parse pbm, pgm and ppm file (ascii and binary)"""

    def __init__(self, filename: str):
        """Initalisation

        :param filename: Path of the ppm file to parse
        :type filename: str
        :raises ValueError: Error raised when file is not a ppm file
        """
        available_format = {".pbm", ".pgm", ".ppm"}
        extension = filename[-4:]
        if extension not in available_format:
            raise ValueError("File is not a bitmap file")
        self.filename = filename
        self.infos = {
            "file version": None,
            "size": None,
            "maximum color value": None,
            "picture": [
                [],
            ],
        }
        parse = {
            ".pbm": self.parse_pbm,
            ".pgm": self.parse_pgm,
            ".ppm": self.parse_ppm,
        }
        parse[extension]()

    def __setitem__(self, key: str, value):
        """Change the value of `self.infos` dictionnary

        :param key: Key
        :type key: str
        :param value: The new value
        :type value: any
        """
        self.infos[key] = value

    def __getitem__(self, key):
        """Access to a value of `self.infos` dictionnary

        :param key: _description_
        :type key: _type_
        :return: _description_
        :rtype: _type_
        """
        return self.infos[key]

    def remove_comments(self, string):
        """Remove comments of a given string
        In ppm file format, comments starts with '#'

        :param string: The string that may contain comments
        :type string: str
        :return: string without comments
        :rtype: str

        >>> remove_comments('P4')
        'P4'
        >>> remove_comments('P4#version')
        'P4'
        """
        for index, car in enumerate(string):
            if car == "#":
                return string[:index]
        return string

    def parse_pbm(self):
        """Parse .pbm file.
        pbm represents black and white images.
        pbm files have the following structure:
        ```
        P1 # version (can be P4 too)
        7 10 # size : width of 7 and height of 10
        # image
        0 0 0 0 0 0 0
        0 0 0 0 0 1 0
        0 0 0 0 0 1 0
        0 0 0 0 0 1 0
        0 0 0 0 0 1 0
        0 0 0 0 0 1 0
        0 0 0 0 0 1 0
        0 1 0 0 0 1 0
        0 0 1 1 1 0 0
        0 0 0 0 0 0 0
        ```
        """
        self["maximum color value"] = 1
        last_instruction = 0
        current_width = 0
        with open(self.filename, "rb") as file:
            for line in file:
                if last_instruction < 2:
                    line = self.remove_comments(line.decode("utf-8").rstrip())
                    if last_instruction == 0 and line != "":
                        self["file version"] = line
                        last_instruction += 1
                    elif last_instruction == 1 and line != "":
                        self["size"] = tuple(map(int, line.split()))
                        width = self["size"][0]
                        last_instruction += 1
                else:
                    if int(self["file version"][1]) <= 3:
                        for car in line.decode().split():
                            if current_width == width:
                                current_width = 0
                                self["picture"].append([])
                            if car == "0":
                                self["picture"][-1].append([0, 0, 0])
                            else:
                                self["picture"][-1].append([255, 255, 255])
                            current_width += 1
                    else:
                        for byte in list(line):
                            b = bin(byte)[2:]
                            if len(b) < 8:
                                b = "0" * (8 - len(b)) + b
                            for nb in b:
                                if current_width == width:
                                    current_width = 0
                                    self["picture"].append([])
                                    break
                                    # This break is very VERY important.
                                    # If the byte number is 65, its '1000001'
                                    # in binary (so '01000001' because we are
                                    # working on 8 bits). But if the width is
                                    # 52 and current width is 48, we just have
                                    # to proceed for the first four bit,
                                    # which are '0100', and don't continue
                                    # by adding to the next line '0001'
                                if nb == "0":
                                    self["picture"][-1].append([0, 0, 0])
                                else:
                                    self["picture"][-1].append([255, 255, 255])
                                current_width += 1

    def parse_pgm(self):
        """Parse .pgm file.
        pgm represents images with gray scale.
        pgm files have the following structure:
        ```
        P2 # version (can be P5 too)
        24 7 # : width of 24 and height of 7
        15 # maximum color value
        # image
        0 0 0 0 0 0 0 0 0 0 0 0 0  0  0  0  0 0 0  0  0  0  0 0
        0 3 3 3 3 0 0 7 7 7 7 0 0 11 11 11 11 0 0 15 15 15 15 0
        0 3 0 0 0 0 0 7 0 0 0 0 0 11  0  0  0 0 0 15  0  0 15 0
        0 3 3 3 0 0 0 7 7 7 0 0 0 11 11 11  0 0 0 15 15 15 15 0
        0 3 0 0 0 0 0 7 0 0 0 0 0 11  0  0  0 0 0 15  0  0  0 0
        0 3 0 0 0 0 0 7 7 7 7 0 0 11 11 11 11 0 0 15  0  0  0 0
        0 0 0 0 0 0 0 0 0 0 0 0 0  0  0  0  0 0 0  0  0  0  0 0
        ```
        """
        last_instruction = 0
        current_width = 0
        with open(self.filename, "rb") as file:
            for line in file:
                if last_instruction < 3:
                    line = self.remove_comments(line.decode("utf-8").rstrip())
                    if last_instruction == 0 and line != "":
                        self["file version"] = line
                        last_instruction += 1
                    elif last_instruction == 1 and line != "":
                        self["size"] = tuple(map(int, line.split()))
                        width = self["size"][0]
                        last_instruction += 1
                    elif last_instruction == 2 and line != "":
                        self["maximum color value"] = int(line)
                        last_instruction += 1
                else:
                    if int(self["file version"][1]) <= 3:
                        iterable = line.decode().rstrip().split()
                    else:
                        iterable = list(line)
                    for car in iterable:
                        if current_width == width:
                            current_width = 0
                            self["picture"].append([])
                        b = self.balance(int(car), self["maximum color value"])
                        self["picture"][-1].append([b, b, b])
                        current_width += 1

    def parse_ppm(self):
        """Parse .ppm file.
        ppm represents images with gray scale.
        ppm files have the following structure:
        ```
        P3 # version (can be P6 too)
        4 4 # size: width of 4 and height of 4
        20 # maximum color value
        # image
        20  0  0    0  0  0    0  0  0   20 13  0
        0  0  0    0 20 10    0  0  0    0  0  0
        0  0  0    0  0  0    0 20 10    0  0  0
        0 20  0    0  0  0    0  0  0    0  0  0
        ```
        """
        last_instruction = 0
        current_width = 0
        with open(self.filename, "rb") as file:
            for line in file:
                if last_instruction < 3:
                    line = self.remove_comments(line.decode("utf-8").rstrip())
                    if last_instruction == 0 and line != "":
                        self["file version"] = line
                        last_instruction += 1
                    elif last_instruction == 1 and line != "":
                        self["size"] = tuple(map(int, line.split()))
                        width = self["size"][0]
                        last_instruction += 1
                    elif last_instruction == 2 and line != "":
                        self["maximum color value"] = int(line)
                        last_instruction += 1
                else:
                    if int(self["file version"][1]) <= 3:
                        iterable = line.decode().rstrip().split()
                    else:
                        iterable = list(line)
                    temp = []
                    rgb_counter = 0
                    for car in iterable:
                        if current_width == width:
                            current_width = 0
                            self["picture"].append([])
                        temp.append(self.balance(int(car), self["maximum color value"]))
                        rgb_counter += 1
                        if rgb_counter == 3:
                            rgb_counter = 0
                            self["picture"][-1].append(temp)
                            current_width += 1
                            temp = []

    def balance(self, n: int, max_value: int = 1):
        """Rebalance a number to get its value between 0 and 255
        (depending on its maximum possible value)

        :param n: the number to rebalance
        :type n: int
        :param max_value: the maximum value of the number, defaults to 1
        :type max_value: int, optional
        :return: the rebalanced number
        :rtype: int
        """
        return int((n / max_value) * 255)