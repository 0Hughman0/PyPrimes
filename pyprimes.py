from PIL import Image
from random import randrange

# path to file containing prime list
PRIME_FILENAME = "primes.txt"

# size of square to fill
SQUARE_SIZE = 2000

# yields the next prime from file
def generate_prime_froms_file(file):
    for line in file.readlines():
        for number in line.split():
            yield int(number)
    raise IndexError("ran out of prime numbers :L")

# yields a tuple pair (number, is_prime) up to up_to, uses primes from PRIME_FILENAME
def gen_labelled_ints(up_to=100000):
    with open(PRIME_FILENAME, "r") as prime_file:
        primes = generate_prime_froms_file(prime_file)
        next_prime = next(primes)
        for i in range(up_to):
            if i == next_prime:
                yield (i, True)
                next_prime = next(primes)
            else:
                yield (i, False)

# yields a tuple (x, y) of integer coordinates running in a square spiral shape from (0, 0)
def spiral(length_x, length_y):
    x = 0
    y = 0
    increment = 0
    direction = 1
    for i in range(length_x * length_y):
        for l in range(increment):
            x += direction
            yield x , y
        for h in range(increment):
            y += direction
            yield x, y
        increment += 1
        direction = -direction

labelled_ints = gen_labelled_ints(SQUARE_SIZE * SQUARE_SIZE)

# create blank image
image = Image.new("RGB", (SQUARE_SIZE, SQUARE_SIZE), "white")
pixels = image.load()

origin_x = int(SQUARE_SIZE / 2)
origin_y = int(SQUARE_SIZE / 2)

shade_increment = 255 / (SQUARE_SIZE * SQUARE_SIZE)
shade = 0

# iterate through spiral coords and labelled integers in parallel
for coords, labelled_int in zip(spiral(SQUARE_SIZE, SQUARE_SIZE), labelled_ints):
    x, y = coords
    number, is_prime = labelled_int
    if is_prime:
        # change pixel colour to random dark colour
        pixels[x + origin_x, y + origin_y] = (
                        randrange(0, 230),
                        randrange(0, 230),
                        randrange(0, 230))
    else:
        try:
            pixels[x + origin_x, y + origin_y] = (255, 255, 255)
        except IndexError:
            print(x + origin_x, y + origin_y, " out of range!")
            
image.save("pretty primes pic.bmp")
image.show()