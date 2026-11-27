import random
import time
import streamlit as st
import streamlit.components.v1 as components

# Cấu hình trang
st.set_page_config(
    page_title="Học Giải Rubik 3x3 - Cơ Bản & CFOP",
    page_icon="🧊",
    layout="wide",
)

st.title("🧊 Ứng Dụng Học Giải Rubik 3x3")
st.markdown(
    "Luyện tập từ phương pháp cơ bản (LBL) đến phương pháp giải nhanh **CFOP** "
    "(quy ước **mặt Vàng ở trên**, **mặt Trắng ở dưới**) với mô phỏng 3D và bộ bấm giờ."
)

# Khởi tạo trạng thái lưu tiến độ học CFOP
if "learned_cfop" not in st.session_state:
    st.session_state.learned_cfop = set()

# Lật Vàng lên trên (U), Trắng xuống dưới (D)
BASE_ORIENTATION = "z2"


def combine_setup_alg(setup_alg: str) -> str:
    """Ghép phép lật z2 (Vàng trên, Trắng dưới) với chuỗi setup của từng trường hợp."""
    cleaned = (setup_alg or "").strip()
    return f"{BASE_ORIENTATION} {cleaned}".strip()


def render_twisty_case_preview(
    setup_alg: str,
    solve_alg: str,
    height: int = 225,
    camera_latitude: int = 35,
    camera_longitude: int = 35,
):
    """Hiển thị trình phát Rubik 3D với mặt Vàng ở trên và mặt Trắng ở dưới."""
    full_setup = combine_setup_alg(setup_alg)
    html_code = f"""
    <script src="https://cdn.cubing.net/js/cubing/twisty" type="module"></script>
    <div style="background: #f8f9fa; border: 1px solid #e0e4e8; border-radius: 10px; padding: 8px;">
        <twisty-player
            puzzle="3x3x3"
            experimental-setup-alg="{full_setup}"
            alg="{solve_alg}"
            camera-latitude="{camera_latitude}"
            camera-longitude="{camera_longitude}"
            background="none"
            control-panel="bottom-row"
            style="width: 100%; height: {height}px;">
        </twisty-player>
    </div>
    """
    components.html(html_code, height=height + 20)


def render_f2l_pair_spotlight_card(
    item: dict,
    default_camera: tuple[int, int] = (35, 35),
    default_expanded: bool = True,
    highlight_f2l_pair: bool = True,
):
    """Hiển thị công thức F2L kèm mô hình 3D và khung đèn chiếu làm sáng 2 mảnh góc + cạnh cần giải."""
    full_setup = combine_setup_alg(item.get("setup", ""))
    with st.expander(
        f"**{item['title']}** — `{item['alg']}`",
        expanded=default_expanded,
    ):
        col_info, col_view = st.columns([1.2, 1.1])
        with col_info:
            st.markdown(f"**Nhóm:** {item.get('group', 'F2L')}")
            st.markdown(f"**Nhận diện:** {item['desc']}")
            st.markdown("**Công thức:**")
            st.code(item["alg"], language="text")
            if item.get("tip"):
                st.info(f"💡 **Mẹo:** {item['tip']}")

            checked = st.checkbox(
                "Đã thuộc công thức này",
                key=item["id"],
                value=(item["id"] in st.session_state.learned_cfop),
            )
            if checked:
                st.session_state.learned_cfop.add(item["id"])
            else:
                st.session_state.learned_cfop.discard(item["id"])

        with col_view:
            lat, lon = item.get("camera", default_camera)
            stickering_attr = 'stickering="F2L"' if highlight_f2l_pair else ""

            spotlight_html = ""
            if highlight_f2l_pair:
                spotlight_html = """
                <div style="
                    margin-top: 8px;
                    padding: 10px 12px;
                    border-radius: 10px;
                    background: #141820;
                    color: #ffffff;
                    border: 1px solid #2d3548;
                ">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size:12px; font-weight:700; color:#ffd43b;">
                            🔆 ĐÈN CHIẾU 2 Ô MẢNH CẦN GIẢI (KHE FR)
                        </span>
                        <span style="font-size:11px; color:#adb5bd;">Vàng trên • Trắng dưới</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                        <div style="
                            background: linear-gradient(135deg, #fff3bf 0%, #ffd43b 100%);
                            color: #1a1a1a;
                            padding: 8px 10px;
                            border-radius: 8px;
                            border: 2px solid #ffffff;
                            box-shadow: 0 0 14px rgba(255, 212, 59, 0.95);
                        ">
                            <div style="font-size:10px; font-weight:800; letter-spacing:0.5px;">MẢNH 1 • GÓC</div>
                            <div style="font-size:13px; font-weight:800;">Góc Trắng - Đỏ - Xanh</div>
                        </div>
                        <div style="
                            background: linear-gradient(135deg, #d0ebff 0%, #4dabf7 100%);
                            color: #0b192c;
                            padding: 8px 10px;
                            border-radius: 8px;
                            border: 2px solid #ffffff;
                            box-shadow: 0 0 14px rgba(77, 171, 247, 0.95);
                        ">
                            <div style="font-size:10px; font-weight:800; letter-spacing:0.5px;">MẢNH 2 • CẠNH</div>
                            <div style="font-size:13px; font-weight:800;">Cạnh Đỏ - Xanh (Tầng 2)</div>
                        </div>
                    </div>
                </div>
                """

            html_code = f"""
            <script src="https://cdn.cubing.net/js/cubing/twisty" type="module"></script>
            <div style="background: #f8f9fa; border: 1px solid #dfe5ec; border-radius: 10px; padding: 8px;">
                <twisty-player
                    puzzle="3x3x3"
                    {stickering_attr}
                    experimental-setup-alg="{full_setup}"
                    alg="{item['alg']}"
                    camera-latitude="{lat}"
                    camera-longitude="{lon}"
                    background="none"
                    control-panel="bottom-row"
                    style="width: 100%; height: 205px;">
                </twisty-player>
                {spotlight_html}
            </div>
            """
            components.html(html_code, height=325 if highlight_f2l_pair else 230)


