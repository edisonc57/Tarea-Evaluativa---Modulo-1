
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================
st.set_page_config(
    page_title="Oil & Gas Analytics | IPR",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS PERSONALIZADO
# ============================================================
st.markdown(
    """
    <style>
        /* Fondo general */
        .stApp {
            background: #f4f7f9;
        }

        /* Barra lateral */
        section[data-testid="stSidebar"] {
            background: #102a43;
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        /* Tarjetas */
        .card {
            background: white;
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 18px;
            box-shadow: 0 5px 18px rgba(16, 42, 67, 0.10);
            border: 1px solid #d9e2ec;
        }

        .card:hover {
            transform: translateY(-2px);
            transition: 0.2s ease;
            box-shadow: 0 8px 24px rgba(16, 42, 67, 0.16);
        }

        .hero {
            background: linear-gradient(135deg, #102a43, #243b53);
            color: white;
            border-radius: 18px;
            padding: 30px;
            margin-bottom: 24px;
        }

        .hero h1 {
            margin-bottom: 8px;
            font-size: 2.2rem;
        }

        .hero p {
            margin-bottom: 0;
            font-size: 1.05rem;
        }

        .section-title {
            color: #102a43;
            font-weight: 700;
            font-size: 1.35rem;
            margin-top: 8px;
            margin-bottom: 12px;
        }

        .formula {
            background: #eef4f8;
            border-left: 5px solid #1f7a8c;
            border-radius: 8px;
            padding: 14px 18px;
            margin: 10px 0;
            font-family: "Courier New", monospace;
        }

        .small-note {
            color: #52606d;
            font-size: 0.90rem;
        }

        /* Botones de Streamlit */
        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        /* Métricas */
        div[data-testid="stMetric"] {
            background: white;
            border-radius: 14px;
            padding: 12px;
            border: 1px solid #d9e2ec;
            box-shadow: 0 3px 12px rgba(16, 42, 67, 0.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FUNCIONES DE CÁLCULO
# ============================================================
def validate_inputs(pr, pb, j, pwf):
    """Valida que los parámetros sean físicamente consistentes."""
    if pr <= 0:
        return False, "La presión promedio del reservorio (Pr) debe ser mayor que 0 psi."
    if pb <= 0:
        return False, "La presión de burbuja (Pb) debe ser mayor que 0 psi."
    if j <= 0:
        return False, "El índice de productividad (J) debe ser mayor que 0 STB/d/psi."
    if pwf < 0:
        return False, "La presión de fondo fluyente (Pwf) no puede ser negativa."
    if pb >= pr:
        return False, "Para este ejercicio debe cumplirse Pr > Pb."
    if pwf > pr:
        return False, "Pwf no puede ser mayor que Pr."
    return True, ""


def composite_ipr(pr, pb, j, pwf):
    """
    Calcula la IPR compuesta para un yacimiento inicialmente subsaturado.

    Si Pwf >= Pb:
        qo = J(Pr - Pwf)

    Si Pwf < Pb:
        qB = J(Pr - Pb)
        qo = qB + (J*Pb/1.8) * [1 - 0.2(Pwf/Pb) - 0.8(Pwf/Pb)^2]

    Además:
        qo,max = qB + J*Pb/1.8
    """
    qb = j * (pr - pb)
    qomax = qb + (j * pb / 1.8)

    if pwf >= pb:
        qo = j * (pr - pwf)
        regime = "Por encima o en la presión de burbuja"
    else:
        ratio = pwf / pb
        qo = qb + (j * pb / 1.8) * (1 - 0.2 * ratio - 0.8 * ratio**2)
        regime = "Por debajo de la presión de burbuja"

    return qo, qb, qomax, regime


def ipr_curve(pr, pb, j, n_points=300):
    """Genera puntos de la curva IPR completa entre Pwf=0 y Pwf=Pr."""
    pwf_values = np.linspace(0, pr, n_points)
    qo_values = []

    qb = j * (pr - pb)

    for pwf in pwf_values:
        if pwf >= pb:
            qo = j * (pr - pwf)
        else:
            ratio = pwf / pb
            qo = qb + (j * pb / 1.8) * (
                1 - 0.2 * ratio - 0.8 * ratio**2
            )
        qo_values.append(max(qo, 0))

    return pwf_values, np.array(qo_values)


# ============================================================
# COMPONENTE HTML + JAVASCRIPT
# ============================================================
def javascript_status_card(regime, pwf, pb):
    """Tarjeta con una interacción visible implementada con JavaScript."""
    if pwf >= pb:
        initial_message = "El punto calculado está en el régimen lineal."
        status = "LINEAL"
    else:
        initial_message = "El punto calculado está en el régimen de Vogel."
        status = "VOGEL"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: transparent;
            }}
            .js-card {{
                background: #ffffff;
                border: 1px solid #d9e2ec;
                border-radius: 14px;
                padding: 18px;
                box-shadow: 0 4px 14px rgba(16,42,67,.08);
            }}
            .badge {{
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                background: #eef4f8;
                color: #102a43;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            button {{
                background: #102a43;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px 14px;
                cursor: pointer;
                font-weight: bold;
            }}
            button:hover {{
                background: #243b53;
            }}
            #message {{
                margin-top: 12px;
                color: #52606d;
            }}
        </style>
    </head>
    <body>
        <div class="js-card">
            <div class="badge" id="badge">{status}</div>
            <div>
                <strong>Condición actual:</strong> Pwf = {pwf:.1f} psi |
                Pb = {pb:.1f} psi
            </div>
            <p id="message">{initial_message}</p>
            <button onclick="analizar()">Analizar régimen</button>
        </div>

        <script>
            function analizar() {{
                const badge = document.getElementById("badge");
                const message = document.getElementById("message");

                if ({pwf} >= {pb}) {{
                    badge.innerHTML = "LINEAL";
                    message.innerHTML =
                        "JavaScript confirma: Pwf está por encima de Pb, " +
                        "por lo que se utiliza qo = J(Pr - Pwf).";
                }} else {{
                    badge.innerHTML = "VOGEL";
                    message.innerHTML =
                        "JavaScript confirma: Pwf está por debajo de Pb, " +
                        "por lo que se utiliza la expresión no lineal de Vogel.";
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html


# ============================================================
# BARRA LATERAL / NAVEGACIÓN PRINCIPAL
# ============================================================
st.sidebar.markdown("## 🛢️ Oil & Gas Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegación",
    ["Home", "Ejercicios"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Bootcamp Data Analytics for Oil & Gas")
st.sidebar.caption("Aplicación desarrollada con Python + Streamlit + HTML + CSS + JavaScript")


# ============================================================
# HOME
# ============================================================
if page == "Home":
    st.markdown(
        """
        <div class="hero">
            <h1>🛢️ Oil & Gas Analytics</h1>
            <p>
                Aplicación web para análisis técnico de producción,
                perforación y reservorios mediante Python y Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h3>👨‍💻 Participante</h3>
                <p><strong>Edison Contreras</strong></p>
                <p class="small-note">
                    Petroleum Engineer | Data Analytics for Oil & Gas
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h3>📚 Programa</h3>
                <p><strong>Bootcamp Data Analytics for Oil & Gas</strong></p>
                <p class="small-note">
                    Aplicación orientada al análisis de problemas de ingeniería
                    mediante herramientas de programación y visualización.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card">
            <div class="section-title">🎯 Propósito de la aplicación</div>
            <p>
                Esta aplicación integra Python, Streamlit, HTML, CSS y JavaScript
                para desarrollar herramientas sencillas de cálculo aplicadas a
                Producción, Perforación y Reservorios.
            </p>
            <p>
                El primer ejercicio implementa una calculadora de desempeño de
                afluencia (IPR) para un yacimiento de petróleo inicialmente
                subsaturado, diferenciando el comportamiento lineal por encima
                de la presión de burbuja y el comportamiento de Vogel por debajo
                de dicha presión.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info("Utiliza la barra lateral para entrar en **Ejercicios**.")


# ============================================================
# EJERCICIOS
# ============================================================
else:
    st.markdown(
        """
        <div class="hero">
            <h1>📊 Ejercicios técnicos</h1>
            <p>Producción · Perforación · Reservorios</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_prod, tab_perf, tab_res = st.tabs(
        ["🛢️ Producción", "🔩 Perforación", "🧱 Reservorios"]
    )

    # --------------------------------------------------------
    # PRODUCCIÓN
    # --------------------------------------------------------
    with tab_prod:
        st.markdown(
            """
            <div class="card">
                <div class="section-title">
                    Ejercicio 1 — Producción: IPR compuesta con punto de burbuja
                </div>
                <p>
                    Calculadora de desempeño de afluencia para un yacimiento
                    inicialmente subsaturado. La aplicación selecciona
                    automáticamente el modelo según Pwf respecto a Pb.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        input_col, info_col = st.columns([1, 1])

        with input_col:
            st.subheader("📥 Parámetros de entrada")

            pr = st.number_input(
                "Pr — Presión promedio del reservorio [psi]",
                min_value=1.0,
                value=3000.0,
                step=50.0,
            )

            pb = st.number_input(
                "Pb — Presión de burbuja [psi]",
                min_value=1.0,
                value=2200.0,
                step=50.0,
            )

            j = st.number_input(
                "J — Índice de productividad [STB/d/psi]",
                min_value=0.0001,
                value=1.5,
                step=0.1,
                format="%.4f",
            )

            pwf = st.number_input(
                "Pwf — Presión de fondo fluyente [psi]",
                min_value=0.0,
                value=1800.0,
                step=50.0,
            )

        with info_col:
            st.subheader("📐 Modelo de cálculo")

            st.markdown(
                """
                <div class="formula">
                    Si Pwf ≥ Pb:<br>
                    qo = J(Pr − Pwf)
                </div>

                <div class="formula">
                    qB = J(Pr − Pb)
                </div>

                <div class="formula">
                    Si Pwf &lt; Pb:<br>
                    qo = qB + (J·Pb/1.8)
                    · [1 − 0.2(Pwf/Pb) − 0.8(Pwf/Pb)²]
                </div>

                <div class="formula">
                    qo,max = qB + (J·Pb/1.8)
                </div>
                """,
                unsafe_allow_html=True,
            )

        valid, error_message = validate_inputs(pr, pb, j, pwf)

        if not valid:
            st.error(error_message)
        else:
            qo, qb, qomax, regime = composite_ipr(pr, pb, j, pwf)

            st.markdown("### 📈 Resultados")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric("Caudal de petróleo qo", f"{qo:,.2f} STB/d")

            with m2:
                st.metric("Caudal a Pb (qB)", f"{qb:,.2f} STB/d")

            with m3:
                st.metric("Caudal máximo qo,max", f"{qomax:,.2f} STB/d")

            if pwf >= pb:
                st.success(
                    f"🟢 Régimen lineal: Pwf = {pwf:.1f} psi ≥ Pb = {pb:.1f} psi."
                )
            else:
                st.warning(
                    f"🟠 Régimen de Vogel: Pwf = {pwf:.1f} psi < Pb = {pb:.1f} psi."
                )

            # Interacción JavaScript requerida por la tarea
            st.markdown("### ⚙️ Interacción HTML + JavaScript")
            components.html(
                javascript_status_card(regime, pwf, pb),
                height=185,
            )

            # ------------------------------------------------
            # CURVA IPR
            # ------------------------------------------------
            st.markdown("### 📉 Curva IPR completa")

            pwf_curve, qo_curve = ipr_curve(pr, pb, j)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(qo_curve, pwf_curve, linewidth=2.5, label="IPR compuesta")
            ax.scatter(
                [qo],
                [pwf],
                s=90,
                zorder=5,
                label="Punto calculado",
            )
            ax.axhline(
                pb,
                linestyle="--",
                linewidth=1.5,
                label=f"Pb = {pb:.0f} psi",
            )
            ax.axhline(
                pr,
                linestyle=":",
                linewidth=1.2,
                label=f"Pr = {pr:.0f} psi",
            )

            ax.set_xlabel("Caudal de petróleo, qo [STB/d]")
            ax.set_ylabel("Presión de fondo fluyente, Pwf [psi]")
            ax.set_title("IPR compuesta — Modelo lineal + Vogel")
            ax.grid(True, alpha=0.25)
            ax.legend()
            fig.tight_layout()

            st.pyplot(fig, use_container_width=True)

            st.markdown(
                """
                <div class="card">
                    <strong>Interpretación:</strong>
                    la curva combina el comportamiento lineal cuando la presión
                    de fondo está por encima de la presión de burbuja y el
                    comportamiento no lineal de Vogel cuando Pwf cae por debajo
                    de Pb. El punto calculado se actualiza automáticamente al
                    modificar los parámetros.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # PERFORACIÓN
    # --------------------------------------------------------
    with tab_perf:
        st.markdown(
            """
            <div class="card">
                <div class="section-title">🔩 Perforación</div>
                <p>
                    Módulo reservado para el cálculo de presión hidrostática
                    del lodo a partir del peso del lodo y la TVD, con
                    comparación frente a la presión de formación.
                </p>
                <p class="small-note">
                    Este módulo se mantiene preparado para incorporar el
                    ejercicio correspondiente.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # RESERVORIOS
    # --------------------------------------------------------
    with tab_res:
        st.markdown(
            """
            <div class="card">
                <div class="section-title">🧱 Reservorios</div>
                <p>
                    Módulo reservado para la estimación volumétrica del
                    Petróleo Original en Sitio (POES).
                </p>
                <p class="small-note">
                    Este módulo se mantiene preparado para incorporar el
                    ejercicio correspondiente.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

