# Steam Wishlist Tracker

MVP em Python + SQLite + Streamlit para acompanhar jogos da sua wishlist da Steam e destacar apenas os que estão em promoção.

## O que este protótipo faz

- Salva manualmente uma lista de AppIDs da Steam
- Atualiza os dados sob demanda (botão "Atualizar agora")
- Consulta endpoint público da Steam Store API para preço e desconto
- Armazena os dados em SQLite (`database.db`)
- Exibe tabela com:
  - Nome
  - Preço atual
  - Preço original
  - Percentual de desconto
  - Data da última atualização

## Estrutura

```text
steam-wishlist-tracker/
├── app.py
├── database.py
├── steam_api.py
├── models.py
├── requirements.txt
├── README.md
└── database.db
```

## Requisitos

- Python 3.10+

## Como executar

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Rode a aplicação:

```bash
streamlit run app.py
```

3. No navegador:
   - Informe os AppIDs (separados por vírgula ou quebra de linha)
   - Clique em **Salvar lista**
   - Clique em **Atualizar agora**
   - Veja os jogos em promoção na tabela

## Observações do MVP

- Não usa autenticação
- Não tem notificações
- Não tem scheduler (atualização apenas manual)
- Não mantém histórico de preços
- Jogos sem preço disponível no endpoint (ex.: alguns F2P/DLCs) podem não aparecer nos resultados
