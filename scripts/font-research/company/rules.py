# 라이선스 본문에서 조건 문구를 찾는 규칙.
import re

NEG = r"(금지|불가|안\s?됩니다|없습니다|할 수 없|허용하지 않|제한)"
RULES = [
    ("수정 금지", r"(수정|개작|변형|편집)[^.\n]{0,40}" + NEG),
    ("재배포 금지", r"(재배포|배포)[^.\n]{0,30}" + NEG),
    ("판매 금지", r"(판매|유료)[^.\n]{0,30}" + NEG),
    ("BI·CI·로고 금지", r"(CI|BI|로고|상표|브랜드)[^.\n]{0,40}" + NEG),
    ("출처 표기 필수", r"출처[^.\n]{0,20}(표기|표시|명시|밝)[^.\n]{0,15}(해야|하여야|필수|바랍니다|주셔야|합니다)"),
    ("출처 표기 권장", r"출처[^.\n]{0,20}(표기|표시|명시)[^.\n]{0,10}권장"),
    ("별도 승인 필요", r"(사전|별도|서면)[^.\n]{0,10}(승인|허가|허락|협의|동의|문의)"),
    ("이용 등록 필요", r"(정보|회원|사용자)\s?(등록|가입)[^.\n]{0,10}(후|하여야|해야|하신)"),
    ("업종 제한", r"(게임|산업군|업종|정치|종교|성인)[^.\n]{0,30}(금지|불가|사용할 수 없)"),
    ("OFL", r"(Open Font License|SIL OFL|OFL\s?1\.1|오픈 폰트 라이선스)"),
]
# 웹 임베딩에 따로 승인을 받으라는 문장
WEB_APPROVAL = re.compile(r"(임베딩|임베디드|임베이딩|웹\s?폰트|웹폰트|탑재|서버)[^.\n]{0,60}?(사전|별도|서면)?[^.\n]{0,10}?"
                          r"(승인|허가|허락|협의|문의 후|별도 문의가 필요|동의 후|동의를|계약)")
# '상업적·비상업적 목적으로 자유롭게'는 허용이고, '판매하는 등 상업적 사용 금지'는 판매 금지라서 뺀다.
NON_COMMERCIAL = re.compile(r"(비상업[^.\n]{0,12}(한하여|한해|만\s?사용|용도로만|목적으로만)|"
                            r"(?<![비/·,])(?<!판매하는 등 )(?<!양도하는 등 )상업적\s?(이용|사용|목적)[^.\n]{0,15}(금지|불가|할 수 없))")
SALE_CONTEXT = re.compile(r"(판매|양도|재판매|다음 각 호|다음의 경우)[^.\n]{0,40}$")



# '별도의 허가 없이', '허락이 필요하지 않으나' 처럼 뒤에서 뒤집는 말
NEGATED_AFTER = re.compile(r"^[^.\n]{0,15}(없이|필요하지 않|필요 없|필요없|않아도|않습니다|않으나)")
NOISE_TAGS = re.compile(r"^(굵기|\d+가지|폰트 옵션|가변|이탤릭)$")


def find_conditions(text):
    """본문에서 조건 이름 목록을 돌려준다. OFL 이면 OFL 조건 한 줄로 바꾼다."""
    found = []
    for name, pat in RULES:
        for m in re.finditer(pat, text):
            if not NEGATED_AFTER.search(text[m.end():m.end() + 20]):
                found.append(name)
                break
    if "OFL" in found:
        return ["OFL(글꼴 단독 판매 금지·고치면 이름 바꿈)"] + [x for x in found if x == "이용 등록 필요"]
    if "출처 표기 필수" in found and "출처 표기 권장" in found:
        found.remove("출처 표기 필수")
    return found


def needs_web_approval(text):
    for m in WEB_APPROVAL.finditer(text):
        if not NEGATED_AFTER.search(text[m.end():m.end() + 20]):
            return True
    return False


def split_tags(tags):
    """눈누 형태 태그에서 굵기 정보를 떼어 (형태, 굵기) 로 나눈다."""
    shape = [t for t in tags if not NOISE_TAGS.match(t)]
    n = next((t for t in tags if re.match(r"^\d+가지$", t)), "")
    w = (n + " 굵기" if n else "") + (" · 가변" if "가변" in tags else "")
    return shape, w.strip(" ·")


COMMERCIAL_OK = re.compile(r"(상업[^.\n]{0,25}(사용|이용)\s?(할 수 있|가능|하실 수 있)|상업용|상업적 용도 포함|상업적 목적 포함)")


def commercial_status(text):
    """'ok' / 'partial'(허용 문장과 제한 문장이 함께) / 'no'(제한 문장만)."""
    neg = any(not SALE_CONTEXT.search(text[max(0, m.start() - 60):m.start()])
              for m in NON_COMMERCIAL.finditer(text))
    pos = bool(COMMERCIAL_OK.search(text))
    if not neg:
        return "ok"
    return "partial" if pos else "no"