def render_algorithm_cards(
    items: list[dict],
    default_camera: tuple[int, int] = (35, 35),
    highlight_f2l_pair: bool = False,
):
    """Hiển thị danh sách công thức kèm mô phỏng 3D và ô đánh dấu đã thuộc."""
    for item in items:
        if highlight_f2l_pair:
            render_f2l_pair_spotlight_card(
                item=item,
                default_camera=default_camera,
                default_expanded=True,
                highlight_f2l_pair=True,
            )
            continue

        with st.expander(f"**{item['title']}** — `{item['alg']}`", expanded=True):
            col_info, col_view = st.columns([1.3, 1])
            with col_info:
                st.markdown(f"**Nhận diện:** {item['desc']}")
                st.markdown("**Công thức:**")
                st.code(item["alg"], language="text")
                if item.get("tip"):
                    st.info(f"💡 **Mẹo:** {item['tip']}")

                checked = st.checkbox(
                    "Đã thuộc công thức này",
                    key=item["id"],
                    value=(item["id"] in st.session_state.learned_cfop),
                )
                if checked:
                    st.session_state.learned_cfop.add(item["id"])
                else:
                    st.session_state.learned_cfop.discard(item["id"])

            with col_view:
                lat, lon = item.get("camera", default_camera)
                render_twisty_case_preview(
                    setup_alg=item["setup"],
                    solve_alg=item["alg"],
                    camera_latitude=lat,
                    camera_longitude=lon,
                )


def render_cross_section():
    """Phần 1: Cross ở mặt đáy Trắng (mặt Vàng ở trên)."""
    st.subheader("1️⃣ Cross — Giải chữ thập ở mặt đáy Trắng")
    st.caption("Mặt Vàng ở trên, mặt Trắng ở dưới. Nhấn Play để xem cách đưa cạnh trắng vào đáy.")

    col_c1, col_c2 = st.columns([1.35, 1])
    with col_c1:
        st.markdown("""
        * **Mục tiêu:** Giải thẳng 4 viên cạnh trắng ở **mặt đáy (D — Trắng)** và khớp màu tâm bên trong **dưới 8 bước xoay**.
        * **Khác biệt với cách cơ bản:** Giữ sẵn mặt Trắng ở dưới, mặt Vàng ở trên; đưa cạnh trắng xuống đáy trực tiếp thay vì làm hoa cúc ở mặt vàng.
        * **Nguyên tắc luyện tập:**
          1. **Tận dụng 15 giây quan sát (Inspection):** Nhớ vị trí cả 4 viên cạnh trắng trước khi chạm tay vào khối.
          2. **Giải theo vị trí tương đối:** Đặt đúng thứ tự các màu quanh đáy Trắng, sau đó xoay mặt D một lượt để khớp toàn bộ tâm.
          3. **Tập giải nhắm mắt (Blind Cross):** Quan sát xong, nhắm mắt và xoay hết Cross để tăng khả năng nhìn trước cho F2L.
        """)
        st.info(
            "**Tóm tắt chỉ số Phần 1**\n\n"
            "- Mặt trên / đáy: **Vàng (U) / Trắng (D)**\n"
            "- Số công thức học thuộc: **0** (Giải trực quan)\n"
            "- Số bước tối ưu: **6 – 8 moves**\n"
            "- Mục tiêu thời gian: **< 3 giây**"
        )
    with col_c2:
        st.markdown("**Ví dụ mô phỏng đưa 1 cạnh trắng vào đáy:**")
        render_twisty_case_preview(
            setup_alg="F2 D' R2 D",
            solve_alg="D' R2 D F2",
            camera_latitude=25,
            camera_longitude=35,
        )


