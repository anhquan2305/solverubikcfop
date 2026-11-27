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
    "với 41 trường hợp F2L làm nổi bật **2 mảnh góc + cạnh cần giải**, OLL, PLL và bộ bấm giờ."
)

# Khởi tạo trạng thái lưu tiến độ học CFOP
if "learned_cfop" not in st.session_state:
    st.session_state.learned_cfop = set()

# ==========================================
# BỘ DỮ LIỆU ĐẦY ĐỦ 41 TRƯỜNG HỢP F2L (KHE FR)
# ==========================================
F2L_41_CASES = [
    # --- NHÓM 1: CẢ GÓC VÀ CẠNH Ở TẦNG TRÊN, TÁCH RỜI (16 TRƯỜNG HỢP) ---
    {
        "id": "f2l_01",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #01: Góc trắng Phải, cạnh khớp tâm Trước",
        "desc": "Viên góc có mặt trắng ở bên phải, cạnh nằm trên đỉnh và khớp màu với tâm mặt trước.",
        "alg": "U R U' R'",
        "tip": "Đưa cạnh khớp tâm rồi dùng R U' R' gắp thẳng vào khe FR.",
    },
    {
        "id": "f2l_02",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #02: Góc trắng Phải, cạnh trên đỉnh lệch tâm Trước",
        "desc": "Góc có mặt trắng ở bên phải, cạnh ở trên đỉnh nhưng khác màu tâm trước.",
        "alg": "U' F' U F",
        "tip": "Dùng khe trước-trái (FL) đưa cặp vào gọn gàng.",
    },
    {
        "id": "f2l_03",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #03: Góc trắng Phải, cạnh nằm sau-phải",
        "desc": "Góc có mặt trắng ở bên phải, cạnh ở vị trí thuận lợi phía sau.",
        "alg": "R U R' U2 R U R'",
        "tip": "Ghép tạm rồi đẩy vào khe trước-phải.",
    },
    {
        "id": "f2l_04",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #04: Góc trắng Phải, cạnh nằm trước-trái",
        "desc": "Góc có mặt trắng ở bên phải, cạnh nằm ở mặt trên phía trái.",
        "alg": "U2 R U' R' U' R U' R'",
        "tip": "Xoay U2 đưa về vị trí chuẩn trước khi ghép.",
    },
    {
        "id": "f2l_05",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #05: Góc trắng Phải, cạnh cần lật chiều",
        "desc": "Góc có mặt trắng ở bên phải, cạnh ở tầng trên cần đảo hướng trước khi ghép.",
        "alg": "U' R U2 R' U R U R'",
        "tip": "Tách khoảng cách hợp lý để ghép không bị kẹt.",
    },
    {
        "id": "f2l_06",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Phải)",
        "title": "F2L #06: Góc trắng Phải, cạnh nằm ở vị trí đối diện",
        "desc": "Góc có mặt trắng ở bên phải, cạnh nằm xa trên đỉnh.",
        "alg": "R U2 R' U' R U R'",
        "tip": "Đưa cặp về gần khe FR rồi chèn vào.",
    },
    {
        "id": "f2l_07",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #07: Góc trắng Trước, cạnh khớp tâm Phải",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh khớp màu với tâm mặt phải.",
        "alg": "U' F' U F",
        "tip": "Ghép nhanh bằng mặt trước và đưa vào khe.",
    },
    {
        "id": "f2l_08",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #08: Góc trắng Trước, cạnh ở đỉnh lệch tâm Phải",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh trên đỉnh chưa khớp tâm phải.",
        "alg": "R U R'",
        "tip": "Đưa cạnh vào đúng vị trí rồi gắp vào khe FR.",
    },
    {
        "id": "f2l_09",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #09: Góc trắng Trước, cạnh nằm bên trái",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh nằm ở khu vực bên trái tầng trên.",
        "alg": "U2 R U R' U R U' R'",
        "tip": "Tách ra và đưa cạnh về đúng phía trước khi ghép.",
    },
    {
        "id": "f2l_10",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #10: Góc trắng Trước, cạnh nằm phía sau",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh ở phía sau tầng trên.",
        "alg": "U' R U' R' U2 R U' R'",
        "tip": "Giấu góc rồi ghép cạnh mượt mà.",
    },
    {
        "id": "f2l_11",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #11: Góc trắng Trước, cạnh cần xoay ngược hướng",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh cần đổi chiều trước khi ghép.",
        "alg": "U' R U2 R' U R U' R'",
        "tip": "Kiểm tra màu cạnh trước khi chèn xuống.",
    },
    {
        "id": "f2l_12",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Trước)",
        "title": "F2L #12: Góc trắng Trước, cạnh ở vị trí đối xứng",
        "desc": "Góc có mặt trắng hướng ra trước, cạnh nằm cách 2 bước xoay.",
        "alg": "R U' R' U2 R U' R'",
        "tip": "Thực hiện liền mạch theo nhịp R và U.",
    },
    {
        "id": "f2l_13",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Lên)",
        "title": "F2L #13: Góc trắng Lên đỉnh, cạnh khớp tâm Phải",
        "desc": "Mặt trắng của viên góc hướng lên trên, cạnh khớp tâm phải.",
        "alg": "U2 R U R' U R U' R'",
        "tip": "Góc trắng hướng lên thường cần ghép tách trước rồi mới đưa vào khe.",
    },
    {
        "id": "f2l_14",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Lên)",
        "title": "F2L #14: Góc trắng Lên đỉnh, cạnh khớp tâm Trước",
        "desc": "Mặt trắng của viên góc hướng lên trên, cạnh khớp tâm trước.",
        "alg": "U' R U' R' U2 R U' R'",
        "tip": "Đưa cặp về trạng thái dễ chèn vào khe FR.",
    },
    {
        "id": "f2l_15",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Lên)",
        "title": "F2L #15: Góc trắng Lên đỉnh, cạnh ở bên trái",
        "desc": "Mặt trắng của viên góc hướng lên trên, cạnh ở phía trái tầng trên.",
        "alg": "R U R' U' R U R' U' R U R'",
        "tip": "Dùng chuỗi R U R' U' lặp lại để xử lý gọn.",
    },
    {
        "id": "f2l_16",
        "group": "1. Tách rời ở tầng trên (Góc trắng hướng Lên)",
        "title": "F2L #16: Góc trắng Lên đỉnh, cạnh ở phía sau",
        "desc": "Mặt trắng của viên góc hướng lên trên, cạnh ở phía sau tầng trên.",
        "alg": "R U' R' U2 F' U' F",
        "tip": "Phối hợp mặt R và F' để ghép nhanh.",
    },

    # --- NHÓM 2: DÍNH NHAU Ở TẦNG TRÊN (8 TRƯỜNG HỢP) ---
    {
        "id": "f2l_17",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #17: Cặp dính đúng hướng, đưa thẳng vào khe",
        "desc": "Góc và cạnh đã dính nhau đúng màu, đưa thẳng vào khe FR.",
        "alg": "R U2 R' U' R U R'",
        "tip": "Nhận diện nhanh cặp đúng màu để đưa xuống ngay.",
    },
    {
        "id": "f2l_18",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #18: Cặp dính đúng hướng, cần xoay U trước",
        "desc": "Góc và cạnh đã khớp màu với nhau nhưng lệch vị trí trên đỉnh.",
        "alg": "U2 R U' R' U' R U R'",
        "tip": "Căn chỉnh trên tầng trên rồi mới chèn xuống.",
    },
    {
        "id": "f2l_19",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #19: Cặp dính ngược chiều, đưa vào khe FR",
        "desc": "Góc và cạnh dính nhau nhưng đảo màu, đưa vào khe trước-phải.",
        "alg": "U R U2 R' U R U' R'",
        "tip": "Tách ra theo nhịp U R U2 R' rồi ghép lại.",
    },
    {
        "id": "f2l_20",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #20: Cặp dính ngược chiều, cần chỉnh U'",
        "desc": "Góc và cạnh dính nhau ngược chiều ở vị trí lệch về bên trái.",
        "alg": "U' R U' R' U2 R U' R'",
        "tip": "Tách đôi cặp mảnh trước khi đẩy vào khe.",
    },
    {
        "id": "f2l_21",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #21: Cặp dính tạo khối góc-cạnh lệch tâm",
        "desc": "Góc và cạnh dính liền nhưng tâm chưa khớp mặt trước/phải.",
        "alg": "R U' R' U R U2 R' U R U' R'",
        "tip": "Chia làm 2 nhịp: đưa lên tách rồi ghép chèn.",
    },
    {
        "id": "f2l_22",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #22: Cặp dính nằm ngang trên đỉnh",
        "desc": "Góc và cạnh dính nhau nằm ngang trên mặt U.",
        "alg": "F' U2 F U' R U R'",
        "tip": "Dùng F' mở đường rồi đưa vào khe FR.",
    },
    {
        "id": "f2l_23",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #23: Cặp dính hướng góc xuống dưới",
        "desc": "Cặp dính nhau nhưng mặt trắng của góc hướng lệch sang bên.",
        "alg": "U2 R2 U2 R' U' R U' R2",
        "tip": "Dùng R2 để xoay nhanh vị trí góc và cạnh.",
    },
    {
        "id": "f2l_24",
        "group": "2. Dính nhau ở tầng trên",
        "title": "F2L #24: Cặp dính ngược màu ở vị trí sau-phải",
        "desc": "Cặp dính nhau nhưng sai hướng ở góc sau-phải tầng trên.",
        "alg": "U' F' U F R U R'",
        "tip": "Xử lý cạnh trước rồi ghép vào khe FR.",
    },

    # --- NHÓM 3: GÓC NẰM TRONG KHE, CẠNH Ở TẦNG TRÊN (9 TRƯỜNG HỢP) ---
    {
        "id": "f2l_25",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #25: Góc trắng hướng ra trước trong khe FR",
        "desc": "Viên góc ở khe FR có mặt trắng hướng ra mặt trước, cạnh ở tầng trên.",
        "alg": "U' R' F R F' R U R'",
        "tip": "Lấy góc ra kết hợp ghép cạnh trên đỉnh.",
    },
    {
        "id": "f2l_26",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #26: Góc trắng hướng sang phải trong khe FR",
        "desc": "Viên góc ở khe FR có mặt trắng hướng sang phải, cạnh ở tầng trên.",
        "alg": "U R U' R' U' F' U F",
        "tip": "Đưa góc lên ghép với cạnh rồi chèn lại.",
    },
    {
        "id": "f2l_27",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #27: Góc đúng vị trí khe FR nhưng sai chiều",
        "desc": "Viên góc ở đúng khe FR nhưng mặt trắng không nằm ở đáy.",
        "alg": "R U' R' U R U' R'",
        "tip": "Đưa góc lên trên rồi xử lý như cặp thường.",
    },
    {
        "id": "f2l_28",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #28: Góc lệch chiều trong khe, cạnh khớp mặt trước",
        "desc": "Góc nằm sai hướng trong khe FR, cạnh nằm trên đỉnh khớp tâm trước.",
        "alg": "R U R' U' R U R'",
        "tip": "Ghép trực tiếp khi đưa góc lên trên.",
    },
    {
        "id": "f2l_29",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #29: Góc lệch chiều trong khe, cạnh ở bên trái",
        "desc": "Góc kẹt trong khe FR, cạnh nằm ở khu vực trái tầng trên.",
        "alg": "R U' R' U' R U R'",
        "tip": "Đưa góc lên đúng nhịp để ghép với cạnh.",
    },
    {
        "id": "f2l_30",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #30: Góc kẹt trong khe, cạnh nằm phía sau",
        "desc": "Góc ở khe FR bị xoay ngược, cạnh nằm ở mặt sau tầng trên.",
        "alg": "R U R' U' F' U' F",
        "tip": "Kết hợp xoay R và F' gọn tay.",
    },
    {
        "id": "f2l_31",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #31: Góc kẹt trong khe, cạnh cần đảo hướng",
        "desc": "Góc nằm trong khe FR, cạnh trên đỉnh cần đổi chiều.",
        "alg": "U' R U R' U R U' R'",
        "tip": "Tách góc ra và chỉnh hướng cạnh đồng thời.",
    },
    {
        "id": "f2l_32",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #32: Góc kẹt trong khe, cạnh đối diện",
        "desc": "Góc nằm trong khe FR, cạnh ở vị trí xa trên đỉnh.",
        "alg": "R U2 R' U' R U R'",
        "tip": "Đưa góc lên rồi ghép đưa vào khe.",
    },
    {
        "id": "f2l_33",
        "group": "3. Góc trong khe, cạnh trên đỉnh",
        "title": "F2L #33: Góc kẹt trong khe, cặp gần hoàn chỉnh",
        "desc": "Góc nằm trong khe FR, cạnh ở vị trí gần ghép nhất.",
        "alg": "U' R U' R' U R U' R'",
        "tip": "Dùng nhịp U' R U' R' để đưa cặp vào chuẩn.",
    },

    # --- NHÓM 4: CẠNH NẰM TRONG KHE, GÓC Ở TẦNG TRÊN (8 TRƯỜNG HỢP) ---
    {
        "id": "f2l_34",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #34: Cạnh nằm trong khe FR, góc trắng hướng Phải",
        "desc": "Viên cạnh nằm sẵn ở khe FR, góc có mặt trắng hướng sang phải trên đỉnh.",
        "alg": "R U R' U' R U R'",
        "tip": "Lấy cạnh ra và ghép cùng góc trên đỉnh.",
    },
    {
        "id": "f2l_35",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #35: Cạnh nằm trong khe FR, góc trắng hướng Trước",
        "desc": "Viên cạnh nằm sẵn ở khe FR, góc có mặt trắng hướng ra trước trên đỉnh.",
        "alg": "U' F' U F U R U' R'",
        "tip": "Tách cạnh lên ghép góc rồi đưa vào khe.",
    },
    {
        "id": "f2l_36",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #36: Cạnh nằm trong khe FR, góc trắng hướng Lên",
        "desc": "Viên cạnh nằm trong khe FR, mặt trắng của góc hướng lên trên đỉnh.",
        "alg": "U2 R U' R' U' R U R'",
        "tip": "Đưa góc về đúng vị trí rồi ghép với cạnh.",
    },
    {
        "id": "f2l_37",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #37: Cạnh nằm trong khe FR, góc lệch bên trái",
        "desc": "Cạnh ở khe FR, góc nằm ở phía trái tầng trên.",
        "alg": "R U' R' U R U' R'",
        "tip": "Rút cạnh lên ghép với góc rồi chèn lại.",
    },
    {
        "id": "f2l_38",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #38: Cạnh nằm trong khe FR, góc ở phía sau",
        "desc": "Cạnh ở khe FR, góc nằm phía sau tầng trên.",
        "alg": "R U2 R' U' R U R'",
        "tip": "Xoay U2 căn góc trước khi ghép.",
    },
    {
        "id": "f2l_39",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #39: Cạnh nằm trong khe FR, góc cần đổi hướng",
        "desc": "Cạnh ở khe FR, góc trên đỉnh cần xoay đổi hướng.",
        "alg": "U R U' R' U R U' R'",
        "tip": "Thực hiện nhịp U R U' R' đều tay.",
    },
    {
        "id": "f2l_40",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #40: Cạnh kẹt sai chiều trong khe FR, góc trắng Phải",
        "desc": "Cạnh ở khe FR bị đảo chiều, góc có mặt trắng hướng phải.",
        "alg": "R U' R' U2 R U' R'",
        "tip": "Đưa cạnh đảo chiều lên ghép đồng thời với góc.",
    },
    {
        "id": "f2l_41",
        "group": "4. Cạnh trong khe, góc trên đỉnh",
        "title": "F2L #41: Cạnh kẹt sai chiều trong khe FR, góc trắng Trước",
        "desc": "Cạnh ở khe FR bị đảo chiều, góc có mặt trắng hướng ra trước.",
        "alg": "U' R U' R' U R U' R'",
        "tip": "Tách cạnh sai chiều ra và ghép vào khe FR.",
    },
]


