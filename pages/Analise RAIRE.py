import calendar
from datetime import date, timedelta

import requests
import streamlit as st

st.set_page_config(page_title="Automação RAIRE", page_icon="🏠")
st.title("🏠 Automação RAIRE")
st.caption(
    "Ferramentas de apoio ao Reembolso de Aluguel de Imóvel Residencial no "
    "Exterior (Módulo 16 do Manual de Pagamento de Pessoal do COMAER)."
)

# ---------------------------------------------------------------------------
# Tabela de Fatores de Conversão
# Fonte: Portaria MRE nº 494, de 20/11/2023 (Anexo 37 do Guia de
# Administração dos Postos). Cidades marcadas como referência (FCG) no
# documento original foram mantidas sem distinção especial aqui.
# ---------------------------------------------------------------------------
FATORES = {
    "África do Sul": {"Cidade do Cabo": 63, "Pretória": 63},
    "Albânia": {"Tirana": 36},
    "Alemanha": {"Berlim": 58, "Frankfurt": 58, "Munique": 63},
    "Angola": {"Luanda": 163},
    "Arábia Saudita": {"Riade": 78},
    "Argélia": {"Argel": 94},
    "Argentina": {
        "Buenos Aires": 80,
        "Córdoba": 25,
        "Mendoza": 25,
        "Paso de Los Libres": 28,
        "Puerto Iguazu": 12,
    },
    "Armênia": {"Ierevan": 39},
    "Austrália": {"Camberra": 42, "Sidney": 70},
    "Áustria": {"Viena": 55},
    "Azerbaijão": {"Baku": 51},
    "Bahamas": {"Nassau": 90},
    "Bahrein": {"Manama": 57},
    "Bangladesh": {"Daca": 107},
    "Barbados": {"Bridgetown": 55},
    "Belarus": {"Minsk": 33},
    "Bélgica": {"Bruxelas": 43},
    "Belize": {"Belmopan": 57},
    "Benin": {"Cotonou": 88},
    "Bolívia": {
        "Cobija": 38,
        "Cochabamba": 31,
        "Guayaramerin": 25,
        "La Paz": 38,
        "Puerto Quijarro": 25,
        "Santa Cruz de la Sierra": 36,
    },
    "Bósnia e Herzegovina": {"Sarajevo": 34},
    "Botsuana": {"Gaborone": 60},
    "Bulgária": {"Sófia": 39},
    "Burkina Faso": {"Uagadougou": 79},
    "Cabo Verde": {"Praia": 40},
    "Camarões": {"Iaundé": 50},
    "Canadá": {"Montreal": 40, "Ottawa": 46, "Toronto": 47, "Vancouver": 53},
    "Catar": {"Doha": 62},
    "Cazaquistão": {"Astana": 58},
    "Chile": {"Santiago": 52},
    "China": {"Cantão": 67, "Chengdu": 69, "Hong-Kong": 155, "Pequim": 105, "Xangai": 105},
    "Chipre": {"Nicósia": 44},
    "Colômbia": {"Bogotá": 42, "Letícia": 19},
    "República Democrática do Congo": {"Kinshasa": 81},
    "República do Congo": {"Brazzaville": 58},
    "Coreia do Norte": {"Pyongyang": 50},
    "Coreia do Sul": {"Seul": 95},
    "Croácia": {"Zagreb": 38},
    "Costa do Marfim": {"Abidjan": 63},
    "Costa Rica": {"São José": 40},
    "Cuba": {"Havana": 50},
    "Dinamarca": {"Copenhague": 52},
    "Egito": {"Cairo": 52},
    "El Salvador": {"São Salvador": 36},
    "Emirados Árabes Unidos": {"Abu-Dhabi": 68},
    "Equador": {"Quito": 51},
    "Eslováquia": {"Bratislava": 36},
    "Eslovênia": {"Liubliana": 28},
    "Espanha": {"Barcelona": 48, "Madrid": 49},
    "Estônia": {"Talin": 42},
    "Etiópia": {"Adis-Abeba": 75},
    "EUA": {
        "Atlanta": 46,
        "Boston": 69,
        "Chicago": 59,
        "Hartford": 38,
        "Houston": 60,
        "Los Angeles": 73,
        "Miami": 82,
        "Nova York": 108,
        "Orlando": 39,
        "São Francisco": 88,
        "Washington": 68,
    },
    "Filipinas": {"Manila": 64},
    "Finlândia": {"Helsinki": 45},
    "França": {"Marselha": 55, "Paris": 77},
    "Gabão": {"Libreville": 100},
    "Gana": {"Acra": 59},
    "Geórgia": {"Tbilisi": 36},
    "Grécia": {"Atenas": 36},
    "Guatemala": {"Guatemala": 38},
    "Guiana": {"Georgetown": 46, "Lethem": 22},
    "Guiana Francesa": {"Caiena": 41, "Saint Georges L'oyapock": 50},
    "Guiné": {"Conacri": 57},
    "Guiné Bissau": {"Bissau": 82},
    "Guiné Equatorial": {"Malabo": 94},
    "Haiti": {"Porto Príncipe": 63},
    "Honduras": {"Tegucigalpa": 38},
    "Hungria": {"Budapeste": 35},
    "Índia": {"Mumbai": 108, "Nova Delhi": 87},
    "Indonésia": {"Jacarta": 65},
    "Irã": {"Teerã": 50},
    "Iraque": {"Bagdá": 50},
    "Irlanda": {"Dublin": 72},
    "Israel": {"Tel-Aviv": 97},
    "Itália": {"Milão": 52, "Roma": 53},
    "Jamaica": {"Kingston": 39},
    "Japão": {"Hamamatsu": 80, "Nagoya": 80, "Tóquio": 100},
    "Jordânia": {"Amã": 40},
    "Kuaite": {"Kuaite": 61},
    "Líbano": {"Beirute": 63},
    "Líbia": {"Trípoli": 88},
    "Malásia": {"Kuala Lumpur": 40},
    "Mali": {"Bamako": 86},
    "Marrocos": {"Rabat": 50},
    "Mauritânia": {"Nuakchott": 50},
    "México": {"México": 50},
    "Myanmar": {"Yangon": 69},
    "Moçambique": {"Maputo": 67},
    "Namíbia": {"Windhoek": 63},
    "Nepal": {"Katmandu": 70},
    "Nicarágua": {"Manágua": 50},
    "Nigéria": {"Abuja": 93, "Lagos": 107},
    "Noruega": {"Oslo": 36},
    "Nova Zelândia": {"Wellington": 36},
    "Omã": {"Mascate": 68},
    "Palestina": {"Ramallah": 57},
    "Panamá": {"Panamá": 41},
    "Paquistão": {"Islamabad": 70},
    "Países Baixos": {"Amsterdã": 62, "Haia": 42},
    "Paraguai": {
        "Assunção": 40,
        "Ciudad del Este": 35,
        "Concepcion": 17,
        "Encarnación": 17,
        "Pedro Juan Caballero": 28,
        "Salto del Guairá": 23,
    },
    "Peru": {"Iquitos": 26, "Lima": 35},
    "Polônia": {"Varsóvia": 40},
    "Portugal": {"Faro": 36, "Lisboa": 54, "Porto": 36},
    "Quênia": {"Nairobi": 50},
    "Reino Unido": {"Edimburgo": 55, "Londres": 100},
    "República Dominicana": {"São Domingos": 46},
    "República Tcheca": {"Praga": 39},
    "Romênia": {"Bucareste": 59},
    "Rússia": {"Moscou": 128},
    "Santa Lúcia": {"Castries": 51},
    "Santa Sé": {"Vaticano": 53},
    "São Tomé e Príncipe": {"São Tomé": 50},
    "Senegal": {"Dacar": 57},
    "Sérvia": {"Belgrado": 47},
    "Singapura": {"Singapura": 117},
    "Síria": {"Damasco": 55},
    "Sri Lanka": {"Colombo": 54},
    "Sudão": {"Cartum": 63},
    "Suécia": {"Estocolmo": 41},
    "Suíça": {"Berna": 60, "Genebra": 89, "Zurique": 107},
    "Suriname": {"Paramaribo": 44},
    "Tailândia": {"Bangkok": 65},
    "Taiwan": {"Taipé": 77},
    "Tanzânia": {"Dar-es-Salaam": 65},
    "Timor Leste": {"Díli": 69},
    "Togo": {"Lomé": 100},
    "Trinidad e Tobago": {"Port-of-Spain": 57},
    "Tunísia": {"Túnis": 44},
    "Turquia": {"Ancara": 36, "Istambul": 57},
    "Ucrânia": {"Kiev": 94},
    "Uruguai": {
        "Artigas": 13,
        "Chui": 12,
        "Montevidéu": 48,
        "Rio Branco": 12,
        "Rivera": 19,
    },
    "Venezuela": {
        "Caracas": 70,
        "Ciudad Guayana": 38,
        "Puerto Ayacucho": 29,
        "Santa Elena do Uairén": 29,
    },
    "Vietnã": {"Hanói": 63},
    "Zâmbia": {"Lusaca": 57},
    "Zimbábue": {"Harare": 42},
}

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📋 Checklist de Documentação",
        "🌍 Fator / Valor-Limite",
        "📅 Valor-Limite Diário",
        "💱 Conversor de Câmbio",
    ]
)

