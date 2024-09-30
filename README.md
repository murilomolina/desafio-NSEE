# Desafio-NSEE
## Preparação dos dados 
A preparação dos dados ser ́a feita a partir do Registro Hospitalar de Câncer de São Paulo,
Realizando as seleções abaixo, a partir do banco.

1. Selecionar pacientes com Topografia de pulmão (TOPOGRUP = C34);

2. Selecionar pacientes com estado de Residência de São Paulo (UFRESID = SP);

3. Selecionar pacientes com Base do Diagnóstico com Confirmacão Microscópica (BASEDIAG = 3);

4. Retirar categorias 0, X e Y da coluna ECGRUP;

5. Retirar pacientes que fizeram Hormonioterapia e TMO (HORMONIO = 1 e TMO = 1);

6. Selecionar pacientes com Ano de Diagnóstico até 2019 (ANODIAG ¡= 2019);

7. Retirar pacientes com IDADE menor do que 20 anos;

8. Calcular a diferen ̧ca em dias entre Diagnóstico e Consulta, Tratamento e Diagnóstico,
Tratamento e Consulta, a partir dessas 3 datas (DTCONSULT, DTDIAG e DTTRAT).
Após o cálculo, codificar as colunas da seguinte forma:
• CONSDIAG – 0 = até 30 dias; 1 = entre 31 e 60 dias; 2 = mais de 61 dias;
• DIAGTRAT – 0 = até 60 dias; 1 = entre 61 e 90 dias; 2 = mais de 91 dias; 3 = Não tratou (datas de tratamento vazias);
• TRATCONS – 0 = até 60 dias; 1 = entre 61 e 90 dias; 2 = mais de 91 dias; 3 = Não tratou (datas de tratamento vazias).

9. Extrair somente o número das colunas DRS e DRSINSTITU;

10. Criar a coluna binária de ́obito, a partir da coluna ULTINFO, onde as categorias 1 e 2 representam que o paciente está vivo e as 3 e 4 representam o  ́obito por qualquer motivo;

11. Retirar as colunas:
UFNASC, UFRESID, CIDADE, DTCONSULT, CLINICA , DTDIAG,
BASEDIAG, TOPOGRUP, DESCTOPO, DESCMORFO, T, N, M, PT, PN,
PM, S , G, LOCALTNM, IDMITOTIC, PSA, GLEASON, OUTRACLA,
META01, META02, META03, META04, DTTRAT, NAOTRAT,
TRATAMENTO, TRATHOSP, TRATFANTES, TRATFAPOS, HORMONIO,
TMO, NENHUMANT, CIRURANT, RADIOANT, QUIMIOANT, HORMOANT,
TMOANT, IMUNOANT, OUTROANT, HORMOAPOS, TMOAPOS, DTULTINFO,
CICI , CICIGRUP, CICISUBGRU, FAIXAETAR, LATERALI, INSTORIG,
RRAS, ERRO, DTRECIDIVA, RECNENHUM, RECLOCAL, RECREGIO,
RECDIST, REC01, REC02, REC03, REC04, CIDO, DSCCIDO,
HABILIT , HABIT11 , HABILIT1 , CIDADEH, PERDASEG

## Pré-Processamento
Após a conclusão das etapas anteriores de preparac ao dos dados, realize o pré-processamento do conjunto de dados resultante, de forma a deix ́a-lo pronto para aplicação em um modelo de machine learning. Certifique-se de que todas as vari ́aveis estejam devidamente tratadas e adequadas para treinar um modelo. A vari ́avel de sa ́ıda a ser utilizada ́e ́obito, criada na Etapa 10.