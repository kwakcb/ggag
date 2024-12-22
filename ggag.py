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
    ("KWAK[용서_연민_사랑]", "고장상황", "MOSS_Copy", "OLT광3종", "OLT Check", "OLT_1stRN", "L2 Check", "IP SETTING", 
     "SDN_L2_YESNO"  ,"OPR", "10G","ftp긴급복구","U4224B_SDN","각종일지","TV_ch","인터넷상품","국사찾기")
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
-엑셀 체크표시 없애기 : A열선택 -> F5+옵션+개체 + DEL\n
*멀티룸팩 1:2 RN 광으로변경시 타이번호 그대로 가기\n\n



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
        "logging session[console] enable",
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
            
            
elif menu == "인터넷상품":
    st.header("■ 인터넷상품/속도")
    st.text("-슈퍼프리미엄 10G\n" 
            "-프리미엄플러스 5G : E5924K E5908KE V3024V V2908V\n" 
            "-프리미엄 2.5G : E5924K E5908KE V3024V V2908V\n"
            "-에센스 1G : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-베이직 500M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-슬림플러스 200M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n"
            "-슬림 100M : E5924K E5908KE V3024V V2908V : V29XXGB V27XXGB E56XXR E50XX : U4214B U4224B : E5608C V2708M\n")
    
elif menu == "국사찾기":
    st.header("■ 국사/분기국사 찾기")
    
    #data
    data_kuk = {
        "bonbu_kuk": ["충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)",
        "대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)",
        "부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)",
        "전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)",
        "부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)",
        "대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)",
        "전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)",
        "충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)",
        "전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)",
        "대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)",
        "대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)",
        "전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)",
        "대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)",
        "충남&충북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)",
        "부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)",
        "대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)","충남&충북NW운용본부(N)",
        "충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","전남&전북NW운용본부(N)",
        "부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)",
        "충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)",
        "부산&경남NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)",
        "충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","충남&충북NW운용본부(N)","대구&경북NW운용본부(N)",
        "부산&경남NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)",
        "전남&전북NW운용본부(N)","전남&전북NW운용본부(N)","부산&경남NW운용본부(N)","대구&경북NW운용본부(N)","부산&경남NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)",
        "부산&경남NW운용본부(N)","전남&전북NW운용본부(N)","충남&충북NW운용본부(N)","부산&경남NW운용본부(N)","충남&충북NW운용본부(N)",
        "전남&전북NW운용본부(N)","대구&경북NW운용본부(N)","대구&경북NW운용본부(N)"
        ],
        "center_kuk": ["충북액세스운용센터","부산액세스운용센터","충남액세스운용센터","전남액세스운용센터","경남액세스운용센터",
        "경남액세스운용센터","경북액세스운용센터","대구액세스운용센터","경북액세스운용센터","충남액세스운용센터",
        "대구액세스운용센터","대구액세스운용센터","경남액세스운용센터","전북액세스운용센터","전남액세스운용센터",
        "전남액세스운용센터","경북액세스운용센터","충남액세스운용센터","전남액세스운용센터","전남액세스운용센터",
        "전남액세스운용센터","전남액세스운용센터","충남액세스운용센터","충북액세스운용센터","전남액세스운용센터",
        "경북액세스운용센터","경북액세스운용센터","충남액세스운용센터","부산액세스운용센터","전북액세스운용센터",
        "대구액세스운용센터","부산액세스운용센터","부산액세스운용센터","충남액세스운용센터","충북액세스운용센터",
        "부산액세스운용센터","부산액세스운용센터","전북액세스운용센터","경북액세스운용센터","경남액세스운용센터",
        "전남액세스운용센터","전남액세스운용센터","대구액세스운용센터","충남액세스운용센터","부산액세스운용센터",
        "경남액세스운용센터","전북액세스운용센터","전북액세스운용센터","충남액세스운용센터","충북액세스운용센터",
        "경남액세스운용센터","경남액세스운용센터","전남액세스운용센터","충남액세스운용센터","충북액세스운용센터",
        "대구액세스운용센터","대구액세스운용센터","전남액세스운용센터","충남액세스운용센터","대구액세스운용센터",
        "전남액세스운용센터","부산액세스운용센터","충남액세스운용센터","부산액세스운용센터","전남액세스운용센터",
        "경북액세스운용센터","전북액세스운용센터","대구액세스운용센터","충남액세스운용센터","부산액세스운용센터",
        "경남액세스운용센터","전남액세스운용센터","부산액세스운용센터","부산액세스운용센터","전남액세스운용센터",
        "전남액세스운용센터","경남액세스운용센터","전북액세스운용센터","경남액세스운용센터","대구액세스운용센터",
        "충남액세스운용센터","경남액세스운용센터","전남액세스운용센터","전남액세스운용센터","전북액세스운용센터",
        "경북액세스운용센터","부산액세스운용센터","경남액세스운용센터","부산액세스운용센터","전남액세스운용센터",
        "대구액세스운용센터","전남액세스운용센터","충남액세스운용센터","전남액세스운용센터","충북액세스운용센터",
        "전남액세스운용센터","대구액세스운용센터","전북액세스운용센터","경북액세스운용센터","부산액세스운용센터",
        "부산액세스운용센터","전북액세스운용센터","전북액세스운용센터","충남액세스운용센터","전남액세스운용센터",
        "대구액세스운용센터","충남액세스운용센터","부산액세스운용센터","전남액세스운용센터","전남액세스운용센터",
        "전북액세스운용센터","경북액세스운용센터","경남액세스운용센터","부산액세스운용센터","대구액세스운용센터",
        "경남액세스운용센터","전북액세스운용센터","경남액세스운용센터","충남액세스운용센터","충북액세스운용센터",
        "대구액세스운용센터","전남액세스운용센터","경북액세스운용센터","전남액세스운용센터","전남액세스운용센터",
        "경북액세스운용센터","전북액세스운용센터","대구액세스운용센터","충남액세스운용센터","부산액세스운용센터",
        "경북액세스운용센터","부산액세스운용센터","충남액세스운용센터","경북액세스운용센터","경남액세스운용센터",
        "경남액세스운용센터","충남액세스운용센터","충북액세스운용센터","경북액세스운용센터","경남액세스운용센터",
        "경남액세스운용센터","대구액세스운용센터","대구액세스운용센터","충남액세스운용센터","충남액세스운용센터",
        "전남액세스운용센터","경남액세스운용센터","대구액세스운용센터","부산액세스운용센터","전북액세스운용센터",
        "전남액세스운용센터","충남액세스운용센터","전북액세스운용센터","충남액세스운용센터","경북액세스운용센터",
        "경북액세스운용센터","경북액세스운용센터","대구액세스운용센터","경남액세스운용센터","전남액세스운용센터",
        "경남액세스운용센터","경남액세스운용센터","경남액세스운용센터","전남액세스운용센터","전남액세스운용센터",
        "충남액세스운용센터","전남액세스운용센터","경북액세스운용센터","부산액세스운용센터","충북액세스운용센터",
        "경남액세스운용센터","전남액세스운용센터","경북액세스운용센터","경북액세스운용센터","대구액세스운용센터",
        "충남액세스운용센터","경북액세스운용센터","경북액세스운용센터","전남액세스운용센터","충북액세스운용센터",
        "경남액세스운용센터","경남액세스운용센터","전남액세스운용센터","대구액세스운용센터","충남액세스운용센터",
        "경북액세스운용센터","경남액세스운용센터","경북액세스운용센터","대구액세스운용센터","충남액세스운용센터",
        "충남액세스운용센터","충북액세스운용센터","경남액세스운용센터","경북액세스운용센터","전북액세스운용센터",
        "부산액세스운용센터","전북액세스운용센터","부산액세스운용센터","전남액세스운용센터","전북액세스운용센터",
        "경남액세스운용센터","충남액세스운용센터","전남액세스운용센터","부산액세스운용센터","전북액세스운용센터",
        "전북액세스운용센터","충북액세스운용센터","부산액세스운용센터","전남액세스운용센터","부산액세스운용센터",
        "충북액세스운용센터","경남액세스운용센터","전남액세스운용센터","경남액세스운용센터","전북액세스운용센터",
        "경남액세스운용센터","경남액세스운용센터","충북액세스운용센터","경남액세스운용센터","경남액세스운용센터",
        "경남액세스운용센터","충남액세스운용센터","대구액세스운용센터","부산액세스운용센터","경북액세스운용센터",
        "충남액세스운용센터","충북액세스운용센터","충북액세스운용센터","충북액세스운용센터","대구액세스운용센터",
        "경남액세스운용센터","충남액세스운용센터","경남액세스운용센터","전북액세스운용센터","경북액세스운용센터",
        "전남액세스운용센터","전남액세스운용센터","경남액세스운용센터","대구액세스운용센터","경남액세스운용센터",
        "경남액세스운용센터","전북액세스운용센터","경북액세스운용센터","전남액세스운용센터","충남액세스운용센터",
        "경남액세스운용센터","전남액세스운용센터","충남액세스운용센터","부산액세스운용센터","충남액세스운용센터",
        "전남액세스운용센터","경북액세스운용센터","경북액세스운용센터"
        ],
        "ktteam1_kuk": ["서청주운용팀","남부산운용팀","서대전운용팀","해남운용팀","거제운용팀",
        "진주운용팀","경주운용팀","경산운용팀","경주운용팀","서대전운용팀",
        "달서운용팀","수성운용팀","통영도서무선통신팀","정읍운용팀","고흥운용팀",
        "광주운용팀","구미운용팀","세종운용팀","광산운용팀","동순천운용팀",
        "광주운용팀","광산운용팀","홍성운용팀","서청주운용팀","북순천운용팀",
        "구미운용팀","구미운용팀","서대전운용팀","구포운용팀","군산운용팀",
        "칠곡운용팀","구포운용팀","동래운용팀","대전운용팀","충주운용팀",
        "동래운용팀","해운대운용팀","익산운용팀","상주운용팀","김해운용팀",
        "나주운용팀","서광주운용팀","대구운용팀","대전운용팀","남부산운용팀",
        "남울산운용팀","남원운용팀","전주운용팀","남천안운용팀","청주운용팀",
        "동진주운용팀","마산운용팀","고흥운용팀","서대전운용팀","제천운용팀",
        "서대구운용팀","달서운용팀","광주운용팀","서산운용팀","대구운용팀",
        "목포운용팀","남부산운용팀","대전운용팀","북부산운용팀","북광주운용팀",
        "구미운용팀","군산운용팀","동대구운용팀","대전운용팀","동래운용팀",
        "마산운용팀","목포운용팀","동부산운용팀","중부산운용팀","동순천운용팀",
        "여수운용팀","울산운용팀","북전주운용팀","동진주운용팀","동대구운용팀",
        "둔산운용팀","마산운용팀","목포운용팀","목포운용팀","전주운용팀",
        "상주운용팀","동래운용팀","김해운용팀","동래운용팀","고흥운용팀",
        "수성운용팀","광산운용팀","보령운용팀","고흥운용팀","옥천운용팀",
        "북광주운용팀","대구운용팀","북전주운용팀","영주운용팀","북부산운용팀",
        "북부산운용팀","익산운용팀","정읍운용팀","보령운용팀","북광주운용팀",
        "대구운용팀","둔산운용팀","북부산운용팀","북순천운용팀","여수운용팀",
        "북전주운용팀","북포항운용팀","동진주운용팀","사하운용팀","동대구운용팀",
        "진주운용팀","북전주운용팀","동진주운용팀","홍성운용팀","청주운용팀",
        "수성운용팀","서광주운용팀","상주운용팀","동순천운용팀","서광주운용팀",
        "구미운용팀","군산운용팀","서대구운용팀","서대전운용팀","남부산운용팀",
        "상주운용팀","중부산운용팀","서산운용팀","안동운용팀","남울산운용팀",
        "창원운용팀","보령운용팀","서청주운용팀","구미운용팀","울산운용팀",
        "울산운용팀","서대구운용팀","서대구운용팀","천안운용팀","세종운용팀",
        "광산운용팀","김해운용팀","수성운용팀","동부산운용팀","남원운용팀",
        "북순천운용팀","용전운용팀","정읍운용팀","남천안운용팀","경주운용팀",
        "안동운용팀","안동운용팀","동대구운용팀","양산운용팀","목포도서무선통신팀",
        "울산운용팀","양산운용팀","남울산운용팀","여수운용팀","여수운용팀",
        "서대전운용팀","광산운용팀","북포항운용팀","중부산운용팀","옥천운용팀",
        "마산운용팀","목포운용팀","안동운용팀","영주운용팀","경산운용팀",
        "홍성운용팀","영주운용팀","포항운용팀","동순천운용팀","옥천운용팀",
        "거제운용팀","남울산운용팀","해남운용팀","칠곡운용팀","용전운용팀",
        "포항운용팀","울산운용팀","북포항운용팀","달서운용팀","세종운용팀",
        "둔산운용팀","충주운용팀","마산운용팀","안동운용팀","익산운용팀",
        "해운대운용팀","남원운용팀","사하운용팀","북광주운용팀","전주운용팀",
        "거제운용팀","보령운용팀","해남운용팀","해운대운용팀","전주운용팀",
        "정읍운용팀","제천운용팀","해운대운용팀","해남운용팀","중부산운용팀",
        "서청주운용팀","동진주운용팀","목포운용팀","마산운용팀","전주운용팀",
        "김해운용팀","진주운용팀","서청주운용팀","창원운용팀","마산운용팀",
        "창원운용팀","천안운용팀","경산운용팀","동래운용팀","안동운용팀",
        "홍성운용팀","청주운용팀","옥천운용팀","충주운용팀","칠곡운용팀",
        "마산운용팀","서산운용팀","통영도서무선통신팀","북전주운용팀","포항운용팀",
        "광산운용팀","목포운용팀","동진주운용팀","경산운용팀","마산운용팀",
        "진주운용팀","익산운용팀","상주운용팀","나주운용팀","서산운용팀",
        "진주운용팀","해남운용팀","서산운용팀","해운대운용팀","홍성운용팀",
        "광주운용팀","북포항운용팀","북포항운용팀"
        ],
        "ktteam2_kuk": ["진천운용팀","동부산운용부","대전운용팀","목포운용부","동진주운용부",
        "동진주운용부","포항운용부","동대구운용부","포항운용부","대전운용팀",
        "서대구운용부","동대구운용부","동진주운용부","정읍운용팀","순천운용부",
        "광주운용부","구미운용부","둔산운용부","서광주운용팀","순천운용부",
        "광주운용부","서광주운용팀","홍성운용팀","진천운용팀","순천운용부",
        "구미운용부","구미운용부","대전운용팀","북부산운용부","익산운용부",
        "서대구운용부","북부산운용부","동부산운용부","대전운용팀","충주운용팀",
        "동부산운용부","동부산운용부","익산운용부","구미운용부","창원운용부",
        "서광주운용팀","서광주운용팀","서대구운용부","대전운용팀","동부산운용부",
        "울산운용팀","전주운용부","전주운용부","천안운용부","청주운용부",
        "동진주운용부","창원운용부","순천운용부","대전운용팀","충주운용팀",
        "서대구운용부","서대구운용부","광주운용부","홍성운용팀","서대구운용부",
        "목포운용부","동부산운용부","대전운용팀","북부산운용부","광주운용부",
        "구미운용부","익산운용부","동대구운용부","대전운용팀","동부산운용부",
        "창원운용부","목포운용부","동부산운용부","북부산운용부","순천운용부",
        "순천운용부","울산운용팀","전주운용부","동진주운용부","동대구운용부",
        "둔산운용부","창원운용부","목포운용부","목포운용부","전주운용부",
        "구미운용부","동부산운용부","창원운용부","동부산운용부","순천운용부",
        "동대구운용부","서광주운용팀","홍성운용팀","순천운용부","청주운용부",
        "광주운용부","서대구운용부","전주운용부","안동운용부","북부산운용부",
        "북부산운용부","익산운용부","정읍운용팀","홍성운용팀","광주운용부",
        "서대구운용부","둔산운용부","북부산운용부","순천운용부","순천운용부",
        "전주운용부","포항운용부","동진주운용부","북부산운용부","동대구운용부",
        "동진주운용부","전주운용부","동진주운용부","홍성운용팀","청주운용부",
        "동대구운용부","서광주운용팀","구미운용부","순천운용부","서광주운용팀",
        "구미운용부","익산운용부","서대구운용부","대전운용팀","동부산운용부",
        "구미운용부","북부산운용부","홍성운용팀","안동운용부","울산운용팀",
        "창원운용부","홍성운용팀","진천운용팀","구미운용부","울산운용팀",
        "울산운용팀","서대구운용부","서대구운용부","천안운용부","둔산운용부",
        "서광주운용팀","창원운용부","동대구운용부","동부산운용부","전주운용부",
        "순천운용부","대전운용팀","정읍운용팀","천안운용부","포항운용부",
        "안동운용부","안동운용부","동대구운용부","울산운용팀","목포운용부",
        "울산운용팀","울산운용팀","울산운용팀","순천운용부","순천운용부",
        "대전운용팀","서광주운용팀","포항운용부","북부산운용부","청주운용부",
        "창원운용부","목포운용부","안동운용부","안동운용부","동대구운용부",
        "홍성운용팀","안동운용부","포항운용부","순천운용부","청주운용부",
        "동진주운용부","울산운용팀","목포운용부","서대구운용부","대전운용팀",
        "포항운용부","울산운용팀","포항운용부","서대구운용부","둔산운용부",
        "둔산운용부","충주운용팀","창원운용부","안동운용부","익산운용부",
        "동부산운용부","전주운용부","북부산운용부","광주운용부","전주운용부",
        "동진주운용부","홍성운용팀","목포운용부","동부산운용부","전주운용부",
        "정읍운용팀","충주운용팀","동부산운용부","목포운용부","북부산운용부",
        "진천운용팀","동진주운용부","목포운용부","창원운용부","전주운용부",
        "창원운용부","동진주운용부","진천운용팀","창원운용부","창원운용부",
        "창원운용부","천안운용부","동대구운용부","동부산운용부","안동운용부",
        "홍성운용팀","청주운용부","청주운용부","충주운용팀","서대구운용부",
        "창원운용부","홍성운용팀","동진주운용부","전주운용부","포항운용부",
        "서광주운용팀","목포운용부","동진주운용부","동대구운용부","창원운용부",
        "동진주운용부","익산운용부","구미운용부","서광주운용팀","홍성운용팀",
        "동진주운용부","목포운용부","홍성운용팀","동부산운용부","홍성운용팀",
        "광주운용부","포항운용부","포항운용부"
        ],
        "office_kuk": ["가경","가야","강경","강진","거제",
        "거창","건천","경산","경주","계룡",
        "고령","고산","고성","고창","고흥",
        "곡성","공단","공주","광산","광양",
        "광주","광주하남","광천","괴산","구례",
        "구미","구미공단","구봉","구포","군산",
        "군위","금곡","금사","금산","금왕",
        "금정","기장","김제","김천","김해",
        "나주","남광주","남대구","남대전","남부산",
        "남울산","남원","남전주","남천안","남청주",
        "남해","내서","녹동","논산","단양",
        "달서","달성","담양","당진","대구",
        "대불","대연","대전","덕포","동광주",
        "동구미","동군산","동대구","동대전","동래",
        "동마산","동목포","동부산","동삼","동순천",
        "동여수","동울산","동전주","동진주","동촌",
        "둔산","마산","목포","무안","무주",
        "문경","미남","밀양","반송","벌교",
        "범물","법성포","보령","보성","보은",
        "본촌","봉덕","봉동","봉화","부산강서",
        "강서","부송","부안","부여","북광주",
        "북대구","북대전","북부산","북순천","북여수",
        "북전주","북포항","사천","사하","산격",
        "산청","삼례","삼천포","삽교","상당",
        "상동","상무","상주","서광양","서광주",
        "서구미","서군산","서대구","서대전","서면",
        "서문경","서부산","서산","서안동","서울산",
        "서창원","서천","서청주","선산","성남",
        "울산성남","성서","성주","성환","세종",
        "송정","수산","수성","수영","순창",
        "순천","신탄진","신태인","아산","안강",
        "안계","안동","안심","양산","양을산",
        "양정","양주","언양","여수","여천",
        "연무","영광","영덕","영도","영동",
        "영산","영암","영양","영주","영천",
        "예산","예천","오천","옥곡","옥천",
        "옥포","온산","완도","왜관","용전",
        "울릉","울산","울진","월배","유구",
        "유성","음성","의령","의성","익산",
        "일광","임실","장림","장성","장수",
        "장승포","장항","장흥","재송","전주",
        "정읍","제천","좌동","죽교","중부",
        "증평","지족","진도","진북","진안",
        "진영","진주","진천","진해","창녕",
        "창원","천안","청도","청룡","청송",
        "청양","청주","충북영동","충주","칠곡",
        "칠원","태안","통영","팔복","포항",
        "하남","하당","하동","하양","함안",
        "함양","함열","함창","함평","합덕",
        "합천","해남","해미","해운대","홍성",
        "화순","후포","흥해"
        ],
        "MOSteam_kuk": ["청주","중부산","논산","해남","통영",
        "진주","동대구","동대구","포항","논산",
        "남대구","동대구","통영","정읍","순천",
        "북광주","구미","세종","북광주","순천",
        "북광주","서광주","홍성","충주","남원",
        "구미","구미","서대전","서부산","익산",
        "구미","서부산","동부산","서대전","충주",
        "동부산","동부산","전주","구미","김해",
        "서광주","서광주","남대구","동대전","중부산",
        "울산","남원","전주","천안","청주",
        "진주","창원","순천","논산","충주",
        "남대구","남대구","북광주","서산","서대구",
        "목포","중부산","동대전","서부산","북광주",
        "구미","익산","서대구","동대전","중부산",
        "창원","목포","중부산","서부산","순천",
        "순천","울산","전주","진주","서대구",
        "서대전","창원","목포","목포","전주",
        "문경","중부산","김해","동부산","순천",
        "남대구","서광주","홍성","북광주","동대전",
        "북광주","남대구","전주","안동","김해",
        "김해","익산","정읍","논산","북광주",
        "서대구","서대전","서부산","순천","순천",
        "전주","포항","진주","서부산","서대구",
        "진주","익산","진주","홍성","청주",
        "남대구","서광주","문경","순천","서광주",
        "구미","익산","서대구","서대전","중부산",
        "문경","서부산","서산","안동","울산",
        "창원","논산","청주","구미","울산",
        "울산","서대구","서대구","천안","세종",
        "서광주","김해","남대구","중부산","북광주",
        "순천","동대전","정읍","천안","포항",
        "문경","안동","동대구","동부산","목포",
        "울산","동부산","울산","순천","순천",
        "논산","서광주","포항","서부산","동대전",
        "창원","목포","안동","안동","동대구",
        "홍성","문경","포항","순천","동대전",
        "통영","울산","해남","서대구","동대전",
        "포항","울산","포항","남대구","세종",
        "서대전","충주","진주","안동","익산",
        "동부산","남원","서부산","서광주","남원",
        "통영","논산","북광주","동부산","전주",
        "정읍","충주","동부산","북광주","서부산",
        "청주","진주","목포","창원","전주",
        "김해","진주","청주","창원","창원",
        "창원","천안","동대구","동부산","안동",
        "홍성","청주","동대전","충주","서대구",
        "창원","서산","통영","전주","포항",
        "서광주","목포","진주","동대구","창원",
        "진주","익산","문경","서광주","홍성",
        "진주","해남","서산","동부산","홍성",
        "북광주","포항","포항"
        ]
    }

