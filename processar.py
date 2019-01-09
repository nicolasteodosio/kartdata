def parse_file():
    file = open("samples/kart.txt", 'r')
    file2 = open("samples/kartparsed.txt", 'w')
    for line in file:
        file2.write("; ".join(line.split()))
        file2.write("\n")
    file.close()
    file2.close()

if __name__ == '__main__':
    parse_file()