def invert_alg(alg: str) -> str:
    """Đảo ngược chuỗi công thức xoay để tạo trạng thái setup trước khi giải."""
    tokens = alg.strip().split()
    reversed_tokens = []
    for token in reversed(tokens):
        if token.endswith("2"):
            reversed_tokens.append(token)
        elif token.endswith("'"):
            reversed_tokens.append(token[:-1])
        else:
            reversed_tokens.append(f"{token}'")
    return " ".join(reversed_tokens)


def render_twisty_case_preview(
    setup_alg: str,
    solve_alg: str,
    height: int = 225,
    camera_latitude: int = 35,
    camera_longitude: int = 35,
    highlight_f2l_pair: bool = False,
):
    """Hiển thị trình phát Rubik 3D; nếu highlight_f2l_pair=True sẽ làm sáng 2 mảnh góc + cạnh cần giải của cặp FR."""
    stickering_attr = 'stickering="F2L"' if highlight_f2l_pair else ""
    badge_html = (
        '<div style="display:flex; justify-content:space-between; align-items:center; '
        'margin-bottom:6px; font-size:12px;">'
        '<span style="background:#fff3cd; color:#664d03; border:1px solid #ffecb5; '
        'padding:2px 8px; border-radius:999px; font-weight:600;">'
        '✨ Đang làm sáng 2 mảnh cần giải (Góc + Cạnh cặp FR)</span>'
        '<span style="color:#6c757d;">Các mảnh khác làm mờ nhẹ</span>'
        '</div>'
        if highlight_f2l_pair
        else ""
    )

    # Làm mờ các mảnh không thuộc cặp F2L mục tiêu khi bật highlight_f2l_pair
    dim_style = ""
    if highlight_f2l_pair:
        dim_style = """
        <style>
            .f2l-dim-wrap twisty-player {
                filter: drop-shadow(0 0 8px rgba(255, 193, 7, 0.45));
            }
        </style>
        """

    html_code = f"""
    <script src="https://cdn.cubing.net/js/cubing/twisty" type="module"></script>
    {dim_style}
    <div class="f2l-dim-wrap" style="background: #f8f9fa; border: 1px solid #dfe5ec; border-radius: 10px; padding: 8px;">
        {badge_html}
        <twisty-player
            puzzle="3x3x3"
            {stickering_attr}
            experimental-setup-alg="{setup_alg}"
            alg="{solve_alg}"
            camera-latitude="{camera_latitude}"
            camera-longitude="{camera_longitude}"
            background="none"
            control-panel="bottom-row"
            style="width: 100%; height: {height}px;">
        </twisty-player>
    </div>
    """
    components.html(html_code, height=height + (46 if highlight_f2l_pair else 20))


