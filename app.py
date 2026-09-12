import streamlit as st
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(page_title="Oil & Gas Analytics", page_icon="🛢️", layout="wide")

st.markdown("""
<style>
.stApp {background:#0b3d36}
.block-container {max-width:1200px;padding-top:2rem}

.hero {
    background-image:linear-gradient(rgba(5,35,30,.55),rgba(5,35,30,.70)),
    url("https://i0.wp.com/diazvillanueva.com/wp-content/uploads/2021/12/pozos-petroleo-atardecer.jpg");
    background-size:cover;background-position:center;
    padding:55px 35px;border-radius:20px;color:white;margin-bottom:25px
}
.hero h1{font-size:42px;margin:0}.hero p{font-size:18px}

.card {
    background:#f7faf9;padding:20px;border-radius:16px;margin:10px 0;
    color:#173f38;box-shadow:0 5px 15px rgba(0,0,0,.18)
}
.result {
    background:#f7faf9;padding:18px;border-radius:15px;text-align:center;
    color:#173f38;box-shadow:0 4px 12px rgba(0,0,0,.18);
    transition:all .3s ease
}
.result:hover {
    transform:translateY(-5px);
    box-shadow:0 0 18px rgba(130,220,180,.65)
}
h2,h3{color:white}
button{border-radius:25px!important}
</style>
""", unsafe_allow_html=True)

# Navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Home"

c1, c2, _ = st.columns([1, 1, 5])

with c1:
    if st.button("⌂  Home", use_container_width=True):
        st.session_state.pagina = "Home"

with c2:
    if st.button("⚙  Ejercicios", use_container_width=True):
        st.session_state.pagina = "Ejercicios"

# Home
if st.session_state.pagina == "Home":
    st.markdown("""
    <div class="hero">
        <h1>🛢️ Oil & Gas Analytics</h1>
        <p>Herramientas de análisis técnico para la industria Oil & Gas</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>👨‍💻 Participante</h3>
            <p><b>Edison Contreras</b></p>
            <p>Bootcamp Data Analytics for Oil & Gas</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3>🎯 Propósito</h3>
            <p>Aplicación web desarrollada con Python y Streamlit para
            realizar cálculos de Producción, Perforación y Reservorios.</p>
        </div>
        """, unsafe_allow_html=True)

# Ejercicios
else:
    st.markdown("""
    <div class="hero">
        <h1>⚙️ Ejercicios técnicos</h1>
        <p>Producción · Perforación · Reservorios</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["🛢️ Producción", "🔩 Perforación", "🧱 Reservorios"]
    )

    with tab1:
        st.markdown("""
        <div class="card">
            <h3>IPR compuesta con punto de burbuja</h3>
            <p>Calculadora para un yacimiento inicialmente subsaturado.
            El modelo cambia automáticamente entre comportamiento lineal y Vogel.</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Parámetros de entrada")
            Pr = st.number_input("Pr — Presión promedio [psi]",
                                 min_value=1.0,value=3000.0,step=50.0)
            Pb = st.number_input("Pb — Presión de burbuja [psi]",
                                 min_value=1.0,value=2200.0,step=50.0)
            J = st.number_input("J — Índice de productividad [STB/d/psi]",
                                min_value=0.0001,value=1.5,step=0.1)
            Pwf = st.number_input("Pwf — Presión de fondo fluyente [psi]",
                                  min_value=0.0,value=1800.0,step=50.0)

        with c2:
            st.subheader("Modelo")
            st.markdown("""
            <div class="card">
            <b>Si Pwf ≥ Pb</b><br>
            qo = J(Pr − Pwf)
            <br><br>
            <b>Si Pwf &lt; Pb</b><br>
            qB = J(Pr − Pb)<br>
            qo = qB + (J Pb / 1.8)
            [1 − 0.2(Pwf/Pb) − 0.8(Pwf/Pb)²]
            </div>
            """, unsafe_allow_html=True)

        if Pb >= Pr:
            st.error("Debe cumplirse Pr > Pb.")
            st.stop()

        if Pwf > Pr:
            st.error("Pwf no puede ser mayor que Pr.")
            st.stop()

        qB = J * (Pr - Pb)
        qmax = qB + J * Pb / 1.8

        if Pwf >= Pb:
            qo = J * (Pr - Pwf)
            regime = "LINEAL"
        else:
            x = Pwf / Pb
            qo = qB + (J * Pb / 1.8) * (1 - 0.2*x - 0.8*x**2)
            regime = "VOGEL"

        st.subheader("Resultados")
        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(
                f'<div class="result"><b>qo</b><h2>{qo:,.2f}</h2><p>STB/d</p></div>',
                unsafe_allow_html=True)
        with r2:
            st.markdown(
                f'<div class="result"><b>qB</b><h2>{qB:,.2f}</h2><p>STB/d</p></div>',
                unsafe_allow_html=True)
        with r3:
            st.markdown(
                f'<div class="result"><b>qo,max</b><h2>{qmax:,.2f}</h2><p>STB/d</p></div>',
                unsafe_allow_html=True)

        st.success(f"Condición de operación: {regime}")

        # JavaScript
        st.subheader("Interacción con JavaScript")
        js = f"""
        <div style="background:#f7faf9;padding:18px;border-radius:15px;
                    font-family:Arial;color:#173f38">
            <b>Condición: {regime}</b>
            <p id="mensaje">Pulsa el botón para analizar el régimen.</p>
            <button onclick="analizar()" style="padding:8px 15px;border:0;
                    border-radius:8px;background:#0b3d36;color:white;cursor:pointer">
                Analizar
            </button>
        </div>
        <script>
        function analizar() {{
            document.getElementById("mensaje").innerHTML =
            "Pwf = {Pwf:.1f} psi y Pb = {Pb:.1f} psi. " +
            "Se utiliza el modelo {regime}.";
        }}
        </script>
        """
        components.html(js, height=145)

        # Gráfico con Plotly
        st.subheader("Curva IPR")
        pwf_values = np.linspace(0, Pr, 200)
        qo_values = []

        for p in pwf_values:
            if p >= Pb:
                q = J * (Pr - p)
            else:
                x = p / Pb
                q = qB + (J * Pb / 1.8) * (1 - 0.2*x - 0.8*x**2)
            qo_values.append(q)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=qo_values,y=pwf_values,mode="lines",name="IPR"))
        fig.add_trace(go.Scatter(
            x=[qo],y=[Pwf],mode="markers",name="Punto calculado",
            marker=dict(size=12)))
        fig.add_hline(
            y=Pb,line_dash="dash",
            annotation_text=f"Pb = {Pb:.0f} psi")

        fig.update_layout(
            xaxis_title="Caudal de petróleo qo [STB/d]",
            yaxis_title="Pwf [psi]",
            title="IPR compuesta — Lineal + Vogel",
            template="plotly_white",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("""
        <div class="card">
            <h3>🔩 Perforación</h3>
            <p>Cálculo de presión hidrostática del lodo a partir del peso
            del lodo y la profundidad vertical verdadera (TVD).</p>
            <p><b>Próximamente:</b> implementación del ejercicio.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="card">
            <h3>🧱 Reservorios</h3>
            <p>Estimación volumétrica del Petróleo Original en Sitio (POES).</p>
            <p><b>Próximamente:</b> implementación del ejercicio.</p>
        </div>
        """, unsafe_allow_html=True)