def render_f2l_cases_with_visuals():
    """Phần 2: 4 trường hợp F2L cơ bản làm sáng 2 mảnh góc + cạnh cần giải."""
    st.subheader("2️⃣ F2L (First Two Layers) — Minh họa trực quan từng trường hợp")
    st.caption(
        "Mặt Vàng ở trên, mặt Trắng ở dưới. Đèn chiếu làm sáng 2 mảnh góc + cạnh cần giải cho khe FR."
    )

    f2l_visual_cases = [
        {
            "id": "f2l_1",
            "group": "F2L cơ bản",
            "title": "Trường hợp 1: Mặt trắng của góc hướng sang phải, cạnh khớp mặt trước",
            "desc": "Đưa cạnh khớp màu tâm trước rồi xoay gắp cả cặp góc-cạnh xuống khe FR.",
            "setup": "R U R' U'",
            "alg": "U R U' R'",
            "tip": "Ghép cặp và đưa vào khe liền mạch trong 4 nước xoay.",
        },
        {
            "id": "f2l_2",
            "group": "F2L cơ bản",
            "title": "Trường hợp 2: Cặp ghép sẵn trên đỉnh, mặt trắng góc hướng ra trước",
            "desc": "Góc và cạnh đã đứng cạnh nhau trên đỉnh nhưng lệch màu; xoay đưa thẳng vào khe.",
            "setup": "R U' R'",
            "alg": "R U R'",
            "tip": "Giữ góc ở vị trí trước-phải rồi đẩy vào khe gọn gàng.",
        },
        {
            "id": "f2l_3",
            "group": "F2L cơ bản",
            "title": "Trường hợp 3: Tách cặp bị dính sai hướng",
            "desc": "Góc và cạnh đang dính liền nhau trên đỉnh nhưng sai chiều, cần tách ra ghép lại.",
            "setup": "R U2 R' U R U R' U",
            "alg": "U' R U' R' U2 R U' R'",
            "tip": "Tách hai mảnh trước khi đưa vào khe để tránh kẹt màu.",
        },
        {
            "id": "f2l_4",
            "group": "F2L cơ bản",
            "title": "Trường hợp 4: Mảnh kẹt sẵn trong khe sai chiều",
            "desc": "Cả góc và cạnh đều nằm sẵn ở khe FR nhưng bị xoay ngược hướng.",
            "setup": "R U R' U' R U R'",
            "alg": "R U' R' U R U' R'",
            "tip": "Đưa cặp lên tầng trên trước rồi xử lý như cặp thường.",
        },
    ]

    render_algorithm_cards(f2l_visual_cases, highlight_f2l_pair=True)


