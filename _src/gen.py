import os, json, html, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from regions_all import ALL as REGIONS, RBY, SIDO
from data_trades import TRADES as T1, NEXT
from data_trades2 import TRADES2
from data_partners import PARTNERS
from icons import icon, LOGO
from data_popup import AREAS
_all = {t['slug']: t for t in T1 + TRADES2}
ORDER = ['hasugu','nusu','yeolsoe','boiler','jeongi','dongpa','yuri','aircon','sujeon','bangsu','jeonghwa','cheongso','julnun','yupum','bangyeok','bidulgi','sadari','shutter','naengjang','ganpan','popup']
TRADES = [_all[s] for s in ORDER]
TBY = {t['slug']: t for t in TRADES}
GROUPS = [('집 수리·고장', ORDER[:11]), ('청소·정리·방역', ORDER[11:16]), ('상가·업소', ORDER[16:])]
def group_of(slug):
    return next(g for g in GROUPS if slug in g[1])
def pros(t, r=None):
    L = list(PARTNERS.get((t['slug'], r['slug'] if r else None), [])) + list(PARTNERS.get(t['slug'], []))
    L = L[:3]
    if DEMO:
        where = r['name'] if r else '인천'
        while len(L) < 3:
            k = len(L) + 1
            L.append(dict(name=f'제휴 업체 {k}', phone=f'0500-000-000{k}', note='시안용 예시'))
    return L

DOMAIN = 'https://hongsos.co.kr'
PHONE = '0500-000-0000'   # 제휴 후 가상번호로 교체
DEMO = True
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/hongsos/site'
UPDATED = '2026-11-18'
E = html.escape
TEL = PHONE.replace('-', '')
CSS = open(os.path.join(os.path.dirname(__file__), 'style.css')).read()
FONTS = '<link rel="preload" href="/fonts/bhs.woff2" as="font" type="font/woff2" crossorigin>'
PH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
TIP = dict(newapt='아파트 단지명과 동·호수, 방문 차량 주차 등록 방법', old='골목 진입이 되는지, 차를 세울 곳이 있는지', shop='상호와 영업 시간, 작업 가능한 시간대', ind='공장·창고 출입 절차와 담당자 연락처', rural='정확한 지번 주소와 진입로 상태, 주변 큰 건물이나 표지판', island='섬 이름과 배편 시간, 선착장에서 거리', univ='건물주 동의 여부와 공용 현관 비밀번호')

def page(title, desc, path, body, ld, c='#15171C', ink='#FFFFFF', first=None, loc='전국'):
    canon = DOMAIN + path
    demo = '<p class="demo">시안입니다. 번호와 사진은 예시예요.</p>' if DEMO else ''
    return f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta name="theme-color" content="{c}"><meta name="color-scheme" content="light dark"><meta name="apple-mobile-web-app-title" content="홍라이프 긴급출동"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/s.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body style="--c:{c};--ink:{ink}">{demo}
<header class="top"><a class="logo" href="/">{LOGO}<span>홍라이프 긴급출동</span></a><span class="loc">{loc}</span></header>
<main>{body}</main>
<footer><p class="joinlink"><a href="/join/">업체 사장님이세요? 무료 등록 신청하기</a></p><p>홍라이프 긴급출동은 지역 업체를 전화로 이어 드리는 중개 서비스입니다. 시공과 비용 청구는 연결된 업체가 직접 합니다. 비용은 참고 범위이며 현장에 따라 달라집니다.</p><p>최종 업데이트 {UPDATED}</p></footer>
<a class="bar" aria-label="지금 전화하기" href="tel:{(first or PHONE).replace('-','')}">{PH}<span>지금 전화하기</span><b>{first or PHONE}</b></a>
</body></html>'''

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i+1, "name": n, "item": DOMAIN + p} for i, (n, p) in enumerate(items)]}

def faqld(fs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fs]}

def magnet(where, name, what, crumb_html, plist=None, slug=None):
    if plist:
        rows = ''.join(f'<li><a href="tel:{p["phone"].replace("-","")}" aria-label="{E(p["name"])}, {E(p["phone"])}로 전화 걸기"><span>{E(p["name"])}<small>{E(p.get("note",""))}</small></span><b>{E(p["phone"])}</b></a></li>' for p in plist)
        call = f'<p class="pros-h">누르면 바로 연결돼요</p><ol class="pros">{rows}</ol>'
    else:
        call = f'<a class="num" href="tel:{TEL}"><span>누르면 바로 연결</span><b>{PHONE}</b></a>'
    return f'''<div class="mag">
