# 📒 Agenda de Contatos

Aplicação web simples de agenda de contatos desenvolvida com **Python + Flask + SQLite**.

## 🚀 Funcionalidades

- ✅ Cadastrar novos contatos (nome, e-mail, telefone)
- ✅ Listar todos os contatos
- ✅ Buscar contato por nome
- ✅ Editar contato existente
- ✅ Remover contato

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3 | Linguagem principal |
| Flask | Framework web |
| SQLite | Banco de dados |
| HTML / CSS | Interface do usuário |
| Jinja2 | Templates (engine do Flask) |

## 📁 Estrutura do projeto

```
agenda-contatos/
├── app.py                  # Aplicação principal (rotas e banco)
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Este arquivo
├── static/
│   └── css/
│       └── style.css       # Estilos da interface
└── templates/
    ├── base.html           # Template base (header, footer)
    ├── index.html          # Lista de contatos
    └── form.html           # Formulário de cadastro/edição
```

## ▶️ Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/agenda-contatos.git
cd agenda-contatos
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / Mac:**
```bash
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute a aplicação

```bash
python app.py
```

### 6. Acesse no navegador

```
http://localhost:5000
```

O banco de dados (`agenda.db`) é criado automaticamente na primeira execução.

## 📸 Telas

| Tela | Descrição |
|---|---|
| `/` | Lista de contatos com busca |
| `/novo` | Formulário para adicionar contato |
| `/editar/<id>` | Formulário para editar contato |

## 👩‍💻 Autora

Desenvolvido durante o curso **Técnico em Desenvolvimento de Sistemas**  
MedTec · SENAC AR/RN · 2026
