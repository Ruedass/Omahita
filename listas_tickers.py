"""
Listas Predefinidas de Tickers por Sector y Categoría
Usa estas listas en tu screener según tus intereses
"""

# MEGA CAPS (Market Cap > $500B)
MEGA_CAPS = [
    'AAPL',   # Apple
    'MSFT',   # Microsoft  
    'GOOGL',  # Alphabet
    'AMZN',   # Amazon
    'NVDA',   # NVIDIA
    'META',   # Meta
    'TSLA',   # Tesla
    'BRK-B',  # Berkshire Hathaway
]

# TECHNOLOGY
TECH = [
    'AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AVGO', 'ORCL', 'CSCO',
    'ADBE', 'CRM', 'AMD', 'INTC', 'IBM', 'NOW', 'INTU', 'QCOM',
    'TXN', 'AMAT', 'MU', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'MCHP'
]

# FINANCIALS
FINANCIALS = [
    'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW',
    'AXP', 'USB', 'PNC', 'TFC', 'COF', 'BK', 'STT', 'SIVB'
]

# HEALTHCARE
HEALTHCARE = [
    'UNH', 'JNJ', 'LLY', 'ABBV', 'MRK', 'PFE', 'TMO', 'ABT',
    'DHR', 'BMY', 'AMGN', 'CVS', 'MDT', 'GILD', 'CI', 'ISRG',
    'VRTX', 'REGN', 'HUM', 'ZTS', 'BSX', 'SYK', 'ELV', 'MCK'
]

# CONSUMER DISCRETIONARY
CONSUMER_DISC = [
    'AMZN', 'TSLA', 'HD', 'NKE', 'MCD', 'SBUX', 'TJX', 'BKNG',
    'LOW', 'ABNB', 'CMG', 'MAR', 'GM', 'F', 'ORLY', 'AZO',
    'YUM', 'DG', 'ROST', 'DHI', 'LEN', 'ULTA', 'DPZ', 'POOL'
]

# CONSUMER STAPLES
CONSUMER_STAPLES = [
    'WMT', 'PG', 'COST', 'KO', 'PEP', 'PM', 'MO', 'CL',
    'MDLZ', 'ADM', 'KMB', 'GIS', 'HSY', 'K', 'CHD', 'CLX',
    'SJM', 'CAG', 'CPB', 'MKC', 'HRL', 'TSN', 'KHC', 'KR'
]

# ENERGY
ENERGY = [
    'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO',
    'OXY', 'WMB', 'HAL', 'KMI', 'BKR', 'HES', 'DVN', 'FANG',
    'MRO', 'APA', 'OKE', 'TRGP', 'LNG', 'EQT', 'CTRA', 'CHRD'
]

# INDUSTRIALS
INDUSTRIALS = [
    'UPS', 'HON', 'BA', 'UNP', 'CAT', 'RTX', 'GE', 'LMT',
    'DE', 'MMM', 'FDX', 'NSC', 'ETN', 'EMR', 'ITW', 'CSX',
    'GD', 'NOC', 'WM', 'TDG', 'CARR', 'PCAR', 'JCI', 'CMI'
]

# UTILITIES
UTILITIES = [
    'NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL',
    'WEC', 'ED', 'ES', 'AWK', 'DTE', 'PPL', 'EIX', 'FE',
    'ETR', 'AEE', 'CMS', 'CNP', 'NI', 'LNT', 'EVRG', 'PNW'
]

# REAL ESTATE
REAL_ESTATE = [
    'PLD', 'AMT', 'EQIX', 'PSA', 'SPG', 'WELL', 'O', 'DLR',
    'CBRE', 'AVB', 'EQR', 'VTR', 'SBAC', 'WY', 'ARE', 'INVH',
    'MAA', 'ESS', 'UDR', 'EXR', 'CPT', 'HST', 'SUI', 'CUBE'
]

# MATERIALS
MATERIALS = [
    'LIN', 'APD', 'SHW', 'ECL', 'DD', 'NEM', 'FCX', 'NUE',
    'DOW', 'VMC', 'MLM', 'PPG', 'CTVA', 'ALB', 'BALL', 'IP',
    'PKG', 'AMCR', 'AVY', 'CF', 'MOS', 'FMC', 'EMN', 'CE'
]

