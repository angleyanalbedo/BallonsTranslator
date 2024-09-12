import os
import zipfile

from qtpy.QtCore import QThread


def create_cbz(folder_path, cbz_name, output_dir):
    # 确保输出文件名以 .cbz 结尾
    if not cbz_name.endswith('.cbz'):
        cbz_name += '.cbz'

    # 创建 zip 文件
    cbz_path = os.path.join(output_dir, cbz_name)
    with zipfile.ZipFile(cbz_path, 'w') as cbz:
        for root, _, files in os.walk(folder_path):
            for file in sorted(files):
                # 仅打包图像文件
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    file_path = os.path.join(root, file)
                    cbz.write(file_path, os.path.relpath(file_path, folder_path))


class CbzWorker(QThread):
    def __init__(self, folder_path, cbz_name, output_dir):
        super().__init__()
        self.folder_path = folder_path
        self.cbz_name = cbz_name
        self.output_dir = output_dir

    def run(self):
        create_cbz(self.folder_path, self.cbz_name, self.output_dir)