def render_algorithm_cards(
    items: list[dict],
    default_camera: tuple[int, int] = (35, 35),
    default_expanded: bool = True,
    highlight_f2l_pair: bool = False,
):
    """Hiển thị danh sách công thức kèm mô phỏng 3D và ô đánh dấu đã thuộc."""
    for item in items:
        setup_alg = item.get("setup") or invert_alg(item["alg"])
        with st.expander(
            f"**{item['title']}** — `{item['alg']}`",
            expanded=default_expanded,
        ):
            col_info, col_view = st.columns([1.3, 1])
            with col_info:
                st.markdown(f"**Nhóm:** {item.get('group', 'CFOP')}")
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
                    setup_alg=setup_alg,
                    solve_alg=item["alg"],
                    camera_latitude=lat,
                    camera_longitude=lon,
                    highlight_f2l_pair=highlight_f2l_pair,
                )


def render_cross_section():
    """Phần 1: Cross kèm mô phỏng 3D trực quan."""
    st.subheader("1️⃣ Cross — Giải chữ thập ở mặt đáy")
    st.caption("Nhấn Play trên mô hình 3D để xem cách đưa cạnh trắng xuống mặt đáy (D) và khớp tâm.")

    col_c1, col_c2 = st.columns([1.35, 1])
    with col_c1:
        st.markdown("""
        * **Mục tiêu:** Giải thẳng 4 viên cạnh trắng ở **mặt đáy (D)** và khớp màu tâm bên trong **dưới 8 bước xoay**.
        * **Khác biệt với cách cơ bản:** Không làm hoa cúc ở mặt trên, không lật ngược khối Rubik sau khi xong Cross.
        * **Nguyên tắc luyện tập:**
          1. **Tận dụng 15 giây quan sát (Inspection):** Nhớ vị trí cả 4 viên cạnh trước khi chạm tay vào khối.
          2. **Giải theo vị trí tương đối:** Đặt đúng thứ tự các màu quanh đáy, sau đó xoay mặt D một lượt để khớp toàn bộ tâm.
          3. **Tập giải nhắm mắt (Blind Cross):** Quan sát xong, nhắm mắt và xoay hết Cross để tăng khả năng nhìn trước cho F2L.
        """)
        st.info(
            "**Tóm tắt chỉ số Phần 1**\n\n"
            "- Số công thức học thuộc: **0** (Giải trực quan)\n"
            "- Số bước tối ưu: **6 – 8 moves**\n"
            "- Mục tiêu thời gian: **< 3 giây**"
        )
    with col_c2:
        st.markdown("**Ví dụ mô phỏng đưa 1 cạnh trắng vào đáy:**")
        render_twisty_case_preview(
            setup_alg="F2 D' R2 D",
            solve_alg="D' R2 D F2",
            camera_latitude=-25,
            camera_longitude=35,
        )


