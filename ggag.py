import streamlit as st
import streamlit.components.v1 as components
import json
import webbrowser
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

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
    ("KWAK[용서_연민_사랑]", "고장상황", "MOSS_Copy", "OLT광3종", "OLT Check", "OLT_1stRN", "L2 Check", "IP SETTING", "SDN_L2_YESNO"  ,"OPR", "10G","ftp긴급복구","U4224B_SDN","각종일지","TV_ch","인터넷상품")
)

if menu == "KWAK[용서_연민_사랑]":
    st.title("""■ Memo
-전원분야 고장성 경보 범위-\n
[한전정전] [차단기OFF] [변압기 고장] [국사 화재] [국사 침수]\n
-네트워트 현황보고-\n
[MOSS 항목] 전원,교환,액세스\n
[PING경보] ACCESS_XDSL,엔토피아\n
[공사정보] 작업통제_대쉬보드 총건수_1000/page설정_ 작업현황 전체복사 후 A2셀에 주변서식에 맟추기 붙여넣기\n
-동명 국사 : 구미공단국사 / 광주하남국사 / 부산강서국사 / 울산성남국사 / 충북영동국사\n 
-엑셀 체크표시 없애기 : A열선택 -> F5+옵션+개체 + DEL\n\n


■ 유관기관 연락처\n
-OSP 관제센터: 02-500-6150\n
-IP망 관제센터: 042-478-1600\n
-전원관제: 042-478-1800\n
-과천 제1관제센터(교환): 02-500-6080\n
-무선: 042-489-6831\n
-NOC:1577-7315\n
-교환기술부\n
.충: 042-255-2470\n
.호: 062-513-1200\n
.부: 051-464-4699\n
.대: 053-477-3010\n\n

-분기국사출입문(전원)\n
.충: 042-478-7550, 7540\n
.호: 062-230-3355\n
.부: 051-464-2300\n
.대: 053-477-1985 \n\n

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
    # ======================================================================================================
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
    #==================================================================================================
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


   


    # Streamlit 애플리케이션 제목 설정
    st.header("■ 어댑터 교체")

    # 두 개의 입력 필드 생성
    before_adapter = st.text_input("전_어댑터")
    after_adapter = st.text_input("후_어댑터")

    # 현재 날짜 가져오기
    current_date = datetime.now().strftime("%Y년 %m월 %d일")
    # 어댑터 교체 출력 버튼 생성
    if st.button("어댑터 출력"):
        if before_adapter and after_adapter:
            output = f"[{current_date}] 어댑터 {before_adapter} > {after_adapter}"
            st.write(output)
        
            # 복사 버튼과 HTML 코드 추가
            #copy_script = f"""
            #<div>
             #   <textarea id="outputText" style="width: 100%;">{output}</textarea>
             #   <button onclick="navigator.clipboard.writeText(document.getElementById('outputText').value)">복사</button>
            #</div>
            #"""
            #components.html(copy_script, height=100)
        else:
            st.write("모든 입력 필드를 채워주세요.")

    # 스티커 부착 섹션
    st.header("■ 스티커 부착")

    # 두 개의 숫자 입력 필드 생성
    namecard_type = st.number_input("명함형 입력", min_value=0, max_value=100)
    sticker_type = st.number_input("스티커형 입력", min_value=0, max_value=100)

    # 스티커 부착 출력 버튼 생성
    if st.button("스티커 출력"):
        if namecard_type > 0 and sticker_type > 0:
            output = f"[{current_date}] 명함형: {namecard_type}, 스티커형: {sticker_type}"
            st.write(output)
        elif namecard_type > 0:
            output = f"[{current_date}] 명함형: {namecard_type}"
            st.write(output)
        elif sticker_type > 0:
            output = f"[{current_date}] 스티커형: {sticker_type}"
            st.write(output)
    else:
        # 모든 값이 0일 때는 출력하지 않음
        st.write("숫자가 0보다 큰 값을 입력하세요.")

    
elif menu == "MOSS_Copy":
    st.header("■ MOSS_Copy")
    
    # 코드 블록을 표시합니다
    st.code("DB 현행화 중...")
    st.code("Link 현행화 중...")
    st.code("★ 장비교체 NeOSS, NMS, SDN 현행화 완료")
    st.code("★ 상황전파 수정요청")
    st.code("★ 안전작업[차량 안전운전] 하시기 바랍니다.")
    st.code("★ Follower추가")
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
                f"(U9024A)#sh pon onu ddm {user_input2}",
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
    st.header("■ OLT Check")
    
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
        "sh ip interface brief\n" 
        "sh port status ethernet 3/1\n"
        "sh onu ddm epon 1/1\n"
        "sh olt rssi-info epon 1/1\n"
        "sh olt statistics epon 1/1\n"
        "sh olt statistics onu epon 1/1\n"
        "sh arp | inc 183.106.186.23\n"
        "sh olt mac epon 1/1 | inc 183.106.186.23\n\n"
        "[다산 L3 V5124F]\n"
        "sh run grep ip\n"
        "conf t\n"
        "arp access-list kt\n"
        "no permit ip 121.148.73.251 mac 00:07:70:96:af:96\n"
        "permit ip 121.148.73.251 mac any\n")
    
    

