# TaskTracker CLI

Uma ferramenta de linha de comando para gerenciar suas tarefas do dia a dia. Acompanhe o que precisa fazer, o que está em andamento e o que já foi concluído — tudo pelo terminal.

---

## Funcionalidades

- Adicionar tarefas com descrição
- Atualizar a descrição de uma tarefa existente
- Deletar tarefas
- Marcar tarefas como **em progresso** ou **concluída**
- Listar todas as tarefas ou filtrar por status
- Persistência local em arquivo `tasks.json`

---

## Requisitos

- Python 3.12+

---

## Instalação

Clone o repositório e acesse o diretório:

```bash
git clone git@github.com:EberteSampaio/TaskTracker.git
cd TaskTracker
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
python -m venv .venv             # WSL
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

---

## Uso

O ponto de entrada é o arquivo `task-cli.py`. Todos os comandos são passados como argumentos posicionais.

### Adicionar uma tarefa

```bash
python task-cli.py add "Comprar mantimentos"
# Output: Task added successfully (ID: 1)
```

### Atualizar uma tarefa

```bash
python task-cli.py update <id> "Nova descrição da tarefa"
```

### Deletar uma tarefa

```bash
python task-cli.py delete <id>
```

### Marcar como em progresso

```bash
python task-cli.py mark-in-progress <id>
```

### Marcar como concluída

```bash
python task-cli.py mark-done <id>
```

### Listar tarefas

```bash
# Listar todas
python task-cli.py list

# Filtrar por status
python task-cli.py list todo
python task-cli.py list in-progress
python task-cli.py list done
```

### Comandos resumidos

| Comando              | Descrição                              |
|----------------------|----------------------------------------|
| `add <desc>`         | Adiciona uma nova tarefa               |
| `update <id> <desc>` | Atualiza descrição de uma tarefa       |
| `delete <id>`        | Remove uma tarefa                      |
| `list [status]`      | Lista tarefas (com filtro opcional)    |
| `mark-in-progress <id>` | Marca uma tarefa como em progresso  |
| `mark-done <id>`     | Marca uma tarefa como concluída        |

---

## Estrutura do Projeto

```
TaskTracker/
├── task-cli.py                  # Ponto de entrada da aplicação
├── tasks.json                   # Armazenamento local das tarefas
└── src/
    └── task/
        ├── task.py              # Modelo Task e enum TaskStatus
        ├── commands.py          # Padrão Command (ICommand + implementações)
        ├── repository.py        # Padrão Repository (interface + JsonTaskRepository)
        └── exceptions/
            └── exceptions.py    # Exceções de domínio
```

### Decisões de arquitetura

- **Command Pattern** — cada operação (`add`, `update`, `delete`, etc.) é encapsulada em sua própria classe, isolando responsabilidades e facilitando extensão.
- **Repository Pattern** — a camada de acesso a dados é abstraída atrás de `ITaskRepository`, permitindo trocar o mecanismo de persistência (JSON, banco de dados, etc.) sem alterar a lógica de negócio.
- **Domain Exceptions** — erros esperados (tarefa não encontrada, comando inválido) sobem como exceções de domínio tipadas, tratadas no ponto de entrada sem vazar detalhes internos.

---

## Status das tarefas

| Status        | Descrição                        |
|---------------|----------------------------------|
| `todo`        | Tarefa criada, ainda não iniciada |
| `in-progress` | Tarefa em andamento               |
| `done`        | Tarefa concluída                  |

---

## Exemplo de `tasks.json`

```json
[
    {
        "id": 1,
        "description": "Comprar mantimentos",
        "status": "in-progress",
        "created_at": "2026-06-04T10:00:00",
        "updated_at": "2026-06-04T11:30:00"
    }
]
```

---

## Inspiração

Projeto baseado no desafio [Task Tracker](https://roadmap.sh/projects/task-tracker) do roadmap.sh.
