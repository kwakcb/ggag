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

etc_memo = st.text_input("memo input")
st.code(etc_memo)

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

# 코드 블록을 표시합니다
st.code("DB 작업중.....")
st.code("Link 현행화.....")
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
        alert('Copied to clipboard: ' + text);
    }}, function(err) {{
        alert('Failed to copy text: ' + err);
    }});
}}

// 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('copy-button').addEventListener('click', function() {{
        copyToClipboard("{selected_option}");
    }});
}});
</script>
<button id="copy-button">Copy to Clipboard</button>
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
moss_recover = st.text_input("회복내용")
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
        alert('Copied to clipboard: ' + text);
    }}, function(err) {{
        alert('Failed to copy text: ' + err);
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
<button id="copy-button">Copy to Clipboard</button>
"""

# 클립보드 복사 버튼을 HTML로 삽입
components.html(copy_script, height=100)

# 선택된 항목 및 텍스트를 화면에 표시
#st.write(f"■ 회복 HEAD: {selected_option1}")
#st.write(f"회복내용: {moss_recover}")
#st.write(moss_thankyou)
#if selected_option2 != " ":
#    st.write(f"<NOC_선조치> {selected_option2}")
