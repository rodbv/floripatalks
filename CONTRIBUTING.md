# Contribuindo para FloripaTalks

[![Unit Tests](https://github.com/rodbv/floripatalks/actions/workflows/test.yml/badge.svg)](https://github.com/rodbv/floripatalks/actions/workflows/test.yml)

Muito obrigado por querer contribuir com o FloripaTalks! Siga as orientações abaixo para garantir que sua contribuição seja bem-vinda e fácil de revisar.

## 🚀 Como Contribuir

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

## 🛠️ Ambiente de Desenvolvimento

- Python 3.12+
- uv (gerenciador de pacotes Python)
- Django 5.2.4

### Comandos Úteis (Justfile)

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

## 🌍 Internacionalização (i18n)

O FloripaTalks já está preparado para múltiplos idiomas, com o português brasileiro como padrão. Para adicionar ou atualizar traduções:

1. Marque todos os textos do código Python com `gettext_lazy as _`:
   ```python
   from django.utils.translation import gettext_lazy as _
   nome = models.CharField(_("Nome"), max_length=100)
   ```
   E nos templates:
   ```django
   {% load i18n %}
   <h1>{% trans "Bem-vindo" %}</h1>
   ```
2. Gere os arquivos de tradução:
   ```sh
   django-admin makemessages -l pt_BR
   ```
3. Edite o arquivo gerado em `locale/pt_BR/LC_MESSAGES/django.po` e adicione suas traduções:
   ```
   msgid "Date of birth"
   msgstr "Data de nascimento"
   ```
4. Compile as traduções:
   ```sh
   django-admin compilemessages
   ```
5. Para adicionar outro idioma, repita o processo com o código do novo idioma (ex: `en` para inglês).

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
