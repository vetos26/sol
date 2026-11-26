"""Calculation state and arithmetic, independent from the Kivy interface."""
from decimal import Decimal, DecimalException, localcontext


class Calculator:
    SYMBOLS = {'+': '+', '-': '−', '*': '×', '/': '÷'}
    MAX_DIGITS = 12

    def __init__(self):
        self.clear()

    def clear(self):
        self.entry = '0'
        self.accumulator = None
        self.operator = None
        self.waiting = False
        self.finished = False
        self.error = False
        self.history = ''
        self.last_operator = None
        self.last_operand = None

    @staticmethod
    def format_number(value):
        if not value:
            return '0'
        # Keep normal results readable, switching to scientific notation only
        # when they would not comfortably fit on the calculator's display.
        normalized = value.normalize()
        if -12 <= normalized.adjusted() <= 13:
            text = format(normalized, 'f')
            if len(text) <= 14:
                return text
        return format(normalized, '.7E').replace('E+', 'e').replace('E', 'e')

    @property
    def display(self):
        return 'Ошибка' if self.error else self.entry

    def _fail(self):
        self.clear()
        self.error = True
        self.history = 'Деление на ноль невозможно'

    def digit(self, digit):
        if digit not in '0123456789' or len(digit) != 1:
            return
        if self.error or self.finished:
            self.clear()
        if self.waiting or 'e' in self.entry:
            self.entry = digit
            self.waiting = False
            return
        if sum(c.isdigit() for c in self.entry) >= self.MAX_DIGITS:
            return
        if self.entry == '0':
            self.entry = digit
        elif self.entry == '-0':
            self.entry = '-' + digit
        else:
            self.entry += digit

    def decimal(self):
        if self.error or self.finished:
            self.clear()
        if self.waiting:
            self.entry = '0.'
            self.waiting = False
        elif '.' not in self.entry and 'e' not in self.entry:
            self.entry += '.'

    def backspace(self):
        if self.error:
            self.clear()
        elif not self.waiting and not self.finished:
            if 'e' in self.entry:
                self.entry = '0'
                return
            self.entry = self.entry[:-1]
            if self.entry in ('', '-'):
                self.entry = '0'

    def sign(self):
        if self.error:
            return
        if self.waiting:
            self.entry = '0'
            self.waiting = False
        self.entry = self.entry[1:] if self.entry.startswith('-') else '-' + self.entry
        if self.finished:
            self.finished = False
            self.history = ''

    def percent(self):
        if self.error:
            return
        # Percentage is the displayed value divided by 100.
        self.entry = self.format_number(Decimal(self.entry) / 100)
        if self.waiting:
            self.waiting = False
        if self.finished:
            self.finished = False
            self.history = ''

    @staticmethod
    def _calculate(left, operator, right):
        with localcontext() as ctx:
            ctx.prec = 28
            if operator == '+':
                return left + right
            if operator == '-':
                return left - right
            if operator == '*':
                return left * right
            return left / right

    def operation(self, operator):
        if self.error or operator not in self.SYMBOLS:
            return
        value = Decimal(self.entry)
        if self.operator and not self.waiting:
            try:
                value = self._calculate(self.accumulator, self.operator, value)
            except DecimalException:
                self._fail()
                return
            self.entry = self.format_number(value)
            # Use the displayed, rounded value for subsequent calculations.
            value = Decimal(self.entry)
        self.accumulator = value
        self.operator = operator
        self.waiting = True
        self.finished = False
        self.last_operator = self.last_operand = None
        self.history = f'{self.format_number(value)} {self.SYMBOLS[operator]}'

    def equals(self):
        if self.error:
            return
        if self.operator:
            left = self.accumulator
            right = left if self.waiting else Decimal(self.entry)
            operator = self.operator
        elif self.finished and self.last_operator:
            left = Decimal(self.entry)
            right = self.last_operand
            operator = self.last_operator
        else:
            return
        try:
            result = self._calculate(left, operator, right)
        except DecimalException:
            self._fail()
            return
        self.history = (f'{self.format_number(left)} {self.SYMBOLS[operator]} '
                        f'{self.format_number(right)} =')
        self.entry = self.format_number(result)
        self.last_operator, self.last_operand = operator, right
        self.accumulator = self.operator = None
        self.waiting = False
        self.finished = True
