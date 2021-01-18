import pygame
import random
from PIL import Image

BLOCK_LEN = 32
INPUT_IMAGE = 'lenna.png'
OUTPUT_IMAGE = 'lenna-shuffle.png'


class Block:

    def __init__(self, index, value):
        self.index = index
        self.value = value


def bubble_sort(window, image, shuffled_image):
    for i in range(len(shuffled_image)):
        for j in range(0, len(shuffled_image) - i - 1):
            if shuffled_image[j].index > shuffled_image[j + 1].index:
                shuffled_image[j], shuffled_image[j + 1] = shuffled_image[j + 1], shuffled_image[j]
        draw_image(window, image, shuffled_image)
    return True


def selection_sort(window, image, shuffled_image):
    for i in range(len(shuffled_image)):
        min_id = i
        for j in range(i + 1, len(shuffled_image)):
            if shuffled_image[min_id].index > shuffled_image[j].index:
                min_id = j
        shuffled_image[i], shuffled_image[min_id] = shuffled_image[min_id], shuffled_image[i]
        draw_image(window, image, shuffled_image)
    return True


def insertion_sort(window, image, shuffled_image):
    for i in range(1, len(shuffled_image)):
        block = shuffled_image[i]
        j = i - 1
        while j >= 0 and block.index < shuffled_image[j].index:
            shuffled_image[j + 1] = shuffled_image[j]
            j -= 1
        shuffled_image[j + 1] = block
        draw_image(window, image, shuffled_image)
    return True


def shell_sort(window, image, shuffled_image):
    gap = len(shuffled_image) // 2
    while gap > 0:
        for i in range(gap, len(shuffled_image)):
            block = shuffled_image[i]
            j = i
            while j >= gap and shuffled_image[j - gap].index > block.index:
                shuffled_image[j] = shuffled_image[j - gap]
                j -= gap
            shuffled_image[j] = block
            draw_image(window, image, shuffled_image)
        gap //= 2
        # draw_image(window, image, shuffled_image)
    return True


