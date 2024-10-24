import streamlit as st
import streamlit.components.v1 as components
import json
import webbrowser
import pandas as pd


# 서브넷 마스크와 CIDR 형식 대응표
subnet_options = {
    "/24": "255.255.255.0",
    "/25": "255.255.255.128",
    "/26": "255.255.255.192",
    "/27": "255.255.255.224",
    "/28": "255.255.255.240",
    "/29": "255.255.255.248",
    "/30": "255.255.255.252"
}

# 모델별 서브넷 마스크 형식 설정
model_subnet_formats = {
    "U3024B": "/24",  # CIDR 형식
    "E5624R": "/24",  # CIDR 형식
    "MVD10024": "255.255.255.0",  # 서브넷 마스크 형식
    "V5972": "/24",  # CIDR 형식
    "V2724GB": "/24",  # CIDR 형식
    "V2708GA": "/24",  # CIDR 형식
    "V3024V": "/24",  # CIDR 형식
    "V5124F": "/24"  # CIDR 형식
}

if 'fault_info' not in st.session_state:
    st.session_state.fault_info = ""

if 'dispatch_info' not in st.session_state:
    st.session_state.dispatch_info = ""
    
# 제목을 표시합니다 ver1.0 2024.6.27

# 사이드바에 메뉴 생성
menu = st.sidebar.radio(
    "",
    ("KWAK", "고장상황", "MOSS_Copy", "OLT광3종", "OLT Check", "OLT_1stRN", "L2 Check", "IP SETTING", "OPR", "10G","ftp긴급복구","U4224B_SDN","각종일지")
)

if menu == "KWAK":
    st.title("""■ Memo
-전원분야 고장성 경보 범위-\n
[한전정전] 한전정전으로 발전기 가동 또는 축전기 방전 중\n
[차단기OFF] VCB / ACB / MG / MC OFF로 축전지 방전, 발전기 가동 중\n
[변압기 고장] 축전기 방전 또는 발전기 가동 중\n
[국사 화재] 화재감지기 작동 현장 출동중\n
[국사 침수] 침수 알람 발생 현장 출동중\n

-네트워트 현황보고-\n
[MOSS 항목] 전원,교환,액세스\n
[PING경보] ACCESS_XDSL,엔토피아\n
[공사정보] 작업통제_대쉬보드 총건수_1000/page설정_ 작업현황 전체복사 후 A2셀에 주변서식에 맟추기 붙여넣기\n\n
■ 유관기관 연락처\n
-OSP 관제센터: 02-500-6150\n
-IP망 관제센터: 042-478-1600\n
-전원관제: 042-478-1800\n
-과천 제1관제센터(교환): 02-500-6080\n
-무선: 042-489-6831\n
-NOC:1577-7315\n\n

-교환기술부\n
.충: 042-255-2470\n
.호: 062-513-1200\n
.부: 051-464-4699\n
.대:053-477-3010\n\n

-분기국사출입문(전원)\n
.충: 042-478-7550, 7540\n
.호:062-230-3355\n
.부:051-464-2300\n
.대:053-477-1985 \n\n

※유선제어팀: neobiz_gmoscc_c1000_d3595@ktmos.co.kr
​  -> L2/L3 정비요청 및 민원요청관련 업무 등

""")
# Display the clickable weather radar link
    st.markdown("[기상청 레이더 영상](https://www.weather.go.kr/w/image/radar.do)")

    # Right-aligned subheader
    st.markdown("""
    <div style='text-align: right;'>
    <h3>by Kwak.cb</h3>
    </div>
    """, unsafe_allow_html=True)
    