# ---------------------------------------------------------------------------
# 1. Checklist de documentação (item 16.5.8)
# ---------------------------------------------------------------------------
with tab1:
    st.header("Checklist de Documentação")
    st.caption("Conforme item 16.5.8 do Módulo 16")

    situacao = st.radio(
        "Situação do contrato",
        [
            "1º mês da contratação, alteração ou renovação de contrato",
            "A partir do 2º mês (contrato já vigente)",
        ],
    )

    if situacao.startswith("1º"):
        docs = [
            "Contrato assinado pelo locador e pelo locatário",
            "Tradução do contrato para o português",
            "Declaração de Pagamento assinada pelo militar (Anexo H)",
            "Requerimento de reembolso de aluguel no exterior (Anexo I), "
            "assinado pelo Adido/Chefe da Representação (quando houver) e pelo militar",
            "Comprovante de pagamento (recibo assinado pelo locador, "
            "nota fiscal, ou fatura + comprovante bancário)",
        ]
    else:
        docs = [
            "Declaração de Pagamento assinada pelo militar (Anexo H)",
            "Comprovante de pagamento (recibo assinado pelo locador, "
            "nota fiscal, ou fatura + comprovante bancário)",
        ]

    st.subheader("Documentos exigidos")
    checks = {doc: st.checkbox(doc, key=f"doc_{i}") for i, doc in enumerate(docs)}

    faltando = [d for d, ok in checks.items() if not ok]
    st.divider()
    if faltando:
        st.warning(f"Faltam {len(faltando)} documento(s) para esta remessa:")
        for d in faltando:
            st.write(f"- {d}")
    else:
        st.success("Documentação completa para envio à SDPP/PP2!")

