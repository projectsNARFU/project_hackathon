import json
import ast


def create_coord(info_coord):
    with open("choosed_coords.geojson", 'w') as f:
        f.write(json.dumps(info_coord))
    f.close()


def input_coord():
    """вводим координаты местности"""
    coord = input("введите координаты в формате: широта долгота")
    coord = coord.replace(',', '')
    coord = coord.split()

    info_coord = {"coordinates": coord, "type": "Point"}
    create_coord(info_coord)


if __name__ == '__main__':
    input_coord()

    with open("choosed_coords.geojson", 'r') as f:
        info_coord = f.readline()
        info_coord = ast.literal_eval(info_coord)
    f.close()
