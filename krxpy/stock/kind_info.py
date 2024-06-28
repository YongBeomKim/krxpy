from .base import *

# 기업상장코드 확인함수
def code_info(to_dict=False, raw=True):
    r"""기업정보 호출함수
    to_dict : {기업이름:기업코드}"""
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
    df = pandas.read_html(url, header=0)[0]
    df['종목코드'] = df['종목코드'].map(lambda x: f'{x:0>6}')
    if to_dict:
        return pandas.Series(df['종목코드'].tolist(), index=df['회사명'].tolist())
    return df


# 거래현황정보
class Info:

    code_dict:dict = code_info(to_dict=True)
    url_issue:str = "https://kind.krx.co.kr/investwarn/tradinghaltissue.do"
    url_warn:str  = "https://kind.krx.co.kr/investwarn/investattentwarnrisky.do"
    headers:dict = {
        "Accept":"text/html, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-US,en;q=0.5",
        "Connection":"keep-alive",
        "Content-Length":"180",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"kind.krx.co.kr",
        "Origin":"https://kind.krx.co.kr",
        "Referer":"https://kind.krx.co.kr/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "TE":"trailers",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
        "X-Requested-With":"XMLHttpRequest"
    }
    data: dict = {
        "currentPageSize":"100",
        "pageIndex":"1",
        "forward":"tradinghaltissue_sub",
        # "marketType":"2", # "2" 코스닥
    }

    # 작업기준 날짜
    def __init__(self, date:str=None):
        self.date = date_to_string(date)

    # 거래정지 종목
    def halt(self, market=1):
        # https://kind.krx.co.kr/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain
        r"""매매 거래정지 종목"""
        url_issue:str = "https://kind.krx.co.kr/investwarn/tradinghaltissue.do"
        headers:dict = {
            "Accept":"text/html, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Length":"180",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Host":"kind.krx.co.kr",
            "Origin":"https://kind.krx.co.kr",
            "Referer":"https://kind.krx.co.kr/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain",
            "Sec-Fetch-Dest":"empty",
            "Sec-Fetch-Mode":"cors",
            "Sec-Fetch-Site":"same-origin",
            "TE":"trailers",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "X-Requested-With":"XMLHttpRequest"
        }
        data: dict = {
            "currentPageSize":"100",
            "pageIndex":"1",
            "forward":"tradinghaltissue_sub",
            "method":"searchTradingHaltIssueSub",
        }
        data_issue = data
        data_issue["marketType"] = str(market)
        response = requests.post(url=url_issue, data=data_issue, headers=headers)
        df = pandas.read_html(response.text)[0]
        code_dict = self.code_dict
        df = df[df['종목명'].isin(list(code_dict.keys()))]
        codes = [code_dict[_]   for _ in df['종목명']]
        df.insert(1, '상장코드', codes)
        df = df.drop(columns=['번호']).reset_index(drop=True)
        df.insert(0, '구분', '거래정지')
        df.insert(0, '날짜', datetime.date.today().isoformat())
        return df

    # 투자주의 종목
    def risky(self, start=None, end=None):
        r"""투자주의 종목"""
        today = datetime.date.today().isoformat()
        if start == None:
            start = today
        if end == None:
            end = today

        data = self.data
        data["method"] = "investattentwarnriskySub"
        data["forward"]="invstcautnisu_sub"
        data["orderMode"]="4"
        data["menuIndex"]="1"
        data["orderStat"]="D"
        data["searchFromDate"] = today
        data["startDate"] = start
        data["endDate"] = end

        response = requests.post(url=self.url_warn, data=data, headers=self.headers)
        code_dict = self.code_dict
        df = pandas.read_html(response.text)[0]
        df = df.iloc[:, 1:]
        df.columns = ["종목명", "사유", "공시일", "지정일"]
        df = df[df['종목명'].isin(list(code_dict.keys()))]
        codes = [code_dict[_]   for _ in df['종목명']]
        df.insert(0, '상장코드', codes)
        df.insert(0, '구분', '투자주의')
        df.insert(0, '날짜', today)
        return df        

    # 투자경고 종목
    def warning(self, start=None, end=None):
        r"""투자경고 종목 : 사유 공시 없음"""
        today = datetime.date.today().isoformat()
        if start == None:
            start = today
        if end == None:
            end = today
        data = self.data
        data["method"] = "investattentwarnriskySub"
        data["forward"]="invstwarnisu_sub"
        data["orderMode"]="3"
        data["menuIndex"]="2"
        data["orderStat"]="D"
        data["searchFromDate"] = today
        data["startDate"] = start
        data["endDate"] = end

        response = requests.post(url=self.url_warn, data=data, headers=self.headers)
        code_dict = self.code_dict
        df = pandas.read_html(response.text)[0]
        df = df.iloc[:, 1:-1]
        df.columns = ["종목명", "공시일", "지정일"]
        df = df[df['종목명'].isin(list(code_dict.keys()))]
        codes = [code_dict[_]   for _ in df['종목명']]
        df.insert(0, '상장코드', codes)
        df.insert(0, '구분', '투자경고')
        df.insert(0, '날짜', today)
        df.insert(4, '사유', None)
        return df        

    # 전체적인 데이터 수집하기
    def get(self):
        r"""거래정지 및 투자주의 경고종목 크롤링
        => 반복실행 및 오류 발생시 자동 보완기능 추가"""

        # 위의 메세지 크롤링 반복하며 실행
        try:
            df_halt1 = self.halt(market=1); time.sleep(.5)
            df_halt2 = self.halt(market=2); time.sleep(.5)
            df_risky = self.risky(start=self.date, end=self.date); time.sleep(.5)
            df_warnig = self.warning(start=self.date, end=self.date)
            df_list = [
                _df.loc[:,["날짜","구분","상장코드","종목명","사유"]]  
                for _df in [df_halt1, df_halt2, df_risky, df_warnig]
            ]
            df = pandas.concat(df_list).reset_index(drop=True)
            df['날짜'] = pandas.DatetimeIndex(df['날짜'])
            return df

        except Exception as e:
            print(e)
            return None


# 종목별 현황정보
def notice_kind(date:str=None):
    r"""종목별 현황정보
    date (str) : 수집기준 날짜"""

    info = Info(date=date)
    return info.get()