def render_f2l_41_section():
    """Phần 2: Toàn bộ 41 trường hợp F2L làm sáng 2 mảnh góc + cạnh cần giải."""
    st.subheader("2️⃣ F2L (First Two Layers) — Đủ 41 trường hợp chuẩn")
    st.caption(
        "Mỗi trường hợp làm nổi bật **2 mảnh cần giải (1 viên góc + 1 viên cạnh của cặp FR)** "
        "để bạn dễ quan sát cách ghép cặp và đưa vào khe."
    )

    groups = ["Tất cả (41 trường hợp)"] + sorted({c["group"] for c in F2L_41_CASES})
    col_f1, col_f2, col_f3 = st.columns([1.3, 1.4, 0.8])

    with col_f1:
        selected_group = st.selectbox("Nhóm trường hợp F2L:", groups)
    with col_f2:
        search_query = st.text_input(
            "Tìm kiếm trường hợp F2L:",
            placeholder="Ví dụ: #01, U R U' R', góc trắng...",
        )
    with col_f3:
        expand_all = st.toggle("Mở sẵn mô phỏng 3D", value=False)

    filtered = []
    q = search_query.strip().lower()
    for case in F2L_41_CASES:
        if selected_group != "Tất cả (41 trường hợp)" and case["group"] != selected_group:
            continue
        haystack = f"{case['title']} {case['desc']} {case['alg']} {case['tip']}".lower()
        if not q or q in haystack:
            filtered.append(case)

    f2l_learned = sum(1 for c in F2L_41_CASES if c["id"] in st.session_state.learned_cfop)
    st.progress(
        f2l_learned / len(F2L_41_CASES),
        text=f"Đã thuộc F2L: {f2l_learned}/{len(F2L_41_CASES)} trường hợp • Đang hiển thị: {len(filtered)} trường hợp",
    )

    if not filtered:
        st.warning("Không tìm thấy trường hợp F2L phù hợp với bộ lọc hiện tại.")
        return

    should_expand = expand_all or (len(filtered) <= 4)
    render_algorithm_cards(
        filtered,
        default_camera=(35, 35),
        default_expanded=should_expand,
        highlight_f2l_pair=True,
    )


