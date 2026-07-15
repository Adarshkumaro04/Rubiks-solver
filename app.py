import streamlit as st
import twophase.solver as sv
import time

st.set_page_config(page_title="Rubik's Cube Solver", page_icon="◆", layout="centered")

COLOR_MAP = {
    'U': '#FFFFFF', 'R': '#B71C2B', 'F': '#00843D',
    'D': '#FFC72C', 'L': '#E8590C', 'B': '#0057B8',
}

st.markdown("""
<style>
    .main .block-container { padding-top: 2.5rem; max-width: 760px; }

    .header-row { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 0.2rem; }
    .app-title { font-size: 1.9rem; font-weight: 700; letter-spacing: -0.01em; color: #E6EDF3; margin: 0; }
    .badge {
        display: inline-block; background: #1F2937; border: 1px solid #30363D;
        border-radius: 20px; padding: 4px 12px; font-size: 0.72rem; color: #8B949E;
        text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;
    }
    .subtitle { color: #8B949E; font-size: 0.95rem; margin-top: 0.3rem; margin-bottom: 1.8rem; line-height: 1.5; }

    .section-label {
        font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.08em; color: #6B7280; margin-bottom: 0.5rem; margin-top: 1.6rem;
    }

    .cube-card {
        background: #0D1117; border: 1px solid #21262D; border-radius: 10px;
        padding: 32px; display: flex; justify-content: center; margin: 0.3rem 0 1.2rem 0;
    }
    .cell {
        width: 24px; height: 24px; border-radius: 3px;
        border: 1px solid rgba(0,0,0,0.3);
    }
    .facegrid { display: grid; grid-template-columns: repeat(3, 24px); gap: 2px; }
    .facerow { display: flex; gap: 2px; }

    .stat-box {
        background: #0D1117; border: 1px solid #21262D; border-radius: 8px;
        padding: 14px 8px; text-align: center;
    }
    .stat-num { font-size: 1.4rem; font-weight: 700; color: #E6EDF3; font-variant-numeric: tabular-nums; }
    .stat-label { font-size: 0.68rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }

    .move-chip {
        display: inline-block; background: #161B22; border: 1px solid #21262D;
        border-radius: 6px; padding: 5px 10px; margin: 3px; font-family: 'SFMono-Regular', Consolas, monospace;
        font-size: 0.82rem; color: #C9D1D9;
    }
    .move-chip .idx { color: #4B5563; margin-right: 6px; font-weight: 600; }

    div.stButton > button {
        border-radius: 6px; font-weight: 600; padding: 0.5rem 1.5rem;
        border: 1px solid #30363D; background: #21262D;
    }
    div.stButton > button:hover { border-color: #58A6FF; color: #58A6FF; }

    .footer-note {
        margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid #21262D;
        font-size: 0.8rem; color: #6B7280; line-height: 1.6;
    }
    .footer-note a { color: #58A6FF; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-row">
    <p class="app-title">Rubik's Cube Solver</p>
    <span class="badge">Two-Phase Algorithm</span>
</div>
<p class="subtitle">
    Solves any scrambled 3×3 Rubik's Cube from a 43-quintillion-state search space in 
    under 20 moves, typically in milliseconds. Implementation based on the two-phase 
    algorithm developed by Herbert Kociemba.
</p>
""", unsafe_allow_html=True)

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
    <div style="display:flex;flex-direction:column;align-items:center;gap:2px;">
        <div style="margin-left:108px;">{grid('U')}</div>
        <div class="facerow">{grid('L')}{grid('F')}{grid('R')}{grid('B')}</div>
        <div style="margin-left:108px;">{grid('D')}</div>
    </div>
    '''

FACE_NAMES = {'U': 'Up', 'R': 'Right', 'F': 'Front', 'D': 'Down', 'L': 'Left', 'B': 'Back'}
TURN_NAMES = {'1': "90° CW", '2': "180°", '3': "90° CCW"}

def parse_moves(solution_str):
    return solution_str.split('(')[0].strip().split()

demo = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'

st.markdown('<div class="section-label">Cube State Input</div>', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    cubestring = st.text_input(
        "Cube definition string",
        value="", placeholder="54-character facelet string — leave blank for demo scramble",
        label_visibility="collapsed"
    )
with col2:
    solve_clicked = st.button("Solve", use_container_width=True)

active_cube = None
solution = None
elapsed = None

if solve_clicked:
    cs = cubestring.strip() if cubestring.strip() else demo
    if len(cs) != 54:
        st.error(f"Cube string must be exactly 54 characters (received {len(cs)}).")
    else:
        active_cube = cs
        with st.spinner("Running two-phase search..."):
            start = time.time()
            solution = sv.solve(cs, 19, 2)
            elapsed = time.time() - start
else:
    active_cube = demo

st.markdown('<div class="section-label">Cube State</div>', unsafe_allow_html=True)
st.markdown(f'<div class="cube-card">{render_cube_html(active_cube)}</div>', unsafe_allow_html=True)

if solution:
    moves = parse_moves(solution)

    st.markdown('<div class="section-label">Solve Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{len(moves)}</div><div class="stat-label">Moves</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{elapsed*1000:.0f}ms</div><div class="stat-label">Solve Time</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">2</div><div class="stat-label">Search Phases</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Solution</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Readable steps", "Standard notation"])
    with tab1:
        chips = ""
        for i, move in enumerate(moves, 1):
            face, turn = move[0], move[1]
            chips += f'<span class="move-chip"><span class="idx">{i}</span>{FACE_NAMES[face]} · {TURN_NAMES[turn]}</span>'
        st.markdown(chips, unsafe_allow_html=True)
    with tab2:
        st.code(solution, language=None)
else:
    st.caption("Demo scramble shown above. Enter a cube state or click Solve to run the search.")

st.markdown("""
<div class="footer-note">
    Two-phase solving algorithm and pruning tables by 
    <a href="https://github.com/hkociemba/RubiksCube-TwophaseSolver" target="_blank">Herbert Kociemba</a>.
    Interface and implementation by the project author.
</div>
""", unsafe_allow_html=True)
