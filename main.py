from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
from tkinter import filedialog, Tk
from PIL import Image

app = Ursina()

# Define the size of the platform
platform_size = 60

# Create a 3D grid of cubes to represent the platform
platform = Entity(
    model='plane',
    scale=platform_size,
    texture='grass',
    collider='mesh',
)

# Create a variable to store the selected texture
selected_texture = None

# Create a function to handle opening the file dialog and selecting a texture
def open_file_dialog():
    global selected_texture
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select PNG file',
        filetypes=(('PNG files', '*.png'), ('All files', '*.*')),
    )
    if file_path:
        selected_texture = Texture(Image.open(file_path))
    return file_path

# Create a FirstPersonController to allow the player to move around
player = FirstPersonController()

# Define the size of the blocks
block_size = 1

# Create a function to handle placing blocks
def place_block():
    if selected_texture:
        # Create a new block
        global block
        block = Entity(
            model='cube',
            color=color.white,
            texture=selected_texture,
            scale=(block_size, block_size, block_size),
            collider='box',
        )
        # Calculate the grid position for the new block
        position = mouse.world_point
        position = round(position / block_size) * block_size
        block.position = position

def set_block_size():
    global block_size
    input_text = input_field('Enter block size:', default=str(block_size))
    try:
        block_size = float(input_text)
        block.scale = (block_size, block_size, block_size)
    except ValueError:
        print('Invalid block size')

# Create a function to handle removing blocks
def remove_block():
    hit_info = raycast(origin=camera.position, direction=camera.forward, distance=8, ignore=[player, platform])
    if hit_info.hit:
        hit_entity = hit_info.entity
        destroy(hit_entity)

# Add the place_block() and remove_block() functions to the input() function
def input(key):
    global selected_texture
    if key == 'left mouse down':
        place_block()
    elif key == 'right mouse down':
        remove_block()
    elif key == 't': # If the player presses the T key
        set_block_size()
    elif key == 'r':
        open_file_dialog()
    elif key == 't':
        selected_texture = None
    elif key == 'q':
        quit()
    elif key == 'escape':
        selected_texture = None
    elif key == 'c':
        os.system('cls' if os.name == 'nt' else 'clear') # clear console

# Run the app
app.run()