data_branch = {
        "bonbu_branch": ["충청","충청","호남","충청","충청","대구","부산","부산","충청","충청","부산","충청","호남","충청","대구","대구","부산","부산",
                         "충청","충청","호남","충청","호남","충청","대구","대구","호남","대구","호남","부산","부산","충청","대구","대구","충청","부산",
                         "부산","대구","충청","대구","대구","대구","대구","대구","대구","대구","충청","충청","대구","부산","호남","대구","호남","부산",
                         "충청","대구","부산","호남","대구","충청","부산","부산","부산","호남","충청","호남","호남","호남","대구","충청","호남","호남",
                         "대구","대구","호남","대구","대구","부산","호남","호남","충청","부산","호남","충청","충청","대구","부산","충청","호남","호남",
                         "부산","충청","부산","대구","부산","호남","부산","부산","부산","호남","대구","호남","대구","호남","호남","대구","충청","호남",
                         "호남","호남","대구","충청","대구","충청","대구","호남","충청","충청","호남","호남","충청","충청","호남","호남","충청","대구",
                         "호남","충청","충청","충청","부산","충청","호남","충청","대구","호남","부산","호남","대구","부산","대구","부산","호남","부산",
                         "대구","호남","대구","충청","대구","충청","부산","부산","대구","대구","호남","호남","호남","충청","충청","부산","호남","충청",
                         "호남","호남","대구","부산","대구","충청","충청","충청","충청","호남","호남","호남","호남","충청","호남","충청","호남","대구",
                         "호남","호남","부산","대구","부산","호남","부산","호남","충청","대구","호남","부산","호남","호남","호남","호남","호남","충청",
                         "대구","대구","호남","대구","대구","대구","대구","충청","충청","부산","대구","대구","대구","부산","부산","대구","호남","대구",
                         "대구","대구","호남","대구","대구","대구","호남","호남","부산","대구","대구","충청","호남","부산","충청","충청","충청","대구",
                         "대구","부산","부산","대구","호남","충청","대구","대구","호남","충청","충청","대구","호남","호남","충청","충청","충청","충청",
                         "부산","부산","충청","부산","호남","호남","대구","충청","부산","충청","호남","대구","대구","호남","부산","부산","부산","충청",
                         "호남","호남","충청","충청","대구","호남","부산","부산","호남","대구","호남","대구","대구","부산","대구","대구","부산","충청",
                         "호남","부산","호남","대구","대구","대구","대구","대구","호남","대구","부산","부산","대구","대구","부산","부산","대구","대구",
                         "대구","호남","부산","부산","부산","대구","부산","부산","대구","호남","충청","부산","부산","대구","대구","충청","대구","호남",
                         "호남","호남","호남","충청","호남","호남","대구","부산","대구","대구","부산","호남","호남","부산","호남","호남","충청","충청",
                         "호남","호남","대구","호남","부산","대구","호남","호남","부산","충청","대구","호남","호남","부산","대구","대구","충청","충청",
                         "충청","부산","대구","대구","호남","충청","충청","대구","호남","호남","충청","대구","호남","충청","대구","충청","부산","부산",
                         "충청","호남","충청","호남","대구","충청","대구","충청","충청","호남","충청","호남","충청","대구","호남","부산","호남","대구",
                         "대구","충청","대구","호남","호남","대구","호남","대구","충청","충청","호남","부산","호남","대구","대구","호남","부산","부산",
                         "호남","대구","충청","충청","대구","충청","호남","호남","부산","대구","충청","부산","충청","호남","부산","대구","충청","부산",
                         "부산","호남","충청","충청","부산","대구","충청","호남","충청","호남","충청","호남","호남","충청","호남","호남","충청","대구",
                         "호남","대구","부산","충청","호남","대구","부산","대구","호남","충청","호남","호남","대구","호남","호남","호남","호남","호남",
                         "호남","충청","부산","충청","부산","부산","대구","대구","대구","호남","충청","대구","부산","충청","충청","호남","충청","부산",
                         "충청","대구","부산","충청","대구","부산","호남","대구","충청","대구","대구","충청","대구","충청","충청","충청","호남","호남",
                         "호남","부산","호남","부산","호남","부산","부산","대구","호남","호남","대구","대구","충청","충청","호남","충청","충청","대구",
                         "충청","호남","호남","충청","대구","호남","부산","부산","충청","부산","호남","충청","호남","충청","부산","부산","부산","대구",
                         "대구","부산","대구","호남","부산","호남","부산","대구","부산","충청","충청","부산","충청","부산","충청","호남","부산","충청",
                         "부산","부산","충청","호남","호남","충청","호남","대구","대구","대구","충청","호남","대구","호남","호남","충청","부산","부산",
                         "부산","대구","대구","호남","호남","충청","대구","부산","충청","호남","충청","대구","충청","대구","호남","충청","대구","호남",
                         "호남","충청","호남","대구","호남","부산","부산","호남","충청","호남","충청","대구","충청","충청","부산","부산","대구","대구",
                         "부산","호남","충청","충청","대구","충청","부산","대구","호남","충청","대구","호남","호남","대구","호남","충청","대구","대구",
                         "대구","호남","호남","충청","부산","대구","부산","호남","대구","부산","대구","충청","호남","호남","호남","대구","충청","대구",
                         "대구","호남","호남","충청","대구","호남","대구","충청","충청","호남","부산","부산","호남","충청","대구","충청","부산","대구",
                         "대구","대구","부산","호남","호남","대구","대구","충청","호남","부산","부산","호남","대구","호남","호남","부산","호남","대구",
                         "충청","호남","호남","충청","대구","충청","부산","부산","충청","호남","부산","충청","호남","호남","충청","부산","호남","충청",
                         "부산","부산","대구","호남","부산","부산","대구","호남","호남","부산","호남","대구","대구","부산","대구","대구","대구","대구",
                         "호남","충청","호남","충청","충청","충청","부산","대구","호남","호남","호남","부산","충청","호남","대구","대구","충청","부산",
                         "대구","대구","부산","호남","호남","대구","충청","대구","호남","대구","부산","충청","부산","부산","충청","대구","호남","호남",
                         "충청","부산","호남","부산","부산","부산","충청","대구","대구","대구","충청","부산","부산","호남","호남","대구","호남","부산",
                         "부산","호남","대구","대구","호남","부산","대구","충청","대구","대구","충청","대구","대구","대구","호남","부산","대구","부산",
                         "호남","충청","호남","대구","호남","호남","충청","호남","충청","호남","부산","호남","호남","충청","부산","대구","호남","부산",
                         "호남","부산","호남","호남","부산","충청","호남","충청","부산","호남","호남","호남","대구","대구","충청","호남","호남","충청",
                         "충청","충청","충청","충청","대구","대구","충청","부산","충청","충청","호남","충청","대구","호남","호남","호남","대구","대구",
                         "부산","충청","부산","호남","충청","충청","호남","충청","충청","부산","호남","충청","충청","충청","호남","충청","충청","호남",
                         "부산","대구","충청","호남","호남","대구","충청","충청","충청","호남","호남","대구","대구","충청","충청","호남","충청","충청",
                         "대구","호남","부산","부산","호남","호남","충청","대구","호남","충청","충청","대구","충청","충청","대구","대구","충청","호남",
                         "충청","호남","부산","충청","호남","대구","호남","충청","부산","대구","충청","충청","대구","충청","호남","대구","충청","충청",
                         "대구","호남","호남","대구","호남","호남","호남","호남","부산","호남","대구","충청","충청","대구","대구","호남","충청","호남",
                         "대구","대구","충청","충청","호남","대구","부산","호남","충청","충청","충청","대구","충청","호남","충청","호남","호남","호남",
                         "대구","대구","대구","부산","충청","대구","충청","대구","호남","충청","호남","부산","대구","부산","호남","호남","호남","대구",
                         "부산","충청","대구","호남","대구","호남","호남","충청","호남","충청","부산","호남","대구","대구","호남","호남","대구","대구",
                         "충청","부산","대구","충청","충청","대구","호남","충청","부산","호남","충청","대구","대구","충청","대구","충청","충청","호남",
                         "충청","충청","호남","부산","호남","대구","충청","호남","대구","호남","충청","호남","충청","충청","대구","부산","호남","대구",
                         "호남","부산","충청","부산","대구","호남","충청","호남","호남","대구","부산","부산","대구","충청","호남","충청","호남","대구",
                         "부산","호남","호남","부산","대구","부산","호남","충청","충청","대구","대구","부산","충청","충청","부산","부산","호남","대구",
                         "대구","대구","충청","호남","호남","대구","부산","충청","충청","호남","충청","대구","대구","대구","호남","대구","호남","호남",
                         "호남","대구","대구","호남","충청","대구","대구","호남","부산","호남","대구","대구","호남","대구","충청","대구","대구","호남",
                         "호남","호남","대구","호남","대구","호남","대구","충청","호남","충청","부산","부산","호남","충청","부산","대구","호남","대구",
                         "대구","부산","호남","충청","호남","대구","충청","대구","대구","호남","대구","호남","대구","충청","호남","대구","부산","부산",
                         "대구","대구","부산","호남","호남","호남","부산","충청","호남","호남","부산","대구","부산","호남","부산","대구","대구","대구",
                         "충청","충청","부산","호남","부산","충청","호남","호남","대구","호남","충청","호남","호남","부산","부산","부산","부산","호남",
                         "호남","호남","충청","호남","충청","부산","대구","호남","호남","충청","충청","충청","부산","호남","부산","대구","부산","호남",
                         "부산","대구","호남","호남","대구","호남","호남","부산","대구","충청","호남","부산","충청","호남","호남","대구","부산","호남",
                         "부산","대구","대구","호남","대구","호남","호남","부산","부산","대구","부산","호남","호남","호남","부산","대구","대구","부산",
                         "부산","호남","부산","부산","충청","부산","충청","대구","충청","충청","충청","충청","호남","부산","충청","충청","호남","충청",
                         "대구","충청","충청","부산","부산","호남","호남","대구","호남","충청","충청","충청","충청","충청","대구","대구","부산","호남",
                         "대구","호남","호남","호남","호남","충청","호남","호남","대구","대구","대구","호남","대구","대구","호남","부산","호남","부산",
                         "충청","호남","대구","호남","호남","부산","대구","충청","호남","충청","대구","호남","대구","대구","호남","부산","충청","충청",
                         "부산","대구","대구","충청","호남","호남","부산","부산","부산","부산","부산","호남","호남","대구","호남","호남","부산","호남",
                         "충청","호남","충청","충청","호남","충청","부산","부산","충청","부산","부산","대구","호남","부산","호남","충청","충청","충청",
                         "대구","부산","대구","호남","충청","호남","충청","충청","충청","부산","호남","부산","대구","부산","충청","호남","충청","호남",
                         "부산","대구","대구","호남","부산","부산","대구","충청","호남","충청","대구","호남","부산","호남","대구","부산","충청","대구",
                         "충청","충청","충청","호남","호남","대구","부산","부산","충청","호남","충청","호남","부산","호남","부산","충청","대구","대구",
                         "호남","대구","호남","충청","호남","호남","호남","충청","부산","대구","대구","충청","대구","대구","대구","부산","대구","호남",
                         "충청","충청","부산","충청","충청","호남","호남","대구","충청","대구","대구","부산","호남","대구","대구","부산","호남","부산",
                         "호남","부산","대구","대구","대구","대구","부산","대구","호남","부산","호남","대구","충청","부산","충청","호남","부산","부산",
                         "대구","부산","충청","충청","부산","대구","호남","부산","호남","대구","부산","충청","대구","대구","충청","부산","충청","대구",
                         "대구","대구","부산","호남","부산","대구","충청","충청","호남","대구","충청","호남","충청","충청","충청","충청","호남","호남",
                         "대구","대구","충청","대구","대구","충청","호남","대구","충청","부산","호남","호남","부산","대구","부산","충청","충청","충청",
                         "충청","부산","충청","부산","충청","대구","대구","호남","대구","대구","호남","호남","충청","대구","부산","호남","호남","부산",
                         "부산","충청","부산","대구","충청","충청","대구","호남","충청","부산","충청","호남","호남","대구","부산","대구","충청","부산",
                         "호남","부산","대구","대구","대구","충청","충청","대구","호남","호남","충청","호남","호남","호남","부산","부산","대구","호남",
                         "대구","대구","대구","충청","호남","호남","대구","호남","대구","부산","호남","부산","충청","충청","대구","부산","대구","호남",
                         "호남","대구","부산","호남","부산","대구","호남","대구","호남","부산","호남","부산","호남","부산","충청","충청","호남","호남",
                         "대구","부산","충청","호남","호남","호남","부산","호남","충청","호남","대구","부산","대구","충청","호남","대구","대구","충청",
                         "부산","대구","대구","부산","호남","대구","호남","호남","대구","호남","충청","충청","충청","대구","부산","충청","대구","부산",
                         "대구","충청","대구","호남","대구","호남","대구","호남","충청","대구","호남","부산","충청","호남","대구","호남","호남","부산",
                         "대구","호남","부산","부산","부산","대구","호남","충청","호남","충청","대구","호남","대구","호남","부산","호남","대구","부산",
                         "호남","대구","충청","호남","호남","호남","대구","호남","대구","대구","부산","호남","충청","호남","대구"
        ],
        "center_branch": ["충북","충남","전남","충북","충북","경북","부산","경남","충북","충남","경남","충남","전남","충남","경북","경북","경남","경남",
                          "충북","충북","전북","충북","전남","충북","대구","대구","전남","경북","전북","경남","경남","충남","대구","경북","충북","경남",
                          "경남","경북","충북","경북","경북","경북","경북","경북","경북","경북","충북","충남","경북","경남","전남","경북","전남","경남",
                          "충북","대구","경남","전남","경북","충남","경남","경남","경남","전북","충남","전남","전남","전남","대구","충남","전북","전남",
                          "경북","대구","전북","대구","경북","경남","전남","전남","충남","경남","전남","충남","충남","대구","경남","충남","전북","전남",
                          "경남","충남","경남","경북","부산","전북","경남","경남","경남","전북","대구","전북","경북","전북","전남","경북","충북","전남",
                          "전남","전북","대구","충남","경북","충남","경북","전북","충남","충남","전남","전남","충남","충북","전북","전남","충남","경북",
                          "전북","충북","충북","충북","경남","충남","전남","충북","경북","전북","경남","전남","경북","경남","경북","경남","전북","경남",
                          "대구","전북","경북","충북","경북","충남","경남","경남","경북","대구","전남","전남","전남","충남","충북","경남","전남","충북",
                          "전남","전남","경북","경남","경북","충남","충남","충북","충북","전남","전남","전남","전북","충북","전북","충남","전북","경북",
                          "전북","전남","경남","대구","경남","전북","부산","전남","충북","대구","전남","경남","전남","전남","전북","전남","전남","충북",
                          "대구","대구","전남","경북","대구","경북","경북","충북","충남","경남","경북","경북","대구","경남","경남","경북","전북","경북",
                          "대구","경북","전남","경북","경북","경북","전남","전남","경남","대구","대구","충남","전남","경남","충남","충북","충북","경북",
                          "경북","경남","경남","대구","전남","충남","경북","경북","전남","충북","충남","대구","전남","전북","충남","충북","충남","충남",
                          "경남","경남","충북","경남","전북","전북","경북","충남","경남","충남","전남","경북","경북","전남","경남","경남","경남","충남",
                          "전남","전남","충남","충북","경북","전남","부산","부산","전북","대구","전남","경북","경북","경남","경북","경북","경남","충북",
                          "전남","경남","전남","대구","대구","대구","대구","경북","전남","경북","경남","경남","경북","경북","경남","경남","경북","대구",
                          "경북","전북","경남","경남","경남","경북","경남","경남","대구","전북","충북","경남","경남","대구","경북","충남","경북","전북",
                          "전남","전남","전남","충남","전남","전남","경북","경남","경북","경북","경남","전북","전북","경남","전남","전북","충북","충남",
                          "전북","전북","대구","전남","경남","대구","전북","전남","부산","충남","대구","전남","전남","경남","경북","경북","충남","충남",
                          "충남","경남","경북","대구","전북","충남","충북","경북","전남","전남","충남","경북","전북","충북","경북","충북","경남","경남",
                          "충남","전남","충북","전남","경북","충남","경북","충남","충북","전남","충북","전남","충북","경북","전남","경남","전남","경북",
                          "대구","충남","경북","전남","전북","대구","전남","대구","충북","충북","전남","경남","전남","대구","경북","전남","경남","경남",
                          "전북","대구","충남","충남","경북","충북","전남","전남","경남","경북","충남","경남","충남","전북","경남","대구","충남","경남",
                          "경남","전남","충남","충북","경남","대구","충남","전남","충북","전남","충남","전남","전북","충북","전남","전북","충남","경북",
                          "전남","경북","경남","충남","전북","대구","경남","경북","전북","충남","전북","전남","경북","전북","전남","전남","전남","전남",
                          "전남","충북","경남","충남","경남","경남","대구","대구","경북","전남","충북","경북","부산","충북","충남","전북","충북","경남",
                          "충북","대구","부산","충남","경북","부산","전남","대구","충남","경북","경북","충북","경북","충남","충북","충남","전남","전남",
                          "전남","경남","전남","경남","전북","경남","경남","경북","전남","전북","대구","경북","충북","충북","전남","충북","충남","경북",
                          "충북","전남","전남","충남","경북","전남","경남","경남","충북","경남","전남","충남","전남","충북","부산","경남","경남","경북",
                          "대구","경남","경북","전남","경남","전북","경남","대구","경남","충남","충남","경남","충남","경남","충북","전남","경남","충북",
                          "경남","경남","충북","전북","전남","충남","전남","대구","대구","대구","충북","전북","경북","전남","전북","충남","경남","경남",
                          "경남","경북","대구","전북","전남","충북","경북","경남","충남","전남","충남","경북","충북","대구","전북","충북","대구","전남",
                          "전남","충남","전북","대구","전남","경남","경남","전북","충북","전남","충남","경북","충남","충북","경남","경남","대구","대구",
                          "경남","전남","충북","충남","대구","충남","경남","경북","전북","충남","경북","전남","전남","경북","전북","충남","대구","경북",
                          "경북","전북","전북","충남","경남","경북","경남","전남","대구","경남","대구","충북","전남","전남","전남","경북","충남","경북",
                          "경북","전남","전북","충남","대구","전남","경북","충남","충북","전남","경남","경남","전남","충남","경북","충남","경남","대구",
                          "대구","경북","경남","전남","전북","경북","경북","충북","전남","경남","경남","전남","경북","전북","전북","경남","전북","경북",
                          "충남","전북","전북","충남","대구","충남","경남","경남","충북","전북","경남","충남","전남","전남","충북","경남","전남","충북",
                          "경남","경남","경북","전남","경남","경남","경북","전남","전북","경남","전남","경북","경북","경남","대구","대구","대구","대구",
                          "전남","충북","전남","충북","충북","충남","경남","대구","전남","전남","전남","경남","충남","전북","경북","대구","충북","경남",
                          "경북","경북","경남","전남","전남","경북","충남","경북","전북","경북","경남","충남","경남","경남","충북","경북","전북","전북",
                          "충북","경남","전남","경남","경남","경남","충남","경북","경북","대구","충남","경남","경남","전북","전남","대구","전남","경남",
                          "경남","전남","경북","대구","전남","경남","경북","충남","경북","경북","충남","대구","대구","경북","전남","경남","대구","경남",
                          "전북","충남","전남","대구","전북","전남","충남","전북","충남","전북","경남","전북","전남","충남","경남","대구","전북","경남",
                          "전남","경남","전남","전북","경남","충남","전남","충남","경남","전남","전남","전남","대구","대구","충북","전남","전북","충북",
                          "충남","충북","충남","충남","경북","대구","충북","경남","충북","충북","전남","충남","대구","전남","전남","전북","경북","경북",
                          "경남","충북","경남","전남","충남","충남","전남","충남","충남","경남","전남","충남","충북","충북","전남","충남","충남","전남",
                          "경남","대구","충북","전남","전남","경북","충북","충남","충북","전남","전북","대구","경북","충북","충남","전북","충북","충남",
                          "경북","전남","경남","부산","전북","전남","충남","경북","전남","충남","충북","경북","충북","충남","경북","대구","충남","전남",
                          "충남","전북","경남","충남","전남","경북","전남","충남","경남","경북","충남","충남","경북","충남","전남","대구","충북","충남",
                          "경북","전남","전남","경북","전남","전북","전남","전남","경남","전남","경북","충남","충남","경북","대구","전북","충남","전남",
                          "대구","대구","충남","충남","전남","경북","경남","전남","충북","충북","충남","대구","충남","전남","충북","전북","전북","전북",
                          "경북","경북","경북","경남","충북","경북","충남","경북","전북","충남","전남","경남","경북","경남","전남","전북","전북","경북",
                          "경남","충남","경북","전남","대구","전남","전남","충북","전남","충북","경남","전남","대구","대구","전남","전남","경북","경북",
                          "충남","경남","경북","충남","충북","경북","전남","충북","경남","전남","충남","경북","경북","충북","경북","충남","충남","전북",
                          "충북","충남","전북","경남","전남","대구","충남","전남","대구","전남","충남","전북","충남","충북","경북","경남","전남","경북",
                          "전북","경남","충북","경남","대구","전남","충남","전남","전남","경북","경남","경남","경북","충남","전남","충북","전남","경북",
                          "경남","전남","전남","경남","경북","경남","전남","충남","충북","대구","경북","경남","충남","충북","경남","경남","전남","경북",
                          "대구","대구","충북","전북","전북","경북","경남","충북","충북","전남","충남","경북","경북","경북","전남","경북","전북","전남",
                          "전남","경북","경북","전북","충남","경북","경북","전남","경남","전남","대구","경북","전북","경북","충남","경북","대구","전남",
                          "전남","전북","경북","전남","대구","전남","대구","충남","전남","충북","경남","경남","전북","충남","경남","대구","전남","경북",
                          "경북","경남","전북","충남","전남","경북","충남","대구","대구","전남","대구","전남","대구","충북","전남","대구","경남","경남",
                          "경북","대구","경남","전북","전남","전남","경남","충남","전북","전남","경남","대구","경남","전남","경남","경북","경북","대구",
                          "충북","충남","경남","전남","경남","충남","전북","전남","대구","전남","충남","전북","전남","경남","경남","경남","경남","전남",
                          "전북","전남","충북","전남","충남","경남","경북","전북","전남","충남","충남","충남","경남","전북","경남","경북","경남","전남",
                          "경남","경북","전북","전남","경북","전남","전남","경남","대구","충남","전남","경남","충북","전남","전남","경북","경남","전남",
                          "경남","경북","대구","전남","경북","전북","전북","경남","경남","경북","경남","전남","전남","전북","경남","대구","대구","경남",
                          "경남","전남","경남","경남","충남","경남","충남","경북","충남","충남","충남","충남","전남","경남","충남","충남","전남","충남",
                          "대구","충북","충북","경남","경남","전북","전북","대구","전남","충북","충북","충남","충북","충남","경북","경북","경남","전남",
                          "경북","전북","전남","전남","전북","충남","전남","전남","경북","경북","대구","전남","경북","경북","전남","경남","전남","경남",
                          "충남","전북","경북","전남","전남","경남","경북","충북","전북","충남","대구","전남","대구","대구","전남","경남","충북","충남",
                          "경남","대구","경북","충북","전남","전남","부산","경남","경남","경남","경남","전남","전남","경북","전남","전북","경남","전북",
                          "충남","전남","충남","충남","전북","충북","경남","경남","충남","경남","경남","경북","전남","경남","전남","충남","충남","충남",
                          "경북","경남","경북","전북","충북","전북","충남","충남","충남","경남","전남","부산","대구","경남","충남","전남","충남","전북",
                          "경남","경북","경북","전북","경남","경남","경북","충남","전남","충북","경북","전남","경남","전북","경북","경남","충남","경북",
                          "충북","충남","충남","전북","전남","경북","경남","경남","충북","전북","충남","전남","경남","전남","경남","충남","경북","경북",
                          "전남","대구","전남","충남","전남","전남","전북","충남","경남","경북","경북","충남","대구","경북","경북","경남","경북","전북",
                          "충남","충남","경남","충남","충남","전남","전남","경북","충북","경북","경북","경남","전남","경북","대구","부산","전남","경남",
                          "전남","경남","경북","대구","대구","경북","경남","대구","전남","경남","전남","경북","충남","경남","충북","전남","경남","경남",
                          "경북","경남","충남","충남","경남","대구","전남","경남","전남","경북","부산","충남","경북","경북","충남","경남","충남","경북",
                          "대구","경북","부산","전남","경남","경북","충남","충남","전남","경북","충북","전남","충북","충남","충남","충북","전남","전북",
                          "경북","대구","충북","대구","대구","충북","전북","경북","충남","경남","전남","전남","경남","대구","경남","충북","충남","충북",
                          "충남","경남","충남","경남","충남","경북","경북","전남","경북","경북","전남","전남","충남","대구","경남","전남","전북","경남",
                          "경남","충북","경남","경북","충남","충남","경북","전북","충남","경남","충북","전남","전북","경북","경남","경북","충남","경남",
                          "전남","경남","대구","경북","경북","충남","충남","대구","전남","전북","충남","전북","전남","전남","경남","경남","경북","전남",
                          "대구","경북","경북","충남","전남","전남","경북","전남","경북","경남","전남","부산","충남","충북","대구","경남","대구","전북",
                          "전남","경북","경남","전남","경남","대구","전남","경북","전남","경남","전남","경남","전북","경남","충남","충북","전남","전북",
                          "경북","경남","충남","전북","전남","전북","경남","전남","충남","전북","경북","경남","경북","충남","전남","경북","경북","충북",
                          "경남","경북","경북","부산","전남","경북","전북","전북","대구","전남","충남","충남","충남","경북","경남","충북","경북","경남",
                          "경북","충남","경북","전북","대구","전남","대구","전남","충남","대구","전북","경남","충남","전남","대구","전남","전남","부산",
                          "경북","전북","경남","경남","경남","경북","전남","충남","전남","충북","경북","전북","경북","전북","경남","전남","경북","경남",
                          "전남","경북","충북","전남","전남","전북","대구","전북","대구","경북","경남","전남","충남","전북","대구"
        ],
        "ktteam_branch": ["충주운용팀","홍성운용팀","목포운용부","충주운용팀","청주운용부","안동운용부","북부산운용부","창원운용부","충주운용팀",
                          "천안운용부","울산운용팀","대전운용팀","순천운용부","대전운용팀","구미운용부","안동운용부","동진주운용부","동진주운용부",
                          "청주운용부","충주운용팀","전주운용부","충주운용팀","목포운용부","충주운용팀","동대구운용부","동대구운용부","순천운용부",
                          "구미운용부","전주운용부","동진주운용부","울산운용팀","홍성운용팀","동대구운용부","구미운용부","충주운용팀","창원운용부",
                          "창원운용부","구미운용부","진천운용팀","포항운용부","안동운용부","안동운용부","포항운용부","포항운용부","포항운용부",
                          "안동운용부","진천운용팀","홍성운용팀","포항운용부","창원운용부","순천운용부","구미운용부","순천운용부","창원운용부",
                          "진천운용팀","서대구운용부","동진주운용부","순천운용부","구미운용부","대전운용팀","울산운용팀","울산운용팀","동진주운용부",
                          "정읍운용팀","홍성운용팀","광주운용부","순천운용부","목포운용부","동대구운용부","둔산운용부","전주운용부","순천운용부",
                          "포항운용부","서대구운용부","정읍운용팀","동대구운용부","안동운용부","창원운용부","목포운용부","목포운용부","홍성운용팀",
                          "동진주운용부","광주운용부","홍성운용팀","홍성운용팀","서대구운용부","창원운용부","홍성운용팀","전주운용부","광주운용부",
                          "창원운용부","홍성운용팀","동진주운용부","안동운용부","동부산운용부","전주운용부","동진주운용부","동진주운용부","동진주운용부",
                          "정읍운용팀","서대구운용부","익산운용부","포항운용부","익산운용부","서광주운용팀","포항운용부","충주운용팀","순천운용부",
                          "순천운용부","전주운용부","동대구운용부","홍성운용팀","구미운용부","천안운용부","포항운용부","익산운용부","대전운용팀",
                          "홍성운용팀","순천운용부","순천운용부","둔산운용부","진천운용팀","전주운용부","순천운용부","둔산운용부","안동운용부",
                          "정읍운용팀","청주운용부","충주운용팀","진천운용팀","창원운용부","홍성운용팀","순천운용부","청주운용부","포항운용부",
                          "전주운용부","창원운용부","순천운용부","구미운용부","울산운용팀","안동운용부","동진주운용부","전주운용부","동진주운용부",
                          "서대구운용부","전주운용부","안동운용부","청주운용부","포항운용부","홍성운용팀","창원운용부","동진주운용부","안동운용부",
                          "서대구운용부","서광주운용팀","순천운용부","목포운용부","대전운용팀","청주운용부","창원운용부","목포운용부","청주운용부",
                          "목포운용부","순천운용부","구미운용부","창원운용부","포항운용부","홍성운용팀","홍성운용팀","충주운용팀","진천운용팀",
                          "목포운용부","광주운용부","서광주운용팀","전주운용부","청주운용부","익산운용부","둔산운용부","전주운용부","안동운용부",
                          "익산운용부","순천운용부","창원운용부","서대구운용부","창원운용부","익산운용부","동부산운용부","광주운용부","충주운용팀",
                          "서대구운용부","서광주운용팀","창원운용부","목포운용부","목포운용부","전주운용부","목포운용부","서광주운용팀","청주운용부",
                          "동대구운용부","서대구운용부","목포운용부","포항운용부","서대구운용부","포항운용부","포항운용부","청주운용부","홍성운용팀",
                          "창원운용부","포항운용부","안동운용부","동대구운용부","동진주운용부","울산운용팀","포항운용부","익산운용부","구미운용부",
                          "서대구운용부","구미운용부","순천운용부","안동운용부","구미운용부","구미운용부","광주운용부","광주운용부","창원운용부",
                          "동대구운용부","동대구운용부","홍성운용팀","목포운용부","동진주운용부","홍성운용팀","진천운용팀","청주운용부","구미운용부",
                          "포항운용부","창원운용부","울산운용팀","동대구운용부","서광주운용팀","홍성운용팀","포항운용부","안동운용부","순천운용부",
                          "청주운용부","대전운용팀","서대구운용부","순천운용부","전주운용부","홍성운용팀","청주운용부","둔산운용부","홍성운용팀",
                          "창원운용부","울산운용팀","청주운용부","울산운용팀","정읍운용팀","정읍운용팀","포항운용부","둔산운용부","창원운용부",
                          "둔산운용부","목포운용부","포항운용부","포항운용부","순천운용부","동진주운용부","동진주운용부","동진주운용부","대전운용팀",
                          "서광주운용팀","순천운용부","둔산운용부","충주운용팀","포항운용부","목포운용부","북부산운용부","북부산운용부","전주운용부",
                          "서대구운용부","서광주운용팀","구미운용부","구미운용부","울산운용팀","구미운용부","안동운용부","동진주운용부","충주운용팀",
                          "광주운용부","창원운용부","서광주운용팀","동대구운용부","서대구운용부","서대구운용부","서대구운용부","포항운용부","서광주운용팀",
                          "안동운용부","창원운용부","동진주운용부","안동운용부","안동운용부","동진주운용부","창원운용부","안동운용부","동대구운용부",
                          "포항운용부","전주운용부","동진주운용부","창원운용부","울산운용팀","구미운용부","동진주운용부","동진주운용부","서대구운용부",
                          "전주운용부","충주운용팀","창원운용부","동진주운용부","동대구운용부","구미운용부","둔산운용부","구미운용부","전주운용부",
                          "광주운용부","서광주운용팀","목포운용부","대전운용팀","서광주운용팀","서광주운용팀","구미운용부","동진주운용부","포항운용부",
                          "포항운용부","동진주운용부","정읍운용팀","전주운용부","창원운용부","순천운용부","전주운용부","충주운용팀","홍성운용팀",
                          "전주운용부","익산운용부","서대구운용부","순천운용부","창원운용부","동대구운용부","익산운용부","서광주운용팀","북부산운용부",
                          "홍성운용팀","동대구운용부","서광주운용팀","광주운용부","창원운용부","포항운용부","안동운용부","홍성운용팀","대전운용팀",
                          "홍성운용팀","울산운용팀","안동운용부","서대구운용부","전주운용부","홍성운용팀","진천운용팀","포항운용부","순천운용부",
                          "서광주운용팀","둔산운용부","구미운용부","정읍운용팀","충주운용팀","구미운용부","진천운용팀","울산운용팀","동진주운용부",
                          "천안운용부","광주운용부","충주운용팀","순천운용부","포항운용부","대전운용팀","안동운용부","둔산운용부","진천운용팀",
                          "목포운용부","충주운용팀","순천운용부","충주운용팀","안동운용부","목포운용부","창원운용부","순천운용부","안동운용부",
                          "서대구운용부","홍성운용팀","안동운용부","순천운용부","전주운용부","서대구운용부","서광주운용팀","동대구운용부","충주운용팀",
                          "충주운용팀","광주운용부","울산운용팀","광주운용부","서대구운용부","포항운용부","광주운용부","동진주운용부","동진주운용부",
                          "전주운용부","동대구운용부","홍성운용팀","천안운용부","안동운용부","청주운용부","순천운용부","서광주운용팀","동진주운용부",
                          "안동운용부","둔산운용부","동진주운용부","둔산운용부","정읍운용팀","울산운용팀","서대구운용부","대전운용팀","울산운용팀",
                          "울산운용팀","순천운용부","천안운용부","충주운용팀","동진주운용부","동대구운용부","천안운용부","순천운용부","청주운용부",
                          "서광주운용팀","둔산운용부","목포운용부","전주운용부","청주운용부","순천운용부","익산운용부","홍성운용팀","포항운용부",
                          "목포운용부","구미운용부","동진주운용부","둔산운용부","전주운용부","서대구운용부","동진주운용부","구미운용부","익산운용부",
                          "홍성운용팀","전주운용부","순천운용부","포항운용부","익산운용부","목포운용부","목포운용부","순천운용부","목포운용부",
                          "광주운용부","청주운용부","창원운용부","천안운용부","동진주운용부","울산운용팀","서대구운용부","동대구운용부","포항운용부",
                          "광주운용부","충주운용팀","포항운용부","북부산운용부","충주운용팀","홍성운용팀","전주운용부","충주운용팀","동진주운용부",
                          "충주운용팀","동대구운용부","북부산운용부","홍성운용팀","구미운용부","북부산운용부","목포운용부","서대구운용부","천안운용부",
                          "구미운용부","포항운용부","충주운용팀","포항운용부","천안운용부","충주운용팀","홍성운용팀","목포운용부","순천운용부",
                          "서광주운용팀","동진주운용부","광주운용부","창원운용부","전주운용부","동진주운용부","창원운용부","구미운용부","광주운용부",
                          "전주운용부","서대구운용부","안동운용부","청주운용부","충주운용팀","목포운용부","진천운용팀","홍성운용팀","구미운용부",
                          "청주운용부","서광주운용팀","순천운용부","둔산운용부","포항운용부","서광주운용팀","창원운용부","울산운용팀","청주운용부",
                          "동진주운용부","순천운용부","홍성운용팀","목포운용부","청주운용부","북부산운용부","동진주운용부","동진주운용부","포항운용부",
                          "서대구운용부","울산운용팀","안동운용부","서광주운용팀","창원운용부","전주운용부","동진주운용부","서대구운용부","울산운용팀",
                          "둔산운용부","둔산운용부","창원운용부","홍성운용팀","울산운용팀","충주운용팀","서광주운용팀","울산운용팀","진천운용팀",
                          "동진주운용부","창원운용부","진천운용팀","익산운용부","목포운용부","천안운용부","서광주운용팀","동대구운용부","서대구운용부",
                          "서대구운용부","충주운용팀","전주운용부","구미운용부","목포운용부","전주운용부","대전운용팀","울산운용팀","동진주운용부",
                          "창원운용부","안동운용부","서대구운용부","정읍운용팀","순천운용부","충주운용팀","포항운용부","동진주운용부","천안운용부",
                          "목포운용부","둔산운용부","포항운용부","충주운용팀","서대구운용부","전주운용부","충주운용팀","동대구운용부","순천운용부",
                          "광주운용부","대전운용팀","전주운용부","동대구운용부","순천운용부","동진주운용부","울산운용팀","익산운용부","진천운용팀",
                          "광주운용부","홍성운용팀","안동운용부","둔산운용부","충주운용팀","울산운용팀","창원운용부","동대구운용부","서대구운용부",
                          "동진주운용부","서광주운용팀","진천운용팀","둔산운용부","서대구운용부","홍성운용팀","창원운용부","포항운용부","전주운용부",
                          "홍성운용팀","안동운용부","서광주운용팀","목포운용부","안동운용부","익산운용부","대전운용팀","동대구운용부","구미운용부",
                          "안동운용부","정읍운용팀","익산운용부","대전운용팀","동진주운용부","구미운용부","창원운용부","광주운용부","서대구운용부",
                          "동진주운용부","동대구운용부","청주운용부","광주운용부","목포운용부","서광주운용팀","포항운용부","천안운용부","구미운용부",
                          "구미운용부","목포운용부","전주운용부","홍성운용팀","서대구운용부","서광주운용팀","안동운용부","홍성운용팀","청주운용부",
                          "순천운용부","동진주운용부","동진주운용부","순천운용부","둔산운용부","안동운용부","홍성운용팀","동진주운용부","동대구운용부",
                          "동대구운용부","포항운용부","동진주운용부","목포운용부","전주운용부","포항운용부","구미운용부","진천운용팀","목포운용부",
                          "창원운용부","울산운용팀","광주운용부","포항운용부","전주운용부","정읍운용팀","동진주운용부","전주운용부","구미운용부",
                          "천안운용부","전주운용부","전주운용부","홍성운용팀","서대구운용부","대전운용팀","동진주운용부","창원운용부","청주운용부",
                          "정읍운용팀","창원운용부","홍성운용팀","순천운용부","서광주운용팀","충주운용팀","동진주운용부","서광주운용팀","충주운용팀",
                          "동진주운용부","동진주운용부","안동운용부","광주운용부","동진주운용부","창원운용부","포항운용부","광주운용부","익산운용부",
                          "울산운용팀","서광주운용팀","구미운용부","구미운용부","창원운용부","동대구운용부","동대구운용부","서대구운용부","동대구운용부",
                          "목포운용부","충주운용팀","광주운용부","충주운용팀","진천운용팀","천안운용부","동진주운용부","동대구운용부","목포운용부",
                          "서광주운용팀","목포운용부","울산운용팀","대전운용팀","전주운용부","구미운용부","동대구운용부","청주운용부","동진주운용부",
                          "안동운용부","구미운용부","동진주운용부","순천운용부","목포운용부","포항운용부","대전운용팀","포항운용부","전주운용부",
                          "안동운용부","동진주운용부","대전운용팀","동진주운용부","창원운용부","충주운용팀","구미운용부","익산운용부","정읍운용팀",
                          "충주운용팀","동진주운용부","목포운용부","창원운용부","동진주운용부","동진주운용부","홍성운용팀","포항운용부","안동운용부",
                          "동대구운용부","홍성운용팀","동진주운용부","울산운용팀","익산운용부","광주운용부","서대구운용부","서광주운용팀","동진주운용부",
                          "동진주운용부","목포운용부","안동운용부","동대구운용부","광주운용부","울산운용팀","안동운용부","홍성운용팀","포항운용부",
                          "안동운용부","홍성운용팀","서대구운용부","서대구운용부","안동운용부","목포운용부","동진주운용부","서대구운용부","울산운용팀",
                          "익산운용부","천안운용부","목포운용부","동대구운용부","전주운용부","순천운용부","천안운용부","익산운용부","천안운용부",
                          "정읍운용팀","창원운용부","익산운용부","광주운용부","대전운용팀","창원운용부","서대구운용부","익산운용부","창원운용부",
                          "광주운용부","창원운용부","목포운용부","정읍운용팀","울산운용팀","홍성운용팀","목포운용부","홍성운용팀","동진주운용부",
                          "목포운용부","서광주운용팀","순천운용부","서대구운용부","서대구운용부","진천운용팀","목포운용부","전주운용부","충주운용팀",
                          "홍성운용팀","충주운용팀","둔산운용부","천안운용부","안동운용부","동대구운용부","충주운용팀","울산운용팀","청주운용부",
                          "충주운용팀","서광주운용팀","대전운용팀","서대구운용부","목포운용부","순천운용부","전주운용부","포항운용부","포항운용부",
                          "동진주운용부","진천운용팀","창원운용부","순천운용부","홍성운용팀","천안운용부","서광주운용팀","홍성운용팀","천안운용부",
                          "동진주운용부","목포운용부","대전운용팀","충주운용팀","충주운용팀","목포운용부","천안운용부","홍성운용팀","목포운용부",
                          "동진주운용부","서대구운용부","충주운용팀","광주운용부","광주운용부","안동운용부","충주운용팀","천안운용부","충주운용팀",
                          "목포운용부","전주운용부","서대구운용부","안동운용부","청주운용부","천안운용부","전주운용부","충주운용팀","홍성운용팀",
                          "안동운용부","순천운용부","창원운용부","동부산운용부","전주운용부","목포운용부","천안운용부","포항운용부","서광주운용팀",
                          "둔산운용부","진천운용팀","구미운용부","충주운용팀","대전운용팀","구미운용부","동대구운용부","홍성운용팀","목포운용부",
                          "홍성운용팀","정읍운용팀","창원운용부","천안운용부","목포운용부","포항운용부","목포운용부","홍성운용팀","동진주운용부",
                          "구미운용부","홍성운용팀","홍성운용팀","구미운용부","홍성운용팀","순천운용부","동대구운용부","진천운용팀","천안운용부",
                          "구미운용부","목포운용부","목포운용부","안동운용부","목포운용부","전주운용부","목포운용부","서광주운용팀","창원운용부",
                          "서광주운용팀","안동운용부","홍성운용팀","대전운용팀","구미운용부","서대구운용부","전주운용부","홍성운용팀","순천운용부",
                          "동대구운용부","동대구운용부","천안운용부","둔산운용부","광주운용부","안동운용부","동진주운용부","목포운용부","청주운용부",
                          "청주운용부","둔산운용부","서대구운용부","천안운용부","순천운용부","진천운용팀","전주운용부","정읍운용팀","전주운용부",
                          "구미운용부","구미운용부","포항운용부","동진주운용부","청주운용부","안동운용부","홍성운용팀","안동운용부","전주운용부",
                          "홍성운용팀","목포운용부","동진주운용부","안동운용부","동진주운용부","목포운용부","익산운용부","전주운용부","안동운용부",
                          "창원운용부","홍성운용팀","포항운용부","목포운용부","동대구운용부","광주운용부","목포운용부","충주운용팀","광주운용부",
                          "진천운용팀","동진주운용부","서광주운용팀","동대구운용부","서대구운용부","목포운용부","광주운용부","포항운용부","구미운용부",
                          "둔산운용부","창원운용부","포항운용부","홍성운용팀","진천운용팀","포항운용부","순천운용부","청주운용부","동진주운용부",
                          "목포운용부","대전운용팀","구미운용부","안동운용부","충주운용팀","안동운용부","홍성운용팀","둔산운용부","익산운용부",
                          "충주운용팀","홍성운용팀","익산운용부","창원운용부","목포운용부","서대구운용부","둔산운용부","순천운용부","서대구운용부",
                          "목포운용부","홍성운용팀","전주운용부","대전운용팀","충주운용팀","포항운용부","울산운용팀","광주운용부","포항운용부",
                          "전주운용부","동진주운용부","진천운용팀","동진주운용부","서대구운용부","서광주운용팀","천안운용부","순천운용부","순천운용부",
                          "구미운용부","동진주운용부","창원운용부","안동운용부","천안운용부","목포운용부","충주운용팀","목포운용부","포항운용부",
                          "동진주운용부","순천운용부","순천운용부","창원운용부","안동운용부","동진주운용부","서광주운용팀","천안운용부","충주운용팀",
                          "동대구운용부","포항운용부","동진주운용부","천안운용부","진천운용팀","동진주운용부","동진주운용부","광주운용부","안동운용부",
                          "서대구운용부","서대구운용부","진천운용팀","전주운용부","익산운용부","안동운용부","동진주운용부","청주운용부","청주운용부",
                          "순천운용부","홍성운용팀","안동운용부","포항운용부","구미운용부","광주운용부","구미운용부","익산운용부","순천운용부",
                          "광주운용부","안동운용부","구미운용부","익산운용부","홍성운용팀","포항운용부","구미운용부","서광주운용팀","동진주운용부",
                          "목포운용부","서대구운용부","포항운용부","전주운용부","안동운용부","대전운용팀","안동운용부","동대구운용부","목포운용부",
                          "서광주운용팀","익산운용부","포항운용부","순천운용부","서대구운용부","순천운용부","서대구운용부","홍성운용팀","순천운용부",
                          "청주운용부","동진주운용부","창원운용부","전주운용부","홍성운용팀","동진주운용부","동대구운용부","순천운용부","안동운용부",
                          "포항운용부","동진주운용부","전주운용부","홍성운용팀","광주운용부","구미운용부","둔산운용부","서대구운용부","서대구운용부",
                          "목포운용부","동대구운용부","순천운용부","서대구운용부","청주운용부","순천운용부","서대구운용부","창원운용부","창원운용부",
                          "포항운용부","동대구운용부","동진주운용부","익산운용부","광주운용부","목포운용부","동진주운용부","둔산운용부","정읍운용팀",
                          "광주운용부","창원운용부","서대구운용부","창원운용부","순천운용부","동진주운용부","포항운용부","포항운용부","서대구운용부",
                          "청주운용부","둔산운용부","동진주운용부","순천운용부","창원운용부","홍성운용팀","전주운용부","광주운용부","서대구운용부",
                          "광주운용부","천안운용부","전주운용부","순천운용부","창원운용부","울산운용팀","동진주운용부","울산운용팀","순천운용부",
                          "익산운용부","광주운용부","청주운용부","광주운용부","천안운용부","울산운용팀","포항운용부","전주운용부","목포운용부",
                          "둔산운용부","홍성운용팀","홍성운용팀","동진주운용부","익산운용부","창원운용부","포항운용부","창원운용부","순천운용부",
                          "동진주운용부","구미운용부","익산운용부","순천운용부","안동운용부","목포운용부","순천운용부","창원운용부","서대구운용부",
                          "둔산운용부","광주운용부","창원운용부","충주운용팀","순천운용부","서광주운용팀","안동운용부","동진주운용부","서광주운용팀",
                          "창원운용부","안동운용부","서대구운용부","순천운용부","안동운용부","정읍운용팀","전주운용부","울산운용팀","동진주운용부",
                          "포항운용부","창원운용부","목포운용부","서광주운용팀","전주운용부","창원운용부","동대구운용부","동대구운용부","창원운용부",
                          "동진주운용부","순천운용부","동진주운용부","창원운용부","홍성운용팀","동진주운용부","대전운용팀","구미운용부","홍성운용팀",
                          "대전운용팀","천안운용부","홍성운용팀","목포운용부","창원운용부","홍성운용팀","둔산운용부","목포운용부","홍성운용팀",
                          "서대구운용부","진천운용팀","충주운용팀","동진주운용부","창원운용부","전주운용부","전주운용부","동대구운용부","광주운용부",
                          "청주운용부","청주운용부","홍성운용팀","진천운용팀","둔산운용부","포항운용부","포항운용부","울산운용팀","순천운용부",
                          "안동운용부","전주운용부","순천운용부","광주운용부","전주운용부","천안운용부","목포운용부","목포운용부","포항운용부",
                          "안동운용부","동대구운용부","서광주운용팀","안동운용부","안동운용부","목포운용부","동진주운용부","목포운용부","창원운용부",
                          "홍성운용팀","익산운용부","안동운용부","목포운용부","광주운용부","동진주운용부","구미운용부","충주운용팀","정읍운용팀",
                          "천안운용부","동대구운용부","목포운용부","동대구운용부","동대구운용부","목포운용부","창원운용부","청주운용부","홍성운용팀",
                          "동진주운용부","서대구운용부","포항운용부","진천운용팀","목포운용부","목포운용부","북부산운용부","창원운용부","동진주운용부",
                          "창원운용부","동진주운용부","목포운용부","광주운용부","포항운용부","목포운용부","전주운용부","동진주운용부","전주운용부",
                          "둔산운용부","순천운용부","홍성운용팀","둔산운용부","전주운용부","진천운용팀","창원운용부","동진주운용부","대전운용팀",
                          "동진주운용부","동진주운용부","구미운용부","순천운용부","창원운용부","목포운용부","홍성운용팀","홍성운용팀","홍성운용팀",
                          "안동운용부","동진주운용부","안동운용부","전주운용부","충주운용팀","전주운용부","둔산운용부","둔산운용부","둔산운용부",
                          "창원운용부","목포운용부","동부산운용부","동대구운용부","동진주운용부","홍성운용팀","서광주운용팀","대전운용팀","정읍운용팀",
                          "울산운용팀","포항운용부","포항운용부","전주운용부","동진주운용부","창원운용부","안동운용부","대전운용팀","순천운용부",
                          "청주운용부","구미운용부","순천운용부","울산운용팀","익산운용부","구미운용부","동진주운용부","홍성운용팀","안동운용부",
                          "충주운용팀","둔산운용부","홍성운용팀","전주운용부","순천운용부","포항운용부","울산운용팀","창원운용부","충주운용팀",
                          "전주운용부","홍성운용팀","서광주운용팀","창원운용부","서광주운용팀","동진주운용부","홍성운용팀","포항운용부","포항운용부",
                          "순천운용부","서대구운용부","순천운용부","홍성운용팀","목포운용부","순천운용부","정읍운용팀","홍성운용팀","창원운용부",
                          "안동운용부","구미운용부","천안운용부","서대구운용부","포항운용부","구미운용부","창원운용부","포항운용부","전주운용부",
                          "홍성운용팀","대전운용팀","창원운용부","둔산운용부","홍성운용팀","순천운용부","목포운용부","구미운용부","진천운용팀",
                          "포항운용부","포항운용부","동진주운용부","목포운용부","구미운용부","동대구운용부","북부산운용부","목포운용부","동진주운용부",
                          "광주운용부","창원운용부","구미운용부","서대구운용부","서대구운용부","구미운용부","동진주운용부","동대구운용부","순천운용부",
                          "창원운용부","목포운용부","안동운용부","대전운용팀","동진주운용부","진천운용팀","순천운용부","울산운용팀","창원운용부",
                          "구미운용부","울산운용팀","천안운용부","홍성운용팀","동진주운용부","서대구운용부","순천운용부","동진주운용부","광주운용부",
                          "포항운용부","북부산운용부","천안운용부","포항운용부","포항운용부","홍성운용팀","울산운용팀","홍성운용팀","안동운용부",
                          "서대구운용부","안동운용부","동부산운용부","목포운용부","동진주운용부","안동운용부","홍성운용팀","홍성운용팀","목포운용부",
                          "구미운용부","청주운용부","목포운용부","청주운용부","홍성운용팀","천안운용부","진천운용팀","광주운용부","익산운용부",
                          "안동운용부","동대구운용부","진천운용팀","동대구운용부","동대구운용부","충주운용팀","익산운용부","포항운용부","둔산운용부",
                          "동진주운용부","순천운용부","순천운용부","창원운용부","서대구운용부","창원운용부","진천운용팀","홍성운용팀","진천운용팀",
                          "둔산운용부","창원운용부","대전운용팀","동진주운용부","대전운용팀","안동운용부","포항운용부","순천운용부","안동운용부",
                          "안동운용부","광주운용부","목포운용부","홍성운용팀","동대구운용부","창원운용부","순천운용부","정읍운용팀","창원운용부",
                          "창원운용부","진천운용팀","동진주운용부","포항운용부","홍성운용팀","둔산운용부","안동운용부","정읍운용팀","천안운용부",
                          "창원운용부","진천운용팀","순천운용부","정읍운용팀","포항운용부","울산운용팀","안동운용부","대전운용팀","울산운용팀",
                          "목포운용부","창원운용부","동대구운용부","구미운용부","안동운용부","홍성운용팀","대전운용팀","동대구운용부","목포운용부",
                          "전주운용부","홍성운용팀","정읍운용팀","서광주운용팀","순천운용부","창원운용부","동진주운용부","포항운용부","순천운용부",
                          "동대구운용부","안동운용부","안동운용부","천안운용부","서광주운용팀","순천운용부","안동운용부","순천운용부","안동운용부",
                          "동진주운용부","광주운용부","동부산운용부","대전운용팀","진천운용팀","서대구운용부","동진주운용부","동대구운용부",
                          "전주운용부","목포운용부","안동운용부","동진주운용부","목포운용부","동진주운용부","서대구운용부","순천운용부","포항운용부",
                          "서광주운용팀","동진주운용부","목포운용부","창원운용부","정읍운용팀","동진주운용부","홍성운용팀","충주운용팀","목포운용부",
                          "익산운용부","포항운용부","창원운용부","홍성운용팀","전주운용부","순천운용부","정읍운용팀","동진주운용부","목포운용부",
                          "홍성운용팀","정읍운용팀","구미운용부","창원운용부","포항운용부","천안운용부","목포운용부","포항운용부","포항운용부",
                          "진천운용팀","창원운용부","안동운용부","포항운용부","북부산운용부","순천운용부","포항운용부","전주운용부","익산운용부",
                          "동대구운용부","서광주운용팀","홍성운용팀","홍성운용팀","홍성운용팀","구미운용부","동진주운용부","충주운용팀","구미운용부",
                          "창원운용부","안동운용부","둔산운용부","구미운용부","전주운용부","동대구운용부","광주운용부","동대구운용부","목포운용부",
                          "홍성운용팀","서대구운용부","전주운용부","울산운용팀","홍성운용팀","순천운용부","서대구운용부","목포운용부","순천운용부",
                          "동부산운용부","안동운용부","전주운용부","창원운용부","울산운용팀","창원운용부","안동운용부","순천운용부","둔산운용부",
                          "목포운용부","청주운용부","구미운용부","익산운용부","포항운용부","익산운용부","동진주운용부","목포운용부","포항운용부",
                          "울산운용팀","순천운용부","안동운용부","청주운용부","목포운용부","순천운용부","익산운용부","서대구운용부","전주운용부",
                          "동대구운용부","안동운용부","동진주운용부","목포운용부","대전운용팀","정읍운용팀","동대구운용부"
        ],
        "MOSteam_branch": ["충주","서산","해남","충주","청주","문경","김해","진주","충주","천안","동부산","논산","순천","동대전","문경","안동","통영","진주","청주","충주","전주","충주","해남","충주","동대구","동대구","남원","문경","남원","진주","울산","홍성","동대구","문경","충주","김해","창원","구미","충주","동대구","안동","문경","포항","포항","포항","안동","청주","서산","포항","창원","순천","구미","순천","진주","청주","남대구","통영","순천","문경","서대전","울산","울산","진주","정읍","홍성","북광주","순천","해남","동대구","세종","남원","남원","포항","서대구","정읍","동대구","안동","창원","목포","해남","서산","진주","북광주","서산","홍성","구미","김해","서산","전주","북광주","창원","홍성","진주","안동","동부산","남원","진주","진주","진주","정읍","남대구","익산","포항","전주","서광주","포항","충주","순천","남원","남원","동대구","홍성","구미","천안","포항","익산","논산","홍성","순천","남원","세종","청주","전주","순천","세종","문경","정읍","동대전","충주","청주","김해","논산","순천","청주","포항","북광주","창원","순천","구미","울산","안동","통영","전주","통영","남대구","전주","문경","동대전","포항","홍성","창원","진주","안동","서대구","서광주","순천","목포","서대전","동대전","창원","목포","동대전","해남","순천","구미","진주","포항","논산","서산","충주","청주","목포","북광주","서광주","북광주","청주","전주","세종","전주","문경","익산","순천","김해","서대구","창원","전주","동부산","북광주","충주","서대구","서광주","창원","해남","목포","남원","목포","서광주","청주","동대구","서대구","해남","포항","서대구","포항","포항","청주","서산","김해","포항","안동","동대구","진주","울산","포항","익산","문경","서대구","문경","순천","문경","구미","구미","북광주","서광주","김해","동대구","동대구","서산","목포","진주","홍성","청주","청주","문경","포항","창원","울산","동대구","서광주","홍성","포항","안동","순천","청주","동대전","남대구","순천","전주","서산","동대전","세종","논산","김해","동부산","청주","울산","정읍","정읍","동대구","세종","창원","세종","해남","포항","포항","북광주","진주","진주","통영","논산","서광주","순천","서대전","충주","포항","해남","김해","김해","남원","남대구","서광주","구미","구미","울산","문경","안동","진주","충주","북광주","창원","서광주","동대구","서대구","서대구","남대구","포항","서광주","문경","창원","진주","문경","안동","진주","김해","안동","동대구","포항","북광주","통영","진주","울산","문경","진주","통영","서대구","남원","충주","창원","진주","동대구","구미","세종","구미","전주","북광주","서광주","북광주","동대전","서광주","서광주","구미","진주","포항","포항","진주","정읍","남원","창원","순천","남원","충주","홍성","전주","익산","구미","순천","진주","남대구","익산","서광주","김해","홍성","동대구","서광주","북광주","창원","동대구","안동","서산","동대전","홍성","동부산","문경","남대구","남원","홍성","청주","포항","순천","서광주","세종","구미","정읍","충주","구미","충주","울산","통영","천안","북광주","충주","순천","동대구","논산","안동","서대전","청주","해남","충주","순천","충주","안동","목포","창원","순천","문경","서대구","서산","문경","순천","북광주","서대구","서광주","동대구","충주","충주","북광주","동부산","북광주","서대구","포항","북광주","통영","통영","전주","서대구","홍성","천안","안동","동대전","순천","서광주","진주","안동","서대전","통영","세종","정읍","울산","남대구","논산","울산","울산","순천","천안","충주","통영","서대구","천안","북광주","청주","서광주","세종","해남","전주","동대전","남원","전주","논산","포항","해남","문경","통영","세종","전주","서대구","진주","문경","전주","서산","전주","순천","포항","익산","목포","목포","순천","목포","북광주","동대전","김해","천안","진주","울산","서대구","동대구","포항","북광주","충주","포항","김해","충주","서산","전주","충주","통영","충주","동대구","서부산","서산","문경","서부산","목포","서대구","천안","문경","포항","충주","포항","천안","충주","홍성","목포","순천","서광주","진주","북광주","김해","전주","진주","김해","구미","북광주","전주","서대구","안동","동대전","충주","해남","청주","논산","구미","청주","서광주","남원","세종","포항","서광주","창원","동부산","동대전","통영","북광주","홍성","목포","청주","김해","진주","진주","포항","서대구","울산","안동","서광주","창원","남원","진주","남대구","울산","세종","세종","창원","서산","동부산","충주","서광주","울산","청주","통영","진주","청주","전주","목포","천안","서광주","서대구","서대구","서대구","충주","전주","문경","해남","남원","논산","울산","통영","창원","안동","서대구","정읍","순천","충주","포항","통영","천안","해남","세종","포항","충주","서대구","남원","충주","동대구","북광주","북광주","서대전","북광주","동대구","순천","진주","울산","전주","청주","북광주","홍성","안동","세종","충주","울산","창원","동대구","서대구","진주","서광주","청주","세종","구미","서산","창원","포항","전주","서산","안동","서광주","목포","안동","전주","서대전","동대구","구미","안동","정읍","전주","논산","통영","구미","김해","북광주","서대구","진주","동대구","청주","서광주","해남","서광주","포항","천안","문경","문경","목포","전주","홍성","서대구","서광주","문경","논산","청주","남원","진주","통영","순천","세종","안동","서산","진주","동대구","동대구","포항","통영","목포","남원","포항","문경","청주","북광주","김해","울산","북광주","동대구","남원","정읍","통영","남원","구미","천안","전주","남원","홍성","구미","서대전","통영","김해","동대전","정읍","창원","서산","순천","서광주","충주","진주","서광주","충주","진주","통영","안동","서광주","진주","창원","포항","북광주","익산","울산","서광주","구미","구미","김해","동대구","동대구","구미","남대구","북광주","충주","서광주","충주","청주","천안","진주","동대구","목포","서광주","목포","울산","서대전","전주","문경","동대구","동대전","통영","안동","구미","진주","순천","목포","포항","동대전","포항","전주","안동","진주","논산","진주","창원","충주","문경","익산","정읍","충주","진주","해남","김해","진주","진주","논산","포항","안동","서대구","홍성","진주","울산","익산","서광주","서대구","서광주","진주","진주","목포","안동","동대구","북광주","울산","문경","서산","포항","안동","논산","서대구","서대구","안동","해남","진주","서대구","동부산","익산","천안","해남","동대구","전주","순천","천안","익산","천안","정읍","창원","전주","북광주","논산","창원","남대구","익산","진주","서광주","창원","해남","정읍","울산","서산","해남","홍성","통영","해남","서광주","순천","구미","서대구","충주","해남","전주","충주","서산","충주","세종","천안","안동","동대구","충주","울산","동대전","충주","서광주","동대전","남대구","목포","순천","남원","포항","포항","진주","충주","김해","순천","서산","천안","서광주","서산","천안","진주","해남","동대전","충주","충주","해남","천안","홍성","해남","진주","서대구","충주","북광주","북광주","안동","충주","천안","충주","목포","남원","서대구","안동","동대전","천안","남원","충주","서산","안동","순천","창원","동부산","북광주","목포","천안","포항","서광주","세종","충주","문경","충주","서대전","구미","동대구","홍성","북광주","홍성","정읍","진주","천안","목포","포항","목포","서산","진주","문경","홍성","홍성","문경","서산","순천","동대구","충주","천안","구미","목포","해남","안동","목포","전주","해남","서광주","창원","서광주","안동","홍성","서대전","구미","남대구","남원","홍성","순천","동대구","동대구","천안","세종","서광주","안동","진주","목포","동대전","동대전","세종","남대구","천안","순천","청주","북광주","정읍","남원","구미","구미","동대구","진주","동대전","안동","서산","문경","전주","홍성","북광주","진주","안동","통영","목포","익산","전주","안동","김해","서산","포항","목포","동대구","북광주","목포","충주","북광주","충주","진주","서광주","동대구","서대구","해남","서광주","포항","구미","세종","창원","포항","홍성","청주","포항","순천","동대전","진주","해남","논산","구미","안동","충주","문경","서산","세종","익산","충주","서산","익산","창원","목포","구미","세종","순천","남대구","목포","논산","남원","논산","충주","포항","울산","북광주","포항","전주","통영","충주","통영","서대구","서광주","천안","순천","순천","문경","통영","김해","안동","천안","해남","충주","해남","포항","통영","순천","북광주","김해","안동","진주","서광주","천안","충주","동대구","포항","진주","천안","청주","진주","통영","북광주","안동","서대구","남대구","청주","남원","익산","문경","진주","청주","청주","순천","홍성","문경","포항","구미","북광주","구미","익산","순천","북광주","안동","문경","익산","논산","포항","구미","서광주","진주","해남","남대구","포항","남원","안동","동대전","안동","동대구","해남","서광주","익산","포항","남원","남대구","순천","구미","논산","순천","동대전","통영","김해","남원","홍성","통영","남대구","순천","문경","포항","통영","전주","홍성","북광주","구미","세종","남대구","서대구","북광주","동대구","순천","서대구","청주","북광주","서대구","창원","창원","포항","동대구","진주","전주","북광주","목포","진주","세종","정읍","북광주","김해","남대구","김해","순천","통영","동대구","포항","구미","동대전","세종","진주","순천","진주","홍성","남원","북광주","남대구","북광주","천안","전주","남원","창원","동부산","진주","울산",북광주","익산","북광주","동대전","북광주","천안","동부산","포항","전주","목포","세종","서산","홍성","통영","익산","창원","포항","김해","남원","진주","구미","전주","순천","안동","해남","순천","창원","남대구","세종","북광주","김해","충주","순천","서광주","안동","진주","서광주","창원","문경","서대구","순천","안동","정읍","전주","울산","진주","포항","진주","목포","서광주","전주","창원","동대구","동대구","창원","진주","순천","통영","김해","논산","통영","논산","문경","홍성","서대전","천안","서산","목포","김해","홍성","세종","목포","서산","구미","충주","충주","진주","창원","남원","전주","동대구","북광주","동대전","동대전","서산","청주","세종","포항","포항","울산","순천","안동","북광주","순천","북광주","남원","천안","해남","목포","동대구","안동","동대구","서광주","안동","안동","북광주","진주","목포","김해","논산","익산","안동","목포","북광주","진주","문경","충주","정읍","천안","동대구","목포","동대구","동대구","해남","창원","동대전","홍성","통영","구미","포항","청주","목포","북광주","서부산","창원","통영","김해","진주","목포","서광주","포항","해남","남원","통영","남원","세종","순천","논산","세종","북광주","충주","김해","진주","논산","진주","진주","구미","북광주","창원","북광주","홍성","논산","홍성","안동","통영","안동","전주","충주","북광주","세종","서대전","세종","진주","북광주","동부산","남대구","진주","홍성","서광주","동대전","정읍","울산","포항","포항","전주","진주","창원","안동","서대전","순천","동대전","구미","순천","울산","익산","구미","진주","논산","안동","충주","세종","홍성","남원","순천","포항","울산","김해","충주","남원","홍성","서광주","창원","서광주","통영","홍성","포항","포항","순천","서대구","순천","홍성","해남","순천","정읍","홍성","진주","안동","문경","천안","서대구","동대구","문경","김해","포항","전주","서산","동대전","진주","세종","서산","순천","목포","구미","충주","포항","포항","진주","목포","구미","서대구","김해","목포","통영","북광주","진주","구미","서대구","남대구","구미","진주","동대구","순천","김해","북광주","안동","서대전","진주","청주","순천","울산","창원","구미","울산","천안","서산","진주","서대구","순천","진주","북광주","포항","김해","천안","포항","포항","홍성","울산","서산","안동","서대구","문경","동부산","목포","통영","안동","홍성","홍성","목포","문경","동대전","해남","동대전","홍성","천안","청주","북광주","전주","안동","동대구","충주","동대구","동대구","충주","전주","포항","세종","진주","순천","순천","김해","서대구","김해","청주","논산","청주","세종","창원","동대전","통영","서대전","안동","포항","순천","안동","안동","북광주","해남","논산","동대구","진주","순천","정읍","창원","창원","충주","통영","포항","홍성","세종","안동","정읍","천안","창원","청주","순천","정읍","포항","울산","안동","동대전","동부산","해남","김해","서대구","구미","안동","논산","동대전","서대구","목포","북광주","서산","정읍","서광주","남원","김해","진주","포항","순천","동대구","안동","안동","천안","서광주","순천","문경","순천","안동","통영","서광주","동부산","서대전","청주","서대구","통영","동대구","남원","목포","안동","진주","목포","통영","서대구","순천","포항","서광주","통영","목포","창원","정읍","통영","논산","충주","목포","익산","포항","창원","논산","전주","순천","정읍","진주","목포","서산","정읍","구미","김해","포항","천안","목포","포항","포항","청주","창원","안동","포항","서부산","순천","포항","전주","익산","동대구","서광주","홍성","홍성","논산","문경","진주","충주","문경","김해","안동","세종","문경","전주","동대구","서광주","동대구","해남","홍성","구미","전주","울산","논산","순천","남대구","해남","순천","동부산","안동","전주","진주","동부산","창원","안동","순천","세종","해남","동대전","구미","익산","포항","전주","진주","해남","포항","울산","순천","안동","동대전","북광주","북광주","익산","구미","전주","동대구","안동","진주","목포","동대전","정읍","동대구"
        ],
        "office_branch": ["단양","당진","완도","충주","남청주","예천","부산강서","의령","단양","성환","양산","연무","녹동","동대전","서문경","의성","거제","거창","상당","충주","봉동","단양","해남","충주","청도","청도","구례","상주","임실","하동","남울산","홍성","하양","서문경","금왕","김해","창녕","김천","괴산","건천","서안동","예천","경주","안강","영덕","서안동","가경","서산","안강","함안","동여수","김천","순천","의령","가경","고령","고성","동여수","문경","금산","남울산","서울산","사천","부안","광천","곡성","동여수","해남","하양","공주","장수","구례","오천","성주","부안","영천","안동","영산","진도","완도","태안","하동","곡성","당진","삽교","군위","진영","서산","봉동","담양","창녕","보령","거창","안동","기장","남원","산청","사천","사천","부안","달성","서군산","오천","김제","나주","포항","충주","고흥","구례","임실","청도","청양","김천","천안","경주","동군산","논산","예산","광양","구례","공주","진천","무주","북순천","공주","안계","정읍","옥천","제천","진천","밀양","부여","순천","청주","포항","순창","마산","북순천","김천","남울산","의성","거제","남전주","장승포","달성","무주","안계","영동","포항","홍성","함안","사천","서안동","칠곡","영광","여수","진도","금산","옥천","함안","영암","옥천","완도","여수","동구미","의령","경주","부여","태안","충주","가경","진도","동광주","함평","순창","남청주","김제","세종","봉동","예천","부송","녹동","밀양","왜관","진북","김제","금정","담양","제천","성주","나주","진북","완도","영암","남원","영암","나주","남청주","영천","칠곡","해남","북포항","왜관","후포","영덕","청주","당진","밀양","울진","안동","청도","동진주","남울산","경주","동군산","상주","왜관","상주","북순천","안계","김천","공단","담양","장성","밀양","하양","청도","태안","대불","삼천포","청양","서청주","남청주","상주","영덕","영산","온산","경산","나주","보령","영덕","서안동","동여수","청주","동대전","고령","고흥","무주","태안","보은","공주","부여","김해","양주","상당","언양","부안","정읍","건천","세종","마산","공주","완도","경주","안강","보성","남해","하동","통영","논산","나주","동순천","유성","충주","울진","완도","부산강서","부산강서","장수","달성","영광","김천","김천","울산","서문경","청송","삼천포","금왕","화순","진북","나주","하양","왜관","성서","고령","안강","나주","안계","동마산","산청","안계","영주","산청","밀양","의성","영천","영덕","순창","고성","의령","울산","서문경","남해","고성","성주","남원","단양","창녕","진주","청도","김천","세종","김천","남전주","담양","영광","장흥","용전","함평","영광","김천","합천","포항","경주","남해","고창","남원","동마산","고흥","장수","금왕","예산","봉동","동군산","군위","여수","의령","상동","익산","나주","부산강서","보령","영천","상무","담양","창녕","건천","봉화","당진","용전","예산","양산","예천","고령","남원","삽교","진천","울진","여천","영광","공주","김천","정읍","단양","선산","괴산","남울산","거제","아산","화순","제천","녹동","건천","논산","서안동","유성","증평","강진","제천","북순천","금왕","봉화","영암","함안","고흥","예천","성주","서산","예천","고흥","순창","성서","송정","청도","충주","충주","북광주","양산","화순","왜관","경주","화순","거제","거제","동전주","동대구","홍성","아산","봉화","옥천","녹동","함평","지족","영주","유성","고성","유구","고창","언양","남대구","계룡","성남","언양","고흥","천안","단양","거제","동촌","아산","보성","청주","하남","유구","강진","진안","보은","구례","김제","서천","오천","해남","서문경","고성","공주","남전주","성주","함양","문경","김제","태안","무주","북여수","경주","함열","무안","하당","고흥","무안","본촌","영동","김해","천안","합천","남울산","왜관","청도","영덕","화순","단양","울진","부산강서","금왕","당진","동전주","제천","거제","충주","영천","사하","서산","상주","북부산","대불","성주","아산","상주","경주","충주","경주","천안","충주","삽교","무안","여천","영광","합천","동광주","밀양","진안","남해","밀양","선산","담양","무주","성주","안동","영동","충주","해남","진천","서천","구미","남청주","함평","구례","공주","오천","나주","함안","양산","영동","통영","보성","보령","영암","남청주","부산강서","지족","진주","경주","왜관","언양","영주","나주","마산","남원","동진주","달성","언양","공주","세종","영산","태안","양산","단양","나주","동울산","증평","고성","의령","진천","김제","양을산","천안","영광","동촌","성주","왜관","제천","진안","상주","해남","장수","논산","성남","통영","함안","봉화","성주","부안","순천","단양","영덕","고성","천안","완도","세종","경주","단양","성주","남원","음성","영천","보성","화순","금산","순창","영천","서광양","진주","언양","김제","서청주","담양","삽교","봉화","세종","제천","남울산","칠원","청도","성주","삼천포","나주","서청주","세종","군위","당진","영산","울진","진안","서산","청송","나주","양을산","청송","김제","금산","영천","김천","영주","고창","김제","논산","고성","김천","김해","화순","왜관","거창","영천","상당","장성","해남","영광","경주","천안","문경","문경","양을산","봉동","청양","북대구","하남","안계","서천","상당","구례","사천","거제","서광양","유구","의성","당진","사천","경산","영천","후포","통영","무안","남원","안강","상주","진천","장흥","김해","언양","화순","건천","남원","정읍","거제","남원","동구미","아산","봉동","장수","광천","군위","금산","통영","밀양","보은","정읍","함안","서산","북순천","나주","충주","거창","나주","충주","합천","거제","안동","장성","동진주","창원","울진","곡성","익산","언양","송정","김천","김천","밀양","영천","영천","군위","상동","장흥","음성","장성","금왕","진천","성환","산청","영천","대불","영광","대불","서울산","금산","전주","서문경","하양","영동","고성","영주","공단","합천","순천","영암","흥해","동대전","흥해","동전주","봉화","함양","논산","남해","동마산","제천","상주","서군산","고창","금왕","산청","완도","김해","산청","남해","서천","울릉","봉화","동대구","홍성","함양","온산","동군산","장성","성서","상무","사천","함양","영암","서안동","영천","곡성","언양","예천","당진","포항","영양","부여","왜관","왜관","봉화","해남","남해","성주","양산","서군산","아산","완도","하양","무주","광양","천안","익산","천안","고창","진해","김제","담양","논산","영산","고령","동군산","의령","장성","창녕","해남","고창","성남","서산","강진","보령","거제","완도","나주","녹동","군위","성주","괴산","완도","동전주","충주","태안","음성","세종","천안","봉화","청도","충주","언양","보은","충주","함평","신탄진","고령","양을산","북순천","남원","포항","북포항","사천","괴산","밀양","고흥","당진","아산","남광주","태안","천안","지족","해남","용전","제천","제천","해남","천안","삽교","강진","함양","성주","제천","화순","담양","영양","제천","천안","충주","양을산","남원","대구","영주","보은","성환","남원","충주","당진","영주","북순천","진북","기장","순창","영암","천안","북포항","함평","공주","괴산","문경","충주","금산","동구미","영천","예산","죽교","홍성","고창","의령","남천안","영암","경주","양을산","서산","산청","상주","예산","예산","상주","태안","광양","청도","괴산","아산","김천","양을산","강진","서안동","영암","진안","완도","하남","동마산","송정","청송","예산","금산","김천","달성","임실","합덕","여천","하양","영천","아산","공주","장성","청송","하동","진도","영동","영동","세종","고령","아산","순천","가경","순창","고창","남원","김천","김천","건천","하동","옥천","청송","태안","안계","무주","청양","장흥","함양","영주","통영","양을산","부송","진안","의성","진영","태안","경주","양을산","경산","곡성","양을산","충주","화순","괴산","합천","영광","영천","왜관","완도","장성","포항","김천","세종","창원","경주","예산","진천","경주","고흥","영동","동진주","완도","연무","동구미","서안동","단양","예천","태안","세종","서군산","충주","서산","부송","진북","양을산","군위","세종","동여수","고령","진도","서천","남원","논산","충주","경주","양정","화순","포항","진안","거제","괴산","고성","왜관","영광","아산","고흥","북순천","문경","고성","김해","영주","아산","해남","단양","완도","영덕","고성","고흥","보성","밀양","서안동","거창","나주","천안","금왕","영천","경주","진주","아산","서청주","진주","고성","곡성","서안동","왜관","달성","가경","임실","서군산","예천","남해","상당","상당","녹동","보령","예천","영덕","공단","곡성","선산","서군산","서광양","화순","의성","상주","서군산","서천","안강","선산","영광","하동","해남","달성","후포","남원","서안동","용전","서안동","하양","완도","나주","부송","안강","구례","달성","북순천","군위","부여","북순천","보은","거제","밀양","남원","보령","통영","상동","순천","예천","북포항","통영","진안","청양","담양","김천","공주","달성","성주","장흥","하양","북순천","왜관","남청주","보성","성주","진해","동마산","경주","하양","합천","김제","담양","하당","삼천포","세종","정읍","담양","김해","고령","밀양","여수","고성","건천","북포항","군위","옥천","공주","진주","동여수","의령","청양","남원","화순","고령","북광주","천안","봉동","구례","진해","양산","거창","서울산","보성","함열","담양","보은","곡성","천안","양산","오천","팔복","영암","세종","태안","보령","통영","동군산","마산","영덕","김해","구례","함양","구미","김제","여천","안동","해남","여천","영산","고령","공주","담양","밀양","제천","여수","함평","청송","하동","함평","함안","예천","성주","동여수","영주","부안","동전주","온산","거창","포항","의령","하당","상무","무주","칠원","청도","영천","함안","합천","여천","거제","김해","부여","고성","연무","함창","광천","금산","아산","서산","양을산","김해","예산","공주","진도","태안","군위","괴산","충주","동진주","창녕","남원","남전주","청도","화순","보은","옥천","태안","진천","공주","흥해","경주","언양","여천","서안동","순창","순천","담양","남원","아산","해남","하당","건천","서안동","영천","하남","봉화","안동","장흥","합천","양을산","밀양","부여","동군산","안동","진도","곡성","산청","상주","제천","정읍","성환","영천","양을산","하양","영천","강진","영산","보은","광천","통영","군위","포항","증평","무안","장흥","사하","영산","거제","진영","동진주","양을산","장성","흥해","해남","장수","거제","장수","공주","벌교","부여","세종","순창","괴산","김해","동진주","논산","사천","합천","동구미","보성","진해","장흥","청양","부여","보령","봉화","거제","영주","무주","단양","순창","세종","북대전","세종","의령","장흥","일광","상동","사천","청양","함평","동대전","정읍","울산","흥해","오천","진안","동진주","동마산","의성","금산","광양","영동","김천","벌교","언양","군산","김천","사천","서천","서안동","충주","공주","보령","남원","북순천","울진","동울산","김해","금왕","남원","보령","함평","진해","나주","통영","홍성","울진","북포항","광양","왜관","광양","보령","완도","여수","부안","홍성","의령","청송","상주","아산","왜관","건천","상주","밀양","흥해","남전주","태안","대전","의령","공주","당진","여천","양을산","김천","괴산","흥해","포항","함양","양을산","김천","동촌","부산강서","진도","장승포","광주","의령","김천","왜관","고령","김천","하동","하양","여천","진영","죽교","청송","금산","동진주","증평","광양","양정","진북","동구미","온산","천안","태안","남해","성주","북순천","산청","담양","영덕","부산강서","천안","울릉","경주","광천","성남","당진","안동","왜관","예천","기장","무안","고성","영양","청양","보령","영암","상주","옥천","완도","옥천","보령","천안","증평","동광주","김제","청송","영천","괴산","하양","영천","제천","김제","북포항","유구","합천","서광양","동여수","밀양","성주","김해","증평","부여","진천","유구","진북","동대전","통영","금산","청송","영덕","고흥","의성","봉화","화순","해남","부여","영천","의령","벌교","정읍","칠원","칠원","괴산","거제","흥해","예산","공주","의성","고창","아산","마산","가경","광양","정읍","울릉","서울산","영양","신탄진","양산","완도","진영","동촌","김천","청송","서천","동대전","동촌","양을산","순창","서산","정읍","송정","구례","밀양","하동","후포","고흥","청도","영주","서안동","천안","남광주","고흥","예천","여천","서안동","통영","장성","일광","금산","가경","성서","통영","영천","임실","양을산","청송","삼천포","진도","거제","왜관","광양","오천","함평","거제","영암","영산","정읍","거제","서천","제천","양을산","익산","흥해","창녕","부여","남전주","동순천","고창","합천","무안","당진","부안","동구미","밀양","울진","아산","무안","경주","흥해","서청주","마산","청송","울릉","서부산","벌교","안강","북전주","함열","청도","법성포","홍성","홍성","부여","상주","하동","제천","상주","김해","청송","공주","상주","봉동","영천","장성","청도","해남","청양","군위","동전주","울산","서천","여천","월배","해남","여천","기장","의성","봉동","의령","양산","동마산","영양","동여수","공주","완도","영동","김천","익산","후포","김제","합천","해남","경주","남울산","북순천","서안동","보은","장흥","보성","서군산","군위","남전주","영천","영주","함양","양을산","남대전","고창","경산"
        ],
        "branch_branch": ["가곡분기(단양)","가곡분기(당진)","가교분기(완도)","가금분기(충주)","가덕분기(남청주)","가동분기(예천)","가락분기(강서)","가미분기(의령)","가산분기(단양)","가산분기(성환)","가산분기(양산)","가야곡분기(연무)","가야분기(녹동)","가오분기(동대전)","가은분기(문경)","가음분기(의성)","가조분기(거제)","가조분기(거창)","가좌분기(상당)","가주분기(충주)","가천분기(봉동)","가평분기(단양)","가학분기(해남)","가흥분기(충주)","각남분기(청도)","각북분기(청도)","간전분기(구례)","갈골분기(상주)","갈담분기(임실)","갈도분기(하동)","갈밭분기(남울산)","갈산분기(홍성)","갈지분기(하양)","갈평분기(서문경)","감곡분기(금왕)","감노분기(김해)","감리분기(창녕)","감문분기(김천)","감물분기(괴산)","감산분기(건천)","감애분기(서안동)","감천분기(예천)","감포분기(경주)","강교분기(안강)","강구분기(영덕)","강남분기(서안동)","강내분기(가경)","강당분기(서산)",강동분기(안강)","강명분기(함안)","개도분기(동여수)","개령분기(김천)","개령분기(순천)","개승분기(의령)","개신분기(가경)","개진분기(고령)","개천분기(고성)","거문도분기(동여수)","거산분기(문경)","건천분기(금산)","검단분기(남울산)","검단분기(서울산)","검정분기(사천)","격포분기(부안)","결성분기(광천)","겸면분기(곡성)","경호도분기(동여수)","계곡분기(해남)","계당분기(하양)","계룡분기(공주)","계북분기(장수)","계산분기(구례)","계원분기(오천)","계정분기(성주)","계화분기(부안)","고경분기(영천)","고곡분기(안동)","고곡분기(영산)","고군분기(진도)","고금분기(완도)","고남분기(태안)","고남분기(하동)","고달분기(곡성)","고대분기(당진)","고덕분기(삽교)","고로분기(군위)","고모분기(진영)","고북분기(서산)","고산분기(봉동)","고서분기(담양)","고암분기(창녕)",고정분기(보령)","고제분기(거창)","고천분기(안동)","고촌분기(기장)","고촌분기(남원)","곡점분기(산청)","곤명분기(사천)","곤양분기(사천)","곰소분기(부안)","공단분기(달성)","공단분기(서군산)","공당분기(오천)","공덕분기(김제)","공산분기(나주)","공수분기(포항)","공이분기(충주)","과역분기(고흥)","관산분기(구례)","관촌분기(임실)","관하분기(청도)","광금분기(청양)","광기분기(김천)","광덕분기(천안)","광명분기(경주)","광산분기(동군산)","광석분기(논산)","광시분기(예산)","광영분기(광양)","광의분기(구례)","광정분기(공주)","광혜원분기(진천)","괴목분기(무주)","괴목분기(북순천)","교동분기(공주)","교안분기(안계)","교암분기(정읍)","구건분기(옥천)","구곡분기(제천)","구곡분기(진천)","구기분기(밀양)","구룡분기(부여)","구룡분기(순천)","구룡분기(청주)","구룡포분기(포항)","구림분기(순창)","구산분기(마산)","구상분기(북순천)","구성분기(김천)","구암분기(남울산)","구암분기(의성)","구영분기(거제)","구이분기(남전주)","구조라분기(장승포)","구지분기(달성)","구천분기(무주)","구천분기(안계)","구촌분기(충북영동)","구평분기(포항)","구항분기(홍성)","구혜분기(함안)","구호분기(사천)","국곡분기(서안동)","국우분기(칠곡)","군남분기(영광)","군내분기(여수)","군내분기(진도)","군북분기(금산)","군북분기(옥천)","군북분기(함안)","군서분기(영암)","군서분기(옥천)","군외분기(완도)","굴전분기(여수)","궁기분기(동구미)","궁류분기(의령)","권이분기(경주)","규암분기(부여)","근흥분기(태안)","금가분기(충주)","금계분기(가경)","금계분기(진도)","금곡분기(동광주)","금곡분기(함평)","금과분기(순창)","금관분기(청주)","금구분기(김제)","금남분기(조치원)","금당분기(봉동)","금당분기(예천)","금마분기(부송)","금산분기(녹동)","금산분기(밀양)","금산분기(왜관)","금산분기(진북)","금산사분기(김제)","금성동분기(금정)","금성분기(담양)","금성분기(제천)","금수분기(성주)","금안분기(나주)","금암분기(진북)","금일분기(완도)","금정분기(영암)","금지분기(남원)","금지분기(영암)","금천분기(나주)","금천분기(남청주)","금호분기(영천)","금호분기(칠곡)","금호분기(해남)","기계분기(북포항)","기성분기(왜관)","기성분기(후포)","기암분기(영덕)","기암분기(청주)","기지시분기(당진)","기회분기(밀양)","길곡분기(울진)","길안분기(안동)","김전분기(청도)","나동분기(동진주)","나들분기(남울산)","나산분기(경주)","나포분기(동군산)","낙동분기(상주)","낙산분기(왜관)","낙서분기(상주)","낙안분기(북순천)","낙정분기(안계)","남곡분기(김천)","남구미분기(구미공단)","남면분기(담양)","남면분기(장성)","남명분기(밀양)","남산분기(하양)","남성현분기(청도)","남신분기(태안)","남악분기(하당)","남양분기(삼천포)","남양분기(청양)","남이분기(서청주)","남일분기(남청주)","남장분기(상주)","남정분기(영덕)","남지분기(영산)","남창분기(온산)","남천분기(경산)","남평분기(나주)","남포분기(보령)","남호분기(영덕)","남후분기(서안동)","낭도분기(동여수)","낭성분기(청주)","낭월분기(동대전)","내곡분기(고령)","내도분기(고흥)","내도분기(무주)","내리분기(태안)","내북분기(보은)","내산분기(공주)","내산분기(부여)","내삼분기(김해)","내석분기(양주)","내수분기(상당)","내와분기(언양)","내요분기(부안)","내장동분기(정읍)","내칠분기(건천)","내판분기(조치원)","내포분기(마산)","내흥분기(공주)","넙도분기(완도)","노곡분기(경주)","노당분기(안강)","노동분기(보성)","노량분기(남해)","노량분기(하동)","노산분기(통영)","노성분기(논산)","노안분기(나주)","노월분기(동순천)","노은R2분기(유성)","노은분기(충주)","노음분기(울진)","노화분기(완도)","녹산공단분기(강서)","녹산분기(강서)","논곡분기(장수)","논공분기(달성)","논산분기(영광)","농남분기(김천)","농소분기(김천)","농소분기(울산)","농암분기(서문경)","눌인분기(청송)","늑도분기(삼천포)","능산분기(금왕)","능주분기(화순)","다구분기(진북)","다도분기(나주)","다문분기(하양)","다부분기(왜관)","다사분기(성서)","다산분기(고령)","다산분기(안강)","다시분기(나주)","다인분기(안계)","다호분기(동마산)","단계분기(산청)","단밀분기(안계)","단산분기(영주)","단성분기(산청)","단장분기(밀양)","단촌분기(의성)","단포분기(영천)","달산분기(영덕)","답동분기(순창)","당동분기(고성)","당동분기(의령)","당사분기(울산)","당포분기(서문경)","당항분기(남해)","대가분기(고성)","대가분기(성주)","대강분기(남원)","대강분기(단양)","대견분기(창녕)","대곡분기(진주)","대곡분기(청도)","대광분기(김천)","대교분기(세종)","대덕분기(김천)","대덕분기(남전주)","대덕분기(담양)","대덕분기(영광)","대덕분기(죽교)","대동분기(용전)","대동분기(함평)","대마분기(영광)","대방분기(김천)","대병분기(합천)","대보분기(포항)","대본분기(경주)","대사분기(남해)","대산분기(고창)","대산분기(남원)","대산분기(동마산)","대서분기(고흥)","대성분기(장수)","대소분기(금왕)","대술분기(예산)","대아분기(봉동)","대야분기(동군산)","대율분기(군위)","대율분기(여수)","대의분기(의령)","대일분기(상동)","대장분기(익산)","대전분기(나주)","대지분기(강서)","대창분기(보령)","대창분기(영천)","대촌분기(상무)","대치분기(담양)","대합분기(창녕)","대현분기(건천)","대현분기(봉화)","대호분기(당진)","대화동분기(용전)","대흥분기(예산)","덕계분기(양산)","덕계분기(예천)","덕곡분기(고령)","덕과분기(남원)","덕산분기(삽교)","덕산분기(진천)","덕신분기(울진)","덕양분기(여천)","덕용분기(영광)","덕지분기(공주)","덕천분기(김천)","덕천분기(정읍)","덕촌분기(단양)","덕촌분기(선산)","덕평분기(괴산)","덕하분기(남울산)","덕호분기(거제)","도고분기(아산)","도곡분기(화순)","도기분기(제천)","도덕분기(녹동)","도리분기(건천)","도산분기(논산)","도산분기(서안동)","도안분기(유성)","도안분기(증평)","도암분기(강진)","도전분기(제천)","도정분기(북순천)","도청분기(금왕)","도촌분기(봉화)","도포분기(영암)","도항분기(함안)","도화분기(고흥)","도화분기(예천)","도흥분기(성주)","독곶분기(서산)","독양분기(예천)","동강분기(고흥)","동계분기(순창)","동곡분기(성서)","동곡분기(송정)","동곡분기(청도)","동락분기(충주)","동량분기(충주)","동림분기(북광주)","동면분기(양산)","동면분기(화순)","동명분기(왜관)","동방분기(경주)","동복분기(화순)","동부분기(거제)","동상분기(거제)","동상분기(동전주)","동서변분기(동대구)","동성분기(홍성)","동암분기(아산)","동양분기(봉화)","동이분기(옥천)","동정분기(녹동)","동정분기(함평)","동천분기(지족)","동촌분기(영주)","동학사분기(유성)","동해분기(고성)","동해분기(유구)","동호분기(고창)","두동분기(언양)","두류분기(남대구)","두마분기(계룡)","두산분기(울성남)","두서분기(언양)","두원분기(고흥)","두정분기(천안)","두항분기(단양)","둔덕분기(거제)","둔산분기(동촌)","둔포분기(아산)","득량분기(보성)","등동분기(청주)","등림분기(전남하남)","마곡분기(유구)","마량분기(강진)","마령분기(진안)","마로분기(보은)","마산분기(구례)","마산분기(김제)","마산분기(서천)","마산분기(오천)","마산분기(해남)","마성분기(서문경)","마암분기(고성)","마암분기(공주)","마암분기(남전주)","마월분기(성주)","마천분기(함양)","막곡분기(문경)","만경분기(김제)","만리분기(태안)","만선분기(무주)","만성분기(북여수)","망성분기(경주)","망성분기(함열)","망운분기(무안)","망월분기(하당)","망주분기(고흥)","매곡분기(무안)","매곡분기(본촌)","매곡분기(충북영동)","매리분기(김해)","매성분기(천안)","매안분기(합천)","매암분기(남울산)","매원분기(왜관)","매전분기(청도)","매정분기(영덕)","매정분기(화순)","매포분기(단양)","매화분기(울진)","맥도분기(부산강서)","맹동분기(금왕)","면천분기(당진)","명덕분기(동전주)","명도분기(제천)","명동분기(거제)","명서분기(충주)","명주분기(영천)","명지분기(사하)","명지분기(서산)","모동분기(상주)","모라분기(북부산)","모밀분기(대불)","모산분기(성주)","모산분기(아산)","모서분기(상주)","모아분기(경주)","모점분기(충주)","모화분기(경주)","목천분기(천안)","목행분기(충주)","몽곡분기(삽교)","몽탄분기(무안)","묘도분기(여천)","묘량분기(영광)","묘산분기(합천)","무등분기(동광주)","무릉분기(밀양)","무릉분기(진안)","무림분기(남해)","무안분기(밀양)","무을분기(선산)","무정분기(담양)","무풍분기(무주)","무학분기(성주)","묵계분기(안동)","묵정분기(충북영동)","문곡분기(충주)","문내분기(해남)","문백분기(진천)","문산분기(서천)","문성분기(구미)","문의분기(남청주)","문장분기(함평)","문척분기(구례)","문천분기(공주)","문충분기(오천)","문평분기(나주)","문현분기(함안)","물금분기(양산)","물한분기(충북영동)","미남분기(통영)","미력분기(보성)","미산분기(보령)","미암분기(영암)","미원분기(남청주)","미음분기(강서)","미조분기(지족)","미천분기(진주)","박달분기(경주)","반계분기(왜관)","반곡분기(언양)","반구분기(영주)","반남분기(나주)","반동분기(마산)","반선분기(남원)","반성분기(동진주)","반송분기(달성)","반천분기(언양)","반포분기(공주)","반포분기(세종)","반포분기(영산)","방갈분기(태안)","방기분기(양산)","방북분기(단양)","방산분기(나주)","방어진분기(동울산)","방축분기(증평)","배둔분기(고성)","백곡분기(의령)","백곡분기(진천)","백산분기(김제)","백산분기(양을산)","백석분기(천안)","백수분기(영광)","백안분기(동촌)","백운분기(성주)","백운분기(왜관)","백운분기(제천)","백운분기(진안)","백학분기(상주)","번등분기(해남)","번암분기(장수)","벌곡분기(논산)","범서분기(울성남)","법송분기(통영)","법수분기(함안)","법전분기(봉화)","벽진분기(성주)","변산분기(부안)","별량분기(순천)","별방분기(단양)","병곡분기(영덕)","병산분기(고성)","병천분기(천안)","보길분기(완도)","보덕분기(조치원)","보문분기(경주)","보발분기(단양)","보월분기(성주)","보절분기(남원)","보천분기(음성)","보현분기(영천)","복내분기(보성)","복림분기(화순)","복수분기(금산)","복흥분기(순창)","본촌분기(영천)","봉강분기(서광양)","봉강분기(진주)","봉계분기(언양)","봉남분기(김제)","봉명분기(서청주)","봉산분기(담양)","봉산분기(삽교)","봉성분기(봉화)","봉암분기(조치원)","봉양분기(제천)","봉월분기(남울산)","봉촌분기(칠원)","봉하분기(청도)","봉학분기(성주)","봉현분기(삼천포)","봉황분기(나주)","부강분기(서청주)","부강분기(세종)","부계분기(군위)","부곡분기(당진)","부곡분기(영산)","부구분기(울진)","부귀분기(진안)","부남분기(서산)","부남분기(청송)","부덕분기(나주)","부동분기(양을산)","부동분기(청송)","부량분기(김제)","부리분기(금산)","부산분기(영천)","부상분기(김천)","부석분기(영주)","부안분기(고창)","부용분기(김제)","부적분기(논산)","부포분기(고성)","부항분기(김천)","북김해분기(김해)","북면분기(화순)","북삼분기(왜관)","북상분기(거창)","북안분기(영천)","북이분기(상당)","북이분기(장성)","북평분기(해남)","불갑분기(영광)","불분기(경주)","불당분기(천안)","불암분기(문경)","불정분기(문경)","비금분기(양을산)","비봉분기(봉동)","비봉분기(청양)","비산분기(북대구)","비아분기(전남하남)","비안분기(안계)","비인분기(서천)","비중분기(상당)","비촌분기(구례)","비토분기(사천)","사곡분기(거제)","사곡분기(서광양)","사곡분기(유구)","사곡분기(의성)",사기분기(당진)","사남분기(사천)","사동분기(경산)","사동분기(영천)","사동분기(후포)","사량분기(통영)","사마분기(무안)","사매분기(남원)","사방분기(안강)","사벌분기(상주)","사석분기(진천)","사안분기(장흥)","사촌분기(김해)","사촌분기(언양)","사평분기(화순)","산내분기(건천)","산내분기(남원)","산내분기(정읍)","산달도분기(거제)","산동분기(남원)","산동분기(동구미)","산동분기(아산)","산북분기(봉동)","산서분기(장수)","산성분기(광천)","산성분기(군위)","산안분기(금산)","산양분기(통영)","산외분기(밀양)","산외분기(보은)","산외분기(정읍)","산인분기(함안)","산전분기(서산)","산정분기(북순천)","산제분기(나주)","산척분기(충주)","산포분기(거창)","산포분기(나주)","살미분기(충주)","삼가분기(합천)","삼거분기(거제)","삼계분기(안동)","삼계분기(장성)","삼곡분기(동진주)","삼귀분기(창원)","삼근분기(울진)","삼기분기(곡성)","삼기분기(익산)","삼남분기(언양)","삼도분기(송정)","삼락A분기(김천)","삼락B분기(김천)","삼랑진분기(밀양)","삼매분기(영천)","삼부분기(영천)","삼산분기(군위)","삼산분기(상동)","삼산분기(죽교)","삼생분기(음성)","삼서분기(장성)","삼성분기(금왕)","삼용분기(진천)","삼은분기(성환)","삼장분기(산청)","삼창분기(영천)","삼포분기(대불)","삼학분기(영광)","삼호분기(대불)","삼호분기(서울산)","상가분기(금산)","상관분기(전주)","상괴분기(서문경)","상대분기(하양)","상도분기(충북영동)","상리분기(고성)","상망분기(영주)","상모분기(구미공단)","상부분기(합천)","상사분기(순천)","상사분기(영암)","상사분기(흥해)","상소분기(동대전)","상옥분기(흥해)","상운분기(동전주)","상운분기(봉화)","상원분기(함양)","상월분기(논산)","상주분기(남해)","상천분기(동마산)","상천분기(제천)","상촌분기(상주)","상평분기(서군산)","상하분기(고창)","생극분기(금왕)","생비량분기(산청)","생일분기(완도)","생철분기(김해)","생초분기(산청)","서면분기(남해)","서면분기(서천)","서면분기(울릉)","서벽분기(봉화)","서변분기(동대구)","서부분기(홍성)","서상분기(함양)","서생분기(온산)","서수분기(동군산)","서양분기(장성)","서재분기(성서)","서창분기(상무)","서포분기(사천)","서하분기(함양)","서호분기(영암)","서후분기(서안동)","석계분기(영천)","석곡분기(곡성)","석남사분기(언양)","석묘분기(예천)","석문분기(당진)","석병분기(포항)","석보분기(영양)","석성분기(부여)","석적분기(왜관)","석전분기(왜관)","석포분기(봉화)","석호분기(해남)","선구분기(남해)","선남분기(성주)","선리분기(양산)","선유도분기(서군산)","선장분기(아산)","선창분기(완도)","선화분기(하양)","설천분기(무주)","섬거분기(옥곡)","성거분기(천안)","성남분기(익산)","성남분기(천안)","성내분기(고창)","성내분기(진해)","성덕분기(김제)","성도분기(담양)","성동분기(논산)","성사분기(영산)","성산분기(고령)","성산분기(동군산)","성산분기(의령)","성산분기(장성)","성산분기(창녕)","성산분기(해남)","성송분기(고창)","성안분기(울성남)","성연분기(서산)","성전분기(강진)","성주분기(보령)","성포분기(거제)","세동분기(완도)","세지분기(나주)","소록분기(녹동)","소보분기(군위)","소성분기(성주)","소수분기(괴산)","소안분기(완도)","소양분기(동전주)","소용분기(충주)","소원분기(태안)","소이분기(음성)","소정분기(세종)","소정분기(천안)","소천분기(봉화)","소천분기(청도)","소태분기(충주)","소호분기(언양)","속리분기(보은)","손동분기(충주)","손불분기(함평)","송강분기(신탄진)","송곡분기(고령)","송공분기(양을산)","송광분기(북순천)","송동분기(남원)","송동분기(포항)","송라분기(북포항)","송림분기(사천)","송면분기(괴산)","송백분기(밀양)","송산분기(고흥)","송산분기(당진)","송악분기(아산)","송암분기(남광주)","송암분기(태안)","송전분기(천안)","송정분기(지족)","송지분기(해남)","송촌분기(용전)","송학분기(제천)","송한분기(제천)","송호분기(해남)","수남분기(천안)","수덕분기(삽교)","수동분기(강진)","수동분기(함양)","수륜분기(성주)","수리분기(제천)","수리분기(화순)","수북분기(담양)","수비분기(영양)","수산분기(제천)","수신분기(천안)","수안보분기(충주)","수연분기(양을산)","수지분기(남원)","수창분기(대구)","수철분기(영주)","수한분기(보은)","수향분기(성환)","수홍분기(남원)","수회분기(충주)","순성분기(당진)","순흥분기(영주)","승주분기(북순천)","시락분기(진북)","시랑분기(기장)","시산분기(순창)","시종분기(영암)","신계분기(천안)","신광분기(북포항)","신광분기(함평)","신기분기(공주)","신기분기(괴산)","신기분기(문경)","신니분기(충주)","신대분기(금산)","신동분기(동구미)","신령분기(영천)","신례분기(예산)","신리분기(죽교)","신리분기(홍성)","신림분기(고창)","신반분기(의령)","신방분기(남천안)","신북분기(영암)","신서분기(경주)","신석분기(양을산)","신성분기(서산)","신안분기(산청)","신암분기(상주)","신암분기(예산)","신양분기(예산)","신오분기(상주)","신온분기(태안)","신원분기(옥곡)","신원분기(청도)","신월분기(괴산)","신유분기(아산)","신음분기(김천)","신의분기(양을산)","신전분기(강진)","신전분기(서안동)","신정분기(영암)","신정분기(진안)","신지분기(완도)","신창분기(전남하남)","신촌분기(동마산)","신촌분기(송정)","신촌분기(청송)","신택분기(예산)","신평분기(금산)","신평분기(김천)","신평분기(달성)","신평분기(임실)","신평분기(합덕)","신풍분기(여천)","신한분기(하양)","신호분기(영천)","신화분기(아산)","신흥분기(공주)","신흥분기(장성)","신흥분기(청송)","신흥분기(하동)","심동분기(진도)","심원분기(충북영동)","심천분기(충북영동)","쌍류분기(조치원)","쌍림분기(고령)","쌍용분기(아산)","쌍지분기(순천)","쌍청분기(가경)","쌍치분기(순창)","아산분기(고창)","아영분기(남원)","아천분기(김천)","아포분기(김천)","아화분기(건천)","악양분기(하동)","안내분기(옥천)","안덕분기(청송)","안면분기(태안)","안사분기(안계)","안성분기(무주)","안심분기(청양)","안양분기(장흥)","안의분기(함양)","안정분기(영주)","안정분기(통영)","안좌분기(양을산)","안천분기(부송)","안천분기(진안)","안평분기(의성)","안하분기(진영)","안흥분기(태안)","암곡분기(경주)","암태분기(양을산)","압량분기(경산)","압록분기(곡성)","압해분기(양을산)","앙성분기(충주)","앵남분기(화순)","앵천분기(괴산)","야로분기(합천)","야월분기(영광)","약남분기(영천)","약목분기(왜관)","약산분기(완도)","약수분기(장성)","약전분기(포항)","양각분기(김천)","양곡분기(조치원)","양곡분기(창원)","양남분기(경주)","양막분기(예산)","양백분기(진천)","양북분기(경주)","양사분기(고흥)","양산분기(충북영동)","양옥분기(동진주)","양중분기(완도)","양촌분기(연무)","양포분기(동구미)","어담분기(서안동)","어상천분기(단양)","어신분기(예천)","어은분기(태안)","어진분기(세종)","어청도분기(서군산)","엄정분기(충주)","여미분기(서산)","여산분기(부송)","여양분기(진북)","여흘분기(양을산)","연계분기(군위)","연기분기(조치원)","연도분기(동여수)","연동분기(고령)","연동분기(진도)","연봉분기(서천)","연산분기(남원)","연산분기(논산)","연수분기(충주)","연안분기(경주)","연암분기(양정)","연양분기(화순)","연일분기(포항)","연장분기(진안)","연초분기(거제)","연풍분기(괴산)","연화분기(고성)","연화분기(왜관)","염산분기(영광)","염치분기(아산)","염포분기(고흥)","영봉분기(북순천)","영순분기(문경)","영오분기(고성)","영운분기(김해)","영은분기(영주)","영인분기(아산)","영전분기(해남)","영춘분기(단양)","영풍분기(완도)","영해분기(영덕)","영현분기(고성)","예내분기(고흥)","예당분기(보성)","예림분기(밀양)","예안분기(서안동)","오계분기(거창)","오계분기(나주)","오곡분기(천안)","오궁분기(금왕)","오길분기(영천)","오류분기(경주)","오목내분기(진주)","오목분기(아산)","오미분기(서청주)","오미분기(진주)","오방분기(고성)","오산분기(곡성)","오산분기(서안동)","오산분기(왜관)","오설분기(달성)","오송분기(가경)","오수분기(임실)","오식도분기(서군산)","오신분기(예천)","오용분기(지족)","오창과학분기(상당)","오창분기(상당)","오천분기(녹동)","오천분기(보령)","오천분기(예천)","오촌분기(영덕)","오태분기(구미공단)","옥과분기(곡성)","옥관분기(선산)","옥구분기(서군산)","옥룡분기(서광양)","옥리분기(화순)","옥립분기(의성)","옥산분기(상주)","옥산분기(서군산)","옥산분기(서천)","옥산분기(안강)","옥성분기(선산)","옥실분기(영광)","옥종분기(하동)","옥천분기(해남)","옥포분기(달성)","온정분기(후포)","옹정분기(남원)","옹천분기(서안동)","와동분기(용전)","와룡분기(서안동)","와촌분기(하양)","완도","왕곡분기(나주)","왕궁분기(부송)","왕신분기(안강)","외곡분기(구례)","외동분기(달성)","외동분기(북순천)","외량분기(군위)","외산분기(부여)","외서분기(북순천)","외속리분기(보은)","외포분기(거제)","요고분기(밀양)","요천분기(남원)","욕장분기(보령)","욕지분기(통영)","용계분기(상동)","용계분기(순천)","용궁분기(예천)","용기분기(북포항)","용남분기(통영)","용담분기(진안)","용당분기(청양)","용면분기(담양)","용문분기(김천)","용봉분기(공주)","용봉분기(달성)","용사분기(성주)","용산분기(장흥)","용성분기(하양)","용수분기(북순천)","용수분기(왜관)","용암분기(남청주)","용암분기(보성)","용암분기(성주)","용원분기(진해)","용잠분기(동마산)","용장분기(경주)","용전분기(하양)","용주분기(합천)","용지분기(김제)","용치분기(담양)","용포분기(하당)","용현분기(삼천포)","용현분기(세종)","용호분기(정읍)","용흥분기(담양)","우계분기(김해)","우곡분기(고령)","우곡분기(밀양)","우두분기(여수)","우두포분기(고성)","우라분기(건천)","우목분기(북포항)","우보분기(군위)","우산분기(옥천)","우성분기(공주)","우수분기(진주)","우학리분기(동여수)","운곡분기(의령)","운곡분기(청양)","운봉분기(남원)","운산분기(화순)","운수분기(고령)","운암분기(북광주)","운용분기(천안)","운주분기(봉동)","운천분기(구례)","웅동분기(진해)","웅상분기(양산)","웅양분기(거창)","웅촌분기(서울산)","웅치분기(보성)","웅포분기(함열)","원강분기(담양)","원남분기(보은)","원달분기(곡성)","원덕분기(천안)","원동분기(양산)","원동분기(오천)","원동분기(팔복)","원들분기(영암)","원봉분기(세종)","원북분기(태안)","원산도분기(보령)","원산분기(통영)","원장분기(동군산)","원전분기(마산)","원전분기(영덕)","원지분기(김해)","원촌분기(구례)","원촌분기(함양)","원평분기(구미)","원평분기(김제)","원포분기(여천)","월곡분기(안동)","월교분기(해남)","월래분기(여천)","월령분기(영산)","월막분기(고령)","월미분기(공주)","월산분기(담양)","월산분기(밀양)","월악분기(제천)","월암분기(여수)","월야분기(함평)","월정분기(청송)","월진분기(하동)","월천분기(함평)","월촌분기(함안)","월포분기(예천)","월항분기(성주)","월호도분기(동여수)","월호분기(영주)","위도분기(부안)","위봉분기(동전주)","위양분기(온산)","위천분기(거창)","유강분기(포항)","유곡분기(의령)","유교분기(하당)","유덕분기(상무)","유속분기(무주)","유원분기(칠원)","유천분기(청도)","유하분기(영천)","윤내분기(함안)","율지분기(합천)","율촌분기(여천)","율포분기(거제)","율하분기(김해)","은산분기(부여)","은월분기(고성)","은진분기(연무)","은척분기(함창)","은하분기(광천)","음대분기(금산)","음봉분기(아산)","음암분기(서산)","읍동분기(양을산)","응달분기(김해)","응봉분기(예산)","의당분기(공주)","의신분기(진도)","의항분기(태안)","의흥분기(군위)","이곡분기(괴산)","이류분기(충주)","이반성분기(동진주)","이방분기(창녕)","이백분기(남원)","이서분기(남전주)","이서분기(청도)","이서분기(화순)","이원분기(보은)","이원분기(옥천)","이원분기(태안)","이월분기(진천)","이인분기(공주)","이인분기(흥해)","이조분기(경주)","이천분기(언양)","이천분기(여천)","이하분기(서안동)","인계분기(순창)","인안분기(순천)","인암분기(담양)","인월분기(남원)","인주분기(아산)","인지분기(해남)","일로분기(하당)","일부분기(건천)","일직분기(서안동)","임고분기(영천)","임곡분기(전남하남)","임기분기(봉화)","임동분기(안동)","임리분기(장흥)","임북분기(합천)","임자분기(양을산)","임천분기(밀양)","임천분기(부여)","임피분기(동군산)","임하분기(안동)","임회분기(진도)","입면분기(곡성)","입석분기(산청)","입석분기(상주)","입석분기(제천)","입암분기(정읍)","입장분기(성환)","자양분기(영천)","자은분기(양을산)","자인분기(하양)","자천분기(영천)","작천분기(강진)","장가분기(영산)","장갑분기(보은)","장곡분기(광천)","장곡분기(통영)","장군분기(군위)","장기분기(포항)","장내분기(증평)","장동분기(무안)","장동분기(장흥)","장림","장마분기(영산)","장목분기(거제)","장방분기(진영)","장사분기(동진주)","장산분기(양을산)","장산분기(장성)","장성분기(흥해)","장소분기(해남)","장수읍분기(장수)","장승포","장안분기(장수)","장암분기(공주)","장암분기(벌교)","장암분기(부여)","장암분기(세종)","장암분기(순창)","장연분기(괴산)","장유분실","장재분기(동진주)","장전분기(논산)","장전분기(사천)","장전분기(합천)","장천분기(동구미)","장천분기(보성)","장천분기(진해)","장평분기(장흥)","장평분기(청양)","장하분기(부여)","장현분기(보령)","재산분기(봉화)","저구분기(거제)","적동분기(영주)","적상분기(무주)","적성분기(단양)","적성분기(순창)","전동분기(조치원)","전민분기(북대전)","전의분기(조치원)","전화분기(의령)","접정분기(장흥)","정관분기(일광)","정대분기(상동)","정동분기(사천)","정산분기(청양)","정산분기(함평)","정생분기(동대전)","정우분기(정읍)","정자분기(울산)","정자분기(흥해)","정천분기(오천)","정천분기(진안)","정촌분기(동진주)","제동분기(동마산)","제오분기(의성)","제원분기(금산)","제철분기(광양)","조동분기(충북영동)","조마분기(김천)","조성분기(벌교)","조일분기(언양)","조촌분기(군산)","종상분기(김천)","종천분기(사천)","종천분기(서천)","주계분기(서안동)","주덕분기(충주)","주미분기(공주)","주산분기(보령)","주생분기(남원)","주암분기(북순천)","주인분기(울진)","주전분기(동울산)","주중분기(김해)","주천분기(금왕)","주천분기(남원)","주포분기(보령)","주포분기(함평)","죽곡분기(진해)","죽동분기(나주)","죽림분기(통영)","죽림분기(홍성)","죽변분기(울진)","죽장분기(북포항)","죽전분기(옥곡)","죽전분기(왜관)","죽천분기(옥곡)","죽청분기(보령)","죽청분기(완도)","죽포분기(여수)","줄포분기(부안)","중계분기(홍성)","중교분기(의령)","중기분기(청송)","중동분기(상주)","중리분기(아산)","중리분기(왜관)","중말분기(건천)","중벌분기(상주)","중산분기(밀양)","중산분기(흥해)","중인분기(남전주)","중장분기(태안)","중촌분기(대전)","중촌분기(의령)","중흥분기(공주)","중흥분기(당진)","중흥분기(여천)","증도분기(양을산)","증산분기(김천)","지경분기(괴산)","지경분기(흥해)","지곡분기(포항)","지곡분기(함양)","지도분기(양을산)","지례분기(김천)","지묘분기(동촌)","지사분기(부산강서)","지산분기(진도)","지세포분기(장승포)","지원분기(광주)","지정분기(의령)","지좌분기(김천)","지천분기(왜관)","직동분기(고령)","직지사분기(김천)","진교분기(하동)","진량분기(하양)","진례분기(여천)","진례분기(진영)","진목분기(죽교)","진보분기(청송)","진산분기(금산)","진성분기(동진주)","진암분기(증평)","진월분기(옥곡)","진장분기(양정)","진전분기(진북)","진평분기(동구미)","진하분기(온산)","차암분기(천안)","창기분기(태안)","창선분기(지족)","창천분기(성주)","창촌분기(북순천)","창촌분기(산청)","창평분기(담양)","창포분기(영덕)","천가분기(강서)","천동분기(천안)","천부분기(울릉)","천북분기(경주)","천북분기(광천)","천상분기(울성남)","천의분기(당진)","천전분기(안동)","천평분기(왜관)","천향분기(예천)","철마분기(기장)","청계분기(무안)","청광분기(고성)","청기분기(영양)","청남분기(청양)","청라분기(보령)","청룡분기(영암)","청리분기(상주)","청산분기(옥천)","청산분기(완도)","청성분기(옥천)","청소분기(보령)","청수분기(천안)","청안분기(증평)","청옥분기(동광주)","청운분기(김제)","청운분기(청송)","청정분기(영천)","청천분기(괴산)","청천분기(하양)","청통분기(영천)","청풍분기(제천)","청하분기(김제)","청하분기(북포항)","청흥분기(유구)","초계분기(합천)","초남분기(서광양)","초도분기(동여수)","초동분기(수산)","초전분기(성주)","초정분기(김해)","초중분기(증평)","초촌분기(부여)","초평분기(진천)","추계분기(유구)","추곡분기(진북)","추동분기(동대전)","추봉분기(통영)","추부분기(금산)","추현분기(청송)","축산분기(영덕)","축정분기(고흥)","춘산분기(의성)","춘양분기(봉화)","춘양분기(화순)","충리분기(해남)","충화분기(부여)","충효분기(영천)","칠곡분기(의령)","칠동분기(벌교)","칠보분기(정읍)","칠북분기(칠원)","칠서분기(칠원)","칠성분기(괴산)","칠천도분기(거제)","칠포분기(흥해)","탄방분기(예산)","탄천분기(공주)","탑리분기(의성)","탑정분기(고창)","탕정분기(아산)","태봉분기(진북)","태성분기(가경)","태인분기(광양)","태인분기(정읍)","태하분기(울릉)","태화분기(서울산)","택전분기(영양)","테크노분기(신탄진)","통도사분기(양산)","통리분기(완도)","퇴례분기(진영)","파계분기(동촌)","파천분기(김천)","파천분기(청송)","판교분기(서천)","판암분기(동대전)","팔공분기(동촌)","팔금분기(양을산)","팔덕분기(순창)","팔봉분기(서산)","평내분기(정읍)","평동분기(송정)","평산분기(구례)","평촌분기(밀양)","평촌분기(하동)","평해분기(후포)","포두분기(고흥)","풍각분기(청도)","풍기분기(영주)","풍산분기(서안동)","풍세분기(천안)","풍암분기(남광주)","풍양분기(고흥)","풍양분기(예천)","풍유분기(여천)","풍천분기(서안동)","풍화분기(통영)","필암분기(장성)","하근분기(일광)","하금분기(금산)","하복대분기(가경)","하빈분기(성서)","하소분기(통영)","하송분기(영천)","하운암분기(임실)","하의분기(양을산)","하의분기(청송)","하이분기(삼천포)","하조분기(진도)","하청분기(거제)","하판분기(왜관)","하포분기(광양)","학계분기(오천)","학교분기(함평)","학동분기(거제)","학산분기(영암)","학포분기(영산)","한교분기(정읍)","한내분기(거제)","한산분기(서천)","한수분기(제천)","한운분기(양을산)","함라분기(익산)","합덕분기(흥해)","합리분기(창녕)","합정분기(부여)","항가분기(남전주)","해룡분기(동순천)","해리분기(고창)","해인사분기(합천)","해제분기(무안)","해창분기(당진)","해창분기(부안)","해평분기(동구미)","행곡분기(밀양)","행곡분기(울진)","행목분기(아산)","현경분기(무안)","현곡분기(경주)","현내분기(흥해)","현도분기(서청주)","현동분기(마산)","현동분기(청송)","현포분기(울릉)","혈청소분기(서부산)","호동분기(벌교)","호명분기(안강)","호성분기(북전주)","호암분기(함열)","호화분기(청도)","홍농분기(법성포)","홍동분기(홍성)","홍북분기(홍성)","홍산분기(부여)","화개분기(상주)","화개분기(하동)","화당분기(제천)","화령분기(상주)","화목분기(김해)","화목분기(청송)","화봉분기(공주)","화북분기(상주)","화산분기(봉동)","화산분기(영천)","화산분기(장성)","화산분기(청도)","화산분기(해남)","화성분기(청양)","화수분기(군위)","화심분기(동전주)","화암분기(울산)","화양분기(서천)","화양분기(여천)","화원분기(월배)","화원분기(해남)","화장분기(여천)","화전분기(기장)","화전분기(의성)","화정분기(봉동)","화정분기(의령)","화제분기(양산)","화천분기(동마산)","화천분기(영양)","화태중계소","화헌분기(공주)","활목분기(완도)","황간분기(충북영동)","황금분기(김천)","황등분기(익산)","황보분기(후포)","황산분기(김제)","황산분기(합천)","황산분기(해남)","황성분기(경주)","황성분기(남울산)","황전분기(북순천)","회곡분기(서안동)","회인분기(보은)","회진분기(죽교)","회천분기(보성)","회현분기(서군산)","효령분기(군위)","효자분기(남전주)","효정분기(영천)","휴천분기(영주)","휴천분기(함양)","흑산분기(양을산)","흑석분기(남대전)","흥덕분기(고창)","흥산분기(경산)"
        ]
    }
    
    # DataFrame 생성
    df = pd.DataFrame(data_kuk)

    # 국사입력
    input_kuksa = st.text_input("국사 입력")

    # IP로 검색
    if input_kuksa:
        result = df[df["office_kuk"] == input_kuksa]
        if not result.empty:
            #st.success("조회 결과:")
            st.write(result)
        else:
            st.error("해당 국사에 대한 정보가 없습니다.")
    
    # DataFrame 생성
    df = pd.DataFrame(data_branch)

    # 분기국사입력
    input_branch = st.text_input("분기국사 입력")

    # IP로 검색
    if input_branch:
        result = df[df["office_branch"] == input_branch]
        if not result.empty:
            #st.success("조회 결과:")
            st.write(result)
        else:
            st.error("해당 분기국사에 대한 정보가 없습니다.")
            