<nav class="crumb">{crumb_html}</nav>
<p class="where">{icon(slug, 'ic big') if slug else ''}{E(where)}</p>
<h1 class="{'long' if len(name) > 5 else ''}">{E(name)}</h1>
<p class="what">{E(what)}</p>
{call}
<ul class="promise"><li>동네 업체 3곳 중 골라서</li><li>출발 전에 예상 금액 안내</li></ul>
</div>'''

def shot(t, alt):
    return f'<figure class="shot"><img src="/img/{t["photo"]}.jpg" alt="{E(alt)}" width="720" height="964"><figcaption>예시 사진</figcaption></figure>'

def sec(h, inner, cls=''):
    return f'<section class="{cls}"><h2>{h}</h2>{inner}</section>'

def price(t):
    rows = ''.join(f'<li><span>{E(a)}</span><i></i><b>{E(b)}</b></li>' for a, b in t['price'])
    return f'<ul class="menu">{rows}</ul><p class="note">참고 범위예요. 업체가 출발하기 전에 전화로 예상 금액을 먼저 알려드립니다.</p>'

def steps(t):
    li = ''.join(f'<li><b>{E(a)}</b><p>{E(b)}</p></li>' for a, b in t['steps'])
    return f'<ol class="steps">{li}</ol><p class="warn">{E(t["warn"])}</p>'

def sym(t):
    return '<ul class="sym">' + ''.join(f'<li>{E(s)}</li>' for s in t['symptoms']) + '</ul>'

def faq(fs):
    return ''.join(f'<details{" open" if i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(fs))

def tiles(items):
    return '<div class="tiles">' + ''.join(f'<a href="{h}" style="--c:{o["color"]};--ink:{o["ink"]}">{icon(o["slug"])}<span>{E(label)}</span></a>' for h, o, label in items) + '</div>'


def quote_form(where, phone):
    tel = phone.replace('-', '')
    return f'''<section class="quote" id="quote"><h2>견적 요청하기</h2>
