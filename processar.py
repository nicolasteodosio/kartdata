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

if __name__ == '__main__':
    parse_file(caminho='samples', arquivo='kart')
