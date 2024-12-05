from lark import Lark, Transformer
import xml.etree.ElementTree as ET

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

    def NUMBER(self, items):
        number_el = ET.Element('number')
        number_el.text = items[0]
        return number_el

    def const_eval(self, items):
        print(items[0])
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


# Создаем парсер
parser = Lark(grammar, parser='lalr', transformer=XMLTransformer())

# Пример текста для парсинга
text = """
    def abc = 2
    def b = '(1 2)
    def c = $[d:2, e:1]
    def f = '(
        $[
            g: '(1 2 3),
            h: 4
        ]
    )
"""

# Парсим текст и выводим результат в XML
xml_result = parser.parse(text)
tree = ET.ElementTree(xml_result)
output_file_path = "output.xml"

# Открываем файл для записи
with open(output_file_path, 'wb') as output_file:
    tree.write(output_file, encoding='utf-8', xml_declaration=True)