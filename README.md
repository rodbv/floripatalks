# FloripaTalks

Plataforma web para gerenciar tópicos de palestras para eventos locais, permitindo que a comunidade vote, comente e sugira apresentadores.

## Sobre o Projeto

FloripaTalks é uma aplicação web mobile-first desenvolvida para apoiar eventos locais, começando com o "Python Floripa". A plataforma permite que usuários:

- Visualizem tópicos de palestras sugeridos para eventos futuros
- Votem e comentem em tópicos de interesse
- Adicionem novos tópicos
- Sugiram apresentadores para tópicos específicos

## Tecnologias

- **Backend**: Django
- **Frontend**: HTMX + Django-Cotton (componentes)
- **CSS**: Pure CSS
- **Testes**: pytest (TDD)
- **Gerenciamento de Dependências**: uv
- **Automação**: justfile
- **CI/CD**: GitHub Actions
- **Pre-commit**: Ferramentas baseadas em Rust

## Gerenciamento de Dependências

Este projeto usa `uv` para gerenciar dependências. O arquivo `requirements.txt` é mantido no controle de versão para compatibilidade com plataformas de deploy (como Azure App Service).

### Adicionando ou Removendo Dependências

Quando você adicionar ou remover dependências, siga estes passos:

1. **Adicionar uma dependência:**
   ```bash
   uv add nome-do-pacote
   just update-requirements  # Regenera requirements.txt
   git add uv.lock requirements.txt
   git commit -m "chore: add nome-do-pacote"
   ```

2. **Remover uma dependência:**
   ```bash
   uv remove nome-do-pacote
   just update-requirements  # Regenera requirements.txt
   git add uv.lock requirements.txt
   git commit -m "chore: remove nome-do-pacote"
   ```

**Importante**: Sempre execute `just update-requirements` após modificar dependências para manter `requirements.txt` sincronizado com `uv.lock`. Ambos os arquivos devem ser commitados juntos.

## Experimentação com SpecKit

Este projeto é um experimento utilizando o [SpecKit](https://github.com/github/spec-kit), uma ferramenta para desenvolvimento orientado por especificações (Spec-Driven Development). O SpecKit ajuda a manter especificações claras, planos de implementação estruturados e documentação alinhada com o código.

📖 **Documentação**: Veja o [Guia de Uso do SpecKit](docs/speckit-guide.md) para aprender como usar o SpecKit neste projeto.

## Status do Projeto

🚧 **Em desenvolvimento** - Este projeto está em fase inicial de desenvolvimento.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Código de Conduta

Este projeto adere ao [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). Ao participar, você concorda em manter este código.

## Contribuindo

Contribuições são bem-vindas! Por favor, leia o Código de Conduta antes de contribuir.

---

**Nota**: Este é um projeto experimental em desenvolvimento ativo. A documentação e funcionalidades podem mudar.