<p class="lede">아래를 채우고 버튼을 누르면 내용이 적힌 문자 창이 열려요. 보내기만 누르면 업체에 바로 전달됩니다.</p>
<form class="qf" data-tel="{tel}" data-where="{E(where)}">
<label>브랜드·회사 이름<input name="brand" autocomplete="organization" required></label>
<label>행사 장소<input name="place" placeholder="{E(where)} ○○몰 1층" required></label>
<div class="row"><label>오픈 날짜<input name="date" type="date"></label><label>운영 기간<input name="period" placeholder="예: 2주"></label></div>
<div class="row"><label>면적<input name="size" inputmode="numeric" placeholder="예: 10평"></label><label>예산<select name="budget"><option>미정</option><option>500만 원 이하</option><option>500만~1,000만 원</option><option>1,000만~3,000만 원</option><option>3,000만 원 이상</option></select></label></div>
<label>연락받을 번호<input name="phone" type="tel" autocomplete="tel" required></label>
<label>요청 사항<textarea name="memo" rows="3" placeholder="콘셉트, 참고 이미지, 철거 포함 여부 등"></textarea></label>
<button type="submit">견적 문자 보내기</button>
<p class="note">문자 앱에서 내용을 확인한 뒤 보내 주세요. 홍라이프 긴급출동은 업체를 연결해 드리는 중개 서비스입니다.</p>
</form></section>'''

QF_JS = '''<script>document.querySelectorAll('.qf').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);const t=['[팝업 인테리어 견적 요청]','브랜드: '+d.get('brand'),'장소: '+d.get('place'),'오픈: '+(d.get('date')||'미정')+' / 기간: '+(d.get('period')||'미정'),'면적: '+(d.get('size')||'미정')+' / 예산: '+d.get('budget'),'연락처: '+d.get('phone'),'요청: '+(d.get('memo')||'-')].join('\\n');const ios=/iP(hone|ad|od)/.test(navigator.userAgent);location.href='sms:'+f.dataset.tel+(ios?'&':'?')+'body='+encodeURIComponent(t);}));</script>'''

def popup_area_page(a):
    t = TBY['popup']
    path = f'/popup/seoul-{a["slug"]}/'
    title = f'{a["name"]} 팝업스토어 인테리어 · 행사 부스 시공 업체 | 홍라이프 긴급출동'
    desc = f'{a["full"]} 팝업스토어·행사 부스 시공. ' + '·'.join(s for s, _ in a['spots']) + ' 공간별 안내, 참고 비용, 시공 일정 팁. 견적 문자로 바로 요청.'
    tagps = [t['tagp'][g] for g in a['tags'] if g in t['tagp']][:2]
    spots = '<dl class="areas">' + ''.join(f'<div><dt>{E(s)}</dt><dd>{E(d)}</dd></div>' for s, d in a['spots']) + '</dl>'
    others = '<p class="near">' + ''.join(f'<a href="/popup/seoul-{o["slug"]}/">{E(o["name"])}</a>' for o in AREAS if o is not a) + '</p>'
    pl = pros(t, dict(name=a['name'], slug='seoul-'+a['slug']))
    crumb = f'<a href="/">홈</a><a href="/popup/">팝업 인테리어</a><span>{E(a["name"])}</span>'
    fs = t['faq']
    body = magnet(a['full'], t['name'], t['title2'], crumb, pl, 'popup') + shot(t, f'{a["name"]} 팝업스토어 시공 현장') + \
        sec(f'{E(a["name"])} 팝업, 이렇게 다릅니다', f'<p class="lede">{E(a["intro"])}</p><p>{E(a["tip"])}</p>' + ''.join(f'<p>{E(p)}</p>' for p in tagps), 'prose') + \
        sec('공간 유형별로 보기', spots) + quote_form(a['name'], pl[0]['phone']) + \
        sec('이런 일이면 맡기세요', sym(t)) + sec(f'{E(a["name"])} 팝업 인테리어 비용', price(t)) + \
        sec('업체에 연락하기 전에', steps(t)) + sec('자주 묻는 질문', faq(fs)) + \
        sec('다른 서울 팝업 상권', others, 'tight') + QF_JS
    ld = {"@context": "https://schema.org", "@graph": [
        crumbs([('홍라이프 긴급출동', '/'), (t['name'], '/popup/'), (a['name'], path)]), faqld(fs),
        {"@type": "Service", "serviceType": "팝업스토어 인테리어", "areaServed": {"@type": "Place", "name": a['full']},
         "provider": {"@type": "Organization", "name": "홍라이프 긴급출동", "url": DOMAIN}}]}
    return path, page(title, desc, path, body, ld, t['color'], t['ink'], pl[0]['phone'], '서울')


KW = [
 (('원룸','고시','대학가'), ('원룸 건물이 많아 집주인이나 관리인 연락처를 같이 준비해 두면 작업 승인이 빨라집니다', '세입자가 많은 곳이라 비용을 누가 낼지 미리 정해 두면 뒤탈이 없습니다')),
 (('공장','산단','산업','물류','공단','조선소','디지털단지','연구'), ('공장·창고는 출입 절차가 있어 담당자 연락처와 출입 방법을 먼저 알려 주셔야 합니다', '업무용 설비는 장비 규격에 따라 부품이 달라 설비 사진을 보내 주시면 견적이 정확해집니다')),
 (('펜션','전원','농촌','농가','산골','캠핑','산 자락','산자락','마을'), ('도심에서 떨어진 곳이라 정확한 지번 주소와 진입로 상태를 알려 주시면 출장비를 미리 안내받을 수 있습니다', '업체 이동 거리가 길어 도착 시간이 늘 수 있으니 급하면 첫 통화에서 바로 말씀해 주세요')),
 (('해변','바닷가','해안','항구','어촌','항만','섬','강변','한강변','호수'), ('물가와 가까워 습기와 염분 때문에 설비가 빨리 상하는 편이라 부품 상태를 같이 봐 달라고 하시면 좋습니다', '바람과 습기가 많은 곳이라 작업 뒤 실리콘·보온 마감까지 확인하는 게 좋습니다')),
 (('언덕','산복도로','비탈'), ('경사진 골목이 많아 장비 차량이 어디까지 들어올 수 있는지 먼저 확인합니다', '차가 못 들어가는 골목이면 장비를 손으로 옮겨야 해서 시간이 더 걸릴 수 있습니다')),
 (('시장','상권','번화가','식당','카페','상가','관광','유흥','횟집','숙박'), ('가게 영업 전후로 작업 시간을 맞추는 경우가 많아 원하는 시간대를 먼저 말씀해 주시면 됩니다', '영업 중인 가게는 손님 동선을 피해 작업해야 해서 출입구와 작업 공간을 미리 알려 주시면 좋습니다')),
 (('신축','신도시','뉴타운','택지','재건축','재개발','혁신도시'), ('입주한 지 얼마 안 된 단지는 하자보수 기간인지 먼저 확인하면 비용을 아낄 수 있습니다', '신축은 설비 제조사 보증이 남아 있을 수 있어 보증서를 같이 찾아 두시면 좋습니다')),
 (('아파트','단지','주상복합','초고층','고층'), ('아파트 단지는 방문 차량 등록과 엘리베이터 사용을 관리사무소에 미리 알려 두면 작업이 빨라집니다', '공용 배관과 이어진 문제인지 세대 안 문제인지에 따라 비용 부담이 달라질 수 있습니다')),
 (('다세대','주택가','원도심','노후','한옥','주택','빌라','저층'), ('오래된 건물이 많아 부품을 같이 바꿔야 할 수 있으니 예상 금액을 출발 전에 꼭 들어 보세요', '수십 년 된 집은 배관과 배선이 여러 번 덧대어 있어 현장에서 금액이 바뀔 수 있다는 점을 미리 알아 두세요')),
]
def area_notes(r, t):
    out = []
    for i, (a, d) in enumerate(r['areas'][:4]):
        for ks, hints in KW:
            if any(k in d or k in a for k in ks):
                h = hints[(len(a) + len(t['slug']) + i) % 2]
                out.append(f'{a}({d}) 쪽 {t["name"]} 출동은 {h}.')
                break
    return out

def region_page(t, r):
    rn = r['name']; L = r['label']
    path = f'/{t["slug"]}/{r["slug"]}/'
    title = f'{L} {t["name"]} · {t["title2"]} 24시 출장 | 홍라이프 긴급출동'
    areas_txt = '·'.join(a for a, _ in r['areas'][:4])
    desc = f'{L}({r["alias"]}) {t["name"]}. {areas_txt} 생활권별 안내, 참고 비용, 오기 전 조치법을 정리했습니다. 가까운 업체로 24시 전화 연결.'
    tagps = [t['tagp'][g] for g in r['tags'] if g in t['tagp']][:3]
    ri = REGIONS.index(r)
    fs = [t['faq'][(ri+j) % 3] for j in range(2)] + [r['faq']]
    tips = ['증상과 언제부터 그랬는지, 가능하면 사진'] + [TIP[g] for g in r['tags'] if g in TIP] + ['방문 가능한 시간과 받을 연락처']
    areas = '<dl class="areas">' + ''.join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in r['areas']) + '</dl>'
    near = '<p class="near">' + ''.join(f'<a href="/{t["slug"]}/{n}/">{E(RBY[n]["label"])}</a>' for n in r['near']) + '</p>'
    crumb = f'<a href="/">홈</a><a href="/area/{r["slug"]}/">{E(L)}</a><span>{E(t["name"])}</span>'
    body = magnet(L, t['name'], t['title2'], crumb, pros(t, r), t['slug']) + shot(t, f'{rn} {t["name"]} 작업 현장') + \
        sec(f'{E(rn)}에서는 이렇게 다릅니다', f'<p class="lede">{E(t["lead"])} {E(rn)}({E(r["alias"])}) 안에서 가까운 업체를 먼저 연결합니다.</p><p>{E(r["intro"])}</p><p>{E(r["bld"])}</p>' + ''.join(f'<p>{E(p)}</p>' for p in tagps), 'prose') + \
        sec('생활권별로 보기', ''.join(f'<p>{E(x)}</p>' for x in area_notes(r, t)) + areas, 'prose') + \
        sec('전화할 때 알려 주세요', '<ul class="tips">' + ''.join(f'<li>{E(x)}</li>' for x in tips) + f'</ul><p class="season">{E(t["season"])}</p>') + \
        (quote_form(rn, pros(t, r)[0]['phone']) if t['slug'] == 'popup' else '') + \
        sec('이런 일이면 부르세요', sym(t)) + \
        sec(f'{E(rn)} {E(t["name"])} 비용', price(t)) + \
        sec('업체가 오기 전에', steps(t)) + \
        sec('자주 묻는 질문', faq(fs)) + \
        sec(f'옆 동네 {E(t["name"])}', near, 'tight') + \
        sec(f'{E(rn)} {E(group_of(t["slug"])[0])} 다른 출동', tiles([(f'/{s}/{r["slug"]}/', TBY[s], TBY[s]['name']) for s in group_of(t['slug'])[1] if s != t['slug']]), 'tight') + (QF_JS if t['slug'] == 'popup' else '')
    ld = {"@context": "https://schema.org", "@graph": [
        crumbs([('홍라이프 긴급출동', '/'), (t['name'], f'/{t["slug"]}/'), (L, f'/area/{r["slug"]}/'), (t['name'], path)]), faqld(fs),
        {"@type": "Service", "serviceType": t['name'], "areaServed": {"@type": "AdministrativeArea", "name": r['admin']},
         "provider": {"@type": "Organization", "name": "홍라이프 긴급출동", "url": DOMAIN}}]}
    return path, page(title, desc, path, body, ld, t['color'], t['ink'], pros(t, r)[0]['phone'] if pros(t, r) else None, r['sido'])

def trade_hub(t):
    path = f'/{t["slug"]}/'
    title = f'{t["name"]} · {t["title2"]} 지역별 24시 출장 | 서울·경기·인천·광역시 | 홍라이프 긴급출동'
    desc = f'서울·경기·인천과 부산·대구·광주·대전·울산·세종 108개 시·군·구 {t["name"]} 업체 연결. 지역별 안내와 참고 비용, 오기 전 조치법.'
    regs = sido_lists(lambda r: f'/{t["slug"]}/{r["slug"]}/')
    crumb = f'<a href="/">홈</a><span>{E(t["name"])}</span>'
    body = magnet('수도권·광역시', t['name'], t['title2'], crumb, pros(t), t['slug']) + shot(t, f'{t["name"]} 작업 현장') + \
        (sec('서울 주요 팝업 상권', '<ul class="regions">' + ''.join(f'<li><a href="/popup/seoul-{a["slug"]}/"><b>{E(a["name"])}</b><span>{E(a["full"])}</span></a></li>' for a in AREAS) + '</ul>') + quote_form('서울·수도권', pros(t)[0]['phone']) if t['slug'] == 'popup' else '') + \
        sec('어느 동네세요?' if t['slug'] != 'popup' else '지역별 팝업 인테리어', f'<p class="lede">{E(t["lead"])}</p>' + regs) + \
        sec('이런 일이면 부르세요', sym(t)) + sec(f'{E(t["name"])} 비용', price(t)) + \
        sec('업체가 오기 전에', steps(t)) + sec('자주 묻는 질문', faq(t['faq'])) + (QF_JS if t['slug'] == 'popup' else '')
    ld = {"@context": "https://schema.org", "@graph": [crumbs([('홍라이프 긴급출동', '/'), (t['name'], path)]), faqld(t['faq'])]}
    return path, page(title, desc, path, body, ld, t['color'], t['ink'], loc='전국')

def sido_lists(href):
    return ''.join(f'<h3 class="sido" id="{ss}">{E(sf)}</h3><ul class="regions">' + ''.join(f'<li><a href="{href(r)}"><b>{E(r["name"])}</b><span>{E(r["alias"])}</span></a></li>' for r in L) + '</ul>' for s, ss, sf, L in SIDO)

def area_page(r):
    L = r['label']; path = f'/area/{r["slug"]}/'
    title = f'{L} 24시 출장 수리·청소·방역 업체 연결 | 홍라이프 긴급출동'
    desc = f'{L}({r["alias"]}) 하수구·누수·열쇠·보일러·전기·청소·방역 등 21가지 출동 업체를 한 번에. 생활권별 안내와 전화 연결.'
    areas = '<dl class="areas">' + ''.join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in r['areas']) + '</dl>'
    near = '<p class="near">' + ''.join(f'<a href="/area/{n}/">{E(RBY[n]["label"])}</a>' for n in r['near']) + '</p>'
    crumb = f'<a href="/">홈</a><a href="/#{r["sslug"]}">{E(r["sido"])}</a><span>{E(r["name"])}</span>'
    body = f'''<div class="mag home"><nav class="crumb">{crumb}</nav><p class="where">{E(r["alias"])}</p><h1{' class="long"' if len(r['name']) > 5 else ''}>{E(r['name'])}<br>긴급출동</h1><p class="what">{E(r["intro"])}</p><a class="num" href="tel:{TEL}"><span>누르면 바로 연결</span><b>{PHONE}</b></a></div>''' + \
        ''.join(sec(gn, tiles([(f'/{s}/{r["slug"]}/', TBY[s], TBY[s]['name']) for s in gl]), 'tight') for gn, gl in GROUPS) + \
        sec(f'{E(r["name"])}, 이런 곳이에요', f'<p>{E(r["bld"])}</p>' + areas, 'prose') + \
        sec('옆 동네', near, 'tight')
    ld = {"@context": "https://schema.org", "@graph": [crumbs([('홍라이프 긴급출동', '/'), (L, path)])]}
    return path, page(title, desc, path, body, ld, loc=r['sido'])

def home():
    bands = ''.join(f'''<li style="--c:{t["color"]};--ink:{t["ink"]}"><a href="/{t["slug"]}/"><span class="t">{icon(t["slug"], "ic big")}<b>{E(t["name"])}</b><small>{E(t["title2"])}</small></span><img src="/img/{t["photo"]}.jpg" alt="" width="720" height="964" loading="lazy"></a></li>''' for t in TRADES[:4])
    nxt = '<p class="soon">' + ''.join(f'<span>{E(n)}</span>' for n in NEXT) + '</p>'
    regs = sido_lists(lambda r: f'/area/{r["slug"]}/')
    body = f'''<div class="mag home">
