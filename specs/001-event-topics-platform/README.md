# Event Topics Platform - Documentação

Esta pasta contém toda a documentação de especificação, planejamento e implementação da feature "Event Topics Platform" (FloripaTalks).

## 📖 Ordem de Leitura Recomendada

Leia os documentos nesta ordem para entender completamente a feature:

### 1. `quickstart.md` - Visão Geral e Cenários de Teste
**Comece aqui!** Visão geral rápida da feature, cenários de teste e validação. Ideal para entender rapidamente o que o sistema faz.

### 2. `spec.md` - Especificação Funcional
**O que fazer?** Contém:
- User stories com prioridades (P1, P2, P3)
- Requisitos funcionais e não-funcionais
- Entidades principais
- Critérios de sucesso
- Casos extremos

### 3. `plan.md` - Plano Técnico de Implementação
**Como fazer?** Contém:
- Stack tecnológico (Django, HTMX, AlpineJS, etc.)
- Estrutura do projeto
- Arquitetura (use cases, services, DTOs)
- Verificação de conformidade com a constituição
- Fases de implementação

### 4. `research.md` - Decisões Técnicas e Pesquisas
**Por que essas escolhas?** Documenta:
- Decisões técnicas tomadas
- Alternativas consideradas e rejeitadas
- Justificativas para cada escolha tecnológica
- Padrões e melhores práticas adotadas

### 5. `data-model.md` - Modelo de Dados
**Estrutura dos dados.** Contém:
- Entidades do sistema (Event, Topic, User, etc.)
- Relacionamentos entre entidades
- Campos e tipos de dados
- Índices e otimizações
- Soft delete e campos de auditoria

### 6. `tasks.md` - Tarefas de Implementação
**Execução prática.** Contém:
- Lista completa de tarefas ordenadas por dependências
- Organizadas por fases (Setup, Foundational, User Stories)
- Cada tarefa com ID, prioridade e descrição
- Ordem de execução e dependências entre tarefas

## 📁 Estrutura de Pastas

```
001-event-topics-platform/
├── README.md              ← Você está aqui
├── quickstart.md          ← Comece aqui
├── spec.md                ← Especificação
├── plan.md                ← Plano técnico
├── research.md            ← Decisões técnicas
├── data-model.md          ← Modelo de dados
├── tasks.md               ← Tarefas
├── contracts/             ← Contratos HTMX (endpoints)
└── checklists/            ← Checklists de validação
```

## 🔗 Relacionamento entre Documentos

```
quickstart.md
    ↓ (valida)
spec.md
    ↓ (implementa)
plan.md
    ↓ (justifica)
research.md
    ↓ (estrutura)
data-model.md
    ↓ (executa)
tasks.md
```

## 📝 Notas

- **Nomes dos arquivos**: Mantidos como `spec.md`, `plan.md`, etc. para compatibilidade com scripts do SpecKit
- **Ordem numérica**: Use este README como guia de leitura
- **Atualizações**: Quando um documento é atualizado, verifique se os documentos dependentes precisam ser revisados

## 🎯 Para Desenvolvedores

Se você está começando a trabalhar nesta feature:
1. Leia `quickstart.md` para entender o contexto
2. Leia `spec.md` para entender os requisitos
3. Leia `plan.md` para entender a arquitetura
4. Consulte `tasks.md` para ver o que precisa ser feito
5. Use `data-model.md` como referência durante implementação
