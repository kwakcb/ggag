import streamlit as st
import streamlit.components.v1 as components

# 제목을 표시합니다 ver1.0 2024.6.27

# 사이드바에 메뉴 생성
menu = st.sidebar.radio(
    "",
    ("Home", "고장상황", "OLT", "광3종", "L2", "기타")
)

if menu == "Home":
    st.title("Memo")

    # 우측 정렬된 서브헤더 추가
    st.markdown("""
    <div style='text-align: right;'>
    <h3>by Kwak.cb</h3>
    </div>
    """, unsafe_allow_html=True)

    # 메모 입력
    etc_memo = st.text_input("#memo", key="home_memo")

elif menu == "고장상황":
   import streamlit as st
import streamlit.components.v1 as components

# 제목을 표시합니다 ver1.0 2024.6.27
st.title("ktMOS")

# 우측 정렬된 서브헤더 추가
st.markdown("""
<div style='text-align: right;'>
    <h3>by Kwak.cb</h3>
</div>
""", unsafe_allow_html=True)

etc_memo = st.text_input("메모 입력")
st.code(etc_memo)

ip_address = st.text_input("■ [OLT 링크] L2 IP 주소를 입력하세요")

# 여러 개의 추가 텍스트 정의
additional_texts = [
    "sh arp pon | inc ",
    "sh epon ip-macs all all | inc ",
]

# IP 주소가 입력된 경우에만 처리
if ip_address:
    # 각 추가 텍스트와 IP 주소 결합하여 출력
    for text in additional_texts:
        combined_text = text + ip_address
        st.write(combined_text)

# 코드 블록을 표시합니다
st.code("DB 작업중.....")
st.code("링크 현행화.....")
st.code("★장비교체 완료 NeOSS, NMS, SDN")

# 리스트박스에 표시할 항목 목록 정의
options = ["[NOC_10G(용량확대)]","[NOC_BAT(24)]","[NOC_CRC발생]","[NOC_PLK_PSU교체]","[NOC_PSU교체]",
           "[NOC_고객프로파일]","[NOC_광레벨불]","[NOC_자산관리]","[NOC_장비교체]","[NOC_장비철거]",
           "[NOC_전원OFF]","[NOC_중복장애]","[NOC_통합멀티룸]","[NOC_품질개선]"]

# 리스트박스 생성
selected_option = st.selectbox("■ BS HEAD", options)

# 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
copy_script = f"""
<script>
function copyToClipboard(text) {{
    navigator.clipboard.writeText(text).then(function() {{
        alert('클립보드에 복사되었습니다: ' + text);
    }}, function(err) {{
        alert('텍스트 복사 실패: ' + err);
    }});
}}

// 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('copy-button').addEventListener('click', function() {{
        copyToClipboard("{selected_option}");
    }});
}});
</script>
<button id="copy-button">클립보드에 복사</button>
"""

# 클립보드 복사 버튼을 HTML로 삽입
components.html(copy_script, height=100)

# 선택된 항목을 화면에 표시
# st.write(f"{selected_option}")

#------------------------------
# 첫 번째 리스트박스에 표시할 항목 목록 정의
options1 = ["[KT차단기복구]", "[고객원인]","[고객측작업]","[광커넥터복구]","[기타]","[멀티탭 ON/교체]","[모듈교체]",
            "[발전기가동]","[사설정전복구]","[사설차단기복구]","[장비교체]","[장비리셋]","[장비철거]","[전원가복구]",
            "[전원어댑터교체]","[출동중복구]","[타사전환]","[타사전환]","[타사전환]","[폐문]","[한전정전복구]"]

# 첫 번째 리스트박스 생성
selected_option1 = st.selectbox("■ 회복 HEAD", options1)
moss_recover = st.text_input("회복 내용")
moss_thankyou = "수고하셨습니다~"

# 두 번째 리스트박스에 표시할 항목 목록 정의
options2 = [" ","[DB현행화]","[FOLLOW추가]","[문자발송]","[원격조치]", "[원인분석]","[전기작업확인(전화)]","[정전알림이]"]
selected_option2 = st.selectbox("<NOC_선조치>", options2)

# Streamlit 상태 업데이트
st.session_state['selected_option1'] = selected_option1
st.session_state['moss_recover'] = moss_recover
st.session_state['selected_option2'] = selected_option2