def render_oll_section():
    """Phần 3: 2-Look OLL kèm mô phỏng 3D cho từng công thức."""
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
            {
                "id": "oll_line",
                "group": "OLL 3A",
                "title": "Hình đường thẳng (Line)",
                "desc": "3 ô vàng thẳng hàng ngang ở mặt trên.",
                "setup": "F U R U' R' F'",
                "alg": "F R U R' U' F'",
                "tip": "Giữ đường thẳng nằm ngang trước khi thực hiện công thức.",
            },
            {
                "id": "oll_l",
                "group": "OLL 3A",
                "title": "Hình chữ L (L-Shape)",
                "desc": "2 cạnh vàng tạo góc ở vị trí 9h và 12h (hoặc xoay 2 lớp trước).",
                "setup": "f U R U' R' f'",
                "alg": "f R U R' U' f'",
                "tip": "Xoay đồng thời 2 lớp trước (f) giúp tạo chữ thập nhanh.",
            },
            {
                "id": "oll_dot",
                "group": "OLL 3A",
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
                "group": "OLL 3B",
                "title": "Sune (Con cá thuận)",
                "desc": "1 góc vàng ở dưới-trái, 3 góc còn lại hướng ra ngoài.",
                "setup": "R U2 R' U' R U' R'",
                "alg": "R U R' U R U2 R'",
                "tip": "Công thức nền tảng quan trọng nhất cho phần OLL.",
            },
            {
                "id": "oll_antisune",
                "group": "OLL 3B",
                "title": "Anti-Sune (Con cá ngược)",
                "desc": "1 góc vàng ở trên-phải, 3 góc còn lại hướng ngược chiều.",
                "setup": "R U R' U R U2 R'",
                "alg": "R U2 R' U' R U' R'",
                "tip": "Thực hiện ngược chiều Sune để tiết kiệm lượt xoay.",
            },
            {
                "id": "oll_h",
                "group": "OLL 3B",
                "title": "Hình chữ H (Cross + 4 góc đối)",
                "desc": "2 cặp góc vàng hướng đối diện nhau ra trước và sau.",
                "setup": "R U2 R' U' R U R' U' R U' R'",
                "alg": "R U R' U R U' R' U R U2 R'",
                "tip": "Dễ nhớ theo nhịp R-U xen kẽ.",
            },
            {
                "id": "oll_pi",
                "group": "OLL 3B",
                "title": "Hình chữ Pi",
                "desc": "2 góc vàng hướng sang trái, 2 góc hướng ra trước và sau.",
                "setup": "R' U2 R2 U R2 U R2 U2 R'",
                "alg": "R U2 R2 U' R2 U' R2 U2 R",
                "tip": "Tập trung vào cụm R2 xoay liên tiếp.",
            },
            {
                "id": "oll_u",
                "group": "OLL 3B",
                "title": "Hình chữ U (Headlights)",
                "desc": "2 góc vàng đã đúng ở sau, 2 góc trước hướng thẳng về mặt bạn.",
                "setup": "R U2 R D R' U2 R D' R2",
                "alg": "R2 D R' U2 R D' R' U2 R'",
                "tip": "Giữ 2 góc đã khớp màu vàng ở mặt sau.",
            },
            {
                "id": "oll_t",
                "group": "OLL 3B",
                "title": "Hình chữ T",
                "desc": "2 góc vàng bên phải đã đúng, 2 góc bên trái hướng ra trước/sau.",
                "setup": "F R' F' r U R U' r'",
                "alg": "r U R' U' r' F R F'",
                "tip": "Phối hợp lớp đôi r và các bước R-U gọn tay.",
            },
            {
                "id": "oll_bowtie",
                "group": "OLL 3B",
                "title": "Hình nơ (Bowtie / L)",
                "desc": "2 góc vàng chéo nhau đã đúng, 2 góc còn lại lệch hướng.",
                "setup": "R' F' r U R' U' r' F",
                "alg": "F' r U R' U' r' F R",
                "tip": "Kiểm tra kỹ 2 góc chéo đã khớp vàng trước khi xoay.",
            },
        ]

    render_algorithm_cards(oll_items, default_camera=(45, 30), default_expanded=True)


