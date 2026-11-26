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
    "với mô phỏng 3D trực quan từng trường hợp F2L và bộ bấm giờ."
)

# Khởi tạo trạng thái lưu tiến độ học CFOP
if "learned_cfop" not in st.session_state:
    st.session_state.learned_cfop = set()


def render_twisty_case_preview(setup_alg: str, solve_alg: str, height: int = 225):
    """Hiển thị trình phát Rubik 3D cho từng tình huống giải."""
    html_code = f"""
    <script src="https://cdn.cubing.net/js/cubing/twisty" type="module"></script>
    <div style="background: #f8f9fa; border: 1px solid #e0e4e8; border-radius: 10px; padding: 8px;">
        <twisty-player
            puzzle="3x3x3"
            experimental-setup-alg="{setup_alg}"
            alg="{solve_alg}"
            background="none"
            control-panel="bottom-row"
            style="width: 100%; height: {height}px;">
        </twisty-player>
    </div>
    """
    components.html(html_code, height=height + 20)


def render_f2l_cases_with_visuals():
    """Hiển thị 4 trường hợp F2L cơ bản kèm mô phỏng 3D trực quan và đánh dấu đã thuộc."""
    st.subheader("2️⃣ F2L (First Two Layers) — Minh họa trực quan từng trường hợp")
    st.caption(
        "Nhấn nút Play trên từng khung mô phỏng để xem cách ghép cặp góc + cạnh "
        "và đưa vào khe trước-phải (FR)."
    )

    f2l_visual_cases = [
        {
            "id": "f2l_1",
            "title": "Trường hợp 1: Góc trắng hướng sang phải, cạnh khớp mặt trước",
            "desc": "Đưa cạnh khớp màu tâm trước rồi xoay gắp cả cặp góc-cạnh xuống khe FR.",
            "setup": "R U R' U'",
            "alg": "U R U' R'",
            "tip": "Ghép cặp và đưa vào khe liền mạch trong 4 nước xoay.",
        },
        {
            "id": "f2l_2",
            "title": "Trường hợp 2: Cặp ghép sẵn trên đỉnh, góc trắng hướng ra trước",
            "desc": "Góc và cạnh đã đứng cạnh nhau trên đỉnh nhưng lệch màu; xoay đưa thẳng vào khe.",
            "setup": "R U' R'",
            "alg": "R U R'",
            "tip": "Giữ góc ở vị trí trước-phải rồi đẩy vào khe gọn gàng.",
        },
        {
            "id": "f2l_3",
            "title": "Trường hợp 3: Tách cặp bị dính sai hướng",
            "desc": "Góc và cạnh đang dính liền nhau trên đỉnh nhưng sai chiều, cần tách ra ghép lại.",
            "setup": "R U2 R' U R U R' U",
            "alg": "U' R U' R' U2 R U' R'",
            "tip": "Tách hai mảnh trước khi đưa vào khe để tránh kẹt màu.",
        },
        {
            "id": "f2l_4",
            "title": "Trường hợp 4: Mảnh kẹt sẵn trong khe sai chiều",
            "desc": "Cả góc và cạnh đều nằm sẵn ở khe FR nhưng bị xoay ngược hướng.",
            "setup": "R U R' U' R U R'",
            "alg": "R U' R' U R U' R'",
            "tip": "Đưa cặp lên tầng trên trước rồi xử lý như cặp thường.",
        },
    ]

    for case in f2l_visual_cases:
        with st.expander(f"**{case['title']}** — `{case['alg']}`", expanded=True):
            col_info, col_view = st.columns([1.3, 1])
            with col_info:
                st.markdown(f"**Nhận diện:** {case['desc']}")
                st.markdown("**Công thức giải:**")
                st.code(case["alg"], language="text")
                st.info(f"💡 **Mẹo:** {case['tip']}")

                checked = st.checkbox(
                    "Đã thuộc trường hợp này",
                    key=case["id"],
                    value=(case["id"] in st.session_state.learned_cfop),
                )
                if checked:
                    st.session_state.learned_cfop.add(case["id"])
                else:
                    st.session_state.learned_cfop.discard(case["id"])

            with col_view:
                render_twisty_case_preview(setup_alg=case["setup"], solve_alg=case["alg"])


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
    step = st.selectbox(
        "Chọn bước cơ bản:",
        [
            "Bước 1: Tạo chữ thập trắng (White Cross)",
            "Bước 2: Giải 4 góc tầng 1 (First Layer Corners)",
            "Bước 3: Giải tầng 2 (Second Layer Edges)",
            "Bước 4: Tạo chữ thập vàng mặt trên (Yellow Cross)",
            "Bước 5: Hoàn thiện mặt vàng (OLL cơ bản)",
            "Bước 6: Đưa các góc vàng về đúng vị trí (PLL góc)",
            "Bước 7: Hoàn tất các cạnh tầng 3 (PLL cạnh)",
        ],
    )
    st.divider()

    if "Bước 1" in step:
        st.subheader("Bước 1: Tạo chữ thập trắng (White Cross)")
        st.write("- **Mục tiêu:** Đưa 4 viên cạnh trắng về quanh tâm trắng sao cho trùng màu với 4 tâm mặt bên.")
        st.info("💡 **Mẹo:** Làm 'Hoa cúc' quanh tâm vàng trước, xoay khớp tâm bên rồi lật 180° xuống đáy.")
    elif "Bước 2" in step:
        st.subheader("Bước 2: Giải 4 góc tầng 1")
        st.write("- **Mục tiêu:** Đưa 4 viên góc trắng vào đúng vị trí giữa 3 tâm tương ứng.")
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
        st.subheader("Bước 4: Tạo chữ thập vàng")
        st.code("F R U R' U' F'", language="text")
        st.write("- **Dấu chấm** $\\rightarrow$ **Chữ L ngược** (góc 9h–12h) $\\rightarrow$ **Đường thẳng** (nằm ngang) $\\rightarrow$ **Chữ thập**.")
    elif "Bước 5" in step:
        st.subheader("Bước 5: Hoàn thiện mặt vàng (Sune)")
        st.code("R U R' U R U2 R'", language="text")
        st.write("Khi ra hình 'Con cá', hướng đầu cá về góc dưới-bên trái rồi áp dụng công thức.")
    elif "Bước 6" in step:
        st.subheader("Bước 6: Hoán vị góc tầng 3")
        st.code("R' F R' B2 R F' R' B2 R2", language="text")
    elif "Bước 7" in step:
        st.subheader("Bước 7: Hoàn tất các cạnh cuối cùng")
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
    st.markdown("Chọn từng giai đoạn bên dưới để học mục tiêu, cách nhận diện và bộ công thức tương ứng.")

    cfop_part = st.radio(
        "Chọn giai đoạn CFOP:",
        [
            "1️⃣ Phần 1: Cross (Chữ thập đáy)",
            "2️⃣ Phần 2: F2L (Hai tầng đầu)",
            "3️⃣ Phần 3: OLL (Định hướng mặt trên)",
            "4️⃣ Phần 4: PLL (Hoán vị tầng cuối)",
        ],
        horizontal=True,
    )

    st.divider()

    # --- PHẦN 1: CROSS ---
    if "Phần 1" in cfop_part:
        st.subheader("1️⃣ Cross — Giải chữ thập ở mặt đáy")
        col_c1, col_c2 = st.columns([1.4, 1])
        with col_c1:
            st.markdown("""
            * **Mục tiêu:** Giải thẳng 4 viên cạnh trắng ở **mặt đáy (D)** và khớp màu tâm bên trong **dưới 8 bước xoay**.
            * **Sự khác biệt so với cách cơ bản:** Không làm hoa cúc ở mặt trên, không lật ngược khối Rubik sau khi xong Cross.
            * **Nguyên tắc luyện tập:**
              1. **Tận dụng 15 giây quan sát (Inspection):** Nhớ vị trí cả 4 viên cạnh trước khi chạm tay vào khối.
              2. **Giải theo vị trí tương đối:** Đặt đúng thứ tự các màu (Đỏ đối Cam, Xanh lá đối Xanh dương), sau đó xoay mặt D một lượt để khớp toàn bộ tâm.
              3. **Tập giải nhắm mắt (Blind Cross):** Quan sát xong, nhắm mắt và xoay hết Cross để tăng khả năng nhìn trước cho phần F2L.
            """)
        with col_c2:
            st.info(
                "**Tóm tắt chỉ số Phần 1**\n\n"
                "- Số công thức học thuộc: **0** (Giải trực quan)\n"
                "- Số bước tối ưu: **6 – 8 moves**\n"
                "- Mục tiêu thời gian: **< 3 giây**"
            )

    # --- PHẦN 2: F2L (KÈM MÔ PHỎNG 3D) ---
    elif "Phần 2" in cfop_part:
        render_f2l_cases_with_visuals()

    # --- PHẦN 3: OLL ---
    elif "Phần 3" in cfop_part:
        st.subheader("3️⃣ OLL (Orient Last Layer) — Làm đều màu mặt trên")
        st.write(
            "Mục tiêu: Toàn bộ mặt trên cùng màu Vàng (chưa cần đúng màu viền). "
            "Người mới nên dùng **2-Look OLL** (10 công thức chia làm 2 bước nhỏ)."
        )

        oll_sub = st.segmented_control(
            "Chọn bước trong 2-Look OLL:",
            ["Bước 3A: Tạo chữ thập vàng (3 công thức)", "Bước 3B: Lật đều 4 góc vàng (7 công thức)"],
            default="Bước 3A: Tạo chữ thập vàng (3 công thức)",
        )

        if "3A" in oll_sub:
            oll_items = [
                {"id": "oll_line", "title": "Hình đường thẳng (Line)", "desc": "3 ô vàng thẳng hàng ngang ở mặt trên.", "alg": "F R U R' U' F'"},
                {"id": "oll_l", "title": "Hình chữ L (L-Shape)", "desc": "2 cạnh vàng tạo góc ở vị trí 9h và 12h (hoặc xoay 2 lớp trước).", "alg": "f R U R' U' f'"},
                {"id": "oll_dot", "title": "Hình dấu chấm (Dot)", "desc": "Chỉ có tâm vàng ở mặt trên, không có cạnh vàng nào.", "alg": "F R U R' U' F' f R U R' U' f'"},
            ]
        else:
            oll_items = [
                {"id": "oll_sune", "title": "Sune (Con cá thuận)", "desc": "1 góc vàng ở dưới-trái, 3 góc còn lại hướng ra ngoài.", "alg": "R U R' U R U2 R'"},
                {"id": "oll_antisune", "title": "Anti-Sune (Con cá ngược)", "desc": "1 góc vàng ở trên-phải, 3 góc còn lại hướng ngược chiều.", "alg": "R U2 R' U' R U' R'"},
                {"id": "oll_h", "title": "Hình chữ H (Cross + 4 góc đối)", "desc": "2 cặp góc vàng hướng đối diện nhau ra trước và sau.", "alg": "R U R' U R U' R' U R U2 R'"},
                {"id": "oll_pi", "title": "Hình chữ Pi", "desc": "2 góc vàng hướng sang trái, 2 góc hướng ra trước và sau.", "alg": "R U2 R2 U' R2 U' R2 U2 R"},
                {"id": "oll_u", "title": "Hình chữ U (Headlights)", "desc": "2 góc vàng đã đúng ở sau, 2 góc trước hướng thẳng về mặt bạn.", "alg": "R2 D R' U2 R D' R' U2 R'"},
                {"id": "oll_t", "title": "Hình chữ T", "desc": "2 góc vàng bên phải đã đúng, 2 góc bên trái hướng ra trước/sau.", "alg": "r U R' U' r' F R F'"},
                {"id": "oll_bowtie", "title": "Hình nơ (Bowtie / L)", "desc": "2 góc vàng chéo nhau đã đúng, 2 góc còn lại lệch hướng.", "alg": "F' r U R' U' r' F R"},
            ]

        for item in oll_items:
            with st.expander(f"**{item['title']}** — `{item['alg']}`", expanded=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Nhận diện:** {item['desc']}")
                    st.code(item["alg"], language="text")
                with c2:
                    checked = st.checkbox(
                        "Đã thuộc",
                        key=item["id"],
                        value=(item["id"] in st.session_state.learned_cfop),
                    )
                    if checked:
                        st.session_state.learned_cfop.add(item["id"])
                    else:
                        st.session_state.learned_cfop.discard(item["id"])

    # --- PHẦN 4: PLL ---
    elif "Phần 4" in cfop_part:
        st.subheader("4️⃣ PLL (Permute Last Layer) — Hoán vị tầng cuối")
        st.write(
            "Mục tiêu: Đưa toàn bộ góc và cạnh tầng 3 về đúng màu các mặt bên. "
            "Chia làm **2-Look PLL** (2 bước góc + 4 bước cạnh)."
        )

        pll_sub = st.segmented_control(
            "Chọn bước trong 2-Look PLL:",
            ["Bước 4A: Hoán vị các góc (2 công thức)", "Bước 4B: Hoán vị các cạnh (4 công thức)"],
            default="Bước 4A: Hoán vị các góc (2 công thức)",
        )

        if "4A" in pll_sub:
            pll_items = [
                {"id": "pll_t", "title": "T-Perm (Đổi 2 góc kề bên phải)", "desc": "Có 2 góc cùng màu ở mặt bên trái (đặt bên trái rồi làm).", "alg": "R U R' U' R' F R2 U' R' U' R U R' F'"},
                {"id": "pll_y", "title": "Y-Perm (Đổi 2 góc chéo nhau)", "desc": "Không có cặp góc nào cùng màu ở bất kỳ mặt bên nào.", "alg": "F R U' R' U' R U R' F' R U R' U' R' F R F'"},
            ]
        else:
            pll_items = [
                {"id": "pll_ua", "title": "Ua-Perm (Xoay 3 cạnh thuận chiều)", "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy thuận kim đồng hồ.", "alg": "R U' R U R U R U' R' U' R2"},
                {"id": "pll_ub", "title": "Ub-Perm (Xoay 3 cạnh ngược chiều)", "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy ngược kim đồng hồ.", "alg": "R2 U R U R' U' R' U' R' U R'"},
                {"id": "pll_h", "title": "H-Perm (Đổi 2 cặp cạnh đối diện)", "desc": "4 mặt đều có cạnh đối diện màu nhau.", "alg": "M2 U M2 U2 M2 U M2"},
                {"id": "pll_z", "title": "Z-Perm (Đổi 2 cặp cạnh kề nhau)", "desc": "Cạnh trước đổi với cạnh phải, cạnh sau đổi với cạnh trái.", "alg": "M' U M2 U M2 U M' U2 M2"},
            ]

        for item in pll_items:
            with st.expander(f"**{item['title']}** — `{item['alg']}`", expanded=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**Nhận diện:** {item['desc']}")
                    st.code(item["alg"], language="text")
                with c2:
                    checked = st.checkbox(
                        "Đã thuộc",
                        key=item["id"],
                        value=(item["id"] in st.session_state.learned_cfop),
                    )
                    if checked:
                        st.session_state.learned_cfop.add(item["id"])
                    else:
                        st.session_state.learned_cfop.discard(item["id"])

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
        st.subheader("Mô phỏng Rubik 3D & Chạy thử công thức")
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
