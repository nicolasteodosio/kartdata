from unittest import TestCase, mock

from processar import parse_file


class TestParseFile(TestCase):
    def setUp(self):
        self.caminho = 'samples_test'

    def test_parse_sucesso(self):
        parse_file(self.caminho, 'kart')
        with open("{}/kartparsed.txt".format(self.caminho), 'r') as file:
            self.assertEqual(file.readlines(), ['23:49:08.277; 038; –; F.MASSA; 1; 1:02.852; 44,275\n', '23:49:10.858; 033; –; R.BARRICHELLO; 1; 1:04.352; 43,243\n'])

    @mock.patch('processar.open')
    def test_parse_erro(self, arquivo):
        arquivo.side_effect = Exception

        self.assertRaises(Exception, parse_file, self.caminho, 'kart')
