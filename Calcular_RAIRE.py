import streamlit as st
from datetime import datetime, date, timedelta
import folium

import streamlit as st
import subprocess

# Conteúdo da página principal
st.title('Cálculo RAIRE')
# URL da imagem
image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLFPxWi5v7QJCZRHsaH5BX4iZYkeFfkIMpEw&s"

#Código HTML e CSS para ajustar a largura da imagem para 20% da largura da coluna e centralizar
html_code = f'<div style="display: flex; justify-content: center;"><img src="{image_url}" alt="Imagem" style="width:8vw;"/></div>'
# Exibir a imagem usando HTML
st.markdown(html_code, unsafe_allow_html=True)

# Centralizar o texto abaixo da imagem
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>DIRETORIA DE ADMINISTRAÇÃO DA AERONÁUTICA</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 1.2em;'>SUBDIRETORIA DE PAGAMENTO DE PESSOAL</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-size: 1em; text-decoration: underline;'>PP2 - DIVISÃO DE PAGAMENTO DE PESSOAL NO EXTERIOR</h3>", unsafe_allow_html=True)

# Texto explicativo
st.write("Cálculo da RAIRE")

# Dicionário de dados contendo país, posto e fator de conversão
data = {
    "": {},  # Adicionando um país em branco
    "África do Sul": {"Cidade do Cabo - FCG": 63, "Pretória": 63},
    "Albânia": {"Tirana": 36},
    "Alemanha": {"Berlim - FCG": 58, "Frankfurt": 58, "Munique": 63},
    "Angola": {"Luanda - FCG": 163},
    "Arábia Saudita": {"Riade": 78},
    "Argélia": {"Argel": 94},
    "Argentina": {"Buenos Aires": 80, "Córdoba - FCG": 25, "Mendoza": 25, "Paso de Los Libres": 28, "Puerto Iguazu": 12},
    "Armênia": {"Ierevan": 39},
    "Austrália": {"Camberra - FCG": 42, "Sidney": 70},
    "Áustria": {"Viena - FCG": 55},
    "Azerbaijão": {"Baku": 51},
    "Bahamas": {"Nassau - FCG": 90},
    "Bahrein": {"Manama": 57},
    "Bangladesh": {"Daca": 107},
    "Barbados": {"Bridgetown": 55},
    "Belarus": {"Minsk": 33},
    "Bélgica": {"Bruxelas - FCG": 43},
    "Belize": {"Belmopan": 57},
    "Benin": {"Cotonou - FCG": 88},
    "Bolívia": {"Cobija": 38, "Cochabamba": 31, "Guayaramerin": 25, "La Paz - FCG": 38, "Puerto Quijarro": 25, "Santa Cruz de la Sierra": 36},
    "Bósnia e Herzegovina": {"Sarajevo": 34},
    "Botsuana": {"Gaborone": 60},
    "Bulgária": {"Sófia": 39},
    "Burkina Faso": {"Uagadougou": 79},
    "Cabo Verde": {"Praia": 40},
    "Camarões": {"Iaundé": 50},
    "Canadá": {"Montreal - FCG": 40},
    "Catar": {"Doha": 62},
    "Cazaquistão": {"Astana": 58},
    "Chile": {"Santiago - FCG": 52},
    "China": {"Cantão - FCG": 67, "Chengdu": 69, "Hong-Kong": 155, "Pequim": 105, "Xangai": 105},
    "Chipre": {"Nicósia": 44},
    "Colômbia": {"Bogotá - FCG": 42, "Letícia": 19},
    "República Democrática do Congo": {"Kinshasa": 81},
    "República do Congo": {"Brazzaville": 58},
    "Coreia do Norte": {"Pyongyang": 50},
    "Coreia do Sul": {"Seul": 95},
    "Croácia": {"Zagreb": 38},
    "Costa do Marfim": {"Abidjan - FCG": 63},
    "Costa Rica": {"São José": 40},
    "Cuba": {"Havana": 50},
    "Dinamarca": {"Copenhague - FCG": 52},
    "Egito": {"Cairo": 52},
    "El Salvador": {"São Salvador": 36},
    "Emirados Árabes Unidos": {"Abu-Dhabi": 68},
    "Equador": {"Quito - FCG": 51},
    "Eslováquia": {"Bratislava": 36},
    "Eslovênia": {"Liubliana": 28},
    "Espanha": {"Barcelona - FCG": 48, "Madrid": 49},
    "Estônia": {"Talin": 42},
    "Etiópia": {"Adis-Abeba": 75},
    "EUA": {"Atlanta": 46, "Boston - FCG": 69, "Chicago": 59, "Hartford": 38, "Houston": 60, "Los Angeles": 73, "Miami": 82, "Nova York": 108, "Orlando": 39, "São Francisco": 88, "Washington": 68},
    "Filipinas": {"Manila": 64},
    "Finlândia": {"Helsinki": 45},
    "França": {"Marselha": 55, "Paris - FCG": 77},
    "Gabão": {"Libreville": 100},
    "Gana": {"Acra": 59},
    "Geórgia": {"Tbilisi": 36},
    "Grécia": {"Atenas": 36},
    "Guatemala": {"Guatemala": 38},
    "Guiana": {"Georgetown - FCG": 46, "Lethem": 22},
    "Guiana Francesa": {"Caiena - FCG": 41, "Saint Georges L'oyapock": 50},
    "Guiné": {"Conacri": 57},
    "Guiné Bissau": {"Bissau": 82},
    "Guiné Equatorial": {"Malabo": 94},
    "Haiti": {"Porto Príncipe- FCG": 63},
    "Honduras": {"Tegucigalpa": 38},
    "Hungria": {"Budapeste": 35},
    "Índia": {"Mumbai": 108, "Nova Delhi - FCG": 87},
    "Indonésia": {"Jacarta": 65},
    "Irã": {"Teerã": 50},
    "Iraque": {"Bagdá": 50},
    "Irlanda": {"Dublin": 72},
    "Israel": {"Tel-Aviv - FCG": 97},
    "Itália": {"Milão": 52, "Roma - FCG": 53},
    "Jamaica": {"Kingston - FCG": 39},
    "Japão": {"Hamamatsu": 80, "Nagoya - FCG": 80, "Tóquio": 100},
    "Jordânia": {"Amã": 40},
    "Kuaite": {"Kuaite": 61},
    "Líbano": {"Beirute": 63},
    "Líbia": {"Trípoli": 88},
    "Malásia": {"Kuala Lumpur": 40},
    "Mali": {"Bamako": 86},
    "Marrocos": {"Rabat": 50},
    "Mauritânia": {"Nuakchott": 50},
    "México": {"México - FCG": 50},
    "Myanmar": {"Yangon": 69},
    "Moçambique": {"Maputo": 67},
    "Namíbia": {"Windhoek - FCG": 63},
    "Nepal": {"Katmandu": 70},
    "Nicarágua": {"Manágua": 50},
    "Nigéria": {"Abuja": 93, "Lagos - FCG": 107},
    "Noruega": {"Oslo": 36},
    "Nova Zelândia": {"Wellington": 36},
    "Omã": {"Mascate": 68},
    "Palestina": {"Ramallah": 57},
    "Panamá": {"Panamá": 41},
    "Paquistão": {"Islamabad": 70},
    "Países Baixos": {"Amsterdã - FCG": 62, "Haia": 42},
    "Paraguai": {"Assunção": 40, "Ciudad del Este": 35, "Concepcion - FCG": 17, "Encarnación": 17, "Pedro Juan Caballero": 28, "Salto del Guairá": 23},
    "Peru": {"Iquitos - FCG": 26, "Lima": 35},
    "Polônia": {"Varsóvia": 40},
    "Portugal": {"Lisboa": 54, "Porto - FCG": 36},
    "Quênia": {"Nairobi": 50},
    "Reino Unido": {"Edimburgo": 55, "Londres - FCG": 100},
    "República Dominicana": {"São Domingos": 46},
    "República Tcheca": {"Praga": 39},
    "Romênia": {"Bucareste": 59},
    "Rússia": {"Moscou": 128},
    "Santa Lúcia": {"Castries": 51},
    "Santa Sé": {"Vaticano": 53},
    "São Tomé e Príncipe": {"São Tomé": 50},
    "Senegal": {"Dacar": 57},
    "Sérvia": {"Belgrado": 47},
    "Singapura": {"Singapura - FCG": 117},
    "Síria": {"Damasco": 55},
    "Sri Lanka": {"Colombo": 54},
    "Sudão": {"Cartum - FCG": 63},
    "Suécia": {"Estocolmo - FCG": 41},
    "Suíça": {"Berna - FCG": 60, "Genebra": 89, "Zurique": 107},
    "Suriname": {"Paramaribo": 44},
    "Tailândia": {"Bangkok": 65},
    "Taiwan, Província da China": {"Taipé": 77},
    "Tanzânia": {"Dar-es-Salaam": 65},
    "Timor Leste": {"Díli": 69},
    "Togo": {"Lomé": 100},
    "Trinidad e Tobago": {"Port-of-Spain": 57},
    "Tunísia": {"Túnis": 44},
    "Turquia": {"Ancara - FCG": 36, "Istambul": 57},
    "Ucrânia": {"Kiev": 94},
    "Uruguai": {"Montevidéu - FCG": 48, "Rio Branco": 12, "Rivera": 19},
    "Venezuela": {"Caracas - FCG": 70, "Ciudad Guayana": 38, "Puerto Ayacucho": 29, "Santa Elena do Uairén": 29},
    "Vietnã": {"Hanói": 63},
    "Zâmbia": {"Lusaca": 57},
    "Zimbábue": {"Harare": 42}
}

