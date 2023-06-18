from PIL import Image, ImageEnhance
import os
import shutil
import zipfile
import subprocess

#Made by H4XV

input_folder = '.\input'  # Passe den Pfad zum Eingabeordner an
output_folder = '.\Output'  # Passe den Pfad zum Ausgabeordner an

def convert_to_grayscale(image):
    return image.convert('L')

def enhance_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    enhanced_image = enhancer.enhance(factor)
    return enhanced_image

def extract_frames(gif_path, output_folder):
    gif = Image.open(gif_path)
    gif_frames = []
    
    try:
        while True:
            gif_frames.append(gif.copy())
            gif.seek(len(gif_frames))
    except EOFError:
        pass
    
    for i, frame in enumerate(gif_frames):
        frame = frame.convert('RGB')
        frame_gray = convert_to_grayscale(frame)
        frame_enhanced = enhance_contrast(frame_gray, 1.15)
        
        frame_filename = f"frame_{i}.png"
        frame_path = os.path.join(output_folder, frame_filename)
        frame_enhanced.save(frame_path, "PNG")#Made by H4XV


def create_zip_folders(output_folder):
    subfolders = [f.path for f in os.scandir(output_folder) if f.is_dir()]
    
    for folder in subfolders:
        folder_name = os.path.basename(folder)
        zip_filename = os.path.join(output_folder, f"{folder_name}.zip")
        
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, _, files in os.walk(folder):#Made by H4XV
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder))



def del_folders(output_folder):
    subfolders = [f.path for f in os.scandir(output_folder) if f.is_dir()]

    for folder in subfolders:
        try:
            shutil.rmtree(folder)
            print("DELETING FOLDERS.")#Made by H4XV
        except OSError as e:
            print(f"ERROR WHILE DELETING FOLDERS: {e}")

def del_zips(output_folder):
    zip_files = [f.path for f in os.scandir(output_folder) if f.is_file() and f.name.endswith('.zip')]

    for zip in zip_files:
        try:
            os.remove(zip)
            print(f"DELETING ZIP {zip}")
        except OSError as e:
            print(f"ERROR WHILE DELETING FOLDERS: {e}")


def convert_gifs_to_grayscale(input_folder, output_folder):
    gif_files = [f for f in os.listdir(input_folder) if f.endswith('.gif')]
    
    for gif_file in gif_files:
        gif_path = os.path.join(input_folder, gif_file)
        
        # Creates Folder for every GIF
        gif_output_folder = os.path.join(output_folder, os.path.splitext(gif_file)[0])
        os.makedirs(gif_output_folder, exist_ok=True)
        
        # Extracting frames of the gif
        extract_frames(gif_path, gif_output_folder)
    
    # Creates zip files
    create_zip_folders(output_folder)
    
    #Delets Folder
    del_folders(output_folder)
#Made by H4XV



convert_gifs_to_grayscale(input_folder, output_folder)

cmd = f"python zip2Animation.py -d .\Output"
        
        # CMD-Kommando ausführe
subprocess.call(cmd, shell=True)

del_zips(output_folder)
#Made by H4XV


