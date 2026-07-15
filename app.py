import streamlit as st
import twophase.solver as sv
import time

st.set_page_config(page_title="Cube Solver", page_icon="🧩", layout="centered")

COLOR_MAP = {
    'U': '#FFFFFF', 'R': '#C41E3A', 'F': '#009E60',
    'D': '#FFD500', 'L': '#FF5800', 'B': '#0051BA',
}

st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; max-width: 720px; }
    h1 { font-weight: 700; letter-spacing: -0.02em; }
    .subtitle { color: #9CA3AF; font-size: 1rem; margin-top: -0.6rem; margin-bottom: 1.5rem; }
    .cube-card {
        background: #161B22; border: 1px solid #30363D; border-radius: 16px;
        padding: 28px; display: flex; justify-content: center; margin: 1rem 0;
    }
    .cell {
        width: 26px; height: 26px; border-radius: 5px;
        border: 1px solid rgba(0,0,0,0.25);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
    }
    .facegrid { display: grid; grid-template-columns: repeat(3, 26px); gap: 3px; }
    .facerow { display: flex; gap: 3px; }
    .stat-box {
        background: #161B22; border: 1px solid #30363D; border-radius: 12px;
        padding: 16px; text-align: center;
    }
    .stat-num { font-size: 1.6rem; font-weight: 700; color: #E6EDF3; }
    .stat-label { font-size: 0.8rem; color: #8B949E; text-transform: uppercase; letter-spacing: 0.05em; }
    .move-chip {
        display: inline-block; background: #1F2937; border: 1px solid #30363D;
        border-radius: 8px; padding: 6px 12px; margin: 3px; font-family: monospace;
        font-size: 0.85rem; color: #E6EDF3;
    }
    .move-chip .idx { color: #6B7280; margin-right: 6px; }
    div.stButton > button {
        border-radius: 10px; font-weight: 600; padding: 0.5rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🧩 Rubik's Cube Solver")
st.markdown('<p class="subtitle">Two-phase algorithm · solves in under 20 moves, usually in milliseconds</p>', unsafe_allow_html=True)

def render_cube_html(cubestring):
    faces = {
        'U': cubestring[0:9], 'R': cubestring[9:18], 'F': cubestring[18:27],
        'D': cubestring[27:36], 'L': cubestring[36:45], 'B': cubestring[45:54],
    }
    def grid(face):
        cells = faces[face]
        html = '<div class="facegrid">'
        for c in cells:
            html += f'<div class="cell" style="background:{COLOR_MAP[c]};"></div>'
        html += '</div>'
        return html
    return f'''
    <div style="display:flex;flex-direction:column;align-items:center;gap:3px;">
        <div style="margin-left:116px;">{grid('U')}</div>
        <div class="facerow">{grid('L')}{grid('F')}{grid('R')}{grid('B')}</div>
        <div style="margin-left:116px;">{grid('D')}</div>
    </div>
    '''

FACE_NAMES = {'U': 'Up', 'R': 'Right', 'F': 'Front', 'D': 'Down', 'L': 'Left', 'B': 'Back'}
TURN_NAMES = {'1': "90° CW", '2': "180°", '3': "90° CCW"}

def parse_moves(solution_str):
    moves = solution_str.split('(')[0].strip().split()
    return moves

demo = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'

with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        cubestring = st.text_input(
            "Cube definition string (54 characters)",
            value="", placeholder="Leave blank to use a demo scramble",
            label_visibility="collapsed"
        )
    with col2:
        solve_clicked = st.button("Solve →", use_container_width=True)

if solve_clicked:
    cs = cubestring.strip() if cubestring.strip() else demo
    if len(cs) != 54:
        st.error(f"Cube string must be exactly 54 characters (got {len(cs)}).")
    else:
        st.markdown(f'<div class="cube-card">{render_cube_html(cs)}</div>', unsafe_allow_html=True)

        with st.spinner("Solving..."):
            start = time.time()
            solution = sv.solve(cs, 19, 2)
            elapsed = time.time() - start

        moves = parse_moves(solution)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{len(moves)}</div><div class="stat-label">Moves</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{elapsed*1000:.0f}ms</div><div class="stat-label">Solve time</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-box"><div class="stat-num">2</div><div class="stat-label">Phases</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Step-by-step", "Raw notation"])
        with tab1:
            chips = ""
            for i, move in enumerate(moves, 1):
                face, turn = move[0], move[1]
                chips += f'<span class="move-chip"><span class="idx">{i}</span>{FACE_NAMES[face]} · {TURN_NAMES[turn]}</span>'
            st.markdown(chips, unsafe_allow_html=True)
        with tab2:
            st.code(solution, language=None)
else:
    st.markdown(f'<div class="cube-card">{render_cube_html(demo)}</div>', unsafe_allow_html=True)
    st.caption("↑ Demo scramble shown above. Enter your own string or click Solve to run it.")