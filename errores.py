# manejo de errores
class MiError(Exception):
    """error_base"""
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return f"ERROR: {self.__doc__}\n{"\n".join(map(str, self.args))}"
    
class ErrorExcel(MiError):
    """lectura archivo excel"""

class ErrorExtractUrls(MiError):
    """extrayendo urls del dataframe"""

class ErrorPlaywright(MiError):
    """playwright no obtubo el html"""

class ErrorBs4Parser(MiError):
    """bs4 parser"""

class ErrorBs4Find(MiError):
    """bs4 find"""

class ErrorBs4SelOne(MiError):
    """bs4 selectone"""

class ErrorGetInfo(MiError):
    """get info product"""

class ErrorGetPLP(MiError):
    """obteniendo PLP"""

class ErrorGetProductosInfo(MiError):
    """productos info"""