tabela = {
    "Almirante-de-Esquadra, General-de-Exército e Tenente-Brigadeiro.": 150,
    "Vice-Almirante, General-de-divisão e Major-Brigadeiro.": 100,
    "Contra-Almirante, General-de-Brigada e Brigadeiro.": 100,
    "Capitão-de-Mar-e-Guerra/ Coronel e Capitão-de-Fragata / Tenente-Coronel.(Adido Militar, Adjunto de Adido Militar).": 90,
    "Capitão-de-Mar-e-Guerra e Coronel .": 90,
    "Capitão-de-Fragata e Tenente-Coronel.": 80,
    "Capitão-de-Corveta e Major.": 80,
    "Capitão-Tenente e Capitão.": 80,
    "Oficiais Subalternos.": 80,
    "Suboficial, Subtenente e Sargento (Auxiliar de Adido Militar).": 70,
    "Suboficial, Subtenente, Sargento e Praças Especiais (Alunos de Órgão de formação de Oficiais da Ativa).": 70,
    "Cabo e demais Praças.": 70
}

# Função para calcular o valor da RAIRE
def calcular_raire(start_date, end_date, grau_hierarquico, conversion_factor, numero_dependentes):
    delta = end_date - start_date
    dias = delta.days
    if dias >= 30:
        valor_raire = conversion_factor * tabela[grau_hierarquico]
    else:
        proporcao = dias / 30
        valor_raire = conversion_factor * tabela[grau_hierarquico] * proporcao

    # Aplicar acréscimo no valor final da RAIRE baseado no número de dependentes
    if numero_dependentes == 2:
        valor_raire *= 1.05  # 5% de acréscimo para 2 dependentes
    elif numero_dependentes >= 3:
        valor_raire *= 1.10  # 10% de acréscimo para 3 ou mais dependentes
    
    return valor_raire