def render_oll_section():
    """Phần 3: 2-Look OLL ở mặt trên Vàng."""
    st.subheader("3️⃣ OLL (Orient Last Layer) — Làm đều mặt Vàng ở trên")
    st.write(
        "Mục tiêu: Toàn bộ **mặt trên (mặt Vàng)** cùng màu Vàng (chưa cần đúng màu viền). "
        "Người mới nên dùng **2-Look OLL** (10 công thức chia làm 2 bước nhỏ)."
    )

    oll_sub = st.segmented_control(
        "Chọn bước trong 2-Look OLL:",
        ["Bước 3A: Tạo chữ thập vàng (3 công thức)", "Bước 3B: Lật đều 4 góc vàng (7 công thức)"],
        default="Bước 3A: Tạo chữ thập vàng (3 công thức)",
    )

    if "3A" in oll_sub:
        oll_items = [
            {
                "id": "oll_line",
                "title": "Hình đường thẳng (Line)",
                "desc": "3 ô vàng thẳng hàng ngang ở mặt trên.",
                "setup": "F U R U' R' F'",
                "alg": "F R U R' U' F'",
                "tip": "Giữ đường thẳng nằm ngang trước khi thực hiện công thức.",
            },
            {
                "id": "oll_l",
                "title": "Hình chữ L (L-Shape)",
                "desc": "2 cạnh vàng tạo góc ở vị trí 9h và 12h (hoặc xoay 2 lớp trước).",
                "setup": "f U R U' R' f'",
                "alg": "f R U R' U' f'",
                "tip": "Xoay đồng thời 2 lớp trước (f) giúp tạo chữ thập nhanh.",
            },
            {
                "id": "oll_dot",
                "title": "Hình dấu chấm (Dot)",
                "desc": "Chỉ có tâm vàng ở mặt trên, không có cạnh vàng nào.",
                "setup": "f U R U' R' f' F U R U' R' F'",
                "alg": "F R U R' U' F' f R U R' U' f'",
                "tip": "Thực hiện nối tiếp công thức đường thẳng và chữ L.",
            },
        ]
    else:
        oll_items = [
            {
                "id": "oll_sune",
                "title": "Sune (Con cá thuận)",
                "desc": "1 góc vàng ở dưới-trái, 3 góc còn lại hướng ra ngoài.",
                "setup": "R U2 R' U' R U' R'",
                "alg": "R U R' U R U2 R'",
                "tip": "Công thức nền tảng quan trọng nhất cho phần OLL.",
            },
            {
                "id": "oll_antisune",
                "title": "Anti-Sune (Con cá ngược)",
                "desc": "1 góc vàng ở trên-phải, 3 góc còn lại hướng ngược chiều.",
                "setup": "R U R' U R U2 R'",
                "alg": "R U2 R' U' R U' R'",
                "tip": "Thực hiện ngược chiều Sune để tiết kiệm lượt xoay.",
            },
            {
                "id": "oll_h",
                "title": "Hình chữ H (Cross + 4 góc đối)",
                "desc": "2 cặp góc vàng hướng đối diện nhau ra trước và sau.",
                "setup": "R U2 R' U' R U R' U' R U' R'",
                "alg": "R U R' U R U' R' U R U2 R'",
                "tip": "Dễ nhớ theo nhịp R-U xen kẽ.",
            },
            {
                "id": "oll_pi",
                "title": "Hình chữ Pi",
                "desc": "2 góc vàng hướng sang trái, 2 góc hướng ra trước và sau.",
                "setup": "R' U2 R2 U R2 U R2 U2 R'",
                "alg": "R U2 R2 U' R2 U' R2 U2 R",
                "tip": "Tập trung vào cụm R2 xoay liên tiếp.",
            },
            {
                "id": "oll_u",
                "title": "Hình chữ U (Headlights)",
                "desc": "2 góc vàng đã đúng ở sau, 2 góc trước hướng thẳng về mặt bạn.",
                "setup": "R U2 R D R' U2 R D' R2",
                "alg": "R2 D R' U2 R D' R' U2 R'",
                "tip": "Giữ 2 góc đã khớp màu vàng ở mặt sau.",
            },
            {
                "id": "oll_t",
                "title": "Hình chữ T",
                "desc": "2 góc vàng bên phải đã đúng, 2 góc bên trái hướng ra trước/sau.",
                "setup": "F R' F' r U R U' r'",
                "alg": "r U R' U' r' F R F'",
                "tip": "Phối hợp lớp đôi r và các bước R-U gọn tay.",
            },
            {
                "id": "oll_bowtie",
                "title": "Hình nơ (Bowtie / L)",
                "desc": "2 góc vàng chéo nhau đã đúng, 2 góc còn lại lệch hướng.",
                "setup": "R' F' r U R' U' r' F",
                "alg": "F' r U R' U' r' F R",
                "tip": "Kiểm tra kỹ 2 góc chéo đã khớp vàng trước khi xoay.",
            },
        ]

    render_algorithm_cards(oll_items, default_camera=(45, 30))


