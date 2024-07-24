from .base import *
# 크롤링 : https://kind.krx.co.kr
# https://comdoc.tistory.com/entry/%EC%83%81%EC%9E%A5-%EB%B2%95%EC%9D%B8-%EB%AA%A9%EB%A1%9D-KIND


class Kind:

    def __init__(self) -> None:
        self.url_info = "http://kind.krx.co.kr/corpgeneral/corpList.do"
        self.url_ipo = "http://kind.krx.co.kr/listinvstg/pubofrprogcom.do"
        self.headers = {
            "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0"
        }


    def ipo(self, end:str=None, start:str=None):
        form_data = {
            "method":"searchPubofrProgComSub",
            "currentPageSize":"3000",
            "pageIndex":"1",
            "orderMode":"1",
            "orderStat":"D",
            "searchMode":"",
            "searchCodeType":"",
            "searchCorpName":"",
            "isurCd":"",
            "repIsuSrtCd":"",
            "bzProcsNo":"",
            "detailMarket":"",
            "forward":"pubofrprogcom_down",
            "marketType":"",
            "searchCorpNameTmp":"",
            "repMajAgntDesignAdvserComp":"",
            "repMajAgntComp":"",
            "designAdvserComp":"",
            "fromDate":start,
            "toDate":end,
        }
        params = parse.urlencode(form_data, encoding='UTF-8', doseq=True)
        url = f"{self.url_ipo}?{params}"
        response = requests.get(url, headers=self.headers)
        response_io = StringIO(str(response.text))
        return pandas.read_html(response_io, header=0, flavor='html5lib', encoding='cp949')[0]


def ipo_kind(date:str=None, from_date:str=None):
    r"""IPO 일정 캘린더 불러오기
    date      : 신고서 제출일 default) 오늘 
    from_date : 신고서 제출일 default) 오늘 ~ 90일 전"""

    if date is None:
        date = datetime.date.today()
        date = str(date)

    if from_date is None:
        from_date = date_to_string(date, datetime_obj=True)
        from_date = from_date - datetime.timedelta(days=90)

    df = Kind().ipo(start=str(from_date), end=date)

    # Post Processing ...
    items = df.iloc[0,:].values.tolist()
    if len(list(set(items))) < 3:
        df_new = pandas.DataFrame(columns=df.columns)
        df = df_new.copy()

    df = df.sort_values('상장예정일').reset_index(drop=True)
    for column in ['확정공모가',"공모금액(백만원)"]:
        df[column] = list(map(lambda x : 0 if x == '-' else int(x), df[column]))
    return df