<p class="where">서울·경기·인천·광역시</p>
<h1>급할 때<br>붙여 두는<br>번호 하나</h1>
<p class="what">막히고, 새고, 잠기고, 꺼졌을 때. 동네 업체로 바로 이어 드려요.</p>
<a class="num" href="tel:{TEL}"><span>누르면 바로 연결</span><b>{PHONE}</b></a>
</div>
<section class="flush"><h2>가장 많이 찾는 출동</h2><ul class="bands">{bands}</ul></section>
{''.join(sec(gn, tiles([(f'/{s}/', TBY[s], TBY[s]['name']) for s in gl]), 'tight') for gn, gl in GROUPS)}
{sec('동네별로 찾기', '<p class="lede">수도권과 광역시 108개 시·군·구예요. 인천은 2026년 7월 바뀐 9구 2군 기준입니다.</p>' + regs)}
{sec('이렇게 연결돼요', '<ol class="steps"><li><b>전화하기</b><p>무슨 일인지, 주소가 어디인지 말씀해 주세요.</p></li><li><b>가까운 업체 연결</b><p>그 동네에서 바로 갈 수 있는 업체로 이어 드려요.</p></li><li><b>금액 듣고 결정</b><p>업체가 출발하기 전에 예상 금액을 듣고 부를지 정하시면 돼요.</p></li></ol>')}'''
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "홍라이프 긴급출동", "url": DOMAIN + '/'}
    return '/', page('홍라이프 긴급출동 | 하수구·누수·열쇠·보일러 24시 업체 연결', '서울·경기·인천·광역시 108개 시·군·구 하수구 막힘, 누수 탐지, 열쇠·도어락, 보일러, 사다리차, 방역 업체를 24시 전화로 연결합니다.', '/', body, ld, loc='전국')


JOIN_TEL = PHONE  # 신청 받을 번호(050 또는 사장님 업무용 번호로 교체)

def join_page():
    path = '/join/'
    opts = ''.join(f'<option>{E(t["name"])}</option>' for t in TRADES)
    regs = ''.join(f'<label class="ck"><input type="checkbox" name="area" value="{E(s)}"><span>{E(s)}</span></label>' for s, *_ in SIDO)
    body = f'''<div class="mag home" style="--c:#15171C;--ink:#fff">
