import pandas as pd
from dbfread import DBF
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Carrega o arquivo DBF
dbf_path = 'pacigeral_jun24.dbf'

# Carregar o arquivo DBF com codificação 'latin1' e ignorar erros
dbf_data = DBF(dbf_path, encoding='latin1', char_decode_errors='ignore')

# convertendo uma amostra pequena em dataframe
# df_sample = pd.DataFrame([record for i, record in enumerate(dbf_data) if i < 10])
# print(df_sample.head())

# Convertendo todo o arquivo para dataframe
df = pd.DataFrame(iter(dbf_data))

# 1. Filtrar pacientes com Topografia de pulmão (TOPOGRUP = C34)
df_pulmao = df[df['TOPOGRUP'] == 'C34']

# 2. Filtrar pacientes residentes no estado de São Paulo (UFRESID = 'SP')
df_sp_pulmao = df_pulmao[df_pulmao['UFRESID'] == 'SP']

# 3. Selecionar pacientes com Base do Diagnóstico com Confirmação Microscópica (BASEDIAG = 3)
df_diag_confirm = df_sp_pulmao[df_sp_pulmao['BASEDIAG'] == 3]

# 4. Retirar categorias 0, X e Y da coluna ECGRUP
df_cleaned_ecgrup = df_diag_confirm[~df_diag_confirm['ECGRUP'].isin(['0', 'X', 'Y'])]

# 5. Retirar pacientes que fizeram Hormonioterapia e TMO (HORMONIO = 1 e TMO = 1)
df_no_hormonio_tmo = df_cleaned_ecgrup[~((df_cleaned_ecgrup['HORMONIO'] == 1) & (df_cleaned_ecgrup['TMO'] == 1))]

# 6. Selecionar pacientes com Ano de Diagnóstico até 2019 (ANODIAG <= 2019)
df_ano_diag = df_no_hormonio_tmo[df_no_hormonio_tmo['ANODIAG'] <= 2019]

# 7. Retirar pacientes com idade menor que 20 anos
df_maior_20 = df_ano_diag[df_ano_diag['IDADE'] >= 20]

# 8. Calcula a diferença em dias entre Diagnóstico e Consulta, Tratamento e Diagnóstico, Tratamento e Consulta
df_maior_20['CONSDIAG'] = (pd.to_datetime(df_maior_20['DTCONSULT']) - pd.to_datetime(df_maior_20['DTDIAG'])).dt.days
df_maior_20['DIAGTRAT'] = (pd.to_datetime(df_maior_20['DTTRAT']) - pd.to_datetime(df_maior_20['DTDIAG'])).dt.days
df_maior_20['TRATCONS'] = (pd.to_datetime(df_maior_20['DTTRAT']) - pd.to_datetime(df_maior_20['DTCONSULT'])).dt.days

# Codificando as colunas
df_maior_20['CONSDIAG'] = pd.cut(df_maior_20['CONSDIAG'], bins=[-float('inf'), 30, 60, float('inf')], labels=[0, 1, 2])
df_maior_20['DIAGTRAT'] = pd.cut(df_maior_20['DIAGTRAT'], bins=[-float('inf'), 60, 90, float('inf')], labels=[0, 1, 2])
df_maior_20['DIAGTRAT'] = df_maior_20['DIAGTRAT'].fillna(3)  # Codificando como 3 quem não tem tratamento
df_maior_20['TRATCONS'] = pd.cut(df_maior_20['TRATCONS'], bins=[-float('inf'), 60, 90, float('inf')], labels=[0, 1, 2])
df_maior_20['TRATCONS'] = df_maior_20['TRATCONS'].fillna(3)  # Codificando como 3 quem não tem tratamento

# 9. Extrair somente o número das colunas DRS e DRSINSTITU
df_maior_20['DRS'] = df_maior_20['DRS'].str.extract('(\d+)')
df_maior_20['DRSINSTITU'] = df_maior_20['DRSINSTITU'].str.extract('(\d+)')

# 10. Criar a coluna binária de óbito a partir da coluna ULTINFO
df_maior_20['OBITO'] = df_maior_20['ULTINFO'].apply(lambda x: 0 if x in [1, 2] else 1)

# 11. Retirar as colunas
colunas_remover = [
    "UFNASC", "UFRESID", "CIDADE", "DTCONSULT", "CLINICA" , "DTDIAG",
    "BASEDIAG", "TOPOGRUP", "DESCTOPO", 'DESCMORFO', "T", "N", "M", "PT", "PN",
    "PM", "S", "G", "LOCALTNM", "IDMITOTIC", "PSA", "GLEASON", "OUTRACLA",
    "META01", "META02", "META03", "META04", "DTTRAT", "NAOTRAT",
    "TRATAMENTO", "TRATHOSP", "TRATFANTES", "TRATFAPOS", "HORMONIO",
    "TMO", "NENHUMANT", "CIRURANT", "RADIOANT", "QUIMIOANT", "HORMOANT",
    "TMOANT", "IMUNOANT", "OUTROANT", "HORMOAPOS", "TMOAPOS", "DTULTINFO",
    "CICI" , "CICIGRUP", "CICISUBGRU", "FAIXAETAR", "LATERALI", "INSTORIG",
    "RRAS", "ERRO", "DTRECIDIVA", "RECNENHUM", "RECLOCAL", "RECREGIO",
    "RECDIST", "REC01", "REC02", "REC03", "REC04", "CIDO", "DSCCIDO",
    "HABILIT" , "HABIT11" , "HABILIT1" , "CIDADEH", "PERDASEG"
]
df_final = df_maior_20.drop(columns=colunas_remover)

# Exibe os primeiros registros do dataframe final
print(df_final.head())

# Trata valores ausentes
df.dropna(inplace=True)  # Removi linhas com valores ausentes

# Define variáveis independentes
X = df.drop('obito', axis=1)
y = df['obito']

# Codificação de variáveis categóricas e normalização
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Cria um pré-processador usando codificadores e normalizadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])

# Transforma os dados
X_processed = pipeline.fit_transform(X)

# Dividir dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)