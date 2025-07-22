import sys
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
import csv


def inspect_styles(docx_path, csv_path=None):
    doc = Document(docx_path)
    style_info = []
    for style in doc.styles:
        if style.type == WD_STYLE_TYPE.PARAGRAPH:
            style_type = '段落'
        elif style.type == WD_STYLE_TYPE.CHARACTER:
            style_type = '字符'
        elif style.type == WD_STYLE_TYPE.TABLE:
            style_type = '表格'
        elif style.type == WD_STYLE_TYPE.LIST:
            style_type = '列表'
        else:
            style_type = str(style.type)
        style_info.append([style.name, style_type])
        print(f"样式名: {style.name}, 类型: {style_type}")
    if csv_path:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['样式名', '类型'])
            writer.writerows(style_info)
        print(f"已保存到 {csv_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python style_inspect.py 模板文件路径 [输出csv路径]')
        sys.exit(1)
    docx_path = sys.argv[1]
    csv_path = sys.argv[2] if len(sys.argv) > 2 else None
    inspect_styles(docx_path, csv_path) 