<nav class="crumb"><a href="/">홈</a><span>업체 무료 등록</span></nav>
<p class="where">업체 사장님께</p>
<h1 class="long">무료로<br>올려 드려요</h1>
<p class="what">동네에서 직접 뛰는 업체를 찾고 있어요. 조건이 맞으면 첫 3개월은 무료로 우리 동네 페이지에 연결해 드립니다.</p>
</div>
<section class="prose"><h2>이런 업체를 찾아요</h2>
<ul class="tips">
<li>사장님이나 담당 기사가 <b>직접 전화를 받고 상담</b>하는 업체</li>
<li>손님에게 <b>출발 전에 예상 금액을 먼저 안내</b>하는 업체</li>
<li>사업자등록이 되어 있고, 등록한 지역에 <b>실제로 출장</b>을 가는 업체</li>
<li>현장 사진이나 작업 전후 사진을 보내 줄 수 있는 업체</li>
<li>불친절·바가지 민원이 들어오면 연결을 중단하는 데 동의하는 업체</li>
</ul></section>
<section><h2>무료 기간에 받는 것</h2>
<ol class="steps">
<li><b>우리 동네 페이지 등록</b><p>업종과 지역 페이지 맨 위에 업체 이름과 번호가 올라갑니다.</p></li>
<li><b>연결 건수 공유</b><p>매달 몇 명이 전화 버튼을 눌렀는지 알려 드려요.</p></li>
<li><b>3개월 뒤 선택</b><p>계속할지는 그때 결과를 보고 사장님이 정하시면 됩니다. 자동으로 돈이 나가는 일은 없어요.</p></li>
</ol></section>
<section class="quote"><h2>무료 등록 신청</h2>
<p class="lede">신청서를 채우고 버튼을 누르면 내용이 적힌 문자 창이 열려요. 보내기만 누르면 신청 끝입니다.</p>
<form class="jf" data-tel="{JOIN_TEL.replace('-', '')}">
<label>상호<input name="biz" autocomplete="organization" required></label>
<label>대표자 이름<input name="owner" autocomplete="name" required></label>
<label>업종<select name="trade">{opts}<option>기타</option></select></label>
<fieldset><legend>출장 가능 지역</legend><div class="cks">{regs}</div></fieldset>
<label>세부 지역 (시·군·구)<input name="detail" placeholder="예: 강남구, 수원시 영통구"></label>
<label>상담 받는 번호<input name="phone" type="tel" autocomplete="tel" required></label>
<label>직접 통화 가능한 시간<input name="hours" placeholder="예: 매일 8시~22시, 야간 긴급 가능"></label>
<label>사업자등록번호 (선택)<input name="bizno" inputmode="numeric" placeholder="확인 후 등록에만 사용해요"></label>
<label class="ck agree"><input type="checkbox" name="ok1" required><span>사장님이 직접 손님 전화를 받고 상담합니다.</span></label>
<label class="ck agree"><input type="checkbox" name="ok2" required><span>등록 안내와 연결 실적을 문자·전화로 받는 데 동의합니다.</span></label>
<button type="submit">신청 문자 보내기</button>
<p class="note">신청 내용은 업체 등록 확인에만 쓰고, 등록하지 않으면 바로 지웁니다.</p>
</form></section>
<script>document.querySelectorAll('.jf').forEach(f=>f.addEventListener('submit',e=>{{e.preventDefault();const d=new FormData(f);const a=d.getAll('area').join(', ')||'미선택';const t=['[홍라이프 긴급출동 무료 등록 신청]','상호: '+d.get('biz'),'대표: '+d.get('owner'),'업종: '+d.get('trade'),'지역: '+a+' / '+(d.get('detail')||'-'),'번호: '+d.get('phone'),'통화 가능: '+(d.get('hours')||'-'),'사업자번호: '+(d.get('bizno')||'-'),'직접 상담·연락 수신 동의함'].join('\\n');const ios=/iP(hone|ad|od)/.test(navigator.userAgent);location.href='sms:'+f.dataset.tel+(ios?'&':'?')+'body='+encodeURIComponent(t);}}));</script>'''
    ld = {"@context": "https://schema.org", "@graph": [crumbs([('홍라이프 긴급출동', '/'), ('업체 무료 등록', path)])]}
    return path, page('업체 무료 등록 신청 | 홍라이프 긴급출동', '수도권·광역시 출장 업체 사장님을 위한 무료 등록 안내. 직접 상담하는 업체를 동네 페이지에 3개월 무료로 연결해 드립니다.', path, body, ld)

def write(path, s):
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if path != '/' else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(s)

if __name__ == '__main__':
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    urls = []
    for p, s in [home()] + [trade_hub(t) for t in TRADES] + [region_page(t, r) for t in TRADES for r in REGIONS] + [area_page(r) for r in REGIONS] + [popup_area_page(a) for a in AREAS] + [join_page()]:
        write(p, s); urls.append(p)
    FF = ''.join(f'@font-face{{font-family:"{n}";src:url(/fonts/{f}.woff2) format("woff2");font-weight:{w};font-display:swap}}' for n,f,w in [('Black Han Sans','bhs',400),('Gothic A1','ga400',400),('Gothic A1','ga600',600),('Gothic A1','ga800',800)])
    open(os.path.join(OUT, 's.css'), 'w').write(FF + CSS)
    import glob, re as _re, subprocess
    ch = set('0123456789-·/ ')
    for f in glob.glob(OUT + '/**/*.html', recursive=True):
        ch |= set(html.unescape(_re.sub(r'<[^>]+>', ' ', open(f).read())))
    open('/tmp/hs_chars.txt', 'w').write(''.join(sorted(ch)))
    os.makedirs(os.path.join(OUT, 'fonts'))
    for src, o in [('BlackHanSans-Regular','bhs'),('GothicA1-Regular','ga400'),('GothicA1-SemiBold','ga600'),('GothicA1-ExtraBold','ga800')]:
        subprocess.run(['pyftsubset', os.path.expanduser(f'~/.fonts/{src}.ttf'), '--text-file=/tmp/hs_chars.txt', '--flavor=woff2', f'--output-file={OUT}/fonts/{o}.woff2'], check=True)
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'img'), os.path.join(OUT, 'img'))
    sm = ''.join(f'<url><loc>{DOMAIN}{u}</loc><lastmod>{UPDATED}</lastmod></url>' for u in urls)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(LOGO.replace(' class="mark"', ' xmlns="http://www.w3.org/2000/svg"'))
    shutil.copy(os.path.join(os.path.dirname(__file__),'apple-touch-icon.png'), OUT)
    open(os.path.join(OUT, 'CNAME'), 'w').write('hongsos.co.kr\n')
    print(len(urls), 'pages')
