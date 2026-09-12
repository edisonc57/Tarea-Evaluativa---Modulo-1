import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(page_title="Oil & Gas Analytics", page_icon="🛢️", layout="wide")

# CSS
st.markdown("""
<style>
.stApp {background-color:#0b3d3b;color:#f4f8f7}
section[data-testid="stSidebar"] {background-color:#062d2b}
section[data-testid="stSidebar"] * {color:white}
h1,h2,h3,p,label {color:#f4f8f7 !important}
.card {background:#145a56;padding:20px;border-radius:15px;margin-bottom:15px;
box-shadow:0 4px 12px rgba(0,0,0,.20)}
.hero {background-image:linear-gradient(rgba(0,45,43,.55),rgba(0,45,43,.65)),
url("https://i0.wp.com/diazvillanueva.com/wp-content/uploads/2021/12/pozos-petroleo-atardecer.jpg");
background-size:cover;background-position:center;padding:55px 35px;border-radius:18px;margin-bottom:25px}
.hero h1 {color:white !important;font-size:42px}
.hero p {color:white !important}
</style>
""", unsafe_allow_html=True)

def calcular_ipr(pr, pb, j, pwf):
    qb = j * (pr - pb)
    qmax = qb + j * pb / 1.8

    if pwf >= pb:
        qo = j * (pr - pwf)
        regimen = "Lineal"
    else:
        x = pwf / pb
        qo = qb + (j * pb / 1.8) * (1 - 0.2*x - 0.8*x**2)
        regimen = "Vogel"

    return qo, qb, qmax, regimen

def validar(pr, pb, j, pwf):
    if pr <= 0 or pb <= 0 or j <= 0 or pwf < 0:
        return "Los valores deben ser positivos."
    if pb >= pr:
        return "Debe cumplirse Pr > Pb."
    if pwf > pr:
        return "Pwf no puede ser mayor que Pr."
    return None

# Navegación
st.sidebar.title("🛢️ Oil & Gas")
pagina = st.sidebar.radio("Navegación", ["Home", "Ejercicios"])

if pagina == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Oil & Gas Analytics</h1>
        <p>Aplicación web para análisis técnico de la industria Oil & Gas</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>👨‍💻 Participante</h3>
        <p><b>Edison Contreras</b></p>
        <p>Petroleum Engineer | Data Analytics for Oil & Gas</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>📚 Programa</h3>
        <p><b>Bootcamp Data Analytics for Oil & Gas</b></p>
        <p>Python, Streamlit, HTML, CSS y JavaScript.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>🎯 Propósito</h3>
    <p>Aplicación para realizar cálculos de ingeniería relacionados con
    Producción, Perforación y Reservorios mediante una interfaz web.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.title("📊 Ejercicios técnicos")
    prod, perf, res = st.tabs(["🛢️ Producción", "🔩 Perforación", "🧱 Reservorios"])

    with prod:
        st.subheader("Ejercicio 1 — IPR compuesta con punto de burbuja")

        col1, col2 = st.columns(2)

        with col1:
            pr = st.number_input("Pr — Presión del reservorio [psi]", value=3000.0)
            pb = st.number_input("Pb — Presión de burbuja [psi]", value=2200.0)
            j = st.number_input("J — Índice de productividad [STB/d/psi]", value=1.5)
            pwf = st.number_input("Pwf — Presión de fondo fluyente [psi]", value=1800.0)

        with col2:
            st.markdown("""
            <div class="card">
            <h3>📐 Modelo</h3>
            <p>Si Pwf ≥ Pb: <b>qo = J(Pr − Pwf)</b></p>
            <p>Si Pwf &lt; Pb:</p>
            <p><b>qo = qB + (J·Pb/1.8)[1 − 0.2(Pwf/Pb) − 0.8(Pwf/Pb)²]</b></p>
            </div>
            """, unsafe_allow_html=True)

        error = validar(pr, pb, j, pwf)

        if error:
            st.error(error)
        else:
            qo, qb, qmax, regimen = calcular_ipr(pr, pb, j, pwf)

            st.subheader("Resultados")
            a, b, c = st.columns(3)
            a.metric("qo", f"{qo:,.2f} STB/d")
            b.metric("qB", f"{qb:,.2f} STB/d")
            c.metric("qo,max", f"{qmax:,.2f} STB/d")

            if regimen == "Lineal":
                st.success("Régimen lineal: Pwf ≥ Pb")
            else:
                st.warning("Régimen de Vogel: Pwf < Pb")

            components.html(f"""
            <div style="background:#145a56;padding:15px;border-radius:12px;color:white">
                <button onclick="mensaje()" style="padding:8px;border:0;border-radius:7px">
                Analizar régimen</button>
                <p id="msg">Pulsa el botón para analizar el punto.</p>
            </div>
            <script>
            function mensaje() {{
                document.getElementById("msg").innerHTML =
                "Pwf = {pwf:.1f} psi | Pb = {pb:.1f} psi | Régimen: {regimen}";
            }}
            </script>
            """, height=120)

            # Curva IPR con Plotly
            pwfs = [pr * i / 100 for i in range(101)]
            qs = [calcular_ipr(pr, pb, j, p)[0] for p in pwfs]

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=qs, y=pwfs, mode="lines", name="IPR"))
            fig.add_trace(go.Scatter(x=[qo], y=[pwf], mode="markers", name="Punto calculado"))
            fig.add_hline(y=pb, line_dash="dash", annotation_text="Pb")

            fig.update_layout(
                title="Curva IPR compuesta",
                xaxis_title="Caudal de petróleo, qo [STB/d]",
                yaxis_title="Pwf [psi]",
                template="plotly_dark",
                paper_bgcolor="#145a56",
                plot_bgcolor="#145a56"
            )
            st.plotly_chart(fig, use_container_width=True)

    with perf:
        st.markdown("""
        <div class="card">
        <h3>🔩 Perforación</h3>
        <p>Módulo preparado para calcular la presión hidrostática del lodo
        a partir del peso del lodo y la TVD.</p>
        </div>
        """, unsafe_allow_html=True)

    with res:
        st.markdown("""
        <div class="card">
        <h3>🧱 Reservorios</h3>
        <p>Módulo preparado para estimar el Petróleo Original en Sitio (POES).</p>
        </div>
        """, unsafe_allow_html=True)