# Lista de graus hierárquicos
rank_options = list(tabela.keys())

# Seletor de país inicialmente vazio
selected_country = st.selectbox("Selecione o país", [""] + list(data.keys()))

# Se houver um país selecionado
if selected_country:
    st.info(f"Você selecionou: {selected_country}")
    
    # Espaço vazio para o seletor de postos
    selected_post_placeholder = st.empty()

    # Atualiza o seletor de postos
    selected_post_options = list(data[selected_country].keys())
    selected_post = selected_post_placeholder.selectbox("Selecione o posto", selected_post_options)

    if selected_post:
        st.info(f'Você selecionou o posto: {selected_post}',icon="ℹ️")
        
        # Obter o valor do posto selecionado
        conversion_factor = data[selected_country][selected_post]
        st.warning(f"O fator do posto selecionado é: {conversion_factor}")
        
        
        
        # Seletor para indicar se leva dependentes e quantos
        numero_dependentes = st.select_slider("Número de dependentes:", options=[0, 1, 2, 3, 4, 5])
        # Inputs de data para data de ida e volta
        start_date = st.date_input("Selecione a data de início da Portaria:", format="DD/MM/YYYY", min_value=date(2024, 1, 1))
        end_date = st.date_input("Selecione a data de término da Portaria:", format="DD/MM/YYYY")
        
        # Verificar se a data de término é igual ou menor que a data atual
        if end_date <= date.today():
            st.error("Período Incorreto")
        else:
            # Calcular a diferença de dias entre as datas
            delta = end_date - start_date
            st.warning(f"Período de {delta.days} dias")
            
        # Calcular a RAIRE se todas as informações forem fornecidas
        if start_date and end_date and numero_dependentes is not None:
            # Seletor de grau hierárquico
            selected_rank = st.selectbox("Selecione seu grau hierárquico:", rank_options)
            if selected_rank:
                # Obter o valor do grau hierárquico selecionado
                selected_rank_value = tabela[selected_rank]
                st.warning(f"O valor do grau hierárquico selecionado é: {selected_rank_value}")
                
                # Calcular o valor do RAIRE
                valor_raire = calcular_raire(start_date, end_date, selected_rank, conversion_factor, numero_dependentes)

                # Formatar o valor do RAIRE para moeda em dólar
                valor_raire_usd = "${:,.2f}".format(valor_raire)

                # Modificação para formatar o valor em RAIRE
                valor_raire_formatado = "{:,.2f}".format(valor_raire).replace(",", "-").replace(".", ",").replace("-", ".")

                st.success(f"O Valor da RAIRE calculada é: $ {valor_raire_formatado} dólares.")
