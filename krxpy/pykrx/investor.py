from .base import *
from ._tools import df_number_column
from ._krxio import KrxWebIo
from .ticker import get_ticker


class Investor(KrxWebIo):

    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02303"

    def fetch(
            self, ticker:str,
            strtDd: str, endDd: str, askBid: int
        ) -> pandas.DataFrame:

        result = self.read(
            isuCd = ticker,
            strtDd=strtDd, endDd=endDd,
            askBid=askBid, detailView=1, 
            trdVolVal=1, share="1",
        )
        return pandas.DataFrame(result['output'])


def get_invest(start:str, end:str, ticker:str, askBid:int):
    r"""투자자별 매매현황 데이터
    start  : '2020-01-01' 
    end    : '2021-01-01'
    ticker : '005930'
    askBid : 매도, 매수, 순매매 
    trdVolVal : 1(주식수) 2(금액)"""

    column_dict = {"TRD_DD":"날짜", "TRDVAL_TOT":'총합',
        'TRDVAL1':'금융투자', 'TRDVAL2':'보험', 'TRDVAL3':'투신',\
        'TRDVAL4':'사모', 'TRDVAL5':'은행', 'TRDVAL6':'기타금융','TRDVAL7':'연기금',\
        'TRDVAL8':'기타법인', 'TRDVAL9':'개인', 'TRDVAL10':'외국인', 'TRDVAL11':'기타외국인'
    }
    menu_url  = "http://data.krx.co.kr/contents"
    menu_url += "/MDC/MDI/mdiLoader/index.cmd?menuId"
    invest = Investor({
        "Referer":f"{menu_url}=MDC0201020301"
    })
    try:
        ticker_full = get_ticker(ticker)
        askbid_list = ['매도','매수','순매매']
        askBid_dict = {_:no+1  for no,_ in enumerate(askbid_list)}
        askBid      = askBid_dict.get(askBid)
        df = invest.fetch(
            ticker=ticker_full, 
            strtDd=start, endDd=end, 
            askBid=askBid
        )
        if len(df) > 0:
            df = df_number_column(df, df.columns.tolist()[1:])
            df = df.rename(columns=column_dict)
            df = df.astype({_:'int32'  for _ in df.select_dtypes(numpy.float32).columns})
            df = df.astype({_:'int64'  for _ in df.select_dtypes(numpy.float64).columns})
            df['날짜'] = df['날짜'].map(lambda x : date_to_string(x))
            df = df.set_index('날짜')
            return df
        return None

    except Exception as E:
        print(f"{ticker} has Error : {E}")
        return None

