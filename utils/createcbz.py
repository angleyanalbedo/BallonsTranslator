import os
import zipfile

from PyQt6.QtCore import QObject
from qtpy.QtCore import QThread , Signal


def create_cbz(folder_path, cbz_name, output_dir):

    if not cbz_name.endswith('.cbz'):
        cbz_name += '.cbz'

    cbz_path = os.path.join(output_dir, cbz_name)
    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        for root, _, files in os.walk(folder_path):
            for file in sorted(files):
                # 仅打包图像文件
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    cbz.write(file_path, os.path.relpath(file_path, folder_path))

def unpack_cbz(cbz_file, output_dir):
    """
    Unpacks a CBZ file into the specified output directory.

    Args:
        cbz_file (str): The path to the CBZ file to be unpacked.
        output_dir (str): The directory where the contents will be extracted.
    """
    if not os.path.exists(cbz_file):
        raise FileNotFoundError(f"The file {cbz_file} does not exist.")

    if not cbz_file.endswith('.cbz'):
        raise ValueError("The selected file is not a CBZ file.")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    try:
        with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
    except zipfile.BadZipFile:
        raise ValueError("The file is not a valid CBZ (ZIP) file.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")



class CbzWorker(QThread):
    def __init__(self, folder_path, cbz_name, output_dir):
        super().__init__()
        self.folder_path = folder_path
        self.cbz_name = cbz_name
        self.output_dir = output_dir

    def run(self):
        create_cbz(self.folder_path, self.cbz_name, self.output_dir)
        self.finished.emit()

class Unpacker(QThread):

    done = Signal(str)
    def __init__(self,folder_path, output_dir):
        super().__init__()
        self.folder_path = folder_path
        self.output_dir = output_dir

    def run(self):
        unpack_cbz(self.folder_path, self.output_dir)
        self.done.emit(str(self.output_dir))