# 조건에 따라 combinedText 구성
combined_text = f"{selected_option1}\n{moss_recover}\n{moss_thankyou}"
if selected_option2 != " ":
    combined_text += f"\n<NOC_선조치> {selected_option2}"

# 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
copy_script = f"""
<script>
function copyToClipboard(text) {{
    navigator.clipboard.writeText(text).then(function() {{
        alert('클립보드에 복사되었습니다: ' + text);
    }}, function(err) {{
        alert('텍스트 복사 실패: ' + err);
    }});
}}

// 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('copy-button').addEventListener('click', function() {{
        const combinedText = `{combined_text.replace('\\n', '\\\\n')}`;
        copyToClipboard(combinedText);
    }});
}});
</script>
<button id="copy-button">클립보드에 복사</button>
"""

# 클립보드 복사 버튼을 HTML로 삽입
components.html(copy_script, height=100)

# 선택된 항목 및 텍스트를 화면에 표시
#st.write(f"■ 회복 HEAD: {selected_option1}")
#st.write(f"회복내용: {moss_recover}")
#st.write(moss_thankyou)
#if selected_option2 != " ":
#    st.write(f"<NOC_선조치> {selected_option2}")

elif menu == "OLT":
    st.header("OLT")
    
    # 코드 블록을 표시합니다
    st.code("DB 작업중.....")
    st.code("Link 현행화.....")
    st.code("★ 장비교체 NeOSS, NMS, SDN 현행화 완료")

    ip_address = st.text_input("■ [OLT LINK] Enter the L2 IP address")
    
    # 여러 개의 추가 텍스트 정의
    additional_texts = [
        "sh arp pon | inc ",
        "sh epon ip-macs all all | inc ",
    ]
    
    # IP 주소가 입력된 경우에만 처리
    if ip_address:
        # 각 추가 텍스트와 IP 주소 결합하여 출력
        for text in additional_texts:
            combined_text = text + ip_address
            st.write(combined_text)

    SlotPortLink = st.text_input("Slot/Port-Link", key="LLID")

elif menu == "광3종":
    # st.header("광3종")

    # 동원 입력값을 받습니다
    user_input1 = st.text_input("-동원: S/P L", "1/1 1")

    # 유비 입력값을 받습니다
    user_input2 = st.text_input("-유비: S/P", "1/1")

    # 다산 입력값을 받습니다
    user_input3 = st.text_input("-다산: S/P L", "1/1 1")

    # 명령어 목록을 저장할 리스트
    commands1 = []
    commands2 = []
    commands3 = []

    # 동원 입력값 처리
    if user_input1:
        if len(user_input1.split()) == 2:
            commands1 = [
                f"sh epon onu-ddm {user_input1}",
                f"sh epon rssi rx-pwr-periodic {user_input1}",
                f"sh epon crc-monitoring statistics {user_input1}"
            ]
        else:
            st.error("동원 입력값 형식이 올바르지 않습니다. 예: 1/1 1")

    # 유비 입력값 처리
    if user_input2:
        if len(user_input2.split('/')) == 2 and all(part.isdigit() for part in user_input2.replace('/', '').split()):
            commands2 = [
                f"sh pon onu-ddm {user_input2}",
                f"sh pon top onu {user_input2}",
                f"sh pon stats onu-crc {user_input2}"
            ]
        else:
            st.error("유비 입력값 형식이 올바르지 않습니다. 예: 5/8")

    # 다산 입력값 처리
    if user_input3:
        if len(user_input3.split()) == 2:
            commands3 = [
                f"sh epon onu-ddm {user_input3}",
                f"sh epon rssi rx-pwr-periodic {user_input3}",
                f"sh epon crc-monitoring statistics {user_input3}"
            ]
        else:
            st.error("다산 입력값 형식이 올바르지 않습니다. 예: 2/13 40")

    # 각 명령어를 출력
    if commands1:
        st.write("동원---------------------------------------------")
        for cmd in commands1:
            st.write(cmd)
    
    if commands2:
        st.write("유비------------------------------------------------")
        for cmd in commands2:
            st.write(cmd)

    if commands3:
        st.write("다산-----------------------------------------------")
        for cmd in commands3:
            st.write(cmd)

elif menu == "L2":
    st.header("L2")

elif menu == "기타":
    st.header("기타")
