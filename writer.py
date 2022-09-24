import os


class Writer:
    """Object that create a PPM file"""

    def __init__(self, infos: dict, output_version: str, output_name: str):
        """Initialisation

        :param infos: dictionnary representing the image propreties
        :type infos: dict
        :param output_version: The version of PPM to convert
        :type output_version: str
        :param output_name: name of the resulting file
        :type output_name: str
        """
        self.infos = infos
        self.output_version = output_version
        self.picture = infos["picture"]
        self.picture_version = infos["file version"]
        self.picture_size = infos["size"]
        self.maximum_color_value = infos["maximum color value"]
        self.output_name = output_name
        self.file_name = self.is_name_valid()

    def is_name_valid(self):
        """Check if the name given is valid

        :raises FileExistsError: The file already exists
        :raises ValueError: The name contain illegal characters
        :return: the name of the file if valid
        :rtype: str
        """
        extension = {
            "P1": "pbm",
            "P2": "pgm",
            "P3": "ppm",
            "P4": "pbm",
            "P5": "pgm",
            "P6": "ppm",
        }
        name = f"{self.output_name}.{extension[self.output_version]}"
        if os.path.isfile(name):
            raise FileExistsError(
                "An existing file has this name on the selected folder"
            )
        illegal_car = '#%&}{\<>*?/ $!`":@+|='
        for car in self.output_name:
            if car in illegal_car or car == "'":
                raise ValueError("The file name contain illegal characters")
        return name

    def write(self):
        """Main function"""
        if self.output_version in {"P1", "P2", "P3"}:
            self.write_raw()
        else:
            self.write_ascii()

    def write_raw(self):
        """Write a non binary file"""
        width, height = self.picture_size
        with open(self.file_name, "a") as file:
            file.write(self.output_version + "\n")
            file.write(f"{width} {height}\n")
            if self.output_version != "P1":
                file.write(f"{255}\n")

            for y in range(height):
                for x in range(width):
                    cell = self.picture[y][x]
                    if self.output_version == "P1":
                        avg = sum(cell) / 3
                        if avg < 127:
                            file.write("1 ")
                        else:
                            file.write("0 ")
                    elif self.output_version == "P2":
                        avg = int(sum(cell) / 3)
                        file.write(f"{avg} ")
                    else:
                        file.write(f"{cell[0]} {cell[1]} {cell[2]} ")
                file.write("\n")

    def write_ascii(self):
        """Write a binary file"""
        width, height = self.picture_size
        with open(self.file_name, "ab") as file:
            file.write(f"{self.output_version}\n".encode())
            file.write(f"{width} {height}\n".encode())
            if self.output_version != "P4":
                file.write(f"{255}\n".encode())

            for y in range(height):
                for x in range(width):
                    cell = self.picture[y][x]
                    if self.output_version == "P4":
                        avg = sum(cell) / 3
                        v = 0
                        if avg < 127:
                            v = 1
                        file.write(v.to_bytes(1, "big"))
                    elif self.output_version == "P5":
                        avg = int(sum(cell) / 3)
                        file.write(avg.to_bytes(1, "big"))
                    else:
                        file.write(cell[0].to_bytes(1, "big"))
                        file.write(cell[1].to_bytes(1, "big"))
                        file.write(cell[2].to_bytes(1, "big"))
