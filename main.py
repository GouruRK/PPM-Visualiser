def parse_args():
    """Parsing command line arguments with argparse

    :return: a dictionnary with command line arguments
    :rtype: dict
    """
    import argparse

    parser = argparse.ArgumentParser(description="Bitmap")
    parser.add_argument("file", help="The file to process")
    parser.add_argument(
        "-information",
        "-i",
        action="store_true",
        default=False,
        required=False,
        help="Show file data",
    )
    parser.add_argument(
        "-pixel",
        "-p",
        default=1,
        type=int,
        required=False,
        help="Set pixel size",
    )
    parser.add_argument(
        "-rotate",
        "-r",
        default=0,
        type=int,
        required=False,
        choices={0, 90, 180, 270},
        help="Rotate the image to the left",
    )
    parser.add_argument(
        "-convert",
        "-c",
        type=str,
        required=False,
        choices={"P" + digit for digit in "123456"},
        help="Choose the final extension of the file",
    )
    parser.add_argument(
        "-output",
        "-o",
        type=str,
        required=False,
        default="newImage",
        help="Choose the name of the converted file",
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    from parser import Parser

    args = parse_args()
    file = Parser(args["file"])
    if args["information"]:
        for key, value in args.items():
            if key != "picture":
                print(f" {key}: {value}")
    elif args["convert"] is not None:
        from writer import Writer

        writer = Writer(file, args["convert"], args["output"])
        writer.write()
    else:
        from bitmap import Bitmap

        window = Bitmap(file, args["pixel"], args["rotate"])
        window.build()
        print("The file {window.file_name} has been successfully created.")
