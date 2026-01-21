# V4Vision - Dashboard Multi-Tenant

Dashboard de análise de performance comercial, retrospectiva e estratégia para múltiplas empresas.

## ⚠️ IMPORTANTE - Isolamento Total

Este projeto foi configurado para **NÃO INTERFERIR** em nenhum outro container/stack do seu Portainer:

| Item | Valor | Motivo |
|------|-------|--------|
| **Porta padrão** | `8585` | Evita conflito com outros serviços |
| **Prefixo containers** | `v4vision_*` | Identificação única |
| **Prefixo volumes** | `v4vision_*` | Dados isolados |
| **Prefixo variáveis** | `V4VISION_*` | Não conflita com outras env vars |
| **Rede** | `v4vision_internal_network` | Rede isolada |

## 🚀 Características

- **Multi-tenant**: Cada empresa vê apenas seus próprios dados
- **Controle de Acesso**: 
  - Platform Admin: Gerencia todas as empresas
  - Company Admin: Edita dados da sua empresa
  - Viewer: Apenas visualiza
- **Módulos**:
  - Retrospectiva (análise anual com gráficos)
  - Estratégia (planejamento com cenários)
  - Gestão Semanal (acompanhamento operacional)
  - Protocolos (regras do time comercial)

## 🛠️ Stack Tecnológica

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18 + Vite + Tailwind CSS
- **Banco de Dados**: PostgreSQL 15
- **Autenticação**: JWT (Simple JWT)
- **Deploy**: Docker + Docker Compose

## 📦 Instalação

### Requisitos
- Docker
- Docker Compose

### Deploy com Portainer (RECOMENDADO)

1. No Portainer, vá em **Stacks** > **Add Stack**

2. Escolha **Repository** e configure:
   - Repository URL: `https://github.com/oliveermarcelo/v4vision`
   - Branch: `main`
   - Compose path: `docker-compose.yml`

3. Configure as **Environment Variables**:
```
V4VISION_PORT=8585
V4VISION_DEBUG=False
V4VISION_SECRET_KEY=sua-chave-super-secreta-minimo-50-chars
V4VISION_ALLOWED_HOSTS=localhost,127.0.0.1,seudominio.com.br
V4VISION_DB_NAME=v4vision_db
V4VISION_DB_USER=v4vision_user
V4VISION_DB_PASSWORD=sua-senha-segura
V4VISION_CORS_ORIGINS=http://localhost:8585,https://seudominio.com.br
```

4. Clique em **Deploy the stack**

5. Crie o superusuário:
```bash
docker exec -it v4vision_backend python manage.py createsuperuser
```

6. Acesse:
   - Frontend: http://localhost:8585
   - Admin Django: http://localhost:8585/admin

### Deploy Manual (linha de comando)

1. Clone o repositório no servidor:
```bash
git clone <repo-url> v4vision
cd v4vision
```

2. Copie e configure o `.env`:
```bash
cp .env.example .env
nano .env
```

3. Suba os containers:
```bash
docker-compose up -d --build
```

4. Crie o superusuário:
```bash
docker exec -it v4vision_backend python manage.py createsuperuser
```

5. Acesse:
- Frontend: http://localhost
- Admin Django: http://localhost/admin

### Desenvolvimento Local

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (novo terminal)
cd frontend
npm install
npm run dev
```

## 📝 Configuração Inicial

### 1. Criar Empresa no Admin
Acesse `/admin` e crie uma Company com:
- Nome
- Slug (ex: `inpaper`, `empresa-x`)
- Logo (opcional)
- Cor primária (hex)

### 2. Criar Usuários
Crie usuários vinculados à empresa:
- **company_admin**: Pode editar dados
- **viewer**: Apenas visualiza

### 3. Popular Dados
Use o admin ou a API para adicionar:
- Vendedores
- Receitas mensais
- Estratégias
- Protocolos

## 🔐 Roles de Usuário

| Role | Permissões |
|------|------------|
| `platform_admin` | Acesso total, gerencia todas empresas |
| `company_admin` | Edita dados da sua empresa |
| `viewer` | Apenas visualiza dados |

## 📚 API Endpoints

### Autenticação
- `POST /api/auth/login/` - Login (retorna JWT)
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout

### Usuários
- `GET /api/users/me/` - Dados do usuário logado
- `PATCH /api/users/me/` - Atualizar perfil

### Dashboard
- `GET /api/receitas/retrospectiva/?ano=2025` - Dados retrospectiva
- `GET /api/receitas/comparativo_vendedores/?ano=2025` - Vendedores
- `GET /api/estrategias/` - Estratégias
- `GET /api/gestao-semanal/` - Gestão semanal
- `GET /api/protocolos/` - Protocolos

## 🐳 Comandos Docker Úteis

```bash
# Ver logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build

# Entrar no container
docker exec -it v4vision_backend bash

# Migrations
docker exec -it v4vision_backend python manage.py migrate

# Criar superusuário
docker exec -it v4vision_backend python manage.py createsuperuser

# Backup do banco
docker exec v4vision_db pg_dump -U postgres v4vision > backup.sql
```

## 📁 Estrutura do Projeto

```
v4vision/
├── backend/
│   ├── v4vision/          # Configurações Django
│   ├── core/              # Users, Companies, Auth
│   ├── dashboard/         # Módulos do dashboard
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas
│   │   ├── contexts/      # Context API (Auth)
│   │   └── services/      # API calls
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Customização

### Cores
Edite `frontend/tailwind.config.js` para alterar o tema:
```js
colors: {
  primary: {
    500: '#f97316', // Laranja padrão
  }
}
```

### Logo por Empresa
Cada empresa pode ter seu próprio logo no admin. O frontend exibe automaticamente.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato.

---

**V4Vision** - Dashboard de Performance Comercial