def render_pll_section():
    """Phần 4: 2-Look PLL kèm mô phỏng 3D cho từng công thức."""
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
            {
                "id": "pll_t",
                "group": "PLL 4A",
                "title": "T-Perm (Đổi 2 góc kề bên phải)",
                "desc": "Có 2 góc cùng màu ở mặt bên trái (đặt bên trái rồi làm).",
                "setup": "F R U' R' U R U2 R2 F' R U R U' R'",
                "alg": "R U R' U' R' F R2 U' R' U' R U R' F'",
                "tip": "Một trong các công thức PLL phổ biến và dễ nhớ nhịp nhất.",
            },
            {
                "id": "pll_y",
                "group": "PLL 4A",
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
                "group": "PLL 4B",
                "title": "Ua-Perm (Xoay 3 cạnh thuận chiều)",
                "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy thuận kim đồng hồ.",
                "setup": "R2 U R U R' U' R' U' R' U R'",
                "alg": "R U' R U R U R U' R' U' R2",
                "tip": "Đặt cạnh đã đúng vị trí ở mặt sau (Back).",
            },
            {
                "id": "pll_ub",
                "group": "PLL 4B",
                "title": "Ub-Perm (Xoay 3 cạnh ngược chiều)",
                "desc": "1 mặt đã hoàn thiện (đặt ra sau), 3 cạnh còn lại chạy ngược kim đồng hồ.",
                "setup": "R2 U R U R' U' R' U' R' U R'",
                "alg": "R2 U R U R' U' R' U' R' U R'",
                "tip": "Đặt cạnh đã đúng vị trí ở mặt sau (Back).",
            },
            {
                "id": "pll_h",
                "group": "PLL 4B",
                "title": "H-Perm (Đổi 2 cặp cạnh đối diện)",
                "desc": "4 mặt đều có cạnh đối diện màu nhau.",
                "setup": "M2 U' M2 U2' M2 U' M2",
                "alg": "M2 U M2 U2 M2 U M2",
                "tip": "Dùng lớp giữa M2 giúp thao tác nhanh trên 3x3.",
            },
            {
                "id": "pll_z",
                "group": "PLL 4B",
                "title": "Z-Perm (Đổi 2 cặp cạnh kề nhau)",
                "desc": "Cạnh trước đổi với cạnh phải, cạnh sau đổi với cạnh trái.",
                "setup": "M2 U2 M U' M2' U' M2' U' M",
                "alg": "M' U M2 U M2 U M' U2 M2",
                "tip": "Luyện đều tay lớp M và U để chuyển mạch mượt.",
            },
        ]

    render_algorithm_cards(pll_items, default_camera=(45, 30), default_expanded=True)


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
    st.markdown("Chọn từng giai đoạn bên dưới để học mục tiêu, cách nhận diện, xem mô phỏng 3D và bộ công thức.")

    cfop_part = st.radio(
        "Chọn giai đoạn CFOP:",
        [
            "1️⃣ Phần 1: Cross (Chữ thập đáy)",
            "2️⃣ Phần 2: F2L (41 trường hợp)",
            "3️⃣ Phần 3: OLL (Định hướng mặt trên)",
            "4️⃣ Phần 4: PLL (Hoán vị tầng cuối)",
        ],
        horizontal=True,
    )

    st.divider()

    if "Phần 1" in cfop_part:
        render_cross_section()
    elif "Phần 2" in cfop_part:
        render_f2l_41_section()
    elif "Phần 3" in cfop_part:
        render_oll_section()
    elif "Phần 4" in cfop_part:
        render_pll_section()

    # Thanh tiến độ học CFOP (41 F2L + 10 2-Look OLL + 6 2-Look PLL = 57 mục)
    st.divider()
    total_cfop_algs = len(F2L_41_CASES) + 10 + 6
    learned_count = len(st.session_state.learned_cfop)
    st.progress(
        min(learned_count / total_cfop_algs, 1.0),
        text=f"Tiến độ học CFOP: {learned_count}/{total_cfop_algs} mục đã đánh dấu thuộc",
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
