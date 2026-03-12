# Documentação - VRG Transport API License

Índice completo da documentação do projeto.

## Índice

### Uso da API

- **[API - Endpoints e Exemplos](api.md)**  
  Documentação completa dos endpoints, exemplos de requisições e respostas.

- **[Validações](validacoes.md)**  
  Regras de validação do schema Student, autenticação e tratamento de erros.

### Estrutura e Configuração

- **[Estrutura do Projeto](estrutura.md)**  
  Organização de diretórios e responsabilidades de cada módulo.

- **[Configuração](configuracao.md)**  
  Setup de template, fontes, Docker e variáveis de ambiente.

### Desenvolvimento

- **[Testes](testes.md)**  
  Suite completa de testes com pytest: 29 testes, 100% de cobertura.

- **[Padrão de Commits](padrao-commits.md)**  
  Convenções para mensagens de commit.

## Ferramentas Auxiliares

Localizadas em `tools/docs/`:

- **[Preview](../tools/docs/preview.md)** - Visualizar carteirinha gerada
- **[Test API](../tools/docs/test_api.md)** - Teste interativo da API
- **[Map Fields](../tools/docs/map_fields.md)** - Mapeamento de campos

## Status do Projeto

| Aspecto | Status |
|---------|--------|
| Cobertura de Testes | 100% |
| Total de Testes | 29 |
| Validações | Implementadas |
| Documentação API | Completa |
| Docker | Configurado |

## Links Rápidos

### Para Desenvolvedores

1. **Começando:** [Estrutura do Projeto](estrutura.md)
2. **Rodando Testes:** [Documentação de Testes](testes.md)
3. **Entendendo Validações:** [Validações](validacoes.md)

### Para Integração

1. **Usando a API:** [Documentação de API](api.md)
2. **Validando Dados:** [Validações](validacoes.md)
3. **Testando Localmente:** [Tools - Test API](../tools/docs/test_api.md)

### Para Deploy

1. **Configuração:** [Configuração](configuracao.md)
2. **Docker:** Ver [README principal](../README.md)
3. **Variáveis de Ambiente:** [Configuração](configuracao.md)

## Histórico de Atualizações

### 2026-03-12: Validações e Testes

- Adicionado `Field(min_length=1)` em todos os campos obrigatórios
- Suite completa de testes com pytest
- 100% de cobertura de código
- Documentação de validações e testes

### Anterior

- API básica de geração de carteirinhas
- Documentação de API e estrutura
- Ferramentas auxiliares (preview, test, map)
- Docker e configuração

## Contribuindo

Ao contribuir com o projeto:

1. Leia [Padrão de Commits](padrao-commits.md)
2. Execute testes: `pytest`
3. Mantenha cobertura em 100%
4. Atualize documentação relevante
5. Adicione testes para novas funcionalidades

## Suporte

Para dúvidas sobre:

- **Uso da API:** Ver [api.md](api.md)
- **Validações:** Ver [validacoes.md](validacoes.md)
- **Testes:** Ver [testes.md](testes.md)
- **Configuração:** Ver [configuracao.md](configuracao.md)