def render_pll_section():
    """Phần 4: 2-Look PLL ở tầng trên (mặt Vàng trên, mặt Trắng dưới)."""
    st.subheader("4️⃣ PLL (Permute Last Layer) — Hoán vị tầng Vàng trên cùng")
    st.write(
        "Mục tiêu: Đưa toàn bộ góc và cạnh tầng 3 (tầng Vàng) về đúng màu các mặt bên. "
        "Chia làm **2-Look PLL** (2 bước góc + 4 bước cạnh)."
    )

    pll_sub = st.segmented_control(
        "Chọn bước trong 2-Look PLL:",
        ["Bước 4A: Hoán vị các góc (2 công thức)", "Bước 4B: Hoán vị các cạnh (4 công thức)"],
        default="Bước 4A: Hoán vị các góc (2 công thức)",
    )

    if "4A" in pll_sub:
        pll_items = [
            {
                "id": "pll_t",
                "title": "T-Perm (Đổi 2 góc kề bên phải)",
                "desc": "Có 2 góc cùng màu ở mặt bên trái (đặt bên trái rồi làm).",
                "setup": "F R U' R' U R U2 R2 F' R U R U' R'",
                "alg": "R U R' U' R' F R2 U' R' U' R U R' F'",
                "tip": "Một trong các công thức PLL phổ biến và dễ nhớ nhịp nhất.",
            },
            {
                "id": "pll_y",
                "title": "Y-Perm (Đổi 2 góc chéo nhau)",
                "desc": "Không có cặp góc nào cùng màu ở bất kỳ mặt bên nào.",
                "setup": "F R' F' R U R U' R' F R' U R U R' F'",
                "alg": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
                "tip": "Tách làm 2 cụm rõ ràng để tránh nhầm chiều F và F'.",
            },
        ]
    else:
        pll_items = [
            {
                "id": "pll_ua",
                "title": "Ua-Perm (Xoay 3 cạnh thuận chiều)",
                "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy thuận kim đồng hồ.",
                "setup": "R2 U R U R' U' R' U' R' U R'",
                "alg": "R U' R U R U R U' R' U' R2",
                "tip": "Đặt cạnh đã đúng vị trí ở mặt sau (Back).",
            },
            {
                "id": "pll_ub",
                "title": "Ub-Perm (Xoay 3 cạnh ngược chiều)",
                "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy ngược kim đồng hồ.",
                "setup": "R2 U R U R' U' R' U' R' U R'",
                "alg": "R2 U R U R' U' R' U' R' U R'",
                "tip": "Đặt cạnh đã đúng vị trí ở mặt sau (Back).",
            },
            {
                "id": "pll_h",
                "title": "H-Perm (Đổi 2 cặp cạnh đối diện)",
                "desc": "4 mặt đều có cạnh đối diện màu nhau.",
                "setup": "M2 U' M2 U2' M2 U' M2",
                "alg": "M2 U M2 U2 M2 U M2",
                "tip": "Dùng lớp giữa M2 giúp thao tác nhanh trên 3x3.",
            },
            {
                "id": "pll_z",
                "title": "Z-Perm (Đổi 2 cặp cạnh kề nhau)",
                "desc": "Cạnh trước đổi với cạnh phải, cạnh sau đổi với cạnh trái.",
                "setup": "M2 U2 M U' M2' U' M2' U' M",
                "alg": "M' U M2 U M2 U M' U2 M2",
                "tip": "Luyện đều tay lớp M và U để chuyển mạch mượt.",
            },
        ]

    render_algorithm_cards(pll_items, default_camera=(45, 30))


# Tạo 4 Tab chính
tab1, tab2, tab3, tab4 = st.tabs([
    "📚 Cơ bản (LBL)",
    "⚡ Lộ trình CFOP (4 Phần)",
    "🎮 Mô hình 3D & Ký hiệu",
    "⏱️ Luyện tập & Bấm giờ",
])

