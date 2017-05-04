import calc

INP = """a=10;
        a+a;
        fun gg(a,b)
            a=b;
            a
        end;
        fun ff()
            42
        end;
"""


class TestParser:
    def setUp(self):
        calc.new_parser()
        self.g = calc.Generator()
        pass

    def test_parser(self):
        s = INP
        self.g.parse(s)
        print(self.g.print())

    def test_lexer(self):

        # Test it out

        data = INP

        # Give the lexer some input
        calc.lexer.input(data)

        # Tokenize
        while True:

            tok = calc.lexer.token()
            if not tok:
                break      # No more input
            # print(tok)


def main():
    t = TestParser()
    t.setUp()
    t.test_parser()


if __name__ == '__main__':
    main()
