# Catálogo de Filmes · UC32

Sistema CRUD feito com **Python (Flask)** e **SQLite**, publicado no **Render**.

## Funcionalidades
- **Create**: cadastrar filme (título, gênero, ano e nota de 1 a 10)
- **Read**: listar todos os filmes, com total e nota média
- **Update**: editar um filme existente
- **Delete**: excluir um filme (com confirmação)

O banco (`filmes.db`) é criado automaticamente ao iniciar o app.

## Rodar localmente
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:5000

## Estrutura
```
catalogo-filmes/
├── app.py            # rotas e SQL
├── requirements.txt
├── Procfile
├── static/style.css
└── templates/
    ├── base.html
    ├── index.html
    └── form.html
```

## Deploy no Render
1. Suba o projeto em um repositório no GitHub.
2. No [render.com](https://render.com): **New → Web Service** e conecte o repositório.
3. Preencha:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Clique em **Deploy Web Service**.

> No Render gratuito o SQLite é temporário: os dados somem quando o serviço reinicia.
> Isso é esperado para estudo e portfólio.