# ==========================================
# TAB 1: PHƯƠNG PHÁP CƠ BẢN (LAYER-BY-LAYER)
# ==========================================
with tab1:
    st.header("Phương pháp giải từng tầng (Beginner's Method)")
    st.caption("Quy ước: Mặt Vàng ở trên (U), mặt Trắng ở dưới (D).")
    step = st.selectbox(
        "Chọn bước cơ bản:",
        [
            "Bước 1: Tạo chữ thập đáy Trắng (White Cross)",
            "Bước 2: Giải 4 góc tầng đáy Trắng",
            "Bước 3: Giải tầng 2 (Second Layer Edges)",
            "Bước 4: Tạo chữ thập vàng mặt trên",
            "Bước 5: Hoàn thiện mặt vàng (OLL cơ bản)",
            "Bước 6: Đưa các góc vàng về đúng vị trí (PLL góc)",
            "Bước 7: Hoàn tất các cạnh tầng vàng (PLL cạnh)",
        ],
    )
    st.divider()

    if "Bước 1" in step:
        st.subheader("Bước 1: Tạo chữ thập đáy Trắng (White Cross)")
        st.write("- **Mục tiêu:** Đưa 4 viên cạnh trắng về quanh tâm trắng ở đáy sao cho trùng màu với 4 tâm mặt bên.")
        st.info("💡 **Mẹo:** Quan sát cạnh trắng ở trên/bên và đưa trực tiếp xuống mặt Trắng ở dưới.")
    elif "Bước 2" in step:
        st.subheader("Bước 2: Giải 4 góc tầng đáy Trắng")
        st.write("- **Mục tiêu:** Đưa 4 viên góc có màu trắng vào đúng vị trí giữa 3 tâm tương ứng ở đáy.")
        st.code("R U R' U'", language="text")
        st.write("Đặt viên góc ở góc trên-bên phải mặt trước và lặp lại công thức từ 1–5 lần.")
    elif "Bước 3" in step:
        st.subheader("Bước 3: Giải tầng 2")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Đưa cạnh xuống BÊN PHẢI:**")
            st.code("U R U' R' U' F' U F", language="text")
        with col2:
            st.markdown("**Đưa cạnh xuống BÊN TRÁI:**")
            st.code("U' L' U L U F U' F'", language="text")
    elif "Bước 4" in step:
        st.subheader("Bước 4: Tạo chữ thập vàng mặt trên")
        st.code("F R U R' U' F'", language="text")
        st.write("- **Dấu chấm** $\\rightarrow$ **Chữ L ngược** (góc 9h–12h) $\\rightarrow$ **Đường thẳng** (nằm ngang) $\\rightarrow$ **Chữ thập**.")
    elif "Bước 5" in step:
        st.subheader("Bước 5: Hoàn thiện mặt vàng (Sune)")
        st.code("R U R' U R U2 R'", language="text")
        st.write("Khi ra hình 'Con cá', hướng đầu cá về góc dưới-bên trái rồi áp dụng công thức.")
    elif "Bước 6" in step:
        st.subheader("Bước 6: Hoán vị góc tầng vàng")
        st.code("R' F R' B2 R F' R' B2 R2", language="text")
    elif "Bước 7" in step:
        st.subheader("Bước 7: Hoàn tất các cạnh tầng vàng")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Thuận chiều kim đồng hồ:**")
            st.code("R U' R U R U R U' R' U' R2", language="text")
        with col2:
            st.markdown("**Ngược chiều kim đồng hồ:**")
            st.code("R2 U R U R' U' R' U' R' U R'", language="text")

# ==========================================
# TAB 2: LỘ TRÌNH CFOP CHIA 4 PHẦN RÕ RÀNG
# ==========================================
with tab2:
    st.header("⚡ Phương Pháp Giải Nhanh CFOP (Chia 4 Phần)")
    st.markdown("Mặt **Vàng ở trên**, mặt **Trắng ở dưới**. Chọn từng giai đoạn để học mục tiêu, cách nhận diện, mô phỏng 3D và công thức.")

    cfop_part = st.radio(
        "Chọn giai đoạn CFOP:",
        [
            "1️⃣ Phần 1: Cross (Chữ thập đáy Trắng)",
            "2️⃣ Phần 2: F2L (Hai tầng đầu)",
            "3️⃣ Phần 3: OLL (Định hướng mặt Vàng trên)",
            "4️⃣ Phần 4: PLL (Hoán vị tầng Vàng trên)",
        ],
        horizontal=True,
    )

    st.divider()

    if "Phần 1" in cfop_part:
        render_cross_section()
    elif "Phần 2" in cfop_part:
        render_f2l_cases_with_visuals()
    elif "Phần 3" in cfop_part:
        render_oll_section()
    elif "Phần 4" in cfop_part:
        render_pll_section()

    # Thanh tiến độ học CFOP
    st.divider()
    total_cfop_algs = 20  # 4 F2L + 10 OLL + 6 PLL
    learned_count = len(st.session_state.learned_cfop)
    st.progress(
        min(learned_count / total_cfop_algs, 1.0),
        text=f"Tiến độ thuộc công thức CFOP nền tảng: {learned_count}/{total_cfop_algs} công thức",
    )

