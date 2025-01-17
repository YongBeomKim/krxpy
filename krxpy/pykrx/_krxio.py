from .base import *
from ._website import Post


class KrxWebIo(Post):
    r"""수집을 위한 Params 정의하기"""

    def read(self, **params):
        params.update(bld=self.bld)

        if 'strtDd' in params and 'endDd' in params:
            dt_s  = pandas.to_datetime(params['strtDd'])
            dt_e  = pandas.to_datetime(params['endDd'])
            delta = pandas.to_timedelta('730 days')

            result = None
            while dt_s + delta < dt_e:

                dt_tmp = dt_s + delta
                params['strtDd'] = dt_s.strftime("%Y%m%d")
                params['endDd'] = dt_tmp.strftime("%Y%m%d")
                dt_s += delta + pandas.to_timedelta('1 days')
                resp  = super().read(**params)

                if result is None:
                    result = resp.json()
                else:
                    result['output'] += resp.json()['output']

                # 초당 2년 데이터 조회
                time.sleep(1)

            if dt_s <= dt_e:
                params['strtDd'] = dt_s.strftime("%Y%m%d")
                params['endDd'] = dt_e.strftime("%Y%m%d")
                resp = super().read(**params)

                if result is not None:
                    result['output'] += resp.json()['output']
                else:
                    result = resp.json()
            return result
        else:
            resp = super().read(**params)
            return resp.json()

    @property
    def url(self):
        return "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

    @property
    @abstractmethod
    def bld(self):
        return NotImplementedError

    @bld.setter
    def bld(self, val):
        pass

    @property
    @abstractmethod
    def fetch(self, **params):
        return NotImplementedError
