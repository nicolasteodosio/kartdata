from unittest import TestCase, mock

from processar import parse_file, prepara_resultados, calcula_total_prova, finaliza_resultado


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


class TestPreparaResultado(TestCase):
    def setUp(self):
        self.caminho = 'samples_test'

    def test_retorna_mapa_corretamente_completo(self):
        mapa = prepara_resultados(caminho='samples_test', completo=True)

        self.assertEqual(mapa, {'033': {'nome': 'R.BARRICHELLO',
                                        'voltas': [{'horario': '23:49:10.858',
                                                    'media': '43,243',
                                                    'numero': '1',
                                                    'tempo': '1:04.352'}]},
                                '038': {'nome': 'F.MASSA',
                                        'voltas': [{'horario': '23:49:08.277',
                                                    'media': '44,275',
                                                    'numero': '1',
                                                    'tempo': '1:02.852'}]}})

    @mock.patch('processar.open')
    def test_retorna_mapa_corretamente(self, arquivo):
        arquivo.return_value = ['23:49:08.277; 038; –; F.MASSA; 1; 1:02.852; 44,275',
                                '23:49:10.858; 033; –; R.BARRICHELLO; 1; 1:04.352; 43,243',
                                '23:49:08.277; 038; –; F.MASSA; 4; 1:02.852; 44,275',
                                '23:49:10.858; 033; –; R.BARRICHELLO; 4; 1:04.352; 43,243']
        mapa = prepara_resultados(caminho='samples_test')

        self.assertEqual(mapa, {'033': {'nome': 'R.BARRICHELLO',
                                        'voltas': [{'horario': '23:49:10.858',
                                                    'media': '43,243',
                                                    'numero': '1',
                                                    'tempo': '1:04.352'}]},
                                '038': {'nome': 'F.MASSA',
                                        'voltas': [{'horario': '23:49:08.277',
                                                    'media': '44,275',
                                                    'numero': '1',
                                                    'tempo': '1:02.852'},
                                                   {'horario': '23:49:08.277',
                                                    'media': '44,275',
                                                    'numero': '4',
                                                    'tempo': '1:02.852'}]}})

    @mock.patch('processar.open')
    def test_prepara_resultados_exception(self, arquivo):
        arquivo.side_effect = Exception
        self.assertRaises(Exception, prepara_resultados, caminho='samples_test')

    @mock.patch('processar.open')
    def test_prepara_resultado_arquivo_com_erro(self, arquivo):
        arquivo.return_value = ['23:49:08.277; 038; –; F.MASSA; 1; 1:02.852; 44,275',
                                '23:49:10.858; 1:04.352; 43,243',
                                '23:49:08.277; 038; –; F.MASSA; 4; 1:02.852; 44,275',
                                '23:49:10.858; 033; –; R.BARRICHELLO; 4; 1:04.352; 43,243']
        self.assertRaises(IndexError, prepara_resultados, caminho='samples_test')


class TestCalculoTotalProva(TestCase):
    def test_calcula_total_simples(self):
        calculo = calcula_total_prova(['01:01.001', '01:01.001', '01:01.101'])
        self.assertEqual(calculo, '3:3.103')

    def test_calcula_total_aumento_minuto(self):
        calculo = calcula_total_prova(['01:01.001', '01:59.001', '01:01.101'])
        self.assertEqual(calculo, '4:1.103')

    def test_calcula_total_aumento_segundo(self):
        calculo = calcula_total_prova(['01:01.401', '01:45.901', '01:01.101'])
        self.assertEqual(calculo, '3:48.403')

    def test_calcula_total_valores_com_erro_exception(self):
        valores = ['01:01.401', '01:45.901', 'lala']
        self.assertRaises(Exception, calcula_total_prova, valores)

    def test_calcula_total_valores_com_erro(self):
        valores = ['01:01:401', '01:45.901', ]
        self.assertRaises(Exception, calcula_total_prova, valores)


class TestFinalizaResultado(TestCase):
    def test_resultado_fnal_ordenado(self):
        mapa = {'033': {'nome': 'R.BARRICHELLO',
                                        'voltas': [{'horario': '23:49:10.858',
                                                    'media': '43,243',
                                                    'numero': '1',
                                                    'tempo': '1:04.352'}]},
                                '038': {'nome': 'F.MASSA',
                                        'voltas': [{'horario': '23:49:08.277',
                                                    'media': '44,275',
                                                    'numero': '1',
                                                    'tempo': '1:02.852'},
                                                   {'horario': '23:49:08.277',
                                                    'media': '44,275',
                                                    'numero': '4',
                                                    'tempo': '1:02.852'}]}}
        resultado = finaliza_resultado(mapa)

        self.assertEqual(resultado, [
            {'codigo': '038', 'nome': 'F.MASSA', 'qtd_voltas': 2, 'tempo_total_prova': '2:5.704', 'posicao': 1},
            {'codigo': '033', 'nome': 'R.BARRICHELLO', 'qtd_voltas': 1, 'tempo_total_prova': '1:4.352', 'posicao': 2}])

    def test_resultado_fnal_ordenado_mapa_errado(self):
        mapa = {'033': {'nome'}}

        self.assertRaises(Exception, finaliza_resultado, mapa)

    def test_resultado_fnal_ordenado_mapa_nao_dicionario(self):
        mapa = ['033', {'nome'}]

        self.assertRaises(Exception, finaliza_resultado, mapa)