# ==========================================
# TAB 3: MÔ HÌNH 3D TƯƠNG TÁC & KÝ HIỆU
# ==========================================
with tab3:
    col_sim, col_not = st.columns([1.3, 1])

    with col_sim:
        st.subheader("Mô phỏng Rubik 3D (Vàng trên • Trắng dưới)")
        custom_alg = st.text_input(
            "Nhập chuỗi công thức muốn xem mô phỏng (VD: R U R' U R U2 R'):",
            value="R U R' U'",
        )

        rubik_3d_html = f"""
        <script src="https://cdn.cubing.net/js/cubing/twisty" type="module"></script>
        <div style="display: flex; flex-direction: column; align-items: center; background: #f0f2f6; padding: 15px; border-radius: 10px;">
            <twisty-player
                id="player"
                puzzle="3x3x3"
                experimental-setup-alg="{BASE_ORIENTATION}"
                alg="{custom_alg}"
                experimental-setup-anchor="end"
                background="none"
                style="width: 100%; height: 340px;">
            </twisty-player>
        </div>
        """
        components.html(rubik_3d_html, height=380)

    with col_not:
        st.subheader("Bảng quy ước ký hiệu (Notation)")
        st.markdown("""
        * **Mặt trên (U):** Vàng • **Mặt dưới (D):** Trắng
        * **R / L:** Mặt Phải / Trái
        * **U / D:** Mặt Trên / Dưới
        * **F / B:** Mặt Trước / Sau
        * **M:** Lớp giữa (xoay cùng chiều mặt L)
        * **f / r:** Xoay đồng thời 2 lớp Trước / Phải
        
        **Quy tắc chiều xoay:**
        * Chữ in hoa (`R`): Xoay **90° thuận** chiều kim đồng hồ.
        * Dấu phẩy (`R'`): Xoay **90° ngược** chiều kim đồng hồ.
        * Số 2 (`R2`): Xoay **180°**.
        """)

# ==========================================
# TAB 4: LUYỆN TẬP & BẤM GIỜ
# ==========================================
with tab4:
    st.header("Trình tạo Scramble & Bấm giờ")

    def generate_scramble(length=20):
        faces = ["R", "L", "U", "D", "F", "B"]
        modifiers = ["", "'", "2"]
        scramble = []
        last_face = ""
        for _ in range(length):
            face = random.choice([f for f in faces if f != last_face])
            last_face = face
            scramble.append(face + random.choice(modifiers))
        return " ".join(scramble)

    if "scramble" not in st.session_state:
        st.session_state.scramble = generate_scramble()
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "history" not in st.session_state:
        st.session_state.history = []

    st.info(f"### `{st.session_state.scramble}`")
    if st.button("🔄 Tạo Scramble mới"):
        st.session_state.scramble = generate_scramble()
        st.rerun()

    st.divider()
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.session_state.start_time is None:
            if st.button("▶️ Bắt đầu tính giờ", type="primary", use_container_width=True):
                st.session_state.start_time = time.time()
                st.rerun()
        else:
            st.warning("⏳ Đang tính giờ...")
            if st.button("⏹️ Dừng lại (Hoàn thành)", type="primary", use_container_width=True):
                elapsed = round(time.time() - st.session_state.start_time, 2)
                st.session_state.history.insert(
                    0,
                    {"Thời gian (giây)": elapsed, "Scramble": st.session_state.scramble},
                )
                st.session_state.start_time = None
                st.session_state.scramble = generate_scramble()
                st.rerun()

    with col_t2:
        st.subheader("Lịch sử thành tích")
        if st.session_state.history:
            st.dataframe(st.session_state.history, use_container_width=True)
            if st.button("Xóa lịch sử"):
                st.session_state.history = []
                st.rerun()
        else:
            st.write("Chưa có lượt giải nào được ghi nhận.")
