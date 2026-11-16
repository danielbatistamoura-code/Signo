# Oráculo Zodíaco Profissional (SQLite Local)

Aplicação web interativa de Astrologia com banco de dados **SQLite local** rodando diretamente no navegador via **sql.js (WebAssembly)** e persistência automática em **IndexedDB**.

## Arquivos Inclusos
- `index.html` — Aplicação completa (HTML5, CSS3, Bootstrap 5, JavaScript ES6+ e motor SQLite `sql.js`).
- `schema.sql` — Estrutura SQL da tabela `consultas` utilizada no banco de dados SQLite.
- `README.md` — Instruções de uso.

## Como Executar
1. Basta abrir o arquivo `index.html` em qualquer navegador moderno (Chrome, Edge, Firefox, Safari).
2. Não requer instalação de servidor ou backend.
3. Na aba **Banco SQLite**, você pode:
   - Visualizar, filtrar e excluir registros salvos.
   - Clicar em **Exportar .sqlite** para baixar o arquivo físico `oraculo_zodiaco.sqlite` e abri-lo no *DB Browser for SQLite*.
   - Clicar em **Importar .sqlite** para carregar um banco de dados salvo anteriormente.
