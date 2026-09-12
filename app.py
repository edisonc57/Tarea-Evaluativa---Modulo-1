import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(page_title="Oil & Gas Analytics", page_icon="🛢️", layout="wide")

# ESTILO
st.markdown("""
<style>
.stApp {background:#f4f7f9;}
section[data-testid="stSidebar"] {background:#102a43;}
section[data-testid="stSidebar"] * {color:white;}
.card {background:white;padding:20px;border-radius:15px;margin-bottom:18px;box-shadow:0 4px 15px #00000015;}
.hero {background:linear-gradient(#102a43aa,#102a43aa),url("https://i0.wp.com/diazvillanueva.com/wp-content/uploads/2021/12/pozos-petroleo-atardecer.jpg");background-size:cover;background-position:center;color:white;padding:45px 30px;border-radius:18px;margin-bottom:25px;}
.formula {background:#eef4f8;padding:12px;border-radius:8px;margin:8px 0;font-family:monospace;}
</style>
""", unsafe_allow_html=True)

# CÁLCULOS
def ipr(pr, pb, j, pwf):
    qb = j * (pr - pb)
    qmax = qb + j * pb / 1.8

    if pwf >= pb:
        qo = j * (pr - pwf)
        regime = "Lineal"
    else:
        x = pwf / pb
        qo = qb + (j * pb / 1.8) * (1 - 0.2*x - 0.8*x**2)
        regime = "Vogel"

    return qo, qb, qmax, regime


def curva_ipr(pr, pb, j):
    pwf = np.linspace(0, pr, 100)
    qo = [ipr(pr, pb, j, p)[0] for p in pwf]
    return qo, pwf


# NAVEGACIÓN
st.sidebar.title("🛢️ Oil & Gas")
pagina = st.sidebar.radio("Navegación", ["Home", "Ejercicios"])

# HOME
if pagina == "Home":
    st.markdown("""
    <div class="hero">
    <h1>Oil & Gas Analytics</h1>
    <p>Bootcamp Data Analytics for Oil & Gas</p>
    <p>Aplicación para cálculos y análisis de ingeniería de petróleo.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>👨‍💻 Participante</h3>
        <b>Edison Contreras</b>
        <p>Petroleum Engineer | Data Analytics for Oil & Gas</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>📚 Programa</h3>
        <b>Bootcamp Data Analytics for Oil & Gas</b>
        <p>Python, Streamlit, HTML, CSS y JavaScript.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>🎯 Propósito</h3>
    <p>Aplicar herramientas de programación y visualización a problemas
    de Producción, Perforación y Reservorios.</p>
    </div>
    """, unsafe_allow_html=True)

