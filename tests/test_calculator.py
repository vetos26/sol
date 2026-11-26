import unittest
from calculator import Calculator


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.c = Calculator()

    def number(self, text):
        for char in text:
            if char == '.':
                self.c.decimal()
            else:
                self.c.digit(char)

    def test_arithmetic_and_repeated_equals(self):
        self.number('12.5')
        self.c.operation('+')
        self.number('2.5')
        self.c.equals()
        self.assertEqual(self.c.display, '15')
        self.assertEqual(self.c.history, '12.5 + 2.5 =')
        self.c.equals()
        self.assertEqual(self.c.display, '17.5')

    def test_chaining_and_replacing_operator(self):
        self.number('8')
        self.c.operation('+')
        self.c.operation('*')
        self.number('3')
        self.c.operation('-')
        self.number('4')
        self.c.equals()
        self.assertEqual(self.c.display, '20')

    def test_division_by_zero_and_recovery(self):
        self.number('5')
        self.c.operation('/')
        self.number('0')
        self.c.equals()
        self.assertEqual(self.c.display, 'Ошибка')
        self.number('9')
        self.assertEqual(self.c.display, '9')
        self.assertEqual(self.c.history, '')

    def test_editing_sign_and_percent(self):
        self.number('123')
        self.c.backspace()
        self.c.sign()
        self.c.percent()
        self.assertEqual(self.c.display, '-0.12')
        self.c.clear()
        self.assertEqual(self.c.display, '0')

    def test_new_input_after_result(self):
        self.number('2')
        self.c.operation('+')
        self.number('2')
        self.c.equals()
        self.number('7')
        self.assertEqual(self.c.display, '7')
        self.assertEqual(self.c.history, '')

    def test_digit_limit(self):
        self.number('123456789012345')
        self.assertEqual(self.c.display, '123456789012')


if __name__ == '__main__':
    unittest.main()
