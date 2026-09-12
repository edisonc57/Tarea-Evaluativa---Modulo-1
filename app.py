import streamlit as st
import plotly.graph_objects as go
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Oil & Gas Analytics", page_icon="🛢️", layout="wide")

st.markdown("""
<style>
.stApp {background:#0b3d3a;}
.block-container {padding-top:2rem;}
.hero,.card,.result {background:white;border-radius:16px;padding:20px;margin:12px 0;box-shadow:0 6px 20px rgba(0,0,0,.18);}
.hero img {width:100%;height:230px;object-fit:cover;border-radius:12px;}
.hero h1 {text-align:center;color:#0b3d3a;}
.nav a {color:white!important;text-decoration:none;font-size:18px;font-weight:600;margin-right:25px;}
.nav a:hover {color:#9ff3df!important;}
.result {transition:all .3s ease;border:1px solid #d7e6e3;}
.result:hover {transform:translateY(-5px);box-shadow:0 0 18px rgba(170,255,230,.8),0 10px 28px rgba(0,0,0,.25);}
.result h4 {margin:0;color:#477c75;}.result h2 {margin:7px 0;color:#0b3d3a;}
.formula {background:#e5f1ef;border-left:5px solid #16796f;padding:12px;border-radius:8px;margin:8px 0;}
</style>
""", unsafe_allow_html=True)

page = st.query_params.get("page", "Home")

st.markdown("""
<div class="nav">
<a href="?page=Home">⌂ Home</a>
<a href="?page=Ejercicios">⚙ Ejercicios</a>
</div>
""", unsafe_allow_html=True)

def ipr(pr, pb, j, pwf):
    qb = j * (pr - pb)
    qmax = qb + j * pb / 1.8
    if pwf >= pb:
        qo = j * (pr - pwf)
        regime = "Lineal"
    else:
        x = pwf / pb
        qo = qb + j * pb / 1.8 * (1 - 0.2*x - 0.8*x**2)
        regime = "Vogel"
    return qo, qb, qmax, regime

def validar(pr, pb, j, pwf):
    if pr <= 0 or pb <= 0 or j <= 0 or pwf < 0:
        return "Los valores deben ser positivos, excepto Pwf que puede ser 0."
    if pb >= pr:
        return "Debe cumplirse Pr > Pb."
    if pwf > pr:
        return "Pwf no puede ser mayor que Pr."
    return None

if page == "Home":
    st.markdown("""
    <div class="hero">
        <img src="https://i0.wp.com/diazvillanueva.com/wp-content/uploads/2021/12/pozos-petroleo-atardecer.jpg">
        <h1>Oil & Gas Analytics</h1>
    </div>
    <div class="card"><h2>👨‍💻 Participante</h2>
        <p><b>Edison Contreras</b></p><p>Bootcamp Data Analytics for Oil & Gas</p>
    </div>
    <div class="card"><h2>🎯 Propósito</h2>
        <p>Aplicación web desarrollada con Python, Streamlit, HTML, CSS y JavaScript para cálculos básicos de Producción, Perforación y Reservorios.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="hero"><h1>📊 Ejercicios técnicos</h1><p>Producción · Perforación · Reservorios</p></div>
    """, unsafe_allow_html=True)

    produccion, perforacion, reservorios = st.tabs(["🛢️ Producción", "🔩 Perforación", "🧱 Reservorios"])

    with produccion:
        st.subheader("Ejercicio 1 — IPR compuesta con punto de burbuja")
        c1, c2 = st.columns(2)
        with c1:
            pr = st.number_input("Pr — Presión del reservorio [psi]", 1.0, value=3000.0)
            pb = st.number_input("Pb — Presión de burbuja [psi]", 1.0, value=2200.0)
            j = st.number_input("J — Índice de productividad [STB/d/psi]", 0.01, value=1.5)
            pwf = st.number_input("Pwf — Presión de fondo fluyente [psi]", 0.0, value=1800.0)
        with c2:
            st.markdown("""
            <div class="card"><h3>Modelo de cálculo</h3>
            <div class="formula">Pwf ≥ Pb → qo = J(Pr − Pwf)</div>
            <div class="formula">qB = J(Pr − Pb)</div>
            <div class="formula">Pwf &lt; Pb → modelo de Vogel</div>
            <div class="formula">qo,max = qB + J·Pb/1.8</div></div>
            """, unsafe_allow_html=True)

        error = validar(pr, pb, j, pwf)
        if error:
            st.error(error)
        else:
            qo, qb, qmax, regime = ipr(pr, pb, j, pwf)
            st.markdown("### Resultados")
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown(f'<div class="result"><h4>Caudal qo</h4><h2>{qo:,.2f} STB/d</h2></div>', unsafe_allow_html=True)
            with r2:
                st.markdown(f'<div class="result"><h4>Caudal a Pb (qB)</h4><h2>{qb:,.2f} STB/d</h2></div>', unsafe_allow_html=True)
            with r3:
                st.markdown(f'<div class="result"><h4>Caudal máximo</h4><h2>{qmax:,.2f} STB/d</h2></div>', unsafe_allow_html=True)

            if regime == "Lineal":
                st.success(f"🟢 Régimen lineal: Pwf ≥ Pb ({pwf:.0f} ≥ {pb:.0f} psi)")
            else:
                st.warning(f"🟠 Régimen de Vogel: Pwf < Pb ({pwf:.0f} < {pb:.0f} psi)")

            components.html(f"""
            <div style="font-family:Arial;background:white;padding:15px;border-radius:12px">
            <b>Interacción JavaScript</b><p id="msg">Pulsa el botón para analizar el régimen.</p>
            <button onclick="analizar()">Analizar</button>
            <script>function analizar() {{ document.getElementById("msg").innerHTML = "JavaScript: el régimen actual es <b>{regime}</b>."; }}</script>
            </div>
            """, height=120)

            pwf_values = np.linspace(0, pr, 200)
            qo_values = [ipr(pr, pb, j, p)[0] for p in pwf_values]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=qo_values, y=pwf_values, mode="lines", name="IPR compuesta"))
            fig.add_trace(go.Scatter(x=[qo], y=[pwf], mode="markers", name="Punto calculado", marker=dict(size=11)))
            fig.add_hline(y=pb, line_dash="dash", annotation_text=f"Pb = {pb:.0f} psi")
            fig.update_layout(title="Curva IPR — Modelo Lineal + Vogel", xaxis_title="Caudal qo [STB/d]", yaxis_title="Pwf [psi]", template="plotly_white", height=500)
            st.plotly_chart(fig, use_container_width=True)

    with perforacion:
        st.markdown("""
        <div class="card"><h2>🔩 Perforación</h2>
        <p>Módulo preparado para calcular la presión hidrostática del lodo a partir del peso del lodo y la TVD.</p></div>
        """, unsafe_allow_html=True)

    with reservorios:
        st.markdown("""
        <div class="card"><h2>🧱 Reservorios</h2>
        <p>Módulo preparado para estimar el Petróleo Original en Sitio (POES).</p></div>
        """, unsafe_allow_html=True)
