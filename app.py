import streamlit as st
import twophase.solver as sv
import time

COLOR_MAP = {
    'U': '#FFFFFF', 'R': '#C41E3A', 'F': '#009E60',
    'D': '#FFD500', 'L': '#FF5800', 'B': '#0051BA',
}

def render_cube_html(cubestring):
    faces = {
        'U': cubestring[0:9], 'R': cubestring[9:18], 'F': cubestring[18:27],
        'D': cubestring[27:36], 'L': cubestring[36:45], 'B': cubestring[45:54],
    }
    def grid(face):
        cells = faces[face]
        html = '<div style="display:grid;grid-template-columns:repeat(3,20px);gap:2px;">'
        for c in cells:
            html += f'<div style="width:20px;height:20px;background:{COLOR_MAP[c]};border:1px solid #333;"></div>'
        html += '</div>'
        return html
    layout = f'''
    <div style="display:flex;flex-direction:column;align-items:center;gap:2px;">
        <div style="margin-left:88px;">{grid('U')}</div>
        <div style="display:flex;gap:2px;">
            {grid('L')}{grid('F')}{grid('R')}{grid('B')}
        </div>
        <div style="margin-left:88px;">{grid('D')}</div>
    </div>
    '''
    return layout

FACE_NAMES = {'U': 'Up', 'R': 'Right', 'F': 'Front', 'D': 'Down', 'L': 'Left', 'B': 'Back'}
TURN_NAMES = {'1': '90° clockwise', '2': '180°', '3': '90° counter-clockwise'}

def explain_moves(solution_str):
    moves = solution_str.split('(')[0].strip().split()
    lines = []
    for i, move in enumerate(moves, 1):
        face, turn = move[0], move[1]
        lines.append(f"{i}. {move} → Turn {FACE_NAMES[face]} face {TURN_NAMES[turn]}")
    return lines

st.set_page_config(page_title="Rubik's Cube Solver", page_icon="🧩")
st.title("🧩 Rubik's Cube Solver")
st.caption("Two-phase algorithm — solves in under 20 moves, usually in seconds.")

demo = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'
cubestring = st.text_input("Enter a 54-character cube definition string:", value="", placeholder="Leave blank for demo cube")

if st.button("Solve"):
    cs = cubestring.strip() if cubestring.strip() else demo
    if len(cs) != 54:
        st.error("Cube string must be exactly 54 characters.")
    else:
        st.subheader("Scrambled cube")
        st.markdown(render_cube_html(cs), unsafe_allow_html=True)

        with st.spinner("Solving..."):
            start = time.time()
            solution = sv.solve(cs, 19, 2)
            elapsed = time.time() - start

        st.success(f"Solved in {elapsed:.3f} seconds")
        st.code(solution)

        st.subheader("Step-by-step")
        for line in explain_moves(solution):
            st.write(line)