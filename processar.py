from statistics import mean


def parse_file(caminho, arquivo):
    try:
        file = open("{}/{}.txt".format(caminho, arquivo), 'r')
        file2 = open("{}/kartparsed.txt".format(caminho), 'w')
        for line in file:
            file2.write("; ".join(line.split()))
            file2.write("\n")
        file.close()
        file2.close()
    except Exception as e:
        raise e


def prepara_resultados(completo=False, caminho='samples'):
    file = open("{}/kartparsed.txt".format(caminho), 'r')
    mapa = {}
    voltas_dadas = []
    for line in file:
        valores = line.replace('\n', '').split('; ')
        try:
            if not completo:
                if valores[4] == '4' and '4' in voltas_dadas:
                    return mapa

            if valores[1] not in mapa:
                mapa[valores[1]] = {'nome': valores[3],
                                    'voltas': [{'numero': valores[4],
                                                'tempo': valores[5],
                                                'horario': valores[0],
                                                'media': valores[6]}],
                                    }
            else:
                mapa[valores[1]]['voltas'].append({'numero': valores[4],
                                                   'tempo': valores[5],
                                                   'horario': valores[0],
                                                   'media': valores[6]})
            voltas_dadas.append(valores[4])
        except Exception as e:
            raise e
    return mapa


def calcula_total_prova(tempo_voltas):
    minuto_total = 0
    segundo_total = 0
    milisegundo_total = 0

    for tempo in tempo_voltas:
        (minuto, segundo) = tempo.split(':')
        (segundo, milisegundo) = segundo.split('.')
        minuto_total += int(minuto)
        segundo_total += int(segundo)
        milisegundo_total += int(milisegundo)
        if milisegundo_total >= 1000:
            segundo_total += 1
            milisegundo_total -= 1000
        if segundo_total >= 60:
            minuto_total += 1
            segundo_total -= 60

    return '{}:{}.{}'.format(minuto_total, segundo_total, milisegundo_total)


def finaliza_resultado(mapa):
    resultado_prova = []
    for key, value in mapa.items():
        tempo_voltas = []
        for volta in value['voltas']:
            tempo_voltas.append(volta['tempo'])
        tempo_total = calcula_total_prova(tempo_voltas)
        resultado_prova.append({'codigo': key,
                                'nome': value['nome'],
                                'qtd_voltas': len(value['voltas']),
                                'tempo_total_prova': tempo_total
                                })
    resultado_ordenado = sorted(resultado_prova, key=lambda k: (-k['qtd_voltas'], k['tempo_total_prova']))
    for index, resultado in enumerate(resultado_ordenado):
        resultado['posicao'] = index + 1
    return resultado_ordenado


def calcula_melhor_volta(mapa, corrida=False):
    melhor_volta_corrida = []
    for key, value in mapa.items():
        tempo_voltas = []
        for volta in value['voltas']:
            tempo_voltas.append(volta['tempo'])
        min_tempo = min(tempo_voltas)
        melhor_volta_corrida.append({'codigo': key, 'nome': value['nome'], 'melhor_volta': min_tempo})
    if corrida:
        return min(melhor_volta_corrida, key=lambda k: k['melhor_volta'])

    return melhor_volta_corrida


def calcula_velocidade_media(mapa):
    media_velocidade_piloto = []
    for key, value in mapa.items():
        medias = []
        for volta in value['voltas']:
            medias.append(float(volta['media'].replace(',', '.')))
        media_calulada = mean(medias)
        media_velocidade_piloto.append({'codigo': key, 'nome': value['nome'], 'media_velocidade': media_calulada})
    return media_velocidade_piloto


if __name__ == '__main__':
    parse_file(caminho='samples', arquivo='kart')
    mapa = prepara_resultados()
    resultado = finaliza_resultado(mapa)
    resultado_melhor_volta = calcula_melhor_volta(mapa)
    media = calcula_velocidade_media(mapa)
    print('########## RESULTADO CORRIDA ##########')
    print(resultado)
    print('########## MELHOR VOLTA ##########')
    print(resultado_melhor_volta)
    print('########## VELOCIDADE MEDIA ##########')
    print(media)
