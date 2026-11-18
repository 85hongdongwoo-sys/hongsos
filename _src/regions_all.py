# 전 지역 통합: 수도권 + 광역시
from data_regions import REGIONS as _INC
from data_seoul import SEOUL
from data_gyeonggi import GYEONGGI
from data_metro import BUSAN, DAEGU, GWANGJU, DAEJEON, ULSAN, SEJONG

INCHEON = []
for r in _INC:
    d = dict(r)
    d.update(sido='인천', sslug='incheon', slug='incheon-' + r['slug'], near=['incheon-' + n for n in r['near']])
    INCHEON.append(d)

# (시·도 약칭, slug, 정식 명칭, 지역 목록)
SIDO = [('서울', 'seoul', '서울특별시', SEOUL), ('경기', 'gyeonggi', '경기도', GYEONGGI), ('인천', 'incheon', '인천광역시', INCHEON),
        ('부산', 'busan', '부산광역시', BUSAN), ('대구', 'daegu', '대구광역시', DAEGU), ('광주', 'gwangju', '광주광역시', GWANGJU),
        ('대전', 'daejeon', '대전광역시', DAEJEON), ('울산', 'ulsan', '울산광역시', ULSAN), ('세종', 'sejong', '세종특별자치시', SEJONG)]
SFULL = {s: f for s, _, f, _ in SIDO}
ALL = [r for *_, L in SIDO for r in L]
RBY = {r['slug']: r for r in ALL}

FAQ_TAG = {
    'newapt': ('아파트 관리사무소에 먼저 연락해야 하나요?', '세대 안 고장은 바로 업체를 부르셔도 됩니다. 공용 배관이나 윗집·아랫집과 얽힌 문제는 관리사무소에도 같이 알려 두시면 처리가 빠릅니다. 하자보수 기간 안이라면 시공사 접수가 먼저일 수 있습니다.'),
    'old': ('오래된 빌라인데 수리비가 더 나오나요?', '배관이나 설비가 오래되면 부품을 같이 바꿔야 하는 경우가 있어 금액이 조금 오를 수 있습니다. 업체가 출발 전에 예상 범위를 먼저 알려 드리니 듣고 결정하시면 됩니다.'),
    'shop': ('가게 영업 끝나고 밤에 와 줄 수 있나요?', '네. 야간이나 새벽 작업이 가능한 업체를 먼저 연결해 드립니다. 영업 시간과 작업 가능한 시간을 전화로 말씀해 주세요. 야간 할증은 업체마다 다릅니다.'),
    'ind': ('공장이나 창고도 출장 오나요?', '네. 공장·창고·물류센터 설비도 연결합니다. 출입 절차와 담당자 연락처, 작업 가능한 시간을 알려 주시면 맞는 업체를 찾기 쉽습니다.'),
    'rural': ('시내에서 먼 곳인데 출장비가 붙나요?', '거리가 멀면 출장비가 따로 붙을 수 있습니다. 정확한 주소를 말씀해 주시면 가까운 업체를 먼저 찾고, 출장비가 있으면 출발 전에 알려 드립니다.'),
    'univ': ('원룸 세입자인데 바로 불러도 되나요?', '급한 상황이면 먼저 부르셔도 되지만, 비용 부담 문제가 있으니 집주인에게 같이 알려 두시는 게 좋습니다. 영수증과 작업 전후 사진은 꼭 받아 두세요.'),
    'island': ('섬까지 출장이 되나요?', '배편과 날씨에 따라 가능한 날이 정해집니다. 섬 이름과 원하는 날짜를 알려 주시면 출장 가능한 업체와 일정을 확인해 드립니다.'),
}
for r in ALL:
    r.setdefault('faq', FAQ_TAG[r['tags'][0]])
    r['label'] = r['name'] if (r['name'].startswith(r['sido']) or r['sido'] == '경기') else f"{r['sido']} {r['name']}"
    nm = r['name'].split(' ', 1)[1] if r['name'].startswith(r['sido'] + ' ') else r['name']
    r['admin'] = SFULL[r['sido']] if r['sido'] == '세종' else f"{SFULL[r['sido']]} {nm}"

bad = [(r['slug'], n) for r in ALL for n in r['near'] if n not in RBY]
assert not bad, bad
