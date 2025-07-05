# 🎤 FloripaTalks

FloripaTalks é uma plataforma open source criada para facilitar a sugestão, votação e organização de tópicos de palestras nos eventos da comunidade Python Floripa. Com uma interface simples e colaborativa, qualquer pessoa pode propor novos temas, votar nos tópicos que gostaria de ver no evento e se voluntariar para palestrar — ou indicar alguém da comunidade para compartilhar conhecimento.

O projeto foi desenvolvido usando Django e HTMX, garantindo robustez no backend e uma experiência dinâmica no frontend.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)

## 🚀 Funcionalidades

- **Sugestão de tópicos**: Qualquer participante pode sugerir novos temas para as próximas edições dos eventos
- **Votação**: Os usuários podem votar nos tópicos que mais têm interesse em assistir
- **Voluntariado**: É possível se inscrever para palestrar sobre um tema ou indicar outra pessoa da comunidade
- **Compartilhamento**: Compartilhe sugestões de palestras facilmente para engajar mais pessoas
- **Transparência**: Todas as sugestões, votos e voluntariados ficam visíveis para a comunidade, promovendo um processo aberto e democrático

## 🎯 Objetivo

O FloripaTalks nasceu para tornar o processo de escolha de palestras mais participativo, transparente e inclusivo, fortalecendo o espírito colaborativo da comunidade Python Floripa. Queremos incentivar a troca de ideias, dar voz a todos os membros e facilitar a organização dos eventos.

## 🛠️ Stack Tecnológica

- **Backend**: Django 5.2.4
- **Frontend**: HTMX para interações dinâmicas
- **Autenticação**: django-allauth com Google OAuth
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL pronto
- **Gerenciador de Pacotes**: uv
- **Desenvolvimento**: django-extensions, ipdb

## 📋 Pré-requisitos

- Python 3.12+
- uv (gerenciador de pacotes Python)
- Credenciais Google OAuth (para login social)

## 🚀 Início Rápido

### 1. Clone o Repositório
```bash
git clone <url-do-seu-repositorio>
cd floripatalks
```

### 2. Instale as Dependências
```bash
uv sync
```

### 3. Configure as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Execute as Migrações do Banco
```bash
uv run python manage.py migrate
```

### 5. Crie um Superusuário
```bash
uv run python manage.py createsuperuser
```

### 6. Configure o Google OAuth (Opcional)
1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie credenciais OAuth 2.0
3. Adicione a URI de redirecionamento: `http://localhost:8000/accounts/google/login/callback/`
4. No admin do Django, crie uma Aplicação Social com suas credenciais do Google

### 7. Inicie o Servidor de Desenvolvimento
```bash
uv run python manage.py runserver
```

Acesse `http://localhost:8000` para ver a aplicação!

## 🛠️ Desenvolvimento

### Usando o Justfile
Este projeto inclui um `justfile` com comandos Django comuns:

```bash
# Iniciar servidor de desenvolvimento
just run

# Servidor de desenvolvimento básico
just dev

# Shell Django com todos os modelos pré-carregados
just shell

# Criar superusuário
just superuser

# Criar e aplicar migrações
just makemigrations
just migrate

# Executar testes
just test

# Verificar problemas
just check
```

### Comandos Disponíveis
- `just run` - Iniciar servidor Django aprimorado com django-extensions
- `just dev` - Iniciar servidor Django básico
- `just shell` - Shell Django com todos os modelos pré-carregados
- `just superuser` - Criar usuário admin
- `just migrate` - Aplicar migrações do banco
- `just check` - Verificar problemas do Django
- `just clean` - Limpar arquivos de cache Python

## 🔧 Configuração

### Variáveis de Ambiente
As seguintes variáveis de ambiente podem ser definidas no seu arquivo `.env`:

- `DJANGO_SECRET_KEY` - Chave secreta do Django (obrigatória)
- `DJANGO_DEBUG` - Modo debug (True/False)
- `DJANGO_ALLOWED_HOSTS` - Lista separada por vírgulas de hosts permitidos

### Configuração do Google OAuth
1. Crie um projeto no Google Cloud Console
2. Ative a API Google+
3. Crie credenciais OAuth 2.0
4. Adicione URIs de redirecionamento para seus domínios
5. Crie uma Aplicação Social no admin do Django

## 🔒 Segurança

- Todos os segredos são armazenados em variáveis de ambiente
- Arquivo `.env` está no .gitignore
- Credenciais Google OAuth são armazenadas com segurança
- Proteção CSRF habilitada
- Validação segura de senhas

## 🤝 Como Contribuir

Este projeto é open source e toda contribuição é muito bem-vinda!

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Diretrizes de Contribuição
- Mantenha o código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções de código do projeto
- Atualize a documentação quando necessário

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Consulte a [documentação do Django](https://docs.djangoproject.com/)
2. Revise a [documentação do django-allauth](https://django-allauth.readthedocs.io/)
3. Abra uma issue neste repositório

---

**Desenvolvido com ❤️ para a comunidade Python Floripa**
