from .base import *


# 거래현황정보
class Info:

    # code_dict:dict = code_info(to_dict=True)
    url_code:str  = "https://kind.krx.co.kr/corpgeneral/corpList.do"
    url_halt:str  = "https://kind.krx.co.kr/investwarn/tradinghaltissue.do"
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
        "currentPageSize":"500",
        "pageIndex":"1",
        "forward":"tradinghaltissue_sub",
        # "marketType":"2", # "2" 코스닥
    }


    # 작업기준 날짜
    def __init__(self, date:str=None):
        self.date = date_to_string(date)


    def code(self, to_dict=False):
        r"""상장기업정보 불러오기"""
        headers = self.headers
        headers['Cache-Control']='no-cache'
        headers['Content-Length']='211'
        headers['Sec-Fetch-Dest']='document'
        headers['Sec-Fetch-Mode']='navigate'
        headers['Sec-Fetch-User']='?1'
        headers['Upgrade-Insecure-Requests']='1'
        headers['Priority']='u=1'
        headers['Referer']='https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        data = {
            "method": "download",
            "pageIndex": "1",
            "currentPageSize": "300",
            "comAbbrv": "",
            "beginIndex": "",
            "orderMode": "3",
            "orderStat": "D",
            "isurCd": "",
            "repIsuSrtCd": "",
            "searchCodeType": "",
            "marketType": "",
            "searchType": "13",
            "industry": "",
            "fiscalYearEnd": "all",
            "comAbbrvTmp": "",
            "location": "all"
        }
        data["currentPageSize"] = "3500"
        response = requests.post(self.url_code, headers=headers, data=data)
        response_table = StringIO(str(response.text))
        df = pandas.read_html(response_table, flavor='lxml')[0]
        df['종목코드'] = df['종목코드'].map(lambda x: f'{x:0>6}')
        if to_dict:
            return pandas.Series(df['종목코드'].tolist(), index=df['회사명'].tolist())
        return df


    # 거래정지 종목
    def halt(self, market=1):
        # https://kind.krx.co.kr/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain
        r"""매매 거래정지 종목"""
        headers = self.headers
        headers["Referer"]="https://kind.krx.co.kr/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain"
        data = self.data
        data["method"] = "searchTradingHaltIssueSub"
        data["marketType"] = str(market)

        response = requests.post(url=self.url_halt, data=data, headers=headers)
        response_table = StringIO(str(response.text))
        df = pandas.read_html(response_table)[0]

        code_dict = self.code(to_dict=True)
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
        response_table = StringIO(str(response.text))
        df = pandas.read_html(response_table)[0]

        code_dict = self.code(to_dict=True)
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
        response_table = StringIO(str(response.text))
        df = pandas.read_html(response_table)[0]

        code_dict = self.code(to_dict=True)
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
        :: 
        => 반복실행 및 오류 발생시 자동 보완기능 추가"""

        # 위의 메세지 크롤링 반복하며 실행
        df_list = []

        try:   df_list.append(self.halt(market=1)); time.sleep(2)
        except Exception as E:     print(f"Halt no 1 Error: {E}")

        try:   df_list.append(self.halt(market=2)); time.sleep(2)
        except Exception as E:     print(f"Halt no 2 Error: {E}")

        try:   df_list.append(self.risky(start=self.date, end=self.date)); time.sleep(2)
        except Exception as E:     print(f"Risky Error: {E}")

        try:   df_list.append(self.warning(start=self.date, end=self.date)); time.sleep(2)
        except Exception as E:     print(f"Warning Error: {E}")

        if len(df_list) > 0:
            df_list = [
                _df.loc[:,["날짜","구분","상장코드","종목명","사유"]]  
                for _df in df_list
            ]
            df = pandas.concat(df_list).sort_values('구분').reset_index(drop=True)
            df['날짜'] = pandas.DatetimeIndex(df['날짜'])
            return df

        return None



# 종목별 현황정보 (종합 : celery 에서 kumba 오류발생)
def notice_kind(date:str=None):
    r"""종목별 현황정보
    date (str) : 수집기준 날짜"""
    info = Info(date=date)
    return info.get()


# Kind 기업정보
def note_kind(date:str=None, type:str=None):
    r"""Kind 기업정보
    date : '2000-01-01'
    type : code, halt, warning, risky """

    info = Info(date=date)
    type_list = ['halt', 'warning', 'risky']
    assert type in type_list, f"{type} not in {type_list}"
    if type == 'halt':
        return info.halt()
    elif type == 'warning':
        return info.warning()
    elif type == 'risky':
        return info.risky()
    return None


# KIND 상장기업 정보
def info_kind():
    r"""KIND 에서 상장기업정보 불러오기"""
    df = Info().code()
    return df