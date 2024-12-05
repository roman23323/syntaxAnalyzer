import unittest
import os
import subprocess

class TestProgram(unittest.TestCase):

    def setUp(self):
        # Путь к входным и ожидаемым выходным файлам
        self.input_file_1 = 'test/text1.txt'
        self.output_file_1 = 'output1.xml'
        self.expected_output_file_1 = 'test/expected_output_1.xml'

        self.input_file_2 = 'test/text2.txt'
        self.output_file_2 = 'output2.xml'
        self.expected_output_file_2 = 'test/expected_output_2.xml'

    def tearDown(self):
        # Удаляем выходные файлы после тестов, если они существуют
        if os.path.exists(self.output_file_1):
            os.remove(self.output_file_1)
        if os.path.exists(self.output_file_2):
            os.remove(self.output_file_2)
    def test_program_output_1(self):
        # Запускаем программу с первым набором файлов
        subprocess.run(['python', 'syntaxAnalyzer.py', '-i', self.input_file_1, '-o', self.output_file_1])

        # Проверяем, что выходной файл был создан
        self.assertTrue(os.path.exists(self.output_file_1))

        # Проверяем содержимое выходного файла на соответствие ожидаемому
        self.compare_files(self.output_file_1, self.expected_output_file_1)

    def test_program_output_2(self):
        # Запускаем программу со вторым набором файлов
        subprocess.run(['python', 'syntaxAnalyzer.py', '-i', self.input_file_2, '-o', self.output_file_2])

        # Проверяем, что выходной файл был создан
        self.assertTrue(os.path.exists(self.output_file_2))

        # Проверяем содержимое выходного файла на соответствие ожидаемому
        self.compare_files(self.output_file_2, self.expected_output_file_2)

    def compare_files(self, output_file, expected_file):
        """Сравнивает два файла и проверяет их содержимое."""
        with open(output_file, 'r', encoding='utf-8') as f1, open(expected_file, 'r', encoding='utf-8') as f2:
            output_content = f1.read()
            expected_content = f2.read()
            self.assertEqual(output_content.strip(), expected_content.strip(),
                             f'Содержимое файла {output_file} не соответствует {expected_file}')

if __name__ == '__main__':
    unittest.main()