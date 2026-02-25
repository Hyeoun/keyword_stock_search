import requests

URL = "https://raw.githubusercontent.com/Hyeoun/keyword_stock_search/master/themes_with_stocks.json"
DATAS:dict[str, list[str]]

def download_keywords_stocks(url, retries=10):
    """GitHub에서 키워드 데이터를 다운로드 합니다. 실패 시 재시도"""
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Request error: {e}, retry {i + 1}/{retries}")
        raise Exception("The maximum number of retries has been reached. Data download failed.")

def _build_alias_theme_map(theme_map: dict[str, list[str]]) -> dict[str, list[str]]:
    """
    원본 JSON의 키가 '별칭1,별칭2,별칭3' 형태일 수 있다는 가정하에
    각 별칭(콤마로 분리)을 동일한 종목 리스트에 매핑.
    """
    alias_map: dict[str, list[str]] = {}
    for key, stocks in theme_map.items():
        aliases = [a.strip() for a in key.split(",")]
        for a in aliases:
            alias_map[a] = stocks
    return alias_map

def reset_keywords_stocks(url=URL, retries=10):
    """GitHub에서 키워드 데이터를 다운로드하여 매핑합니다."""
    global DATAS
    temp = download_keywords_stocks(url, retries)
    DATAS = _build_alias_theme_map(temp)

def get_stocks(keyword:str) -> list[str]:
    """키워드와 대응되는 종목 리스트를 반환합니다."""
    return DATAS.get(keyword, [])

def get_keywords() -> list[str]:
    """키워드들을 리스트의 형태로 반환합니다."""
    return list(DATAS.keys())

reset_keywords_stocks()