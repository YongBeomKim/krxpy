from .base import *
from ._krxio import KrxWebIo


class Ticker(KrxWebIo):

    @property
    def bld(self):
        return "dbms/comm/finder/finder_stkisu"

    def fetch(
            self, token:str=""
        ) -> pandas.DataFrame:

        result = self.read(
            locale="ko_KR",
            mktsel="ALL",
            typeNo="0",
            searchText=token,
        )
        return pandas.DataFrame(result['block1'])


def get_ticker(ticker:str=None):
    r"""ticker 변환정보 ticker 출력"""

    # 확장자가 없으면 `check_file` 에서 오류발생
    file_name = 'krx_codes.pkl' 
    file_path = "./.pykrx/" + file_name
    CHECK = check_file(file_path)
    if CHECK:
        df = file_pickle(file_path, 'r')

    else:
        menu_url  = "http://data.krx.co.kr/contents"
        menu_url += "/MDC/MDI/mdiLoader/index.cmd?menuId"
        ticker_instance = Ticker({
            "Referer":f"{menu_url}=MDC0201020201"
        })
        df = ticker_instance.fetch()
        file_pickle(file_path, 'w', df)

    df = df.loc[:,['short_code','full_code']]
    code_dict = {_[0]:_[1]  for _ in df.to_dict('split')['data']}
    if ticker is not None: 
        return code_dict.get(ticker)
    else: 
        return code_dict
