# 업종 라인 아이콘 (24px 그리드, 2px 선, 1톤)
P = {
 'hasugu':   '<path d="M3 7h7a4 4 0 0 1 4 4v3"/><path d="M3 4v6"/><path d="M14 14h4v3h-4z"/><path d="M16 19.5c0 1-.7 1.5-1.2 1.5s-1.3-.5-1.3-1.5c0-.8 1.3-2.5 1.3-2.5"/>',
 'nusu':     '<path d="M10 3S5 9 5 13a5 5 0 0 0 7.5 4.3"/><circle cx="16.5" cy="15.5" r="3.5"/><path d="m19 18 2.5 2.5"/>',
 'yeolsoe':  '<circle cx="7.5" cy="12" r="4"/><path d="M11.5 12H21"/><path d="M17 12v3M20 12v2"/>',
 'boiler':   '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M12 17c-2 0-3-1.3-3-3 0-2 3-4.5 3-4.5s3 2.5 3 4.5c0 1.7-1 3-3 3z"/><path d="M8 6h3"/>',
 'jeongi':   '<path d="M13 2 5 13h6l-1 9 8-11h-6z"/>',
 'dongpa':   '<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/><path d="m9.5 4.5 2.5 2 2.5-2M9.5 19.5l2.5-2 2.5 2"/>',
 'yuri':     '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M12 3v18M4 12h16"/><path d="m15 6-1.5 2.5 2 1L14 12"/>',
 'aircon':   '<rect x="3" y="5" width="18" height="7" rx="2"/><path d="M6 9h12"/><path d="M8 15c0 1.5-1 2-1 3.5M12 15v4M16 15c0 1.5 1 2 1 3.5"/>',
 'sujeon':   '<path d="M4 9h9a3 3 0 0 1 3 3v1"/><path d="M8 9V6M5 6h6"/><path d="M16 16v.5M16 19.5v.5"/><path d="M3 21h18"/>',
 'bangsu':   '<path d="M3 11 12 4l9 7"/><path d="M6 10v10h12V10"/><path d="M12 12.5s-2 2.4-2 3.8a2 2 0 0 0 4 0c0-1.4-2-3.8-2-3.8z"/>',
 'jeonghwa': '<rect x="3" y="9" width="18" height="11" rx="3"/><path d="M8 9V6h8v3"/><path d="M7 14h10"/>',
 'cheongso': '<path d="M9 8h5l1 3v10H8V11z"/><path d="M10 8V5h4l3-1.5"/><path d="M19 9l1.5-.5M19 12h2M18.5 15l1.5.8"/>',
 'julnun':   '<rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M3 12h18M12 3v18"/><path d="M15 15l3 3"/>',
 'yupum':    '<path d="M3 8l9-4 9 4v9l-9 4-9-4z"/><path d="M3 8l9 4 9-4M12 12v9"/>',
 'bangyeok': '<ellipse cx="12" cy="14" rx="4.5" ry="6"/><path d="M12 8V5M9 5.5 7 3.5M15 5.5l2-2"/><path d="M7.5 12H4M7.5 16H4M16.5 12H20M16.5 16H20M12 9v11"/>',
 'bidulgi':  '<path d="M4 15c3 0 5-2 6-5 .8-2.5 2.6-4 5-4a3 3 0 0 1 3 3l2 1-2 1v1c0 4-3 7-8 7H4z"/><path d="M8 21l1-2M12 21l.5-2"/><circle cx="15.5" cy="8.5" r=".6" fill="currentColor"/>',
 'sadari':   '<path d="M8 3 5 21M16 3l3 18"/><path d="M7.3 7h9.4M6.7 11h10.6M6 15h12M5.4 19h13.2"/>',
 'shutter':  '<path d="M3 4h18v3H3z"/><path d="M4 7v14M20 7v14"/><path d="M4 10.5h16M4 14h16M4 17.5h16"/>',
 'naengjang':'<rect x="5" y="2.5" width="14" height="19" rx="2"/><path d="M5 10h14M8 6v2M8 13v3"/>',
 'popup':    '<path d="M4 21V9l8-5 8 5v12"/><path d="M4 9h16"/><path d="M8 21v-7h8v7"/><path d="M7 9l1.5 3M12 9v3M17 9l-1.5 3"/>',
 'ganpan':   '<rect x="3" y="4" width="18" height="10" rx="1.5"/><path d="M7 9h10"/><path d="M8 14v6M16 14v6M6 20h4M14 20h4"/>',
}
def icon(slug, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[slug]}</svg>'

# 로고: 냉장고 자석 + 수화기
LOGO = '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="9" fill="#D7261E"/><circle cx="24.5" cy="7.5" r="2.6" fill="#F1F2F0"/><path d="M22.5 20.2v2.6a1.7 1.7 0 0 1-1.9 1.7 17 17 0 0 1-7.4-2.6 16.8 16.8 0 0 1-5.2-5.2A17 17 0 0 1 5.4 9.3 1.7 1.7 0 0 1 7.1 7.4h2.6a1.7 1.7 0 0 1 1.7 1.5c.1.8.3 1.6.6 2.4a1.7 1.7 0 0 1-.4 1.8l-1.1 1.1a13.8 13.8 0 0 0 5.2 5.2l1.1-1.1a1.7 1.7 0 0 1 1.8-.4c.8.3 1.6.5 2.4.6a1.7 1.7 0 0 1 1.5 1.7z" fill="#F1F2F0"/></svg>'