elif menu == "OLT_1stRN":
    st.header("■ OLT_1차RN")
    
    # 데이터 정의 (유비중용량과 다산중용량 데이터가 포함됨)
    data = [
    ("다산중용량", "1/1", "C110"), ("다산중용량", "1/2", "C120"), ("다산중용량", "1/3", "C130"), ("다산중용량", "1/4", "C140"),
    ("다산중용량", "1/5", "C150"), ("다산중용량", "1/6", "C160"), ("다산중용량", "1/7", "C170"), ("다산중용량", "1/8", "C180"),
    ("다산중용량", "1/9", "C190"), ("다산중용량", "1/10", "C1A0"), ("다산중용량", "1/11", "C1B0"), ("다산중용량", "1/12", "C1C0"),
    ("다산중용량", "1/13", "C1D0"), ("다산중용량", "1/14", "C1E0"), ("다산중용량", "1/15", "C1F0"), ("다산중용량", "1/16", "C1G0"),
    ("다산중용량", "2/1", "C210"), ("다산중용량", "2/2", "C220"), ("다산중용량", "2/3", "C230"), ("다산중용량", "2/4", "C240"),
    ("다산중용량", "2/5", "C250"), ("다산중용량", "2/6", "C260"), ("다산중용량", "2/7", "C270"), ("다산중용량", "2/8", "C280"),
    ("다산중용량", "2/9", "C290"), ("다산중용량", "2/10", "C2A0"), ("다산중용량", "2/11", "C2B0"), ("다산중용량", "2/12", "C2C0"),
    ("다산중용량", "2/13", "C2D0"), ("다산중용량", "2/14", "C2E0"), ("다산중용량", "2/15", "C2F0"), ("다산중용량", "2/16", "C2G0"),
    ("유비소용량", "1/1", "J010"), ("유비소용량", "1/2", "J020"), ("유비소용량", "2/1", "J030"), ("유비소용량", "2/2", "J040"),
    ("유비소용량", "3/1", "J050"), ("유비소용량", "3/2", "J060"), ("유비소용량", "4/1", "J070"), ("유비소용량", "4/2", "J080"),
    ("유비소용량", "5/1", "J090"), ("유비소용량", "5/2", "J100"), ("유비소용량", "6/1", "J110"), ("유비소용량", "6/2", "J120"),
    ("유비소용량", "7/1", "J130"), ("유비소용량", "7/2", "J140"), ("유비소용량", "8/1", "J150"), ("유비소용량", "8/2", "J160"),
    ("유비소용량", "9/1", "J170"), ("유비소용량", "9/2", "J180"), ("유비소용량", "10/1", "J190"), ("유비소용량", "10/2", "J200"),
    ("유비중용량", "3/1", "C310"), ("유비중용량", "3/2", "C320"), ("유비중용량", "3/3", "C330"), ("유비중용량", "3/4", "C340"),
    ("유비중용량", "3/5", "C350"), ("유비중용량", "3/6", "C360"), ("유비중용량", "3/7", "C370"), ("유비중용량", "3/8", "C380"),
    ("유비중용량", "3/9", "C390"), ("유비중용량", "3/10", "C3A0"), ("유비중용량", "3/11", "C3B0"), ("유비중용량", "3/12", "C3C0"),
    ("유비중용량", "3/13", "C3D0"), ("유비중용량", "3/14", "C3E0"), ("유비중용량", "3/15", "C3F0"), ("유비중용량", "3/16", "C3G0"),
    ("유비중용량", "4/1", "C410"), ("유비중용량", "4/2", "C420"), ("유비중용량", "4/3", "C430"), ("유비중용량", "4/4", "C440"),
    ("유비중용량", "4/5", "C450"), ("유비중용량", "4/6", "C460"), ("유비중용량", "4/7", "C470"), ("유비중용량", "4/8", "C480"),
    ("유비중용량", "4/9", "C490"), ("유비중용량", "4/10", "C4A0"), ("유비중용량", "4/11", "C4B0"), ("유비중용량", "4/12", "C4C0"),
    ("유비중용량", "4/13", "C4D0"), ("유비중용량", "4/14", "C4E0"), ("유비중용량", "4/15", "C4F0"), ("유비중용량", "4/16", "C4G0"),
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

    # 필터링된 결과 표시
    st.write("SP와 1차RN 목록:")
    st.dataframe(filtered_df)

elif menu == "L2 Check":
    st.header("■ L2 Check")

    commands_dasan = [
        "admin/vertex25",
        "default / bridge",
        "--- ip/route check ---",
        "sh ip int bri",
        "sh ip route",
        "sh ip default",
        "--- no ip address ---",
        "int default",
        "no ip address dhcp",
        "ip address a.b.c.d/m",
        "--- V2924GB ---",
        "(config)#passwd",
        "(config)#passwd ena xxxx",
        "--- V3024V ---",
        "range-interface",
        "int ethernet 0/1",
        "int vlan 1",
        "--- L2 diag ---",
        "sh mac | inc Total",
        "sh ip dhcp sno bin | inc Total",
        "sh ip igmp sno tab | inc Total",
        "sh port status",
        "sh port statistics avg-pps",
        "sh port statistics rmon",
        "sh rate",
        "sh max-hosts ",
        "sh cable-length",
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
        "--- ip/route check ---",
        "sh ip int bri",
        "sh ip route",
        "--- L2 diag ---",
        "sh mac | inc total",
        "sh ip dhcp sno bin | inc total",
        "sh ip igmp sno tab gro | inc total",
        "sh port status",
        "sh port statistics avg type",
        "sh port statistics rmon",
        "sh rate",
        "sh max-hosts",
        "sh port phy-diag",
        "sh logg back | inc gi1",
        "sh rmon statistics gi1",
        "sh self-loop-detection", 
        "clear counters gi1",
        "--- modem reset ---",
        "(config-range-port)#cpe reset gi1-24",
        "--- port description ---",
        "(config-if-gi12)# description XXXX_uplink"
        "--- Barcode System ---",
        "sh bar",
        "barcode system K912144500027470",
        "barcode system MDSM~",
        "--- conf t ---",
        "username root password mos119!",
        "enable password mos119!",
        "range port",
        "no shutdown gi1-24",
        "rate-limit ingress 999999 gi1-24",
        "rate-limit egress 999999 gi1-24",
        "interface gi1"
    ]

    commands_MVD10024 = [
        "admin/password",
        "sh syslog local volate 100",
        "config/vdsl/",
        "sh status 1-24",
        "sh counter 1",
        "sh cpestatus",
        "portdisable/portenable/portreset/cpereset/counterclear 1",
        "sh physicalline 1"
    ]

    commands_DX6524 = [
        ">pm",
        "ip if delete bridge",
        "ip if add bridge 10.0.0.2 10.0.0.1 255.255.255.0",
        "pass",
        "pmpass pass",
        "wr",
        "sr...y",
        "ut",
        "sl show",
        "help[home",
        "su 초기설정",
        "chips$spm show",
        "chips$spm x enable[disable]",
        "chips$spm x 8160[4000] 640 ",
        "chips$ai x",
        "chips$cs all",
        "bridge$ pom",
        "bridge$ ms",
        "snmp$ac read public",
        "snmp$ac write public"
    ]
    commands_IRT800 = [
        "set-ip:",
        "system:",
        "ping:",
        "chg-pwd:",
        "set-community:",
        "set-unblock:2,1",
        "set-mac:",
        "set-subs:",
        "rtrv-ip",
        "rtrv-mcu",
        "rtrv-community",
        "ping: 168.126.63.1, 5;",
        "rtrv-subs:2,4",
        "rtrv-mac",
        "rtrv-chconf:2,4",
        "rtrv-pm:2,4,5"
    ]
    
    commands_HAMX6000 = [
        "root/",
        "sh mod bridgecfg",
        "ping 168.126.63.1",
        "mod user",
        "show shelf/boad/port",
        "show bridgecfg",
        "show iproute",
        "show community",
        "show dsllink",
        "reset board",
        "restart"
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

    st.write("■ MVD10024 ---")
    for cmd in commands_MVD10024:
        st.write(cmd) 
        
    st.write("■ DX6524 ---")
    for cmd in commands_DX6524:
        st.write(cmd) 
    
    st.write("■ IRT800 ---")
    for cmd in commands_IRT800:
        st.write(cmd) 
    
    st.write("■ HAMX6000 ---")
    for cmd in commands_HAMX6000:
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

elif menu == "SDN_L2_YESNO":
    st.header("■ SDN_L2_YESNO")

# Sample Data
    data = {
    "모델명": [
        "DAS_V27O8GB  [UTP2]", "DAS_V2708GC", "DAS_V2708M  [UTP2]", 
        "DAS_V2716GB  [utp2]", "DAS_Y2716GC", "DAS_V2724GB  [UTP2]", 
        "DAS_V2724GC", "DAS_V2908GB  [UTP2]", "DAS_V2916GB  [UTP2]", 
        "DAS_V2924GB  [UTP2]", "DAS V3024V", "LOC_E5008H",
        "LOC_E5016H", "LOC_E5024H", "LOC_E5608C [UTP2]",
        "LOC_E5608R [UTP2]", "LOC_E5616R [UTP2]", "LOC_E5624B",
        "LOC_E5624R [UTP2]", "LOC_E5924K", "LOC_E5924KE",
        "LOC_U4124B", "LOC_U4224B",
        # ...'불가능'
        "DAS_V1624", "V1724", "VERTEX1124", 
        "V1808", "V1816", "V1816-R4-MD", 
        "V1824", "V1824-R3", "V2808K", 
        "V2708M", "V2716G", "V2724G", 
        "DX6524", "IRT-800", "MFS1024", 
        "MFS2324", "MFS2708", "MFS2716", 
        "MFS2716W", "MFS2724", "MVD10024", 
        "MVD10048", "P3316FG", "P3324FG", 
        "P3516FGD", "P3516FGO", "P3524FG", 
        "P3624FGA", "U3024B", "U3024L", 
        "U3048A", "E5016", "E5024", 
        "EX-1172"
        
    ],
    
    "여부": [
        "가능", "가능", "가능", 
        "가능", "가능", "가능",
        "가능", "가능", "가능",
        "가능", "가능", "가능",
        "가능", "가능", "가능",
        "가능", "가능", "가능",
        "가능", "가능", "가능",
        "가능", "가능",  
        # ...'불가능'
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능", "불가능", "불가능",
        "불가능"
    ]
    }   

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Streamlit App
    #st.header("모델명 입력")

    # User Input
    search_query = st.text_input("Enter the model name :")
    # Search and Display Results
    if search_query:
        search_results = df[df["모델명"].str.contains(search_query, case=False, na=False)]
    
        if not search_results.empty:
            st.write("Search Results:")
            st.table(search_results)
        else:
            st.write("No matching models found.")


elif menu == "OPR":
    st.header("■ OPR")
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
    st.header("■ NOC_10G[용량확대]")

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
    st.header("■ ftp긴급복구")

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
    st.header("■ U4224B_SDN")

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
            "#boot system os1 U4200.r114\n"
            "#4224신규개통\n"
            "#네오스 xdsl장치관리-수용변경에서 4124->4224로\n")
            
elif menu == "각종일지":
    st.header("■ 각종일지")
    
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
            "1.NMS-고장상황\n"
            "-ACCESS:고장상황(MOSS)\n"
            ".조직:충호부대제주\n"
            ".기간:금일07:00~금일18:00\n"
            ".상태:전체\n"
            ".작업분야:전체[L2,OLT,AGW,POWER]\n"
            "2.NMS-장애경보이력\n"
            ".시설분류: 가입자수용스위치-XDSL, NTOPIA\n"
            ".조직:충호부대제주\n"
            ".경보원인 : Ping\n"
            ".조회기간 : 금일07:00~금일 18:00\n"
            ".엑셀 저장\n"
            ".전체 복. 붙\n"
            "3.NMS-고장감시(TT)-고장이력\n"
            ".도메인:ACCESS\n"
            ".시작(종료)날짜:당일\n"
            ".부서:해당본부\n"
            ".상태:전체\n"
            ".종류:전체\n"
            ".분야1:ACCESS\n"
            ".분야2:L2\n"
            ".고장:고장\n"
            "엑셀저장: 국사부터 조치2까지 복.붙\n"
            "4.공사정보\n"
            "*NMS-작업통제-대시보드\n"
            ".해당본부 총건수 - 주요공사만 추출\n"
            "5.BS\n"
            "-고장상황 일일 처리건 엑셀저장 후 - 엑셀에서 BS_COUNT시트에서 BS통계 추출 후 복.붙\n\n"
            "================================================================================="
            "[야근네트워크일지]\n"
            "-전일 네트워크 현황보고(유선) 엑셀\n"
            "1.NMS-고장상황\n"
            "-ACCESS:고장상황(MOSS)\n"
            ".조직:충호부대제주\n"
            ".기간:전일18:00~금일09:00\n"
            ".상태:전체\n"
            ".작업분야:전체\n"
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
    
elif menu == "TV_ch":
    st.header("■ TV")
    st.text("[TV Diag]\n"
        "(olt)#sh ip igmp snooping tab | inc L2ip \n"
        "(L2)#sh ip igmp snooping tab gro\n"
        "sh port statistics avg type\n")
    st.text("[TV channel]\n")


    # 데이터 정의
    data = {
        "Service Name": [
            "MBC 에브리원","ENA","NS홈쇼핑","tvN","롯데홈쇼핑",
            "SBS","CJ ONSTYLE","KBS2","GS SHOP","KBS1",
            "현대홈쇼핑","MBC","KT알파 쇼핑","EBS","홈&쇼핑",
            "JTBC","MBN","SK 스토아","채널A","TV조선",
            "신세계쇼핑","tvN STORY","공영쇼핑","연합뉴스TV","YTN",
            "SBS Biz","OBS","Mnet","GS MY SHOP","ENA DRAMA",
            "쇼핑엔티","MBC 드라마넷","LOTTE OneTV","OCN","W쇼핑",
            "KBS drama","현대홈쇼핑+샵","SBS 플러스","CJ ONSTYLE+","JTBC2",
            "tvN SHOW","KBS joy","NS Shop+","SBS funE","OCN Movies",
            "tvN Drama","드라마큐브","iHQ drama","E채널","시네마천국",
            "디스커버리채널","SPOTV","SPOTV2","IB SPORTS","Sky SPORTS",
            "GOLF&PBA","JTBC Golf","SBS 골프","SBS Sports","KBS N Sports",
            "MBC SPORTS+","JTBC GOLF&SPORTS","tvN SPORTS","SPOTV Golf & Health","KTV",
            "국회방송","SBS F!L","GTV","CNTV","티브이조선2",
            "채널S","FUN TV","ENA STORY","Asia N","하이라이트TV",
            "JTBC4","OCN Movies2","Lifetime","Edge TV","MBC ON",
            "OBS W","동아TV","KBS Story","SmileTV Plus","iHQ",
            "OLIFE","K STAR","ONCE","디원","AsiaM",
            "월드 클래식 무비","아이넷TV","채널이엠","CMCTV","EBS2",
            "Ent.TV","다문화티브이","채널A 플러스","MBN플러스","NBS",
            "스크린","채널차이나","엠플렉스","THE MOVIE","인디필름",
            "씨네프","채널나우","채널J","에이플드라마","중화TV",
            "HQ+","CH.U","AXN","텔레노벨라","채널W",
            "TVasiaPlus","HITS","Eurosport","FTV","FISHING TV",
            "바둑TV","K바둑","캐치온 1","캐치온 2","브레인TV",
            "Billiards TV","마운틴 TV","AfreecaTV","CH.WIDE","STN",
            "생활체육 TV","스크린골프존","COOKTV","STATV","SBS M",
            "MBC M","뉴트로TV","ORFEO","한경arteTV","History",
            "GMTV","가요TV","실버아이TV","이벤트 TV","WeLike",
            "붐TV","아이넷라이프","컬쳐플러스","UXN","Asia UHD",
            "SkyUHD","UMAX","UHDDreamTV","에스비에스필UHD","다큐원",
            "MGTV","KBS LIFE","YTN2","OUN","Real TV",
            "Now 제주TV","9colors","MBCNET","채널i","아리랑TV",
            "하비라이프","내셔널지오그래픽","쿠키건강TV","NatGeo Wild","메디컬TV",
            "BBC Earth","HGTV","Animal Planet","사이언스TV","채널뷰",
            "CCTV4","DSC Science","한국경제 TV","머니투데이방송","매일경제TV",
            "이데일리TV","서울경제TV SEN","토마토증권통","팍스경제TV","연합뉴스경제TV",
            "토마토집통","NHK WP","ABC Australia","CNN Int'l","BBC WN",
            "Euro News","CGTN","Fox News","Bloomberg","CNBC",
            "TV5 Monde","복지TV","DW-TV Asia+","해피독티비","DOGTV",
            "VIKI","미드나잇 채널","플레이보이TV","허니TV","핑크하우스",
            "DesireTV","비너스TV","SPOTV ON 1","SPOTV ON 2","법률방송",
            "tbs TV","헬스메디TV","SPOTV Prime","육아방송","k-net",
            "시니어 TV","소상공인방송","JJC지방자치TV","디마티비","폴라리스TV",
            "가톨릭평화방송","BBS불교방송","BTN불교TV","GOODTV","C채널",
            "CTS 기독교TV","CGNTV","CBS TV","원음방송","YCN유림방송",
            "STB 상생방송","TVCHOSUN3","국악방송","한국직업방송","토마토클래식",
            "WeeTV","BALL TV","슬로우TV","ONT","채널칭",
            "한국승마방송","국방TV","더라이프","통일TV","EKBC",
            "채널숨","한국선거방송","리빙TV","사회안전방송","NBNTV",
            "EBS러닝 중학2","TimeShift","USB","Dog & Mom","최신 인기가요",
            "최신발라드가요","K-POP 아이돌","최신가요 차트 HOT150","트로트가요무대","최신트로트히트",
            "응답하라8090","인기성인가요 HOT300","최신히트팝스","한국인이 사랑한 팝송","다문화음악1",
            "다문화음악2","Black Music","Rock Festival","재즈 라운지","홈클래식",
            "클래식 산책","당신을 위한 발라드","2000년대 인기가요","TV속 화제음악","OST 천국",
            "엄마랑EQ동요","Rainy day","한국발라드명곡770","최신인기댄스&힙합","러브발라드명곡550",
            "스무드재즈","클럽 뮤직","파워스테이션","Cool&Hot","채널키즈랜드",
            "Focus Prime","팝콘티비","왈하우스","팝콘게임","금영TV노래방",
            "콘텐츠이용권","The Red","TJ노래방","Live PPV 1","Live 1",
            "Live PPV 2","Live PPV 3","TV 영화 시사회","일정 알리미","뽀로로TV",
            "지니키즈팝","월정액포털","Live 2","아이쿠노래방","아이챌린지",
            "신비아파트","핑크퐁TV","타요와 신나는 놀이","지니게임","TV에 내폰 연결",
            "My 갤러리","TV운세방","지니뮤직","부싯돌게임","ADch6",
            "야호!번개스쿨","TV체커","KT알파 쇼핑 할인팩","IoT 기기연결","IoT헬스밴드",
            "지니키즈TV","지역소식채널","KBN","엘비엔불교방송","지상파/종편",
            "홈쇼핑","스포츠/레져","영화/시리즈","드라마/여성","애니메이션",
            "유아/교육","오락/음악","뉴스/경제","다큐/교양","지자체 TV",
            "비디오스티칭1","비디오스티칭2","비디오스티칭3","갤러리K","빨리오",
            "종로TV","모닝클래스I","(주)연합방송","Key TV","Hope Channel",
            "STN 방송","모닝클래스S","K-POP","드라마 OST","POP",
            "힐링 사운드","유니베라실시간","국방CUG","예술의 전당","GMB",
            "jBSTV","고객상담채널","4_스카이홈쇼핑","4채널 UHD","4채널_지상파",
            "4채널","4채널_영화","4채널_스포츠","하나은행","쇼핑n혜택",
            "쇼핑_sub1","쇼핑_sub2","사장님TV","씨네호텔","생명의 흐름",
            "GCN","문화예술치유","KBNITV","홈쇼핑 now","홈쇼핑 now2",
            "호텔 CUG","CLive","씨네호텔 플러스","마이클럽","채널 키즈랜드",
            "ZooMoo","드림웍스 채널","신기한나라TV","키즈톡톡플러스","Miao Mi",
            "다빈치러닝","edu TV","EBS플러스2","EBS플러스1","EBS English",
            "플레이런TV","JEI English TV","뽀요TV","CBeebies","브라보키즈",
            "대교 노리Q","Baby TV","EBS KIDS","KBS Kids","캐리TV",
            "JEI재능방송","어린이TV","핑크퐁 채널","부메랑","애니플러스",
            "카툰네트워크","SBS Golf2","애니박스","애니원티비","애니맥스",
            "Tooniverse","Focus Prime","지니 TV 가이드","ENA PLAY"
            ],
        
        "채널번호": [
            "0","1","2","3","4",
            "5","6","7","8","9",
            "10","11","12","13","14",
            "15","16","17","18","19",
            "20","21","22","23","24",
            "25","26","27","28","29",
            "30","31","32","33","34",
            "35","36","37","38","39",
            "40","41","42","43","44",
            "45","46","47","48","49",
            "50","51","52","53","54",
            "55","56","57","58","59",
            "60","61","62","63","64",
            "65","66","67","68","69",
            "70","71","72","73","74",
            "75","76","78","79","80",
            "81","82","83","84","85",
            "86","87","88","89","90",
            "91","92","93","94","95",
            "96","97","98","99","100",
            "101","102","103","104","105",
            "106","107","108","109","110",
            "111","112","113","114","116",
            "117","118","119","120","121",
            "122","123","124","125","126",
            "127","128","129","130","131",
            "132","133","134","135","136",
            "137","138","139","140","141",
            "142","143","144","145","146",
            "147","148","149","150","151",
            "152","153","154","155","156",
            "157","158","159","160","161",
            "162","163","164","165","166",
            "167","168","169","170","171",
            "172","173","174","175","176",
            "177","178","180","181","182",
            "183","184","185","186","187",
            "188","189","190","191","192",
            "193","194","195","196","197",
            "198","199","200","201","202",
            "204","205","206","207","208",
            "209","210","211","212","213",
            "214","215","216","217","221",
            "222","223","224","225","226",
            "231","232","233","234","235",
            "236","237","238","239","240",
            "241","250","251","252","253",
            "254","255","256","257","258",
            "259","260","261","262","263",
            "267","273","276","278","285",
            "306","307","539","609","610",
            "611","612","613","614","615",
            "616","617","618","619","620",
            "621","622","623","624","625",
            "626","627","628","629","630",
            "631","632","633","634","635",
            "636","637","638","639","651",
            "652","701","702","703","706",
            "708","710","712","714","715",
            "718","719","720","721","722",
            "723","724","725","727","729",
            "732","733","738","739","742",
            "743","744","747","750","760",
            "766","776","780","783","784",
            "787","789","801","807","808",
            "809","810","811","812","813",
            "814","815","816","817","820",
            "821","822","823","824","825",
            "828","832","833","835","836",
            "838","842","844","845","846",
            "847","851","853","854","855",
            "856","857","859","860","862",
            "863","864","869","870","874",
            "875","876","879","880","881",
            "882","883","885","894","895",
            "897","898","899","900","960",
            "961","962","965","966","968",
            "969","970","971","972","973",
            "974","975","976","977","980",
            "981","982","983","984","985",
            "986","987","988","989","990",
            "991","992","993","994","995",
            "996","997","998","999"

            ],
        "IP": [
            "233.14.173.121","233.13.231.118","233.18.158.79","233.13.231.132","233.18.158.80",
            "233.15.200.41","233.18.158.58","233.18.158.77","233.18.158.62","233.15.200.19",
            "233.18.158.70","233.15.200.55","233.15.220.101","233.18.158.106","233.15.200.137",
            "233.15.200.147","233.15.200.149","233.15.200.110","233.15.200.146","233.15.200.148",
            "233.18.158.83","233.13.231.134","233.15.220.174","233.15.200.150","233.18.158.78",
            "233.14.173.113","233.15.220.102","233.13.231.133","233.18.158.16","233.15.220.180",
            "233.15.200.92","233.14.173.119","233.18.158.102","233.13.231.121","233.15.200.132",
            "233.14.173.104","233.18.158.29","233.14.173.109","233.15.200.89","233.13.231.55",
            "233.13.231.131","233.14.173.105","233.15.200.214","233.14.173.112","233.13.231.136",
            "233.13.231.104","233.14.173.126","233.14.173.125","233.14.173.124","233.15.220.61",
            "233.15.200.100","233.13.231.2","233.14.173.101","233.14.173.102","233.13.231.124",
            "233.14.173.103","233.15.220.83","233.14.173.111","233.14.173.110","233.14.173.106",
            "233.14.173.123","233.15.220.172","233.13.231.103","233.13.231.97","233.15.200.128",
            "233.18.158.55","233.15.220.69","233.15.200.112","233.18.158.72","233.15.220.179",
            "233.15.200.99","233.13.231.125","233.15.200.116","233.18.158.65","233.15.220.85",
            "233.13.231.83","233.13.231.123","233.13.231.127","233.15.220.11","233.14.173.120",
            "233.18.158.81","233.15.220.177","233.14.173.108","233.13.231.13","233.13.231.100",
            "233.13.231.117","233.14.173.128","233.13.231.21","233.15.220.175","233.18.158.46",
            "233.13.231.72","233.15.220.120","233.13.231.24","233.15.200.113","233.15.220.67",
            "233.15.220.63","233.18.158.13","233.15.200.219","233.13.231.17","233.15.200.217",
            "233.14.173.129","233.13.231.128","233.13.231.126","233.15.220.121","233.18.158.20",
            "233.15.220.77","233.14.173.130","233.15.220.176","233.15.220.64","233.15.220.166",
            "233.18.158.17","233.13.231.81","233.13.231.98","233.15.200.122","233.18.158.93",
            "233.15.220.81","233.15.200.94","233.18.158.85","233.13.231.116","233.15.220.122",
            "233.13.231.143","233.15.220.86","233.13.231.122","233.13.231.75","233.13.231.82",
            "233.15.220.119","233.15.220.173","233.13.231.64","233.13.231.120","233.13.231.114",
            "233.15.220.37","233.13.231.69","233.13.231.68","233.15.200.93","233.14.173.114",
            "233.14.173.122","233.15.220.75","233.13.231.107","233.15.200.127","233.13.231.102",
            "233.15.220.156","233.18.158.33","233.13.231.129","233.18.158.109","233.13.231.145",
            "233.15.220.31","233.15.220.65","233.15.200.97","233.14.173.116","233.15.220.32",
            "233.13.231.18","233.18.158.28","233.18.158.47","233.13.231.78","233.15.200.220",
            "233.15.220.38","233.15.220.39","233.15.200.133","233.15.220.128","233.15.200.117",
            "233.15.200.213","233.15.200.82","233.13.231.106","233.18.158.25","233.15.220.105",
            "233.15.200.115","233.13.231.135","233.13.231.111","233.15.220.129","233.15.220.171",
            "233.15.220.154","233.18.158.108","233.13.231.96","233.18.158.86","233.15.200.136",
            "233.15.220.181","233.18.158.107","233.15.220.84","233.18.158.92","233.15.220.109",
            "233.13.231.105","233.13.231.90","233.15.200.126","233.18.158.82","233.18.158.87",
            "233.15.220.178","233.15.220.71","233.15.200.102","233.13.231.150","233.18.158.44",
            "233.15.220.72","233.15.220.73","233.18.158.63","233.15.220.155","233.15.220.151",
            "233.15.220.168","233.18.158.14","233.18.158.21","233.13.231.94","233.13.231.11",
            "233.13.231.191","233.13.231.138","233.13.231.137","233.13.231.58","233.13.231.93",
            "233.15.200.108","233.13.231.73","233.13.231.30","233.13.231.37","233.13.231.108",
            "233.13.231.88","233.13.231.109","233.18.158.32","233.13.231.110","233.15.220.70",
            "233.15.200.107","233.18.158.98","233.18.158.49","233.15.200.221","233.15.200.77",
            "233.15.220.115","233.13.231.91","233.18.158.95","233.13.231.89","233.15.200.95",
            "233.18.158.96","233.18.158.97","233.13.231.92","233.18.158.11","233.15.220.22",
            "233.18.158.99","233.15.220.162","233.13.231.65","233.18.158.56","233.13.231.146",
            "233.15.220.20","233.15.220.127","233.13.231.147","233.15.220.130","233.18.158.48",
            "233.15.200.103","233.15.220.161","233.15.220.163","233.13.231.63","233.13.231.95",
            "233.13.231.70","233.15.220.152","233.13.231.130","233.18.158.35","233.18.158.12",
            "233.15.220.21","233.15.200.118","233.18.158.142","233.13.231.50","233.14.173.141",
            "233.14.173.142","233.14.173.143","233.14.173.131","233.14.173.132","233.14.173.144",
            "233.14.173.145","233.14.173.133","233.14.173.146","233.14.173.147","233.14.173.152",
            "233.14.173.148","233.14.173.150","233.14.173.151","233.14.173.149","233.14.173.134",
            "233.14.173.153","233.14.173.154","233.14.173.155","233.14.173.135","233.14.173.156",
            "233.14.173.136","233.14.173.157","233.14.173.137","233.14.173.138","233.14.173.139",
            "233.14.173.140","233.14.173.158","233.14.173.159","233.14.173.160","233.18.158.160",
            "233.18.158.159","233.15.220.164","233.18.158.116","233.18.158.112","233.15.200.207",
            "233.18.158.137","233.18.158.140","233.15.200.189","233.18.158.133","233.18.158.26",
            "233.15.200.186","233.18.158.144","233.15.200.223","233.15.200.235","233.18.158.152",
            "233.18.158.132","233.18.158.151","233.15.220.79","233.18.158.130","233.15.200.190",
            "233.15.200.193","233.15.200.204","233.15.200.185","233.15.200.238","233.18.158.127",
            "233.15.200.228","233.15.200.234","233.18.158.156","233.18.158.143","233.15.200.199",
            "233.15.200.203","233.15.200.229","233.18.158.139","233.15.200.230","233.18.158.105",
            "233.18.158.120","233.15.200.191","233.18.158.222","233.15.200.233","233.13.231.26",
            "233.13.231.27","233.13.231.28","233.13.231.29","233.13.231.31","233.13.231.32",
            "233.13.231.33","233.13.231.34","233.13.231.35","233.13.231.36","233.15.200.181",
            "233.15.200.104","233.15.200.109","233.15.200.111","233.15.200.196","233.18.158.118",
            "233.18.158.141","233.14.173.73","233.15.200.205","233.15.200.211","233.18.158.123",
            "233.18.158.110","233.14.173.75","233.15.220.23","233.15.220.24","233.15.220.25",
            "233.15.220.26","233.15.220.170","233.18.158.153","233.18.158.119","233.18.158.103",
            "233.18.158.128","233.15.200.192","233.15.220.153","233.15.220.34","233.18.158.53",
            "233.18.158.54","233.18.158.45","233.15.200.86","233.15.220.82","233.18.158.134",
            "233.18.158.145","233.15.200.222","233.18.158.114","233.15.200.206","233.15.200.184",
            "233.15.200.236","233.18.158.122","233.15.200.194","233.15.200.114","233.13.231.87",
            "233.15.200.202","233.15.220.100","233.18.158.136","233.15.200.224","233.18.158.160",
            "233.15.220.165","233.13.231.62","233.13.231.22","233.13.231.12","233.13.231.61",
            "233.15.200.129","233.15.200.216","233.18.158.39","233.15.200.215","233.15.220.66",
            "233.15.200.139","233.15.200.135","233.15.200.101","233.15.200.183","233.13.231.86",
            "233.13.231.59","233.15.200.80","233.13.231.85","233.14.173.107","233.18.158.201",
            "233.13.231.84","233.15.220.125","233.15.220.36","233.15.220.35","233.13.231.112",
            "233.13.231.25","233.14.173.115","233.18.158.74","233.15.220.124","233.15.220.104",
            "233.14.173.117","233.18.158.159","233.18.158.206","233.18.158.23"

            ]
    }

    # DataFrame 생성
    df = pd.DataFrame(data)

    # Streamlit App
    #st.title("IP 조회 시스템")

    # IP 입력
    input_ip = st.text_input("-조회할 IP를 입력하세요:")

    # IP로 검색
    if input_ip:
        result = df[df["IP"] == input_ip]
        if not result.empty:
            #st.success("조회 결과:")
            st.write(result)
        else:
            st.error("해당 IP에 대한 정보가 없습니다.")
            
            
elif menu == "인터넷상품" :
    st.header("■ 인터넷상품/속도")
    st.text("-슈퍼프리미엄 10G\n" 
            "-프리미엄플러스 5G : E5924K E5908KE V3024V V2908V\n" 
            "-프리미엄 2.5G : E5924K E5908KE V3024V V2908V\n"
            "-에센스 1G : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-베이직 500M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-슬림플러스 200M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-슬림 100M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n")