# ---------------------------------------------------------------------------
# 2. Fator de conversão e valor-limite por cidade
# ---------------------------------------------------------------------------
with tab2:
    st.header("Fator de Conversão e Valor-Limite")
    st.caption(
        "Tabela conforme Portaria MRE nº 494/2023 (Anexo 37 do Guia de "
        "Administração dos Postos)."
    )

    pais = st.selectbox("País", sorted(FATORES.keys()))
    cidade = st.selectbox("Cidade/Posto", sorted(FATORES[pais].keys()))
    fator = FATORES[pais][cidade]

    st.metric("Fator de Conversão", fator)

    valor_base = st.number_input(
        "Valor-base de referência (US$)",
        min_value=0.0,
        step=10.0,
        help=(
            "Informe o valor-base vigente para o posto/graduação do "
            "militar (Portaria GM-MD nº 4.685/2023 e legislação correlata)."
        ),
    )

    if valor_base > 0:
        valor_limite = valor_base * fator / 100
        st.metric("Valor-Limite Mensal Estimado (US$)", f"{valor_limite:,.2f}")
        st.caption(
            "Cálculo: Valor-base × Fator ÷ 100. Confirme o valor-base vigente "
            "antes de utilizar oficialmente — este app não substitui a "
            "tabela oficial do Ministério da Defesa."
        )

