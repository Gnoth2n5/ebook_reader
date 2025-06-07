import shutil

from ebooklib import ITEM_DOCUMENT
from ebooklib import epub


class FileHandler:
    @staticmethod
    def copy_file(src_path, dest_path):
        shutil.copy(src_path, dest_path)

    @staticmethod
    def read_file(file_path):
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()  # Sửa lỗi cú pháp
        elif file_path.endswith('.epub'):
            book = epub.read_epub(file_path)
            content = ""
            for item in book.get_items_of_type(ITEM_DOCUMENT):
                content += item.get_content().decode('utf-8') + "\n"
            return content
        else:
            return "Định dạng file không được hỗ trợ."