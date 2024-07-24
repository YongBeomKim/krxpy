from ._headers import HEADERS as KRX_HEADERS
from .base import *
instance = KRX_HEADERS()


@elapsed_time
def info_krx():    
    r"""전종목 기업정보"""

    @duplicate_name
    @convert_code_market(column="시장구분")
    @dataframe_fill_nat(column="상장일")
    def post_process(df):

        # columns 한글로 변경
        df.columns = list(map(lambda x : instance.column_krx_info[x], df.columns))
        # "액면가", "상장주식수" 컬럼의 데이터 "integer" 변환
        tokenizer = re.compile('[.A-zㄱ-힣]+')
        for column_name in ["액면가", "상장주식수"]:

            df[column_name] = list(map(
                lambda x : '1' if(len("".join(tokenizer.findall(x)))>0) else x,
                df[column_name]))

            df[column_name] = list(map(
                lambda x : int(x.replace(',','')) , df[column_name]))
        return df

    # Main Process
    referer = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201010101"
    HEADER = instance.headers
    HEADER["Referer"] = referer
    response = requests.post(
        instance.url, headers=HEADER, data=instance.data
    ).json()
    if response.get('OutBlock_1') is not None:
        df = pandas.DataFrame(response['OutBlock_1'])
        df = post_process(df)
        df['상장일'] = list(map(lambda x :date_to_string(x), df['상장일']))
        return df
    else:
        return None
