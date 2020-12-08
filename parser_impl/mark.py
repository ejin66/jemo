def _parseMark(mark: str):
    result = {}
    for kv in mark.split(","):
        data = kv.split(":")
        if len(data) != 2:
            continue
        key = data[0].strip()
        value = data[1].strip()
        result[key] = value
    return result


class Mark:

    def read(self, mark: str):
        raise NotImplementedError


class ImportMark(Mark):
    library: str = ''

    def read(self, mark: str):
        dic = _parseMark(mark)
        if dic.__contains__("import"):
            self.library = dic["import"]


class RootMark(Mark):
    cls: str = ''
    super: str = ''

    def read(self, mark: str):
        dic = _parseMark(mark)
        if dic.__contains__("class"):
            self.cls = dic["class"]
        if dic.__contains__("super"):
            self.super = dic["super"]
        pass


class LeafMark(Mark):
    alias: str = ''
    nullable: bool = False

    def read(self, mark: str):
        dic = _parseMark(mark)
        if dic.__contains__("alias"):
            self.alias = dic["alias"]
        if dic.__contains__("nullable"):
            self.nullable = (True if dic["nullable"] == "true" else False)


class ObjectMark(LeafMark):
    cls: str = ''

    def read(self, mark: str):
        super(ObjectMark, self).read(mark)
        dic = _parseMark(mark)
        if dic.__contains__("class"):
            self.cls = dic["class"]
