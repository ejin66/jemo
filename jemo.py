import sys

from parser_impl.json_generator import JsonGenerator
from parser_impl.json_parser import JsonParser


def readLineFeed(data: str) -> str:
    lineFeed = ""
    for char in data:
        if char == '\r' or char == '\n':
            lineFeed += char
        elif lineFeed == '':
            continue
        else:
            break
    return lineFeed


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("file path miss")
        exit(1)

    # 源配置文件
    file = sys.argv[1]
    # 生成文件的地址
    generatePath = file.split("/")[-1].split(".")[0] + ".dart"
    if len(sys.argv) > 2:
        generatePath = sys.argv[2]
    # 读取源配置文件
    f = open(file, "r", encoding="UTF-8")
    source = f.read()
    f.close()
    lineFeed = readLineFeed(source)

    parser = JsonParser(lineFeed)
    generator = JsonGenerator(lineFeed)
    parseNodes = parser.parse(source.encode(encoding="utf-8"))
    code = generator.generate(parseNodes)

    # 写到文件
    writeFile = open(generatePath, mode="w+", encoding="utf-8")
    writeFile.write(code)
    writeFile.flush()
    writeFile.close()
