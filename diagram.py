from PIL import Image, ImageFont, ImageDraw
from math import sin, cos, pi
import random

RADIUS = 200
ITEMS_PER_RING = 8


def calc_diagram_size(item_count):
    ring_count = 0
    num_per_ring = ITEMS_PER_RING
    while item_count > 0:
        item_count -= num_per_ring
        ring_count += 1
        num_per_ring = num_per_ring * 2 - 1
    ring_count *= RADIUS * 2.5
    return int(ring_count), int(ring_count)


def save_diagram(path, database):
    image_size = calc_diagram_size(len(database))
    image_center_x = image_size[0] / 2
    image_center_y = image_size[1] / 2
    image = Image.new(mode='RGBA', size=image_size, color=0xffffffff)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'C:\Windows\Font\consola.ttf', size=14)

    degree = 0
    degree_increment = 360 / ITEMS_PER_RING
    next_degree_increment = ITEMS_PER_RING
    first_item = True
    radius_multiply = 1
    position_map = {}
    random.seed()

    for item in database.items():
        if first_item:
            draw_pos = (
                    image_center_x,
                    image_center_y
            )
        else:
            draw_pos = (
                    image_center_x - RADIUS * radius_multiply * sin(degree * pi / 180 - 0.83 * radius_multiply),
                    image_center_y + RADIUS * radius_multiply * cos(degree * pi / 180 - 0.83 * radius_multiply)
            )
        position_map[item[0]] = draw_pos
        if not first_item:
            degree += degree_increment
        if degree >= 360:
            radius_multiply += 1
            next_degree_increment += next_degree_increment * 2 - 1
            degree_increment /= 2
            degree = 0
        first_item &= False

    for item in database.items():
        from_id = item[0]
        rand_color = random.randint(0, 0xcccccc) | 0xc8000000
        for follower in item[1][1]:
            draw.line(
                (
                    position_map[from_id],
                    position_map[follower]
                ),
                fill=rand_color
            )
        for following in item[1][2]:
            draw.line(
                (
                    position_map[from_id],
                    position_map[following]
                ),
                fill=rand_color
            )

    for item in database.items():
        draw.text(
            position_map[item[0]],
            item[1][0],
            font=font,
            fill=(0, 0, 0, 255)
        )

    image.save(path)
    print("Image saved as diagram.png. Showing it to you...")
    image.show()