if menu == "고장상황":
    options = ["[NOC_10G(용량확대)]", "[NOC_BAT(24)]", "[NOC_CRC발생]", "[NOC_PLK_PSU교체]", "[NOC_PSU교체]",
               "[NOC_고객프로파일]", "[NOC_광레벨불]", "[NOC_민원처리]", "[NOC_자산관리]", "[NOC_장비교체]", "[NOC_장비철거]", "[NOC_점검정비]",
               "[NOC_전원OFF]", "[NOC_중복장애]", "[NOC_통합멀티룸]", "[NOC_품질개선]"]

    # 리스트박스 생성
    selected_option = st.selectbox("■ BS HEAD", options, key="bs_head")
    moss_recover_bs = st.text_input("회복내용", key="bs_recover")
    moss_thankyou_bs = "수고하셨습니다~"

    # 두 번째 리스트박스에 표시할 항목 목록 정의
    options2 = [" ", "DB현행화", "FOLLOW추가", "WorkSync", "기타", "문자발송", "원격조치", "원인분석", "전기작업확인(전화)", "정전알림이"]
    selected_option2 = st.selectbox("<선조치_NOC>", options2, key="bs_option2")

    # 조건에 따라 combined_text 구성
    combined_text_bs = f"{selected_option}\n{moss_recover_bs}\n{moss_thankyou_bs}"
    if selected_option2 != " ":
        combined_text_bs += f"\n<선조치_NOC> {selected_option2}"

    # 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
    copy_script_bs_head = f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            // alert(text);  // 이 줄을 제거하거나 주석 처리합니다.
        }}, function(err) {{
            // alert('텍스트 복사 실패: ' + err);  // 이 줄도 제거하거나 주석 처리합니다.
        }});
    }}

    // 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
    document.addEventListener('DOMContentLoaded', function() {{
        document.getElementById('copy-button-bs-head').addEventListener('click', function() {{
            const textToCopy = {json.dumps(combined_text_bs)};
            copyToClipboard(textToCopy);
        }});
    }});
    </script>
    <button id="copy-button-bs-head">클립보드에 복사</button>
    """

    # 클립보드 복사 버튼을 HTML로 삽입
    components.html(copy_script_bs_head, height=100)

    # 긴급복구 리스트박스 생성
    options1 = ["[KT차단기복구]", "[고객원인]", "[고객측작업]", "[광커넥터복구]", "[기타]", "[멀티탭 ON/교체]", "[모듈교체]",
                "[발전기가동]", "[사설정전복구]", "[사설차단기복구]", "[장비교체]", "[장비리셋]", "[장비철거]", "[전원가복구]",
                "[전원어댑터교체]", "[출동중복구]", "[타사전환]", "[폐문]", "[한전정전복구]"]

    # 긴급복구 리스트박스 생성
    selected_option1 = st.selectbox("■ 고장회복 HEAD", options1, key="recover_option1")
    moss_recover = st.text_input("회복내용", key="recover_recover")
    moss_thankyou = "수고하셨습니다~"

    # 두 번째 리스트박스에 표시할 항목 목록 정의
    options2 = [" ", "DB현행화", "FOLLOW추가", "WorkSync", "기타", "문자발송", "원격조치", "원인분석", "전기작업확인(전화)", "정전알림이"]
    selected_option2 = st.selectbox("<선조치_NOC>", options2, key="recover_option2")

    # 조건에 따라 combined_text 구성
    combined_text_recover = f"{selected_option1}\n{moss_recover}\n{moss_thankyou}"
    if selected_option2 != " ":
        combined_text_recover += f"\n<선조치_NOC> {selected_option2}"

    # 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
    copy_script_recover_head = f"""
    <script>
    function copyToClipboard() {{
        const combinedText = {json.dumps(combined_text_recover)};
        navigator.clipboard.writeText(combinedText).then(function() {{
            // alert(combinedText);  // 이 줄을 제거하거나 주석 처리합니다.
        }}, function(err) {{
            // alert('텍스트 복사 실패: ' + err);  // 이 줄도 제거하거나 주석 처리합니다.
        }});
    }}

    // 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
    document.addEventListener('DOMContentLoaded', function() {{
        document.getElementById('copy-button-recover-head').addEventListener('click', copyToClipboard);
    }});
    </script>
    <button id="copy-button-recover-head">클립보드에 복사</button>
    """

    # 클립보드 복사 버튼을 HTML로 삽입
    components.html(copy_script_recover_head, height=100)

    # 헤더 선택 리스트박스
    header_options = ["[L2_정전]", "[L2_선로]", "[아파트_정전]"]
    selected_header = st.selectbox("■ 다량장애 HEAD", header_options, key="header_option")

    # 입력 항목
    site_name = st.text_input("국사_사업장", key="site_name")
    l2_count = st.text_input("L2 대수", key="l2_count")
    subscriber_count = st.text_input("고객수", key="subscriber_count")

    # 헤더에 따라 추가 단어 삽입
    if selected_header == "[L2_정전]":
        extra_text = "일대 한전정전 추정"
    elif selected_header == "[L2_선로]":
        extra_text = "선로장애 추정"
    elif selected_header == "[아파트_정전]":
        extra_text = "공용전원 정전 추정"
    else:
        extra_text = ""

    # 조건에 따라 출력 내용 구성
    combined_text = f"{selected_header} {site_name}  {extra_text} L2*{l2_count} 대 [{subscriber_count}고객]"

    # 클립보드 복사 기능을 위한 HTML과 JavaScript 코드
    copy_script = f"""
    <script>
    function copyToClipboard(text) {{
        navigator.clipboard.writeText(text).then(function() {{
            // alert(text);  // 이 줄을 제거하거나 주석 처리합니다.
        }}, function(err) {{
            // alert('텍스트 복사 실패: ' + err);  // 이 줄도 제거하거나 주석 처리합니다.
        }});
    }}

    // 클릭 이벤트가 발생할 때 클립보드에 텍스트를 복사
    document.addEventListener('DOMContentLoaded', function() {{
        document.getElementById('copy-button').addEventListener('click', function() {{
            const textToCopy = {json.dumps(combined_text)};
            copyToClipboard(textToCopy);
        }});
    }});
    </script>
    <button id="copy-button">클립보드에 복사</button>
    """

    # 출력된 텍스트와 복사 버튼을 HTML로 삽입
    st.write(combined_text)
    components.html(copy_script, height=100)



elif menu == "MOSS_Copy":
    st.header("■ MOSS_Copy")
    
    # 코드 블록을 표시합니다
    st.code("DB/LINK 현행화 중...") 
    st.code("★ 장비교체 NeOSS, NMS, SDN 현행화 완료")
    st.code("★ 상황전파 수정요청")
    st.code("★ PING복구 > MOSS자동회복 > 조치사항 입력 ")
    st.code("★ 경보회복 되었습니다 ")
    st.code("★ 사업장 정보 / 연락처 수정완료 ")
    st.code("장비 경보(Ping) 해제되었습니다.\n최종복구 여부 확인 및 조치사항 입력 후 '회복처리' 요청 드립니다.")
    st.code("[출동중복구]\n출동전 자동회복\n수고하셨습니다~")
    

elif menu == "OLT광3종":
    # st.header("광3종")
    st.header("■ OLT광3종")
    ip_address = st.text_input("■ [OLT LINK] Enter the L2 IP address")
    
    # 여러 개의 추가 텍스트 정의
    additional_texts = [
        "sh arp pon | inc ",
        "sh epon ip-macs all all | inc ",
        "sh arp | inc ",
        "sh olt mac epon 1/1 | inc "
    ]
    
    # IP 주소가 입력된 경우에만 처리
    if ip_address:
        # 각 추가 텍스트와 IP 주소 결합하여 출력
        for text in additional_texts:
            combined_text = text + ip_address
            st.write(combined_text)

    #SlotPortLink = st.text_input("Slot/Port-Link", key="LLID")
        
    # 동원 입력값을 받습니다
    user_input1 = st.text_input("-동원[MEGALITE,DWES0960]: S/P L", "1/1 1")

    # 유비 입력값을 받습니다
    user_input2 = st.text_input("-유비[U9500H,U9732S,U902A]: S/P", "1/1")

    # 다산 입력값을 받습니다
    user_input3 = st.text_input("-다산[V5832XG]: S/P L", "1/1 1")

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
                f"sh epon crc-monitoring statistics {user_input1}",
                f"clear epon crc-monitoring statistics {user_input1}"
           
            ]

        else:
            st.error("동원 입력값 형식이 올바르지 않습니다. 예: 1/1 1")

    # 유비 입력값 처리
    if user_input2:
        if len(user_input2.split('/')) == 2 and all(part.isdigit() for part in user_input2.replace('/', '').split()):
            commands2 = [
                f"(U9500H)#sh pon onu-ddm {user_input2}",
                f"(U9024A)#sh pon onu ddm {user_input1}",
                f"sh pon top onu {user_input2}",
                f"sh pon stats onu-crc {user_input2}",
                f"clear pon statistics counter {user_input2}\n"
                
            ]
        else:
            st.error("유비 입력값 형식이 올바르지 않습니다. 예: 5/8")

    # 다산 입력값 처리
    if user_input3:
        if len(user_input3.split()) == 2:
            commands3 = [
                f"sh epon onu-ddm {user_input3}",
                f"sh onu ddm epon {user_input3}",
                f"sh olt rssi-info epon {user_input3}",
                f"sh olt statistics epon 1/1",
                f"sh olt statistics onu epon 1/1",
                f"sh arp",
                f"sh olt mac epon 1/1",
                f"sh sysl l v r"
               
            ]
        else:
            st.error("다산 입력값 형식이 올바르지 않습니다. 예: 2/13 40")

    # 각 명령어를 출력
    if commands1:
        st.write("■ 동원 ----------")
        for cmd in commands1:
            st.write(cmd)
    
    if commands2:
        st.write("■ 유비 ----------")
        for cmd in commands2:
            st.write(cmd)

    if commands3:
        st.write("■ 다산 ----------")
        for cmd in commands3:
            st.write(cmd)
            
    
    # 제목
    st.header("ㅇ광레벨 입력 및 출력")

    # 입력 받기
    ddm = st.text_input("DDM 값 입력", "-12.11")
    rssi = st.text_input("RSSI 값 입력", "-24.32")
    crc = st.text_input("CRC 값 입력", "0")

    # 조합된 출력 생성
    output = f"#광레벨   DDM : {ddm}  / RSSI : {rssi}  / CRC : {crc}"

    # 출력 화면 표시
    #st.write(output)

    # 클립보드에 복사할 수 있도록 텍스트를 text_area로 표시
    st.text_area("클립보드에 복사할 텍스트", output, height=100)

    
    


elif menu == "OLT Check":
    st.header("OLT Check")
    
    st.text("[동원 DW0960]\n"
        "sh slot\n"
        "sh system\n"
        "대용량PIU:xe1,2,3,4,5,6,9,A,B,C/1~8\n"
        "sh epon port-status 12/4\n"
        "sh epon onu-statistics pon 12/4 0\n"
        "sh mac-address-table xe12/4 | inc 77f6\n"
        "sh epon servic-police 1/1 all\n"
        "sh epon ip-macs 1/1 all | inc a.b.c.d\n"
        "sh epon onu ddm 1/1 all\n"
        "sh epon rssi rx-power-peri 1/1 all\n" 
        "sh epon crc-monitoring statistics 2/2 all\n"
        "clear epon crc-monitoring statistics 2/2 all\n"
        "sh mac-address-table pon1/1\n"
        "sh ip dhcp snoop binding\n"
        "sh ip igmp snoop table group\n"
        "sh ip pim neighbor\n"
        "(config/pon)#reset hybridonu slot/port-ont\n"
        "(config/pon)#reboot hybrid-onu\n"
        "(config/pon)#shutdown onu port\n"
        "(config/pon)#ldshutdown\n"
        "[동원 MEGALITE]\n"
        "소용량PIU:ge1,2,3,4,5,6/1~4\n"
        "sh ip dhcp statistics\n"
        "sh ip igmp snooping gro\n"
        "sh ip pim sparse-mode neighbor detail\n\n"
        "[유비 U-9500H]\n"
        "sh slot\n"
        "sh pon onu ddm 1/1-1\n"
        "sh pon top onu 1/1\n"
        "sh pon olt ddmi 1/1 1\n"
        "sh pon olt dyna bridge-entri 1/1-1\n"
        "sh arp pon | inc a.b.c.d\n"
        "(config-pon)#reboot hybridonu 1/1-2\n"
        "sh pon service-policy onu 1/1-1\n"
        "sh pon[10gpon] stats onu-crc 1/1\n"
        "clear pon statistics counter 8/1-1\n"
        "sh mac-address-table\n"
        "sh ip dhcp sno bin\n"
        "sh ip igmp sno tab rep\n"
        "sh ip pim sparse-mode neigbor\n\n"
        "[유비  U-9200A]\n"
        "sh pon onu ddm 6/1-1\n" 
        "sh pon top onu sum\n"
        "sh pon statistics ave type 6/1\n\n"
        "[다산 V5832XG]\n"
        "sh onu ddm epon 1/1\n"
        "sh olt rssi-info epon 1/1\n"
        "sh olt statistics epon 1/1\n"
        "sh olt statistics onu epon 1/1\n"
        "sh arp | inc 183.106.186.23\n"
        "sh olt mac epon 1/1 | inc 183.106.186.23\n")

elif menu == "OLT_1stRN":
    st.header("■ OLT_1차RN")
    
    # 데이터 정의
    data = [
    ("유비소용량", "1/1", "J010"), ("유비소용량", "1/2", "J020"), ("유비소용량", "2/1", "J030"), ("유비소용량", "2/2", "J040"),
    ("유비소용량", "3/1", "J050"), ("유비소용량", "3/2", "J060"), ("유비소용량", "4/1", "J070"), ("유비소용량", "4/2", "J080"),
    ("유비소용량", "5/1", "J090"), ("유비소용량", "5/2", "J100"), ("유비소용량", "6/1", "J110"), ("유비소용량", "6/2", "J120"),
    ("유비소용량", "7/1", "J130"), ("유비소용량", "7/2", "J140"), ("유비소용량", "8/1", "J150"), ("유비소용량", "8/2", "J160"),
    ("유비소용량", "9/1", "J170"), ("유비소용량", "9/2", "J180"), ("유비소용량", "10/1", "J190"), ("유비소용량", "10/2", "J200"),
    ("유비대용량", "1/1", "C110"), ("유비대용량", "1/2", "C120"), ("유비대용량", "1/3", "C130"), ("유비대용량", "1/4", "C140"),
    ("유비대용량", "1/5", "C150"), ("유비대용량", "1/6", "C160"), ("유비대용량", "1/7", "C170"), ("유비대용량", "1/8", "C180"),
    ("유비대용량", "2/1", "C210"), ("유비대용량", "2/2", "C220"), ("유비대용량", "2/3", "C230"), ("유비대용량", "2/4", "C240"),
    ("유비대용량", "2/5", "C250"), ("유비대용량", "2/6", "C260"), ("유비대용량", "2/7", "C270"), ("유비대용량", "2/8", "C280"),
    ("유비대용량", "3/1", "C310"), ("유비대용량", "3/2", "C320"), ("유비대용량", "3/3", "C330"), ("유비대용량", "3/4", "C340"),
    ("유비대용량", "3/5", "C350"), ("유비대용량", "3/6", "C360"), ("유비대용량", "3/7", "C370"), ("유비대용량", "3/8", "C380"),
    ("유비대용량", "4/1", "C410"), ("유비대용량", "4/2", "C420"), ("유비대용량", "4/3", "C430"), ("유비대용량", "4/4", "C440"),
    ("유비대용량", "4/5", "C450"), ("유비대용량", "4/6", "C460"), ("유비대용량", "4/7", "C470"), ("유비대용량", "4/8", "C480"),
    ("유비대용량", "5/1", "C510"), ("유비대용량", "5/2", "C520"), ("유비대용량", "5/3", "C530"), ("유비대용량", "5/4", "C540"),
    ("유비대용량", "5/5", "C550"), ("유비대용량", "5/6", "C560"), ("유비대용량", "5/7", "C570"), ("유비대용량", "5/8", "C580"),
    ("유비대용량", "8/1", "C810"), ("유비대용량", "8/2", "C820"), ("유비대용량", "8/3", "C830"), ("유비대용량", "8/4", "C840"),
    ("유비대용량", "8/5", "C850"), ("유비대용량", "8/6", "C860"), ("유비대용량", "8/7", "C870"), ("유비대용량", "8/8", "C880"),
    ("유비대용량", "9/1", "C910"), ("유비대용량", "9/2", "C920"), ("유비대용량", "9/3", "C930"), ("유비대용량", "9/4", "C940"),
    ("유비대용량", "9/5", "C950"), ("유비대용량", "9/6", "C960"), ("유비대용량", "9/7", "C970"), ("유비대용량", "9/8", "C980"),
    ("유비대용량", "10/1", "CA10"), ("유비대용량", "10/2", "CA20"), ("유비대용량", "10/3", "CA30"), ("유비대용량", "10/4", "CA40"),
    ("유비대용량", "10/5", "CA50"), ("유비대용량", "10/6", "CA60"), ("유비대용량", "10/7", "CA70"), ("유비대용량", "10/8", "CA80"),
    ("유비대용량", "11/1", "CB10"), ("유비대용량", "11/2", "CB20"), ("유비대용량", "11/3", "CB30"), ("유비대용량", "11/4", "CB40"),
    ("유비대용량", "11/5", "CB50"), ("유비대용량", "11/6", "CB60"), ("유비대용량", "11/7", "CB70"), ("유비대용량", "11/8", "CB80"),
    ("유비대용량", "12/1", "CC10"), ("유비대용량", "12/2", "CC20"), ("유비대용량", "12/3", "CC30"), ("유비대용량", "12/4", "CC40"),
    ("유비대용량", "12/5", "CC50"), ("유비대용량", "12/6", "CC60"), ("유비대용량", "12/7", "CC70"), ("유비대용량", "12/8", "CC80"),
    ("동원소용량", "1/1", "J010"), ("동원소용량", "1/2", "J020"), ("동원소용량", "1/3", "J030"), ("동원소용량", "1/4", "J040"),
    ("동원소용량", "2/1", "J050"), ("동원소용량", "2/2", "J060"), ("동원소용량", "2/3", "J070"), ("동원소용량", "2/4", "J080"),
    ("동원소용량", "3/1", "J090"), ("동원소용량", "3/2", "J100"), ("동원소용량", "3/3", "J110"), ("동원소용량", "3/4", "J120"),
    ("동원소용량", "5/1", "J130"), ("동원소용량", "5/2", "J140"), ("동원소용량", "5/3", "J150"), ("동원소용량", "5/4", "J160"),
    ("동원소용량", "6/1", "J170"), ("동원소용량", "6/2", "J180"), ("동원소용량", "6/3", "J190"), ("동원소용량", "6/4", "J200"),
    ("동원대용량", "1/1", "C110"), ("동원대용량", "1/2", "C120"), ("동원대용량", "1/3", "C130"), ("동원대용량", "1/4", "C140"),
    ("동원대용량", "1/5", "C150"), ("동원대용량", "1/6", "C160"), ("동원대용량", "1/7", "C170"), ("동원대용량", "1/8", "C180"),
    ("동원대용량", "2/1", "C210"), ("동원대용량", "2/2", "C220"), ("동원대용량", "2/3", "C230"), ("동원대용량", "2/4", "C240"),
    ("동원대용량", "2/5", "C250"), ("동원대용량", "2/6", "C260"), ("동원대용량", "2/7", "C270"), ("동원대용량", "2/8", "C280"),
    ("동원대용량", "3/1", "C310"), ("동원대용량", "3/2", "C320"), ("동원대용량", "3/3", "C330"), ("동원대용량", "3/4", "C340"),
    ("동원대용량", "3/5", "C350"), ("동원대용량", "3/6", "C360"), ("동원대용량", "3/7", "C370"), ("동원대용량", "3/8", "C380"),
    ("동원대용량", "4/1", "C410"), ("동원대용량", "4/2", "C420"), ("동원대용량", "4/3", "C430"), ("동원대용량", "4/4", "C440"),
    ("동원대용량", "4/5", "C450"), ("동원대용량", "4/6", "C460"), ("동원대용량", "4/7", "C470"), ("동원대용량", "4/8", "C480"),
    ("동원대용량", "5/1", "C510"), ("동원대용량", "5/2", "C520"), ("동원대용량", "5/3", "C530"), ("동원대용량", "5/4", "C540"),
    ("동원대용량", "5/5", "C550"), ("동원대용량", "5/6", "C560"), ("동원대용량", "5/7", "C570"), ("동원대용량", "5/8", "C580"),
    ("동원대용량", "6/1", "C610"), ("동원대용량", "6/2", "C620"), ("동원대용량", "6/3", "C630"), ("동원대용량", "6/4", "C640"),
    ("동원대용량", "6/5", "C650"), ("동원대용량", "6/6", "C660"), ("동원대용량", "6/7", "C670"), ("동원대용량", "6/8", "C680"),
    ("동원대용량", "9/1", "C910"), ("동원대용량", "9/2", "C920"), ("동원대용량", "9/3", "C930"), ("동원대용량", "9/4", "C940"),
    ("동원대용량", "9/5", "C950"), ("동원대용량", "9/6", "C960"), ("동원대용량", "9/7", "C970"), ("동원대용량", "9/8", "C980"),
    ("동원대용량", "10/1", "CA10"), ("동원대용량", "10/2", "CA20"), ("동원대용량", "10/3", "CA30"), ("동원대용량", "10/4", "CA40"),
    ("동원대용량", "10/5", "CA50"), ("동원대용량", "10/6", "CA60"), ("동원대용량", "10/7", "CA70"), ("동원대용량", "10/8", "CA80"),
    ("동원대용량", "11/1", "CB10"), ("동원대용량", "11/2", "CB20"), ("동원대용량", "11/3", "CB30"), ("동원대용량", "11/4", "CB40"),
    ("동원대용량", "11/5", "CB50"), ("동원대용량", "11/6", "CB60"), ("동원대용량", "11/7", "CB70"), ("동원대용량", "11/8", "CB80"),
    ("동원대용량", "12/1", "CC10"), ("동원대용량", "12/2", "CC20"), ("동원대용량", "12/3", "CC30"), ("동원대용량", "12/4", "CC40"),
    ("동원대용량", "12/5", "CC50"), ("동원대용량", "12/6", "CC60"), ("동원대용량", "12/7", "CC70"), ("동원대용량", "12/8", "CC80")
    ]
    

    # DataFrame으로 데이터 변환
    df = pd.DataFrame(data, columns=["OLT", "SP", "1차RN"])

    # Streamlit 앱 제목
    st.header("OLT 선택")

    # 사용자가 OLT를 선택하도록 선택 상자 생성
    olt_options = sorted(df["OLT"].unique())
    selected_olt = st.selectbox("OLT 선택:", olt_options)

    # 선택된 OLT에 해당하는 데이터 필터링
    filtered_df = df[df["OLT"] == selected_olt][["SP", "1차RN"]]
    #filtered_df = df[["SP", "1차RN"]]

    # 필터링된 결과 표시
    #st.write(f"선택된 OLT: {selected_olt}")
    st.write("SP와 1차RN 목록:")
    st.dataframe(filtered_df)

elif menu == "L2 Check":
    st.header("L2 Check")

    commands_dasan = [
        "admin/vertex25",
        "default / bridge",
        "sh mac | inc Total",
        "sh ip dhcp sno bin | inc Total",
        "sh ip igmp sno tab | inc Total",
        "sh port status",
        "sh port statistics avg-pps",
        "sh port statistics rmon",
        "sh rate",
        "sh max-hosts ",
        "sh cable-length",
        "--- ip/route check ---",
        "sh ip int bri",
        "sh ip route",
        "--- L2 diag ---",
        "show syslog local non-volatile r | include fail",
        "show syslog local non-volatile r | include FAIL",
        "show syslog local non-volatile r | include Start UP",
        "show port statistics rmon | include CRC",
        "sh sysl l n r",
        "--- modem reset ---",
        "(config/cpe)#cpe reset 1-24",
        
        "--- port description ---",
        "sh port desc",
        "(bridge)# port description 24 " ,
        
        "--- conf t ---",
        "bridge",
        "port ena 1-24",
        "rate-limit port 1-24 rate 1000000 ingress dot3x",
        "rate-limit port 1-24 rate 1000000 egress",
        "rate-limit port 1-24 rate 520000 ingress dot3x",
        "rate-limit port 1-24 rate 520000 egress",
        "rate-limit port 1-24 rate 104000 ingress dot3x",
        "rate-limit port 1-24 rate 104000 egress"
    ]

    commands_yubi = [
        "root / premier",
        "vlan1 / range port",
        "sh mac | inc total",
        "sh ip dhcp sno bin | inc total",
        "sh ip igmp sno tab gro | inc total",
        "sh port status",
        "sh port statistics avg type",
        "sh port statistics rmon",
        "sh rate",
        "sh max-hosts",
        "sh port phy-diag",
        "--- L2 diag ---",
        "sh logg back | inc gi1",
        "sh port status",
        "sh rmon statistics gi1",
        "sh self-loop-detection", 
        "clear counters gi1",
        "--- ip/route check ---",
        "sh ip int bri",
        "sh ip route",
        "--- modem reset ---",
        "(config-range-port)#cpe reset gi1-24",
        "--- port description ---",
        "(config-if-gi12)# description XXXX_uplink"
        "--- Barcode System ---",
        "sh bar",
        "barcode system K912144500027470",
        
        "--- conf t ---",
        "username root password mos119!",
        "enable password mos119!",
        "range port",
        "no shutdown gi1-24",
        "rate-limit ingress 999999 gi1-24",
        "rate-limit egress 999999 gi1-24",
        "interface gi1"
    ]

    commands_multiroom = [
        "TIE / 멀티룸팩",
        "5G-GES Sxxxxxxx",
        "UTP4 Gxxxxxxx",
        "UTP2 GxxxUxxx",
        "Extender연결 GxxxBxxx",
        "UTP2 10G업링크 GxxxXxxx",
        "통합형 GxxxLxxx",
        "10G업링크멀티룸 GxxxKxxx",
        "중계용 GxxxTxxx",
        "WIFI GxxxWxxx",
        "1:8 H 업링크 9/18/24",
        "1:5 N 업링크 6/12/18/24",
        "1:3 M 업링크 4/8/12/16/20/24",
        "range port",
        "switchport access vlan 2 gi7-12",
        "switchport access vlan 3 gi13-18",
        "switchport access vlan 4 gi19-24",
        "mac-count 8 gi1-5, gi7-11, gi13-17, gi19-23",
        "flow-control on tx-rx gi6, gi12, gi18, gi24",
        "cpu-mac-filter enable gi1-5, gi7-11, gi13-17, gi19-23",
        "traffic-control pps unicast inbound 20000 10000 block-mode gi1-5, gi7-11, gi13-17, gi19-23",
        "traffic-control pps multicast inbound 300 50 block-mode gi1-5, gi7-11, gi13-17, gi19-23",
        "traffic-control pps broadcast inbound 100 50 block-mode gi1-5, gi7-11, gi13-17, gi19-23",
        "filter dhcp gi1-5, gi7-11, gi13-17, gi19-23",
        "filter netbios gi1-24",
        "igmp-trap gi1-24",
        "self-loop-detection system gi1-5, gi7-11, gi13-17, gi19-23",
        "ip igmp snoop-filter 1 gi1-5, gi7-11, gi13-17, gi19-23",
        "ip arp inspection arp-trap-forward gi1-5, gi7-11, gi13-17, gi19-23"
    ]

    commands_L2Log = [
        "show syslog local non-volatile r | include him",
        "show syslog local non-volatile r | include Oops",
        "show syslog local non-volatile r | include Internal error",
        "show syslog local non-volatile r | include SMP ARM", 
        "show syslog local non-volatile r | include Call",
        "show syslog local non-volatile r | include call",
        "show syslog local non-volatile r | include kernel",
        "show syslog local non-volatile r | include Kernel",
        "show syslog local non-volatile r | include KERNEL",
        "show syslog local non-volatile r | include memory",
        "show syslog local non-volatile r | include fail",
        "show syslog local non-volatile r | include FAIL",
        "show syslog local non-volatile r | include Start UP",
        "show port statistics rmon | include CRC"
    ]

    # Display the commands for each device
    st.write("■ 다산 L2 ---")
    for cmd in commands_dasan:
        st.write(cmd)

    st.write("\n")  # Add a new line for separation

    st.write("■ 유비 L2 ---")
    for cmd in commands_yubi:
        st.write(cmd) 

    st.write("■ Multiroom ---")
    for cmd in commands_multiroom:
        st.write(cmd) 

    st.write("■ L2 Log ---")
    for cmd in commands_L2Log:
        st.write(cmd)



elif menu == "IP SETTING":
    st.header("■ IP SETTING")

    # 장비 모델 선택을 위한 드롭다운 메뉴
    model = st.selectbox("장비 모델을 선택하세요", ["U3024B", "E5624R", "MVD10024", "V5972", "V2724GB", "V2708GA", "V3024V", "V5124F"], key="model")

    # 서브넷 마스크와 CIDR 형식 대응표를 화면에 표시
    st.subheader("-서브넷 마스크")
    st.markdown("""\
    /24 : 255.255.255.0  
    /25 : 255.255.255.128  
    /26 : 255.255.255.192  
    /27 : 255.255.255.224  
    /28 : 255.255.255.240  
    /29 : 255.255.255.248  
    /30 : 255.255.255.252  
    """)

    # 새로운 IP, 서브넷 마스크, 게이트웨이 입력 필드
    st.subheader("- 신규IP")
    col1, col2, col3 = st.columns(3)

    with col1:
        ip_address = st.text_input("신규IP", key="new_ip")

    with col2:
        if model in ["U3024B", "E5624R", "V5972", "V2724GB", "V2708GA", "V3024V", "V5124F"]:
            cidr = st.selectbox("신규S/M (CIDR)", ["/24", "/25", "/26", "/27", "/28", "/29", "/30"], key="new_cidr")
        else:
            subnet_mask = st.text_input("신규S/M", key="new_subnet_mask")

    with col3:
        gateway = st.text_input("신규GW", key="new_gateway")

    # 기존 IP, 서브넷 마스크, 게이트웨이 입력 필드
    st.subheader("- 기존IP ")
    col4, col5, col6 = st.columns(3)

    with col4:
        old_ip_address = st.text_input("기존 IP", key="old_ip")

    with col5:
        if model in ["U3024B", "E5624R", "V5972", "V2724GB", "V2708GA", "V3024V", "V5124F"]:
            old_cidr = st.selectbox("기존S/M (CIDR)", ["/24", "/25", "/26", "/27", "/28", "/29", "/30"], key="old_cidr")
        else:
            old_subnet_mask = st.text_input("기존 S/M", key="old_subnet_mask")

    with col6:
        old_gateway = st.text_input("기존GW", key="old_gateway")

    # 버튼 클릭 시 설정 텍스트 출력
    if st.button("설정 저장"):
        if ip_address and gateway:
             # config_text 변수를 초기화합니다.
            config_text = ""
            if model == "U3024B":
                config_text += "[U3024B]\n\n"
                config_text += "conf t\n"
                config_text += f"int vlan1\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "exit\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip default-gateway {old_gateway}\n"
                config_text += f"ip default-gateway {gateway}\n"
                config_text += "exit\n"
                config_text += "wr m\n"
            
            elif model == "E5624R":
                config_text += "[E5624R]\n\n"
                config_text += "conf t\n"
                config_text += "int vlan1\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += "no ip dhcp\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "exit\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip default-gateway {old_gateway}\n"
                config_text += f"ip default-gateway {gateway}\n"
                config_text += "exit\n"
                config_text += "wr m\n"

            elif model == "MVD10024":
                config_text += "[MVD10024]\n\n"
                config_text += "conf t\n"
                config_text += "int vlan1\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address} {old_subnet_mask}\n"
                config_text += f"ip address {ip_address} {subnet_mask}\n"
                config_text += "exit\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0 0.0.0.0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0 0.0.0.0 {gateway}\n"
                config_text += "exit\n"
                config_text += "wr m\n"

            elif model == "V5972":
                config_text += "[V5972]\n\n"
                config_text += "conf t\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0/0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0/0 {gateway}\n"
                config_text += "int br1\n"
                config_text += "no shutdown\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "end\n"
                config_text += "wr m\n"

            elif model == "V2724GB":
                config_text += "[V2724GB]\n\n"
                config_text += "conf t\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0/0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0/0 {gateway}\n"
                config_text += "int default\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr} pri\n"
                config_text += "end\n"
                config_text += "wr m\n"

            elif model == "V2708GA":
                config_text += "[V2708GA]\n\n"
                config_text += "conf t\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0 0.0.0.0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0 0.0.0.0 {gateway}\n"
                config_text += "int mgmt\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "end\n"
                config_text += "wr m\n"

            elif model == "V3024V":
                config_text += "[V3024V]\n\n"
                config_text += "conf t\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0 0.0.0.0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0 0.0.0.0 {gateway}\n"
                config_text += "int vlan1\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "end\n"
                config_text += "wr m\n"

            elif model == "V5124F":
                config_text += "[V5124F]\n\n"
                config_text += "conf t\n"
                if old_gateway:  # 기존 gw 입력이 있을 경우
                    config_text += f"no ip route 0.0.0.0 0.0.0.0 {old_gateway}\n"
                config_text += f"ip route 0.0.0.0/0 {gateway}\n"
                config_text += "int bridge\n"
                config_text += "set port nego 25-26 off\n"
                config_text += "exit\n"
                config_text += "int br2\n"
                if old_ip_address:  # 기존 IP 입력이 있을 경우
                    config_text += f"no ip address {old_ip_address}{old_cidr}\n"
                config_text += f"ip address {ip_address}{cidr}\n"
                config_text += "end\n"
                config_text += "wr m\n"
            
            st.code(config_text)
        else:
            st.error("IP 주소, 서브넷 마스크, 게이트웨이를 모두 입력해주세요.")

    # 이미지 URL
    image_url = "https://github.com/kwakcb/ggag/blob/main/ip_band.png?raw=true"

    # 이미지 표시
    st.image(image_url, caption="IP BAND 이미지", use_column_width=True)

elif menu == "OPR":
    st.header("OPR")

    
    st.text("[OPR]\n\n"
            "admin/enter/ en\n\n"
            "V5204# sh onu service-info\n"
            "V5204# sh olt mac epon 0/1\n"
            "V5204# sh mac address-table\n"
            "V5204# sh arp\n"
            "V5204# sh ip dhcp snoop bin\n"
            "V5204# sh ip igmp snoop gro\n"
            "V5204# sh int statistics avg-type\n"
            "V5204# ping 168.126.63.1\n\n"
            "ONT ERASE\n"
            "conf t\n"
            "int epon 0/1\n"
            "no onu 1-64\n\n"
            "ONT RESET\n"
            "conf t\n"
            "int epon 0/1\n"
            "onu reset 1-64")


elif menu == "10G":
    st.header("[NOC_10G[용량확대]]")

    st.text("-PING : 1G, 10G\n"
            "-SDN\n"
            " .사전작업[변경IP입력]\n"
            " .10G MODULE CHANGE\n"
            " .사후작업[기존IP삭제]\n"
            "-NEOSS 수정 : L2 TIE, IP, FTTH-RN\n"
            "-CPE RESET\n"
            " .UBI : (CONFIG-RANGE-PORT)#cpe reset gi1-24\n"
            " .DANSAN : (CONFIG/CPE)#cpe reset 1-24\n"
            "ip dhcp snoop bind \n\n"
            "-NMS LINK UPDATE\n"
            "-공사정보 등록 확인\n"
            "-10G OPTIC LEVEL : -11~ -18 DB\n"
            "-5G 속도측정 : 모뎀4번포트에 고정IP\n\n")

elif menu == "ftp긴급복구":
    st.header("ftp긴급복구")

    st.text("[유비]-워드패드로 편집\n"
            "#copy ftp config\n"
            "#ftp server ip : a.b.c.d\n"
            "#user : noc\n"
            "#pass : 1\n"
            "#source ip : 장비ip\n"
            "#dest : start.cfg\n\n"
            "[다산]-메모장으로 편집\n"
            "#copy ftp config download : start.cfg\n"
            "#ftp server ip : a.b.c.d\n"
            "#download file : 장비ip.cfg\n"
            "#user : noc\n"
            "#pass : 1\n")
            
elif menu == "U4224B_SDN":
    st.header("U4224B_SDN")

    st.text("R114[X]->R104[O]\n"
            "#sh flash\n"
            "#boot system os1 U4200.r104\n"
            "#erase os1 U4200.r104\n"
            "#copy ftp os1\n"
            "#ip : 59.27.68.120\n\n"
            "#id : noc\n"
            "#password : 1\n"
            "#Source : U4200.r104\n"
            "#Dest : U4200.r104\n\n"
           
            "#copy ftp config\n"
            "#ip : 59.27.68.120\n"
            "#id : noc\n"
            "#password : 1\n"
            "#Source : 장비ip.cfg\n"
            "#Dest : str.cfg\n"
            "#boot config str.cfg\n"
            "#boot system os1 U4200.r114\n")
            
elif menu == "각종일지":
    st.header("각종일지")
    
    # 고장 특이사항 입력란 (다중라인 입력 허용)
    #st.subheader("고장 특이사항")
    fault_info = st.text_area("■ 고장 특이사항을 입력하세요.", value=st.session_state.fault_info, height=200)
    
    # 출동 특이사항 입력란 (다중라인 입력 허용)
    #st.subheader("출동 특이사항")
    dispatch_info = st.text_area("■ 출동 특이사항을 입력하세요.", value=st.session_state.dispatch_info, height=200)
    
    # 저장 버튼
    if st.button("저장"):
        # 입력된 데이터를 세션 상태에 저장
        st.session_state.fault_info = fault_info
        st.session_state.dispatch_info = dispatch_info
        
        st.success("일지가 성공적으로 저장되었습니다.")
    
    # 이전에 입력된 내용을 출력
    #st.write("이전 고장 특이사항:", st.session_state.fault_info)
    #st.write("이전 출동 특이사항:", st.session_state.dispatch_info)

    
    st.text("[일일본부일지]\n"
            "*NMS-고장감시(TT)-고장이력\n"
            ".도메인:ACCESS\n"
            ".시작(종료)날짜:당일\n"
            ".부서:해당본부\n"
            ".상태:전체\n"
            ".종류:전체\n"
            ".분야1:6액세스\n"
            ".분야2:L2\n"
            ".고장:고장\n"
            "엑셀저장: 국사부터 조치2까지 복.붙\n"
            "*공사정보\n"
            "*NMS-작업통제-대시보드\n"
            ".해당본부 총건수 - 주요공사만 추출\n"
            "*BS\n"
            "-고장상황 일일 처리건 엑셀저장 후 - 엑셀에서 BS_COUNT시트에서 BS통계 추출 후 복.붙\n\n"

            "[야근네트워크일지]\n"
            "-전일 네트워크 현황보고(유선) 엑셀\n"
            "1.NMS-고장상황\n"
            "-ACCESS:고장상황(MOSS)\n"
            ".조직:충호부대제주\n"
            ".기간:전일18:00~금일09:00\n"
            ".상태:전체\n"
            ".작업분야:6액세스\n"
            "검색-엑셀저장-전체복.붙\n"
            "2.NMS-장애경보이력\n"
            ".시설분류: 가입자수용스위치-XDSL, NTOPIA\n"
            ".조직:충호부대제주\n"
            ".경보원인 : Ping\n"
            ".조회기간 : 전일18:00~금일 09:00\n"
            ".엑셀 저장\n"
            ".전체 복. 붙\n"
            "3.NMS-작업통제-대시보드\n"
            "4.전일 날짜 수정 -> 통계\n" 
            "엑셀->워드에 선택붙여넣기(CTRL+SHIFT+V)/RTF로 붙여넣기[소계는 복붙안하셔도 됨)\n"
            "5.특이사항 :\n" 
            ".기상(낙뢰,태풍,소나기,강우[강설]등 재해재난, 장비[케이블]장애, 공사피해\n"
            ".전주 실적이랑 비교 특이하게 차이가 나는 부분 찾아서 기재\n")