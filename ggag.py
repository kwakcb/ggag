import streamlit as st
import streamlit.components.v1 as components

# 제목을 표시합니다 ver1.0 2024.6.27
st.title("#도우미")

# 우측 정렬된 서브헤더 추가
st.markdown("""
<div style='text-align: right;'>
    <h3>by Kwak.cb</h3>
</div>
""", unsafe_allow_html=True)

# 사이드바에 메뉴 생성
menu = st.sidebar.radio(
    "Menu",
    ("Home", "고장상황", "긴급복구", "일지", "기타")
)

if menu == "Home":
    st.header("Notice")
    etc_memo = st.text_input("memo input")
    st.code(etc_memo)

elif menu == "고장상황":
        
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

    options = ["[NOC_10G(용량확대)]","[NOC_BAT(24)]","[NOC_CRC발생]","[NOC_PLK_PSU교체]","[NOC_PSU교체]",
               "[NOC_고객프로파일]","[NOC_광레벨불]","[NOC_자산관리]","[NOC_장비교체]","[NOC_장비철거]",
               "[NOC_전원OFF]","[NOC_중복장애]","[NOC_통합멀티룸]","[NOC_품질개선]"]

    # 리스트박스 생성
    selected_option = st.selectbox("■ BS HEAD", options)

    # 기타 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
    copy_script_bs_head = f"""
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
        document.getElementById('copy-button-bs-head').addEventListener('click', function() {{
            copyToClipboard("{selected_option}");
        }});
    }});
    </script>
    <button id="copy-button-bs-head">Copy to Clipboard</button>
    """

    # 클립보드 복사 버튼을 HTML로 삽입
    components.html(copy_script_bs_head, height=100)

        options1 = ["[KT차단기복구]", "[고객원인]","[고객측작업]","[광커넥터복구]","[기타]","[멀티탭 ON/교체]","[모듈교체]",
                "[발전기가동]","[사설정전복구]","[사설차단기복구]","[장비교체]","[장비리셋]","[장비철거]","[전원가복구]",
                "[전원어댑터교체]","[출동중복구]","[타사전환]","[타사전환]","[타사전환]","[폐문]","[한전정전복구]"]

    # 긴급복구 리스트박스 생성
    selected_option1 = st.selectbox("■ 고장회복 HEAD", options1)
    moss_recover = st.text_input("회복내용")
    moss_thankyou = "수고하셨습니다~"

    # 두 번째 리스트박스에 표시할 항목 목록 정의
    options2 = [" ","[DB현행화]","[FOLLOW추가]","[문자발송]","[원격조치]", "[원인분석]","[전기작업확인(전화)]","[정전알림이]"]
    selected_option2 = st.selectbox("<NOC_선조치>", options2)

    # 조건에 따라 combined_text 구성
    combined_text = f"{selected_option1}\n{moss_recover}\n{moss_thankyou}"
    if selected_option2 != " ":
        combined_text += f"\n<NOC_선조치> {selected_option2}"

    # 긴급복구 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
    copy_script_recover_head = """
    <script>
    function copyToClipboard() {
        const combinedText = `""" + combined_text.replace('\n', '\\n') + """`;
        navigator.clipboard.writeText(combinedText).then(function() {
            alert('Copied to clipboard: ' + combinedText);
        }, function(err) {
            alert('Failed to copy text: ' + err);
        });
    }

    // 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('copy-button-recover-head').addEventListener('click', copyToClipboard);
    });
    </script>
    <button id="copy-button-recover-head">Copy to Clipboard</button>
    """

    # 클립보드 복사 버튼을 HTML로 삽입
    components.html(copy_script_recover_head, height=100)

elif menu == "긴급복구":
    st.header("긴급복구")
    # 이 부분은 공란으로 남겨둡니다.

elif menu == "일지":
    st.header("일지")
    # 이 부분은 공란으로 남겨둡니다.

elif menu == "기타":
    st.header("기타")
    # 이 부분은 공란으로 남겨둡니다.
