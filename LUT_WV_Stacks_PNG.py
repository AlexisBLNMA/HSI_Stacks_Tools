
# Import necessary libraries
import numpy as np  # Import numpy for numerical operations
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from google.colab import drive  # Import drive from google.colab for mounting Google Drive
import tifffile  # Import tifffile for working with TIFF files

# Mount Google Drive to access files
drive.mount('/content/drive')

# Define the path to the input image and the directory to save the generated images
img_path = 'PATH.tif'
save_path = 'SAVE_PATH'

# Define the range of wavelengths
wavelengths = np.arange(Initial_WV, End_WV_Plus1, Shift_channels) #Example (495, 746. 5) from 495 to 745 nm, incrementing by 5 nm

# Function to convert wavelength to RGB color
def wavelength_to_rgb(wavelength):
    # Define RGB values for different wavelength ranges
    if 380 <= wavelength < 440:
        R = -(wavelength - 440) / (440 - 380)
        G = 0.0
        B = 1.0
    elif 440 <= wavelength < 490:
        R = 0.0
        G = (wavelength - 440) / (490 - 440)
        B = 1.0
    elif 490 <= wavelength < 510:
        R = 0.0
        G = 1.0
        B = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        R = (wavelength - 510) / (580 - 510)
        G = 1.0
        B = 0.0
    elif 580 <= wavelength < 645:
        R = 1.0
        G = -(wavelength - 645) / (645 - 580)
        B = 0.0
    elif 645 <= wavelength <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return R, G, B

# Open the TIFF file and process each page
with tifffile.TiffFile(img_path) as tif:
    for i, page in enumerate(tif.pages):
        # Load the image data from the page
        img = page.asarray()

        # Normalize pixel values between 0 and 1
        img_norm = np.interp(img, (img.min(), img.max()), (0, 1))

        # Get RGB color corresponding to the current wavelength
        color = wavelength_to_rgb(wavelengths[i])

        # Apply the color to the image
        img_color = np.repeat(img_norm[..., np.newaxis], 3, axis=-1) * color

        # Create a figure without axes
        plt.figure(figsize=(8, 6))

        # Display the colorized image
        plt.imshow(img_color)

        # Turn off axis
        plt.axis('off')

        # Add wavelength text at the bottom left corner
        plt.text(0.05, 0.05, f'{int(wavelengths[i])} nm', color='white', fontsize=10, transform=plt.gca().transAxes)

        # Save the image without displaying
        save_filename = f'{int(wavelengths[i])}_nm.png'
        save_filepath = save_path + save_filename
        plt.savefig(save_filepath, bbox_inches='tight', pad_inches=0)

        # Close the figure to release memory
        plt.close()
