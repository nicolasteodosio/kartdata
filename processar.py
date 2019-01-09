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


if __name__ == '__main__':
    parse_file(caminho='samples', arquivo='kart')
    mapa = prepara_resultados()
