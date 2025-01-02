import streamlit as st
import datetime
import sqlite3
import os

# Configuração inicial do banco de dados
def init_db():
    db_path = "leitura_biblica.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leituras_concluidas
                 (dia INTEGER PRIMARY KEY, data_conclusao TEXT)''')
    conn.commit()
    conn.close()

# Função para marcar uma leitura como concluída
def marcar_concluida(dia, concluida=True):
    conn = sqlite3.connect("leitura_biblica.db")
    c = conn.cursor()
    if concluida:
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT OR REPLACE INTO leituras_concluidas (dia, data_conclusao) VALUES (?, ?)",
                  (dia, data_atual))
    else:
        c.execute("DELETE FROM leituras_concluidas WHERE dia = ?", (dia,))
    conn.commit()
    conn.close()

# Função para verificar se uma leitura está concluída
def esta_concluida(dia):
    conn = sqlite3.connect("leitura_biblica.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM leituras_concluidas WHERE dia = ?", (dia,))
    resultado = c.fetchone() is not None
    conn.close()
    return resultado

# Função para obter todas as leituras concluídas
def get_leituras_concluidas():
    conn = sqlite3.connect("leitura_biblica.db")
    c = conn.cursor()
    c.execute("SELECT dia FROM leituras_concluidas")
    dias = [row[0] for row in c.fetchall()]
    conn.close()
    return dias

# Dados do plano de leitura (ano completo)
PLANO_LEITURA = {
    # Janeiro
    1: {"passagem": "Lucas 1", "mes": "Janeiro"},
    2: {"passagem": "Lucas 2-3", "mes": "Janeiro"},
    3: {"passagem": "Lucas 4-5", "mes": "Janeiro"},
    4: {"passagem": "Lucas 6-7", "mes": "Janeiro"},
    5: {"passagem": "Lucas 8", "mes": "Janeiro"},
    6: {"passagem": "Lucas 9", "mes": "Janeiro"},
    7: {"passagem": "Lucas 10-11", "mes": "Janeiro"},
    8: {"passagem": "Lucas 12-13", "mes": "Janeiro"},
    9: {"passagem": "Lucas 14-15", "mes": "Janeiro"},
    10: {"passagem": "Lucas 17-18", "mes": "Janeiro"},
    11: {"passagem": "Lucas 19-20", "mes": "Janeiro"},
    12: {"passagem": "Lucas 21-22", "mes": "Janeiro"},
    13: {"passagem": "Lucas 23-24", "mes": "Janeiro"},
    14: {"passagem": "Atos 1-3", "mes": "Janeiro"},
    15: {"passagem": "Atos 4-6", "mes": "Janeiro"},
    16: {"passagem": "Atos 7-8", "mes": "Janeiro"},
    17: {"passagem": "Atos 9-10", "mes": "Janeiro"},
    18: {"passagem": "Atos 11-13", "mes": "Janeiro"},
    19: {"passagem": "Atos 14-16", "mes": "Janeiro"},
    20: {"passagem": "Atos 17-18", "mes": "Janeiro"},
    21: {"passagem": "Atos 19-20", "mes": "Janeiro"},
    22: {"passagem": "Atos 21-22", "mes": "Janeiro"},
    23: {"passagem": "Atos 23-25", "mes": "Janeiro"},
    24: {"passagem": "Atos 26-28", "mes": "Janeiro"},
    25: {"passagem": "Romanos 1-3", "mes": "Janeiro"},
    26: {"passagem": "Romanos 4-7", "mes": "Janeiro"},
    27: {"passagem": "Romanos 8-10", "mes": "Janeiro"},
    28: {"passagem": "Romanos 11-14", "mes": "Janeiro"},
    29: {"passagem": "Romanos 15-16", "mes": "Janeiro"},
    30: {"passagem": "1 Coríntios 1-4", "mes": "Janeiro"},
    31: {"passagem": "1 Coríntios 5-8", "mes": "Janeiro"},
    
    # Fevereiro
    32: {"passagem": "1 Coríntios 9-11", "mes": "Fevereiro"},
    33: {"passagem": "1 Coríntios 12-14", "mes": "Fevereiro"},
    34: {"passagem": "1 Coríntios 15-16", "mes": "Fevereiro"},
    35: {"passagem": "2 Coríntios 1-4", "mes": "Fevereiro"},
    36: {"passagem": "2 Coríntios 5-8", "mes": "Fevereiro"},
    37: {"passagem": "2 Coríntios 9-13", "mes": "Fevereiro"},
    38: {"passagem": "Gálatas 1-4", "mes": "Fevereiro"},
    39: {"passagem": "Gálatas 5-6", "mes": "Fevereiro"},
    40: {"passagem": "Efésios 1-4", "mes": "Fevereiro"},
    41: {"passagem": "Efésios 5-6", "mes": "Fevereiro"},
    42: {"passagem": "Filipenses", "mes": "Fevereiro"},
    43: {"passagem": "Colossenses", "mes": "Fevereiro"},
    44: {"passagem": "1 Tessalonicenses", "mes": "Fevereiro"},
    45: {"passagem": "2 Tessalonicenses", "mes": "Fevereiro"},
    46: {"passagem": "1 Timóteo 1-4", "mes": "Fevereiro"},
    47: {"passagem": "1 Timóteo 5-6", "mes": "Fevereiro"},
    48: {"passagem": "2 Timóteo", "mes": "Fevereiro"},
    49: {"passagem": "Tito e Filemom", "mes": "Fevereiro"},
    50: {"passagem": "Hebreus 1-3", "mes": "Fevereiro"},
    51: {"passagem": "Hebreus 4-7", "mes": "Fevereiro"},
    52: {"passagem": "Hebreus 8-11", "mes": "Fevereiro"},
    53: {"passagem": "Hebreus 12-13", "mes": "Fevereiro"},
    54: {"passagem": "Tiago", "mes": "Fevereiro"},
    55: {"passagem": "1 Pedro", "mes": "Fevereiro"},
    56: {"passagem": "2 Pedro", "mes": "Fevereiro"},
    57: {"passagem": "1 João 1-3", "mes": "Fevereiro"},
    58: {"passagem": "1 João 4-5", "mes": "Fevereiro"},
    59: {"passagem": "2 e 3 João e Judas", "mes": "Fevereiro"},
    
    # Março
    60: {"passagem": "Gênesis 1-3", "mes": "Março"},
    61: {"passagem": "Gênesis 4-7", "mes": "Março"},
    62: {"passagem": "Gênesis 8-11", "mes": "Março"},
    63: {"passagem": "Gênesis 12-15", "mes": "Março"},
    64: {"passagem": "Gênesis 16-18", "mes": "Março"},
    65: {"passagem": "Gênesis 19-22", "mes": "Março"},
    66: {"passagem": "Gênesis 23-26", "mes": "Março"},
    67: {"passagem": "Gênesis 27-29", "mes": "Março"},
    68: {"passagem": "Gênesis 30-32", "mes": "Março"},
    69: {"passagem": "Gênesis 33-35", "mes": "Março"},
    70: {"passagem": "Gênesis 36-38", "mes": "Março"},
    71: {"passagem": "Gênesis 39-41", "mes": "Março"},
    72: {"passagem": "Gênesis 42-44", "mes": "Março"},
    73: {"passagem": "Gênesis 45-47", "mes": "Março"},
    74: {"passagem": "Gênesis 48-50", "mes": "Março"},
    75: {"passagem": "Êxodo 1-3", "mes": "Março"},
    76: {"passagem": "Êxodo 4-6", "mes": "Março"},
    77: {"passagem": "Êxodo 7-9", "mes": "Março"},
    78: {"passagem": "Êxodo 10-12", "mes": "Março"},
    79: {"passagem": "Êxodo 13-15", "mes": "Março"},
    80: {"passagem": "Êxodo 16-18", "mes": "Março"},
    81: {"passagem": "Êxodo 19-21", "mes": "Março"},
    82: {"passagem": "Êxodo 22-24", "mes": "Março"},
    83: {"passagem": "Êxodo 25-27", "mes": "Março"},
    84: {"passagem": "Êxodo 28-30", "mes": "Março"},
    85: {"passagem": "Êxodo 31-33", "mes": "Março"},
    86: {"passagem": "Êxodo 34-36", "mes": "Março"},
    87: {"passagem": "Êxodo 37-38", "mes": "Março"},
    88: {"passagem": "Êxodo 39-40", "mes": "Março"},
    89: {"passagem": "Levítico 1-4", "mes": "Março"},
    90: {"passagem": "Levítico 5-7", "mes": "Março"},
    
    # Abril
    91: {"passagem": "Números 1-4", "mes": "Abril"},
    92: {"passagem": "Números 5-6", "mes": "Abril"},
    93: {"passagem": "Números 7", "mes": "Abril"},
    94: {"passagem": "Números 8-10", "mes": "Abril"},
    95: {"passagem": "Números 11-13", "mes": "Abril"},
    96: {"passagem": "Números 14-15", "mes": "Abril"},
    97: {"passagem": "Números 16-18", "mes": "Abril"},
    98: {"passagem": "Números 19-21", "mes": "Abril"},
    99: {"passagem": "Números 22-24", "mes": "Abril"},
    100: {"passagem": "Números 25-26", "mes": "Abril"},
    101: {"passagem": "Números 27-29", "mes": "Abril"},
    102: {"passagem": "Números 30-31", "mes": "Abril"},
    103: {"passagem": "Números 32-33", "mes": "Abril"},
    104: {"passagem": "Números 34-36", "mes": "Abril"},
    105: {"passagem": "Deuteronômio 1-2", "mes": "Abril"},
    106: {"passagem": "Deuteronômio 3-4", "mes": "Abril"},
    107: {"passagem": "Deuteronômio 5-7", "mes": "Abril"},
    108: {"passagem": "Deuteronômio 8-10", "mes": "Abril"},
    109: {"passagem": "Deuteronômio 11-13", "mes": "Abril"},
    110: {"passagem": "Deuteronômio 14-16", "mes": "Abril"},
    111: {"passagem": "Deuteronômio 17-19", "mes": "Abril"},
    112: {"passagem": "Deuteronômio 20-22", "mes": "Abril"},
    113: {"passagem": "Deuteronômio 23-25", "mes": "Abril"},
    114: {"passagem": "Deuteronômio 26-27", "mes": "Abril"},
    115: {"passagem": "Deuteronômio 28", "mes": "Abril"},
    116: {"passagem": "Deuteronômio 29-31", "mes": "Abril"},
    117: {"passagem": "Deuteronômio 32-34", "mes": "Abril"},
    118: {"passagem": "Josué 1-3", "mes": "Abril"},
    119: {"passagem": "Josué 4-6", "mes": "Abril"},
    120: {"passagem": "Josué 7-8", "mes": "Abril"},
    
    # Maio
    121: {"passagem": "Mateus 1-4", "mes": "Maio"},
    122: {"passagem": "Mateus 5-7", "mes": "Maio"},
    123: {"passagem": "Mateus 8-10", "mes": "Maio"},
    124: {"passagem": "Mateus 11-13", "mes": "Maio"},
    125: {"passagem": "Mateus 14-16", "mes": "Maio"},
    126: {"passagem": "Mateus 17-19", "mes": "Maio"},
    127: {"passagem": "Mateus 20-22", "mes": "Maio"},
    128: {"passagem": "Mateus 23-24", "mes": "Maio"},
    129: {"passagem": "Mateus 25-26", "mes": "Maio"},
    130: {"passagem": "Mateus 27-28", "mes": "Maio"},
    131: {"passagem": "Hebreus 1-4", "mes": "Maio"},
    132: {"passagem": "Hebreus 5-8", "mes": "Maio"},
    133: {"passagem": "Hebreus 9-10", "mes": "Maio"},
    134: {"passagem": "Hebreus 11-13", "mes": "Maio"},
    135: {"passagem": "João 1-3", "mes": "Maio"},
    136: {"passagem": "João 4-5", "mes": "Maio"},
    137: {"passagem": "João 6-8", "mes": "Maio"},
    138: {"passagem": "João 9-11", "mes": "Maio"},
    139: {"passagem": "João 12-13", "mes": "Maio"},
    140: {"passagem": "João 14-16", "mes": "Maio"},
    141: {"passagem": "João 17-18", "mes": "Maio"},
    142: {"passagem": "João 19-21", "mes": "Maio"},
    143: {"passagem": "Apocalipse 1-3", "mes": "Maio"},
    144: {"passagem": "Apocalipse 4-6", "mes": "Maio"},
    145: {"passagem": "Apocalipse 7-9", "mes": "Maio"},
    146: {"passagem": "Apocalipse 10-12", "mes": "Maio"},
    147: {"passagem": "Apocalipse 13-15", "mes": "Maio"},
    148: {"passagem": "Apocalipse 16-18", "mes": "Maio"},
    149: {"passagem": "Apocalipse 19-20", "mes": "Maio"},
    150: {"passagem": "Apocalipse 21-22", "mes": "Maio"},
    151: {"passagem": "Marcos 1-3", "mes": "Maio"},
    
    # Junho
    152: {"passagem": "Marcos 4-6", "mes": "Junho"},
    153: {"passagem": "Marcos 7-9", "mes": "Junho"},
    154: {"passagem": "Marcos 10-11", "mes": "Junho"},
    155: {"passagem": "Marcos 12-13", "mes": "Junho"},
    156: {"passagem": "Marcos 14-16", "mes": "Junho"},
    157: {"passagem": "1 Pedro", "mes": "Junho"},
    158: {"passagem": "2 Pedro", "mes": "Junho"},
    159: {"passagem": "Josué 1-4", "mes": "Junho"},
    160: {"passagem": "Josué 5-8", "mes": "Junho"},
    161: {"passagem": "Josué 9-11", "mes": "Junho"},
    162: {"passagem": "Josué 12-15", "mes": "Junho"},
    163: {"passagem": "Josué 16-18", "mes": "Junho"},
    164: {"passagem": "Josué 19-21", "mes": "Junho"},
    165: {"passagem": "Josué 22-24", "mes": "Junho"},
    166: {"passagem": "Juízes 1-3", "mes": "Junho"},
    167: {"passagem": "Juízes 4-6", "mes": "Junho"},
    168: {"passagem": "Juízes 7-8", "mes": "Junho"},
    169: {"passagem": "Juízes 9-10", "mes": "Junho"},
    170: {"passagem": "Juízes 11-13", "mes": "Junho"},
    171: {"passagem": "Juízes 14-16", "mes": "Junho"},
    172: {"passagem": "Juízes 17-19", "mes": "Junho"},
    173: {"passagem": "Juízes 20-21", "mes": "Junho"},
    174: {"passagem": "1 Samuel 1-3", "mes": "Junho"},
    175: {"passagem": "1 Samuel 4-7", "mes": "Junho"},
    176: {"passagem": "1 Samuel 8-10", "mes": "Junho"},
    177: {"passagem": "1 Samuel 11-13", "mes": "Junho"},
    178: {"passagem": "1 Samuel 14-15", "mes": "Junho"},
    179: {"passagem": "1 Samuel 16-17", "mes": "Junho"},
    180: {"passagem": "1 Samuel 18-20", "mes": "Junho"},
    181: {"passagem": "1 Samuel 21-24", "mes": "Junho"},
    
    # Julho
    182: {"passagem": "1 Samuel 25-27", "mes": "Julho"},
    183: {"passagem": "1 Samuel 28-31", "mes": "Julho"},
    184: {"passagem": "2 Samuel 1-3", "mes": "Julho"},
    185: {"passagem": "2 Samuel 4-7", "mes": "Julho"},
    186: {"passagem": "2 Samuel 8-11", "mes": "Julho"},
    187: {"passagem": "2 Samuel 12-14", "mes": "Julho"},
    188: {"passagem": "2 Samuel 15-17", "mes": "Julho"},
    189: {"passagem": "2 Samuel 18-20", "mes": "Julho"},
    190: {"passagem": "2 Samuel 21-24", "mes": "Julho"},
    191: {"passagem": "1 Reis 1-3", "mes": "Julho"},
    192: {"passagem": "1 Reis 4-6", "mes": "Julho"},
    193: {"passagem": "1 Reis 7", "mes": "Julho"},
    194: {"passagem": "1 Reis 8", "mes": "Julho"},
    195: {"passagem": "1 Reis 9-10", "mes": "Julho"},
    196: {"passagem": "1 Reis 11-13", "mes": "Julho"},
    197: {"passagem": "1 Reis 14-16", "mes": "Julho"},
    198: {"passagem": "1 Reis 17-19", "mes": "Julho"},
    199: {"passagem": "1 Reis 20-22", "mes": "Julho"},
    200: {"passagem": "2 Reis 1-3", "mes": "Julho"},
    201: {"passagem": "2 Reis 4-6", "mes": "Julho"},
    202: {"passagem": "2 Reis 7-9", "mes": "Julho"},
    203: {"passagem": "2 Reis 10-12", "mes": "Julho"},
    204: {"passagem": "2 Reis 13-14", "mes": "Julho"},
    205: {"passagem": "2 Reis 15-17", "mes": "Julho"},
    206: {"passagem": "2 Reis 18-19", "mes": "Julho"},
    207: {"passagem": "2 Reis 20-22", "mes": "Julho"},
    208: {"passagem": "2 Reis 23-25", "mes": "Julho"},
    209: {"passagem": "1 Crônicas 1-3", "mes": "Julho"},
    210: {"passagem": "1 Crônicas 4-6", "mes": "Julho"},
    211: {"passagem": "1 Crônicas 7-9", "mes": "Julho"},
    212: {"passagem": "1 Crônicas 10-12", "mes": "Julho"},
    
    # Agosto
    213: {"passagem": "2 Reis 15-16", "mes": "Agosto"},
    214: {"passagem": "2 Reis 17-18", "mes": "Agosto"},
    215: {"passagem": "2 Reis 19-21", "mes": "Agosto"},
    216: {"passagem": "2 Reis 22-25", "mes": "Agosto"},
    217: {"passagem": "1 Crônicas 1", "mes": "Agosto"},
    218: {"passagem": "1 Crônicas 2-4", "mes": "Agosto"},
    219: {"passagem": "1 Crônicas 5-7", "mes": "Agosto"},
    220: {"passagem": "1 Crônicas 8-9", "mes": "Agosto"},
    221: {"passagem": "1 Crônicas 10-12", "mes": "Agosto"},
    222: {"passagem": "1 Crônicas 13-16", "mes": "Agosto"},
    223: {"passagem": "1 Crônicas 17-19", "mes": "Agosto"},
    224: {"passagem": "1 Crônicas 20-23", "mes": "Agosto"},
    225: {"passagem": "1 Crônicas 24-26", "mes": "Agosto"},
    226: {"passagem": "1 Crônicas 27-29", "mes": "Agosto"},
    227: {"passagem": "2 Crônicas 1-4", "mes": "Agosto"},
    228: {"passagem": "2 Crônicas 5-7", "mes": "Agosto"},
    229: {"passagem": "2 Crônicas 8-11", "mes": "Agosto"},
    230: {"passagem": "2 Crônicas 12-15", "mes": "Agosto"},
    231: {"passagem": "2 Crônicas 16-19", "mes": "Agosto"},
    232: {"passagem": "2 Crônicas 20-22", "mes": "Agosto"},
    233: {"passagem": "2 Crônicas 23-25", "mes": "Agosto"},
    234: {"passagem": "2 Crônicas 26-28", "mes": "Agosto"},
    235: {"passagem": "2 Crônicas 29-30", "mes": "Agosto"},
    236: {"passagem": "2 Crônicas 31-33", "mes": "Agosto"},
    237: {"passagem": "2 Crônicas 34-36", "mes": "Agosto"},
    238: {"passagem": "Oseias 1-4", "mes": "Agosto"},
    239: {"passagem": "Oseias 5-8", "mes": "Agosto"},
    240: {"passagem": "Oseias 9-11", "mes": "Agosto"},
    241: {"passagem": "Oseias 12-14", "mes": "Agosto"},
    242: {"passagem": "Joel", "mes": "Agosto"},
    243: {"passagem": "Amós 1-5", "mes": "Agosto"},
    
    # Setembro
    244: {"passagem": "Miqueias 3-7", "mes": "Setembro"},
    245: {"passagem": "Naum e Habacuque", "mes": "Setembro"},
    246: {"passagem": "Sofonias", "mes": "Setembro"},
    247: {"passagem": "Esdras 1-2", "mes": "Setembro"},
    248: {"passagem": "Esdras 3-5", "mes": "Setembro"},
    249: {"passagem": "Esdras 6-8", "mes": "Setembro"},
    250: {"passagem": "Esdras 9-10", "mes": "Setembro"},
    251: {"passagem": "Neemias 1-3", "mes": "Setembro"},
    252: {"passagem": "Neemias 4-6", "mes": "Setembro"},
    253: {"passagem": "Neemias 7-8", "mes": "Setembro"},
    254: {"passagem": "Neemias 9-10", "mes": "Setembro"},
    255: {"passagem": "Neemias 11-13", "mes": "Setembro"},
    256: {"passagem": "Ester 1-3", "mes": "Setembro"},
    257: {"passagem": "Ester 4-7", "mes": "Setembro"},
    258: {"passagem": "Ester 8-10", "mes": "Setembro"},
    259: {"passagem": "Ageu", "mes": "Setembro"},
    260: {"passagem": "Zacarias 1-4", "mes": "Setembro"},
    261: {"passagem": "Zacarias 5-8", "mes": "Setembro"},
    262: {"passagem": "Zacarias 9-11", "mes": "Setembro"},
    263: {"passagem": "Zacarias 12-14", "mes": "Setembro"},
    264: {"passagem": "Malaquias", "mes": "Setembro"},
    265: {"passagem": "Isaías 1-4", "mes": "Setembro"},
    266: {"passagem": "Isaías 5-8", "mes": "Setembro"},
    267: {"passagem": "Isaías 9-12", "mes": "Setembro"},
    268: {"passagem": "Isaías 13-16", "mes": "Setembro"},
    269: {"passagem": "Isaías 17-21", "mes": "Setembro"},
    270: {"passagem": "Isaías 22-25", "mes": "Setembro"},
    271: {"passagem": "Isaías 26-29", "mes": "Setembro"},
    272: {"passagem": "Isaías 30-32", "mes": "Setembro"},
    273: {"passagem": "Isaías 33-36", "mes": "Setembro"},
    
    # Outubro
    274: {"passagem": "Isaías 37-39", "mes": "Outubro"},
    275: {"passagem": "Isaías 40-42", "mes": "Outubro"},
    276: {"passagem": "Isaías 43-45", "mes": "Outubro"},
    277: {"passagem": "Isaías 46-48", "mes": "Outubro"},
    278: {"passagem": "Isaías 49-51", "mes": "Outubro"},
    279: {"passagem": "Isaías 52-54", "mes": "Outubro"},
    280: {"passagem": "Isaías 55-57", "mes": "Outubro"},
    281: {"passagem": "Isaías 58-60", "mes": "Outubro"},
    282: {"passagem": "Isaías 61-63", "mes": "Outubro"},
    283: {"passagem": "Isaías 64-66", "mes": "Outubro"},
    284: {"passagem": "Jeremias 1-3", "mes": "Outubro"},
    285: {"passagem": "Jeremias 4-6", "mes": "Outubro"},
    286: {"passagem": "Jeremias 7-9", "mes": "Outubro"},
    287: {"passagem": "Jeremias 10-12", "mes": "Outubro"},
    288: {"passagem": "Jeremias 13-15", "mes": "Outubro"},
    289: {"passagem": "Jeremias 16-18", "mes": "Outubro"},
    290: {"passagem": "Jeremias 19-22", "mes": "Outubro"},
    291: {"passagem": "Jeremias 23-25", "mes": "Outubro"},
    292: {"passagem": "Jeremias 26-28", "mes": "Outubro"},
    293: {"passagem": "Jeremias 29-31", "mes": "Outubro"},
    294: {"passagem": "Jeremias 32-34", "mes": "Outubro"},
    295: {"passagem": "Jeremias 35-37", "mes": "Outubro"},
    296: {"passagem": "Jeremias 38-40", "mes": "Outubro"},
    297: {"passagem": "Jeremias 41-43", "mes": "Outubro"},
    298: {"passagem": "Jeremias 44-46", "mes": "Outubro"},
    299: {"passagem": "Jeremias 47-49", "mes": "Outubro"},
    300: {"passagem": "Jeremias 50-52", "mes": "Outubro"},
    301: {"passagem": "Lamentações 1-2", "mes": "Outubro"},
    302: {"passagem": "Lamentações 3-5", "mes": "Outubro"},
    303: {"passagem": "Ezequiel 1-4", "mes": "Outubro"},
    
    # Novembro
    304: {"passagem": "Ezequiel 16", "mes": "Novembro"},
    305: {"passagem": "Ezequiel 17-19", "mes": "Novembro"},
    306: {"passagem": "Ezequiel 20-21", "mes": "Novembro"},
    307: {"passagem": "Ezequiel 22-23", "mes": "Novembro"},
    308: {"passagem": "Ezequiel 24-26", "mes": "Novembro"},
    309: {"passagem": "Ezequiel 27-28", "mes": "Novembro"},
    310: {"passagem": "Ezequiel 29-31", "mes": "Novembro"},
    311: {"passagem": "Ezequiel 32-33", "mes": "Novembro"},
    312: {"passagem": "Ezequiel 34-36", "mes": "Novembro"},
    313: {"passagem": "Ezequiel 37-38", "mes": "Novembro"},
    314: {"passagem": "Ezequiel 39-40", "mes": "Novembro"},
    315: {"passagem": "Ezequiel 41-43", "mes": "Novembro"},
    316: {"passagem": "Ezequiel 44-45", "mes": "Novembro"},
    317: {"passagem": "Ezequiel 46-48", "mes": "Novembro"},
    318: {"passagem": "Daniel 1-2", "mes": "Novembro"},
    319: {"passagem": "Daniel 3-4", "mes": "Novembro"},
    320: {"passagem": "Daniel 5-6", "mes": "Novembro"},
    321: {"passagem": "Daniel 7-8", "mes": "Novembro"},
    322: {"passagem": "Daniel 9-10", "mes": "Novembro"},
    323: {"passagem": "Daniel 11-12", "mes": "Novembro"},
    324: {"passagem": "Oséias 1-4", "mes": "Novembro"},
    325: {"passagem": "Oséias 5-8", "mes": "Novembro"},
    326: {"passagem": "Oséias 9-11", "mes": "Novembro"},
    327: {"passagem": "Oséias 12-14", "mes": "Novembro"},
    328: {"passagem": "Joel 1-3", "mes": "Novembro"},
    329: {"passagem": "Amós 1-4", "mes": "Novembro"},
    330: {"passagem": "Amós 5-9", "mes": "Novembro"},
    331: {"passagem": "Obadias", "mes": "Novembro"},
    332: {"passagem": "Jonas", "mes": "Novembro"},
    333: {"passagem": "Miqueias 1-4", "mes": "Novembro"},
    
    # Dezembro
    334: {"passagem": "Salmos 15-22", "mes": "Dezembro"},
    335: {"passagem": "Salmos 23-31", "mes": "Dezembro"},
    336: {"passagem": "Salmos 32-37", "mes": "Dezembro"},
    337: {"passagem": "Salmos 38-44", "mes": "Dezembro"},
    338: {"passagem": "Salmos 45-51", "mes": "Dezembro"},
    339: {"passagem": "Salmos 52-59", "mes": "Dezembro"},
    340: {"passagem": "Salmos 60-67", "mes": "Dezembro"},
    341: {"passagem": "Salmos 68-71", "mes": "Dezembro"},
    342: {"passagem": "Salmos 72-77", "mes": "Dezembro"},
    343: {"passagem": "Salmos 78-81", "mes": "Dezembro"},
    344: {"passagem": "Salmos 82-89", "mes": "Dezembro"},
    345: {"passagem": "Salmos 90-97", "mes": "Dezembro"},
    346: {"passagem": "Salmos 98-104", "mes": "Dezembro"},
    347: {"passagem": "Salmos 105-106", "mes": "Dezembro"},
    348: {"passagem": "Salmos 107-110", "mes": "Dezembro"},
    349: {"passagem": "Salmos 111-118", "mes": "Dezembro"},
    350: {"passagem": "Sl 119: 1-88", "mes": "Dezembro"},
    351: {"passagem": "Sl 119: 89-176", "mes": "Dezembro"},
    352: {"passagem": "Salmos 120-135", "mes": "Dezembro"},
    353: {"passagem": "Salmos 136-142", "mes": "Dezembro"},
    354: {"passagem": "Salmos 143-150", "mes": "Dezembro"},
    355: {"passagem": "Provérbios 1-4", "mes": "Dezembro"},
    356: {"passagem": "Provérbios 5-8", "mes": "Dezembro"},
    357: {"passagem": "Provérbios 9-13", "mes": "Dezembro"},
    358: {"passagem": "Provérbios 14-17", "mes": "Dezembro"},
    359: {"passagem": "Provérbios 18-21", "mes": "Dezembro"},
    360: {"passagem": "Provérbios 22-24", "mes": "Dezembro"},
    361: {"passagem": "Provérbios 25-28", "mes": "Dezembro"},
    362: {"passagem": "Provérbios 29-31", "mes": "Dezembro"},
    363: {"passagem": "Eclesiastes 1-6", "mes": "Dezembro"},
    364: {"passagem": "Eclesiastes 7-12", "mes": "Dezembro"},
    365: {"passagem": "Cantares", "mes": "Dezembro"}
}

def main():
    st.title("Plano de Leitura Bíblica")
    
    # Inicializa o banco de dados
    init_db()
    
    # Sidebar com as opções de navegação
    opcao = st.sidebar.radio(
        "Escolha uma opção:",
        ["Leitura do Dia", "Progresso"]
    )
    
    if opcao == "Leitura do Dia":
        mostrar_leitura_do_dia()
    else:
        mostrar_progresso()

def mostrar_leitura_do_dia():
    st.header("Leitura do Dia")
    
    # Obtém o dia atual do ano
    dia_atual = datetime.datetime.now().timetuple().tm_yday
    
    if dia_atual in PLANO_LEITURA:
        leitura = PLANO_LEITURA[dia_atual]
        st.subheader(f"Dia {dia_atual} - {leitura['mes']}")
        st.write(f" Leitura: {leitura['passagem']}")
        
        # Checkbox para marcar como concluída
        if st.checkbox("Marcar como concluída", value=esta_concluida(dia_atual)):
            marcar_concluida(dia_atual)
            st.success("Leitura marcada como concluída!")
    else:
        st.error("Não há leitura programada para hoje.")

def mostrar_progresso():
    st.header("Seu Progresso")
    
    # Obtém todas as leituras concluídas
    leituras_concluidas = get_leituras_concluidas()
    total_leituras = len(PLANO_LEITURA)
    
    # Calcula o progresso
    progresso = len(leituras_concluidas) / total_leituras * 100
    
    # Mostra o progresso geral
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Concluído", f"{len(leituras_concluidas)} de {total_leituras}")
    with col2:
        st.metric("Porcentagem", f"{progresso:.1f}%")
    
    st.progress(progresso / 100)
    
    # Mostra todas as leituras com status
    st.subheader("Todas as Leituras")
    
    # Organiza as leituras por mês
    leituras_por_mes = {}
    for dia, leitura in PLANO_LEITURA.items():
        mes = leitura['mes']
        if mes not in leituras_por_mes:
            leituras_por_mes[mes] = []
        leituras_por_mes[mes].append((dia, leitura))
    
    # Lista de meses na ordem correta
    ordem_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    # Para cada mês na ordem correta
    for mes in ordem_meses:
        if mes in leituras_por_mes:
            with st.expander(f"{mes}"):
                # Calcula progresso do mês
                leituras_mes = leituras_por_mes[mes]
                concluidas_mes = [dia for dia, _ in leituras_mes if dia in leituras_concluidas]
                progresso_mes = len(concluidas_mes) / len(leituras_mes) * 100
                
                # Mostra progresso do mês
                st.write(f"**Progresso do mês:** {len(concluidas_mes)} de {len(leituras_mes)} ({progresso_mes:.1f}%)")
                st.progress(progresso_mes / 100)
                
                # Lista as leituras do mês
                for dia, leitura in sorted(leituras_mes):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"Dia {dia}: {leitura['passagem']}")
                    with col2:
                        # Verifica o estado atual
                        esta_marcada = esta_concluida(dia)
                        
                        # Usa uma função para lidar com a mudança de estado
                        def on_change(dia):
                            # Obtém o estado atual do checkbox
                            novo_estado = st.session_state.get(f"check_{dia}", False)
                            
                            # Atualiza o banco de dados
                            marcar_concluida(dia, novo_estado)
                        
                        # Checkbox com callback para mudança de estado
                        st.checkbox(
                            "✓", 
                            key=f"check_{dia}", 
                            value=esta_marcada,
                            on_change=on_change,
                            args=(dia,)
                        )

if __name__ == "__main__":
    main()