# COMMUNICATION SERVICES
COMMUNICATIONS = [
    'GOOGL', 'META', 'NFLX', 'DIS', 'CMCSA', 'T', 'VZ', 'TMUS',
    'CHTR', 'EA', 'ATVI', 'TTWO', 'WBD', 'PARA', 'OMC', 'IPG',
    'FOXA', 'NWSA', 'MTCH', 'LYV', 'PINS', 'SNAP', 'ROKU', 'ZM'
]

# DIVIDEND ARISTOCRATS (25+ años aumentando dividendos)
DIVIDEND_ARISTOCRATS = [
    'MMM', 'ABT', 'ABBV', 'AFL', 'APD', 'ALB', 'ADP', 'AMCR',
    'BDX', 'BF-B', 'BRO', 'CAH', 'CAT', 'CB', 'CHRW', 'CINF',
    'CLX', 'CL', 'KO', 'ED', 'EMR', 'ESS', 'EXPD', 'XOM',
    'FRT', 'GD', 'GPC', 'HRL', 'IBM', 'ITW', 'JNJ', 'KMB',
    'LOW', 'MCD', 'MDT', 'MKC', 'NDSN', 'NEE', 'NUE', 'O',
    'PEP', 'PG', 'PPG', 'ROP', 'SHW', 'SPGI', 'SWK', 'SYY',
    'TROW', 'TGT', 'WMT', 'WST'
]

# ETFs PRINCIPALES (para comparación)
MAJOR_ETFS = [
    'SPY',   # S&P 500
    'QQQ',   # NASDAQ 100
    'DIA',   # Dow Jones
    'IWM',   # Russell 2000
    'VTI',   # Total US Market
    'VEA',   # Developed Markets
    'VWO',   # Emerging Markets
    'AGG',   # Bonds
    'GLD',   # Gold
    'SLV',   # Silver
]

# DOW JONES 30
DOW_30 = [
    'AAPL', 'MSFT', 'JPM', 'V', 'UNH', 'HD', 'PG', 'JNJ',
    'CVX', 'MRK', 'DIS', 'AMGN', 'BA', 'MCD', 'CRM', 'CAT',
    'GS', 'AXP', 'HON', 'IBM', 'NKE', 'CSCO', 'VZ', 'WMT',
    'MMM', 'TRV', 'DOW', 'KO', 'INTC', 'WBA'
]

# VALUE STOCKS (típicamente baratas)
VALUE_STOCKS = [
    'BRK-B', 'JPM', 'BAC', 'XOM', 'CVX', 'WFC', 'C', 'GS',
    'USB', 'PNC', 'WMT', 'KO', 'PEP', 'PM', 'MO', 'T',
    'VZ', 'IBM', 'F', 'GM', 'MMM', 'CAT', 'BA', 'UPS'
]

# GROWTH STOCKS (alto crecimiento)
GROWTH_STOCKS = [
    'NVDA', 'AMD', 'TSLA', 'META', 'GOOGL', 'AMZN', 'NFLX',
    'CRM', 'NOW', 'SNOW', 'DDOG', 'NET', 'CRWD', 'ZS', 'OKTA',
    'PANW', 'SQ', 'SHOP', 'COIN', 'PLTR', 'U', 'ABNB', 'UBER'
]

# SMALL CAPS (Market Cap < $10B)
SMALL_CAPS = [
    'ENPH', 'SEDG', 'RUN', 'FSLR', 'PLUG', 'BE', 'NOVA', 'AEHR',
    'PACW', 'ZION', 'WTFC', 'ABCB', 'FBIZ', 'UCBI', 'HBAN', 'RF',
    'CADE', 'EWBC', 'BANR', 'CVBF', 'FFIN', 'GBCI', 'ONB', 'FIBK'
]

# MID CAPS (Market Cap $10B - $50B)
MID_CAPS = [
    'FTNT', 'DDOG', 'CRWD', 'NET', 'ZS', 'OKTA', 'PANW', 'SNOW',
    'SQ', 'TWLO', 'DOCN', 'CFLT', 'CYBR', 'S', 'ESTC', 'TENB',
    'RPD', 'GTLB', 'PATH', 'BILL', 'WEAV', 'PCTY', 'APPS', 'ZI'
]

