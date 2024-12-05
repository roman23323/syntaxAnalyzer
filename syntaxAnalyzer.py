from lark import Lark, Transformer
import xml.etree.ElementTree as ET
import argparse

grammar = """
    start: (const_decl | const_eval)*

    const_decl: "def" NAME "=" value
    const_eval: "?{" NAME "}"

    array: "'(" value (value)* ")"
    dictionary: "$[" dict_item ("," dict_item)* "]"

    dict_item: NAME ":" value

    ?value: NUMBER
          | array
          | dictionary

    NAME: /[a-zA-Z]+/
    NUMBER: /[0-9]+/

    %import common.WS
    %ignore WS
"""

class XMLTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.variables = {}

    def start(self, items):
        start_el = ET.Element("start")
        for i in items:
            start_el.append(i)
        return start_el

    def const_decl(self, items):
        const_decl_el = ET.Element(items[0])
        const_decl_el.append(items[1])
        self.variables[items[0]] = items[1]
        return const_decl_el

    def array(self, items):
        array_el = ET.Element('array')
        for item in items:
            array_el.append(item)
        return array_el

    def NUMBER(self, item):
        number_el = ET.Element('number')
        number_el.text = item
        return number_el

    def const_eval(self, items):
        if items[0] in self.variables:
            const_eval_el = ET.Element('const_eval')
            const_eval_el.append(self.variables[items[0]])
            return const_eval_el
        else:
            print(f"Переменная {items[0]} не была инициализирована!")
            exit(1)

    def NAME(self, item):
        return item

    def dictionary(self, items):
        dictionary_el = ET.Element('dictionary')
        for item in items:
            dictionary_el.append(item)
        return dictionary_el

    def dict_item(self, items):
        dict_item_el = ET.Element(items[0])
        dict_item_el.append(items[1])
        return dict_item_el

def parse_arguments():
    parser = argparse.ArgumentParser(description='Обработка входного текста и вывод в XML.')
    parser.add_argument('-i', '--input', required=True, help='Путь к входному текстовому файлу')
    parser.add_argument('-o', '--output', required=True, help='Путь к выходному XML-файлу')
    return parser.parse_args()

def read_input_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_output_file(output_path, data):
    with open(output_path, 'wb') as output_file:
        data.write(output_file, encoding='utf-8', xml_declaration=True)

def main():
    # Получение аргументов командной строки
    args = parse_arguments()

    # Чтение входного файла
    input_text = read_input_file(args.input)

    # Создаем парсер
    parser_lark = Lark(grammar, parser='lalr', transformer=XMLTransformer())
    xml_result = parser_lark.parse(input_text)
    tree = ET.ElementTree(xml_result)
    output_file_path = "output.xml"

    # Запись результата в выходной файл
    write_output_file(args.output, tree)

    print("Текст успешно обработан!")

if __name__ == "__main__":
    main()
