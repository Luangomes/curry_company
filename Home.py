import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home",
    page_icon="🎲"
)

#image_path = r'C:\Users\luanG\Desktop\Comunidade DS\Repos\portfolios_projetos\imagem2.jpg'
image = Image.open('imagem2.jpg')
st.sidebar.image(image, width=220)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboar")

st.markdown(
    """
    Growth DashboarGrowth Dashboar foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse Dashboar?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de acompanhamento.
        - Visão Tática: Indiadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador: 
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimentos dos restaurantes.
    
    ### Ask for help
    - Linkedin
        - https://www.linkedin.com/in/luan-gomes-a35982169/
    """
)
