# data.krx.co.kr : 수집기 'pykrx` 를 활용
# 하위 함수로 목록 정의완료하기
from .kind import ipo_kind
from .kind_info import notice_kind, info_kind, note_kind
from .stock_api import info_krx, info_krx_tor


# @property
# def info(self):
#     form_data = {
#         "method":"download",
#         "searchType":"13",
#     }
#     params = parse.urlencode(form_data, encoding='UTF-8', doseq=True)
#     url = f"{self.url_info}?{params}"
#     df  = pandas.read_html(url, header=0, encoding='cp949')[0]
#     return df