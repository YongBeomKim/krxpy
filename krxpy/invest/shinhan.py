from .base import *

import requests
from pytip import FakeAgent

def df_shinhan(code:str=None):
    # http://open.shinhaninvest.com/goodicyber/mk/1206.jsp?code=005930'
    url = f"https://open.shinhansec.com/goodicyber/mk/1206.jsp?code={code}"
    headers = {"User-Agent":FakeAgent.random}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            df = pandas.read_html(response.text)[-1]
            ## Post Processing
            # 컬럼찾기 및 테이블 재조정 하기
            for no,_ in enumerate(df[0]):
                if _ != '날짜':
                    break
            df_new = df.iloc[no:,:]
            df_new.columns = df.iloc[no-1,:].tolist()
            # 날짜 데이터 통일시키기
            df_new.loc[:,'날짜'] = list(map(lambda x : date_to_string(x), df_new['날짜']))
            df_new.loc[:,'날짜'] = pandas.DatetimeIndex(df_new['날짜'])
            df_new = df_new.set_index('날짜')
            df_new = df_new.apply(pandas.to_numeric)

            ## Append Data : 보여지지 않은 데이터 연산으로 추출하기
            # '기관계' 데이터를 근거로 '사모' 와 '기타외국인' 추출하기
            df_new = df_new.rename(columns={
                '외국인계':'외국인','증권':'금융투자','종금':'기타금융',
                '기금':'연기금','기타':'기타법인'})
            df_new = df_new.loc[:,[
                '기관계','금융투자','보험','투신','은행',
                '기타금융','연기금','기타법인','개인','외국인']]

            # 사모펀드 데이터 추출하기
            samo = [
                df_new.iloc[_,0] - df_new.iloc[_,1:7].sum()    
                for _ in range(len(df_new))
            ]
            df_new.insert(4, '사모', samo)
            del df_new['기관계']

            # 기타외국인 데이터 추출하기
            etc_f = [
                (df_new.iloc[_,:].sum() * (-1))    
                for _ in range(len(df_new))
            ]
            df_new.insert(10, '기타외국인', etc_f)
            _data = [df_new.iloc[idx,:].sum()  for idx in range(len(df_new))]
            df_new.insert(11,'총합', _data)
            return df_new

        except Exception as E:
            print(E)
    return None