# ---------------------------------------------------------------------------
# 3. Valor-limite diário (item 16.5.10.1)
# ---------------------------------------------------------------------------
with tab3:
    st.header("Valor-Limite Diário")
    st.caption(
        "Para ressarcimento de períodos de aluguel/estadia inferiores a "
        "1 mês — item 16.5.10.1 do Módulo 16."
    )

    valor_limite_mensal = st.number_input(
        "Valor-Limite Mensal (US$)", min_value=0.0, step=10.0, key="vlm"
    )
    mes_ref = st.selectbox("Mês de referência", MESES)
    dias_periodo = st.number_input(
        "Número de dias do período (aluguel/estadia)",
        min_value=1,
        max_value=31,
        step=1,
        value=1,
    )

    divisor = 28 if mes_ref == "Fevereiro" else 30

    if valor_limite_mensal > 0:
        valor_diario = valor_limite_mensal / divisor
        valor_proporcional = valor_diario * dias_periodo

        col1, col2 = st.columns(2)
        col1.metric("Valor-Limite Diário (US$)", f"{valor_diario:,.2f}")
        col2.metric(
            f"Valor Proporcional ({dias_periodo} dia(s))",
            f"US$ {valor_proporcional:,.2f}",
        )
        st.caption(
            f"Divisor usado: {divisor} dias "
            f"({'fevereiro' if divisor == 28 else 'demais meses'})."
        )

# ---------------------------------------------------------------------------
# 4. Conversor de câmbio (item 16.5.11)
# ---------------------------------------------------------------------------
with tab4:
    st.header("Conversor de Câmbio")
    st.caption(
        "Converte o valor do contrato (em moeda diferente de dólar) para "
        "US$, usando a taxa do primeiro dia útil do mês de competência "
        "— item 16.5.11 do Módulo 16."
    )

    col1, col2 = st.columns(2)
    with col1:
        moeda_origem = st.text_input(
            "Código da moeda do contrato (ex.: EUR, GBP, JPY, ARS)",
            value="EUR",
        ).strip().upper()
        valor_origem = st.number_input(
            "Valor no contrato", min_value=0.0, step=10.0, key="valor_origem"
        )
    with col2:
        data_ref = st.date_input(
            "Mês/ano de competência (qualquer dia do mês)", value=date.today()
        )

    def primeiro_dia_util(ano: int, mes: int) -> date:
        d = date(ano, mes, 1)
        while d.weekday() >= 5:  # sábado=5, domingo=6
            d += timedelta(days=1)
        return d

    sugestao = primeiro_dia_util(data_ref.year, data_ref.month)
    st.info(
        f"Primeiro dia útil sugerido para {calendar.month_name[data_ref.month]}"
        f"/{data_ref.year}: **{sugestao.strftime('%d/%m/%Y')}** "
        "(considerando apenas sábados e domingos — confira feriados locais)."
    )

    if st.button("Converter", type="primary"):
        if valor_origem <= 0:
            st.error("Informe um valor no contrato maior que zero.")
        else:
            try:
                url = f"https://api.frankfurter.app/{sugestao.isoformat()}"
                resp = requests.get(
                    url, params={"from": moeda_origem, "to": "USD"}, timeout=10
                )
                resp.raise_for_status()
                dados = resp.json()
                taxa = dados["rates"]["USD"]
                valor_usd = valor_origem * taxa

                st.success(
                    f"Taxa {moeda_origem} → USD em {dados['date']}: {taxa:.4f}"
                )
                st.metric("Valor convertido (US$)", f"{valor_usd:,.2f}")
            except Exception as exc:
                st.error(
                    f"Não foi possível obter a cotação automaticamente ({exc}). "
                    "Confira manualmente no site do Banco Central do Brasil."
                )

    st.caption(
        "Fonte da cotação: Frankfurter API (câmbio de referência do Banco "
        "Central Europeu). Para fins oficiais de registro no processo "
        "administrativo, confirme a taxa no site do Banco Central do Brasil."
    )