# EJERCICIOS
else:
    st.markdown("""
    <div class="hero">
    <h1>Ejercicios técnicos</h1>
    <p>Producción · Perforación · Reservorios</p>
    </div>
    """, unsafe_allow_html=True)

    prod, perf, res = st.tabs(["🛢️ Producción", "🔩 Perforación", "🧱 Reservorios"])

    # PRODUCCIÓN
    with prod:
        st.markdown("""
        <div class="card">
        <h3>Ejercicio 1 — IPR compuesta con punto de burbuja</h3>
        <p>Calculadora para un yacimiento de petróleo inicialmente subsaturado.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            pr = st.number_input("Pr — Presión del reservorio [psi]", 1.0, 10000.0, 3000.0)
            pb = st.number_input("Pb — Presión de burbuja [psi]", 1.0, 10000.0, 2200.0)
            j = st.number_input("J — Índice de productividad [STB/d/psi]", 0.01, 20.0, 1.5)
            pwf = st.number_input("Pwf — Presión de fondo [psi]", 0.0, 10000.0, 1800.0)

        if pb >= pr:
            st.error("Debe cumplirse Pr > Pb.")
        elif pwf > pr:
            st.error("Pwf no puede ser mayor que Pr.")
        else:
            qo, qb, qmax, regime = ipr(pr, pb, j, pwf)

            # TARJETA DE RESULTADOS CON HTML + CSS + JAVASCRIPT
            html_resultados = f"""
            <style>
                * {{ box-sizing: border-box; }}
                body {{
                    margin: 0;
                    background: transparent;
                    font-family: Arial, sans-serif;
                }}

                #shell {{
                    position: relative;
                    padding: 2px;
                    border-radius: 22px;
                    background: #163d59;
                    overflow: hidden;
                }}

                #shell::before {{
                    content: "";
                    position: absolute;
                    width: 180px;
                    height: 180px;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    background: #16e0c0;
                    filter: blur(22px);
                    opacity: 0;
                    transition: opacity .25s;
                }}

                #shell.active::before {{
                    opacity: .9;
                    animation: giro 3s linear infinite;
                }}

                @keyframes giro {{
                    0% {{ transform: translate(-50%, -50%) rotate(0deg) translateX(270px); }}
                    100% {{ transform: translate(-50%, -50%) rotate(360deg) translateX(270px); }}
                }}

                #card {{
                    position: relative;
                    z-index: 1;
                    background: #173f5f;
                    border-radius: 20px;
                    padding: 22px 28px;
                    color: white;
                }}

                .titulo {{
                    color: #16e0c0;
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 18px;
                }}

                .resultados {{
                    display: flex;
                    gap: 15px;
                    flex-wrap: wrap;
                }}

                .resultado {{
                    flex: 1;
                    min-width: 180px;
                    background: #205577;
                    border-radius: 12px;
                    padding: 15px;
                }}

                .nombre {{
                    font-size: 14px;
                    color: #d8e6ee;
                }}

                .valor {{
                    color: #16e0c0;
                    font-size: 22px;
                    font-weight: bold;
                    margin-top: 5px;
                }}

                #status {{
                    margin-top: 18px;
                    padding-top: 12px;
                    border-top: 1px solid #4b748d;
                    color: #e5edf2;
                }}
            </style>

            <div id="shell">
                <div id="card">
                    <div class="titulo">Resultados IPR</div>

                    <div class="resultados">
                        <div class="resultado">
                            <div class="nombre">Caudal de petróleo qo</div>
                            <div class="valor">{qo:,.2f} STB/d</div>
                        </div>

                        <div class="resultado">
                            <div class="nombre">Caudal a presión de burbuja qB</div>
                            <div class="valor">{qb:,.2f} STB/d</div>
                        </div>

                        <div class="resultado">
                            <div class="nombre">Caudal máximo qo,max</div>
                            <div class="valor">{qmax:,.2f} STB/d</div>
                        </div>
                    </div>

                    <div id="status">Estado: cursor fuera</div>
                </div>
            </div>

            <script>
                const shell = document.getElementById("shell");
                const card = document.getElementById("card");
                const status = document.getElementById("status");

                shell.addEventListener("mouseenter", () => {{
                    shell.classList.add("active");
                    status.textContent = "Estado: interacción activa";
                }});

                shell.addEventListener("mouseleave", () => {{
                    shell.classList.remove("active");
                    status.textContent = "Estado: cursor fuera";
                    card.style.setProperty("--x", "50%");
                    card.style.setProperty("--y", "50%");
                }});

                card.addEventListener("mousemove", (event) => {{
                    const rect = card.getBoundingClientRect();
                    const x = ((event.clientX - rect.left) / rect.width) * 100;
                    const y = ((event.clientY - rect.top) / rect.height) * 100;
                    card.style.setProperty("--x", x + "%");
                    card.style.setProperty("--y", y + "%");
                }});
            </script>
            """

            components.html(html_resultados, height=230)

            if regime == "Lineal":
                st.success("🟢 Régimen lineal: Pwf ≥ Pb")
            else:
                st.warning("🟠 Régimen de Vogel: Pwf < Pb")

            # GRÁFICO CON PLOTLY
            qoc, pwfc = curva_ipr(pr, pb, j)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=qoc, y=pwfc, mode="lines", name="IPR compuesta"
            ))
            fig.add_trace(go.Scatter(
                x=[qo], y=[pwf], mode="markers",
                name="Punto calculado", marker=dict(size=11)
            ))
            fig.add_hline(y=pb, line_dash="dash", annotation_text="Pb")

            fig.update_layout(
                title="Curva IPR compuesta",
                xaxis_title="Caudal de petróleo, qo [STB/d]",
                yaxis_title="Pwf [psi]",
                template="plotly_white",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

    # PERFORACIÓN
    with perf:
        st.markdown("""
        <div class="card">
        <h3>🔩 Perforación</h3>
        <p>Módulo preparado para el cálculo de presión hidrostática
        del lodo usando peso del lodo y TVD.</p>
        </div>
        """, unsafe_allow_html=True)

    # RESERVORIOS
    with res:
        st.markdown("""
        <div class="card">
        <h3>🧱 Reservorios</h3>
        <p>Módulo preparado para la estimación volumétrica del
        Petróleo Original en Sitio (POES).</p>
        </div>
        """, unsafe_allow_html=True)
