# 💰 ProjetoCustos - Gestão Financeira Pessoal

Sistema de controlo financeiro desenvolvido para gestão de receitas e despesas, com autenticação de utilizadores, categorização personalizada e exportação de relatórios.

## 🚀 Funcionalidades

- **Autenticação Segura**: Registo e login de utilizadores com tokens JWT.
- **Gestão de Categorias**: Criação, edição e exclusão de categorias com cores personalizadas.
- **Controlo de Transações**: Registo de entradas (receitas) e saídas (despesas) vinculadas a categorias.
- **Dashboard Visual**: Resumo financeiro com saldo atual, total de receitas/despesas e gráfico comparativo.
- **Relatórios**: Exportação de relatórios mensais em PDF utilizando jsPDF.
- **Interface Responsiva**: Design moderno e limpo focado na experiência do utilizador.

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python / FastAPI**: Framework de alta performance para a API.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **SQLite**: Banco de dados relacional leve.
- **Pydantic**: Validação de dados e esquemas.

### Frontend
- **Vue.js 3**: Framework progressivo para a interface.
- **Pinia**: Gestão de estado global da aplicação.
- **Chart.js**: Visualização de dados em gráficos.
- **Vite**: Ferramenta de build rápida.

## 📦 Como Executar o Projeto

### Pré-requisitos
- Python 3.9+
- Node.js 16+
- Git

### 1. Configurar o Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

cd frontend
npm install
npm run dev