# CRYPTO PROXIES (empresas relacionadas con crypto)
CRYPTO_PROXIES = [
    'COIN',  # Coinbase
    'MSTR',  # MicroStrategy
    'RIOT',  # Riot Platforms
    'MARA',  # Marathon Digital
    'CLSK',  # CleanSpark
    'HUT',   # Hut 8
    'BITF',  # Bitfarms
    'CIFR',  # Cipher Mining
]

# SEMICONDUCTOR
SEMICONDUCTORS = [
    'NVDA', 'AMD', 'INTC', 'TSM', 'AVGO', 'QCOM', 'TXN', 'MU',
    'AMAT', 'LRCX', 'KLAC', 'ASML', 'SNPS', 'CDNS', 'MCHP', 'ADI',
    'MRVL', 'NXPI', 'ON', 'MPWR', 'ENTG', 'SWKS', 'QRVO', 'WOLF'
]

# CLOUD & SAAS
CLOUD_SAAS = [
    'CRM', 'NOW', 'SNOW', 'DDOG', 'WDAY', 'ZM', 'TEAM', 'ADBE',
    'INTU', 'MSFT', 'ORCL', 'SAP', 'VEEV', 'ANSS', 'CDNS', 'SNPS',
    'HUBS', 'ZS', 'OKTA', 'CRWD', 'NET', 'CFLT', 'DOCN', 'MDB'
]

# CHINA STOCKS (ADRs)
CHINA_ADRS = [
    'BABA',  # Alibaba
    'JD',    # JD.com
    'BIDU',  # Baidu
    'PDD',   # PDD Holdings
    'NIO',   # NIO
    'XPEV',  # XPeng
    'LI',    # Li Auto
    'TME',   # Tencent Music
]


def get_tickers_por_categoria(categoria):
    """
    Obtener lista de tickers por categoría
    
    Args:
        categoria (str): Nombre de la categoría
    
    Returns:
        list: Lista de tickers
    """
    categorias = {
        'mega_caps': MEGA_CAPS,
        'tech': TECH,
        'financials': FINANCIALS,
        'healthcare': HEALTHCARE,
        'consumer_disc': CONSUMER_DISC,
        'consumer_staples': CONSUMER_STAPLES,
        'energy': ENERGY,
        'industrials': INDUSTRIALS,
        'utilities': UTILITIES,
        'real_estate': REAL_ESTATE,
        'materials': MATERIALS,
        'communications': COMMUNICATIONS,
        'dividend_aristocrats': DIVIDEND_ARISTOCRATS,
        'etfs': MAJOR_ETFS,
        'dow_30': DOW_30,
        'value': VALUE_STOCKS,
        'growth': GROWTH_STOCKS,
        'small_caps': SMALL_CAPS,
        'mid_caps': MID_CAPS,
        'crypto': CRYPTO_PROXIES,
        'semiconductors': SEMICONDUCTORS,
        'cloud_saas': CLOUD_SAAS,
        'china': CHINA_ADRS,
    }
    
    return categorias.get(categoria.lower(), [])


def get_todas_categorias():
    """Listar todas las categorías disponibles"""
    return [
        'mega_caps', 'tech', 'financials', 'healthcare', 
        'consumer_disc', 'consumer_staples', 'energy', 'industrials',
        'utilities', 'real_estate', 'materials', 'communications',
        'dividend_aristocrats', 'etfs', 'dow_30', 'value', 'growth',
        'small_caps', 'mid_caps', 'crypto', 'semiconductors', 
        'cloud_saas', 'china'
    ]


# Ejemplo de uso
if __name__ == "__main__":
    print("Categorías disponibles:")
    for cat in get_todas_categorias():
        tickers = get_tickers_por_categoria(cat)
        print(f"  {cat}: {len(tickers)} tickers")
    
    print("\n" + "="*80)
    print("Ejemplo - Top 5 Tech:")
    print(", ".join(TECH[:5]))