def merge_sort(window, image, shuffled_image):
    if len(shuffled_image) > 1:
        left_array = shuffled_image[:len(shuffled_image) // 2]
        right_array = shuffled_image[len(shuffled_image) // 2:]

        merge_sort(window, image, left_array)
        merge_sort(window, image, right_array)

        i = j = k = 0

        while i < len(left_array) and j < len(right_array):
            if left_array[i].index < right_array[j].index:
                shuffled_image[k] = left_array[i]
                i += 1
            else:
                shuffled_image[k] = right_array[j]
                j += 1
            k += 1
        while i < len(left_array):
            shuffled_image[k] = left_array[i]
            i += 1
            k += 1
        while j < len(right_array):
            shuffled_image[k] = right_array[j]
            j += 1
            k += 1
    draw_image(window, image, shuffled_image)
    return True


def cocktail_sort(window, image, shuffled_image):
    swapped = True
    start, end = 0, len(shuffled_image) - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            if shuffled_image[i].index > shuffled_image[i + 1].index:
                shuffled_image[i], shuffled_image[i + 1] = shuffled_image[i + 1], shuffled_image[i]
                swapped = True
        # draw_image(window, image, shuffled_image)
        if not swapped:
            break

        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if shuffled_image[i].index > shuffled_image[i + 1].index:
                shuffled_image[i], shuffled_image[i + 1] = shuffled_image[i + 1], shuffled_image[i]
                swapped = True
        start += 1

        draw_image(window, image, shuffled_image)
    return True


def cycle_sort(window, image, shuffled_image):
    writes = 0

    for cycle_start in range(len(shuffled_image) - 1):
        block = shuffled_image[cycle_start]
        position = cycle_start

        for i in range(cycle_start + 1, len(shuffled_image)):
            if shuffled_image[i].index < block.index:
                position += 1

        if position == cycle_start:
            continue

        while block.index == shuffled_image[position].index:
            position += 1
        shuffled_image[position], block = block, shuffled_image[position]
        writes += 1

        while position != cycle_start:
            position = cycle_start
            for i in range(cycle_start + 1, len(shuffled_image)):
                if shuffled_image[i].index < block.index:
                    position += 1
            while block.index == shuffled_image[position]:
                position += 1
            shuffled_image[position], block = block, shuffled_image[position]
            writes += 1
            draw_image(window, image, shuffled_image)
    return True


def quick_sort(window, image, shuffled_image, low, high):
    if len(shuffled_image) == 1:
        return shuffled_image
    if low < high:
        i = low - 1
        pivot_block = shuffled_image[high]
        for j in range(low, high):
            if shuffled_image[j].index <= pivot_block.index:
                i += 1
                shuffled_image[i], shuffled_image[j] = shuffled_image[j], shuffled_image[i]
        shuffled_image[i + 1], shuffled_image[high] = shuffled_image[high], shuffled_image[i + 1]

        draw_image(window, image, shuffled_image)
        quick_sort(window, image, shuffled_image, low, i)
        quick_sort(window, image, shuffled_image, i + 2, high)
        draw_image(window, image, shuffled_image)
    return True


def heap_sort(window, image, shuffled_image):
    for i in range(len(shuffled_image) // 2 - 1, -1, -1):
        heapify(shuffled_image, len(shuffled_image), i)
        draw_image(window, image, shuffled_image)
    for i in range(len(shuffled_image) - 1, 0, -1):
        shuffled_image[i], shuffled_image[0] = shuffled_image[0], shuffled_image[i]
        heapify(shuffled_image, i, 0)
        draw_image(window, image, shuffled_image)
    return True


def heapify(shuffled_image, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and shuffled_image[i].index < shuffled_image[left].index:
        largest = left
    if right < n and shuffled_image[largest].index < shuffled_image[right].index:
        largest = right

    if largest != i:
        shuffled_image[i], shuffled_image[largest] = shuffled_image[largest], shuffled_image[i]

        heapify(shuffled_image, n, largest)


def shuffle_image(image):
    width, height = image.size

    x_block = width // BLOCK_LEN
    y_block = height // BLOCK_LEN
    blocks_values = [(x * BLOCK_LEN, y * BLOCK_LEN, (x + 1) * BLOCK_LEN, (y + 1) * BLOCK_LEN)
                     for y in range(x_block) for x in range(y_block)]

    blocks = []
    for i in range(len(blocks_values)):
        block = Block(i, blocks_values[i])
        blocks.append(block)

    shuffled_image = list(blocks)
    random.shuffle(shuffled_image)

    return shuffled_image


def create_image(image, shuffled_image):
    width, height = image.size

    x_block = width // BLOCK_LEN
    y_block = height // BLOCK_LEN
    blocks_values = [(x * BLOCK_LEN, y * BLOCK_LEN, (x + 1) * BLOCK_LEN, (y + 1) * BLOCK_LEN)
                     for y in range(x_block) for x in range(y_block)]

    result_image = Image.new(image.mode, (width, height))
    for box, block in zip(blocks_values, shuffled_image):
        c_block = image.crop(block.value)
        result_image.paste(c_block, box)
    result_image.save('lenna-shuffle.png')


def draw_image(window, image, shuffled_image):
    create_image(image, shuffled_image)
    image_to_sort = pygame.image.load(OUTPUT_IMAGE)
    window.blit(image_to_sort, (0, 0))
    pygame.display.update()


def main():
    image = Image.open(INPUT_IMAGE)
    width, height = image.size

    shuffled_image = shuffle_image(image)
    create_image(image, shuffled_image)

    pygame.init()

    window = pygame.display.set_mode((width, height))
    window.set_alpha(None)
    pygame.display.set_caption("Sort")

    sorted_image = False
    run = True
    while run:
        draw_image(window, image, shuffled_image)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not sorted_image:
            sorted_image = bubble_sort(window, image, shuffled_image)
            # sorted_image = selection_sort(window, image, shuffled_image)
            # sorted_image = insertion_sort(window, image, shuffled_image)
            # sorted_image = shell_sort(window, image, shuffled_image)
            # sorted_image = merge_sort(window, image, shuffled_image)
            # sorted_image = cocktail_sort(window, image, shuffled_image)
            # sorted_image = cycle_sort(window, image, shuffled_image)
            # sorted_image = quick_sort(window, image, shuffled_image, 0, len(shuffled_image) - 1)
            # sorted_image = heap_sort(window, image, shuffled_image)


if __name__ == '__main__':
    main()
