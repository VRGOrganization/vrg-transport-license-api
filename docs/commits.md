# Padrão de Commits

## Objetivo

Padronizar as mensagens de commit para manter o histórico organizado, compreensível e consistente entre os membros da equipe.

## Estrutura

Formato obrigatório:

tipo: descrição curta no imperativo

Exemplos:
```
feat: adiciona validação no cadastro de usuário
fix: corrige erro ao salvar cliente sem telefone
refactor: reorganiza estrutura de serviços

```

## Tipos Permitidos

| Tipo     | Uso |
|----------|------|
| feat     | Nova funcionalidade |
| fix      | Correção de bug |
| refactor | Alteração interna sem mudar comportamento externo |
| docs     | Documentação |
| style    | Formatação e ajustes de estilo |
| test     | Criação ou alteração de testes |
| chore    | Configurações, dependências ou tarefas técnicas |

## Regras

- Utilizar verbo no imperativo (ex: adiciona, corrige, remove).
- Ser claro e objetivo.
- Um commit deve conter apenas uma responsabilidade.
- As mensagens devem ser escritas em português.
- Não misturar idiomas.

## Escopo (Opcional)

Pode ser utilizado para indicar a área afetada:

tipo(escopo): descrição

Exemplos:
```
feat(auth): adiciona validação de token
fix(api): corrige retorno incorreto de status HTTP

```

Última atualização: 04/03/2026