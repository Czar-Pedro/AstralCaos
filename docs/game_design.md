# AstralCaos — Documento de Design (GDD)

> Documento vivo. Atualizar sempre que uma decisão nova for tomada ou algo mudar.
> Sugestão: salvar como `docs/game_design.md` dentro do repositório e versionar no git.

Última atualização: 14/08/2026

---

## Status geral

| Sistema | Status |
|---|---|
| Personagens (jogador + NPCs) | Definido em geral |
| Inimigos | Definido em geral |
| Combate | Definido em geral |
| Equipamento | Definido em geral |
| Mundo | Definido em geral |
| Narrativa / Quests | Definido em geral |
| Models (código) | Não iniciado |

---

## 1. Personagens

### Jogador
- Existe apenas **1 personagem do jogador**.
- Customizável na criação.
- Status distribuíveis (pontos para investir em atributos ao subir de nível).
- A partir de um certo nível, pode escolher uma **segunda classe** (multiclasse).

### NPCs recrutáveis
- Todos os demais personagens jogáveis são **NPCs recrutáveis**.
- Cada NPC tem **classe fixa** (definida previamente, não escolhida pelo jogador).
- Cada NPC tem **skills próprias** — e pode aprender mais skills ao evoluir.
- Sobem de nível como o jogador, com status distribuíveis.
- **Sistema de relação/afinidade** entre jogador e cada NPC (a ser detalhado — provavelmente afeta desbloqueio de quests pessoais, diálogos, etc.)

### Em aberto
- Como funciona a distribuição de pontos de status (livre? por classe?)
- Lista de classes disponíveis
- Como a afinidade/relação evolui (ações, presentes, diálogos, quests?)

---

## 2. Inimigos

### Tiers
- 3 tiers de inimigos comuns: **fraco, médio, difícil**.
- Cada inimigo individual define seu **próprio range de quantidade** numa horda (não é uma regra global de tier — é definido inimigo a inimigo).
  - Exemplo: um inimigo difícil pode ter horda de 1 a 5; um inimigo fraco pode ter horda de 0 a 10; mas isso varia por inimigo.

### Chefes (bosses)
- Separados dos tiers comuns.
- Aparecem sozinhos ou em pequenos grupos ligados à lore (ex: dois dragões juntos numa luta específica).

### Elementos e dano
- Sistema de **tipos de dano / elementos**.
- Inimigos têm **fraquezas e resistências elementais**.

### Em aberto
- Lista de elementos (fogo, gelo, etc.)
- Lista de inimigos e seus ranges de horda específicos
- Lore dos bosses

---

## 3. Combate

### Formato
- RPG por turnos, estilo Final Fantasy clássico.
- Grupo do jogador: até **4 aliados** em batalha (dentre jogador + NPCs recrutados).
- Horda de inimigos: até **10 inimigos** (variando por composição, ver seção 2).
- **Ataque mirado**: jogador escolhe o alvo específico dentro da horda.

### Ações disponíveis em batalha
- Ataque físico
- Magia
- Habilidade especial
- Item usável
- Defender
- Fugir

### Em aberto
- Ordem de turno (baseada em velocidade/atributo?)
- Fórmulas de dano (físico, mágico, crítico, defesa)
- Como fraquezas elementais afetam o dano

---

## 4. Equipamento

- Sistema de inventário com **vários tipos de equipamento**: armas, armaduras, amuletos, etc.
- Equipamento pode ser **trocado durante o combate**.
- **Sistema de runas**: equipamentos têm slots onde runas podem ser encaixadas/removidas.

### Em aberto
- Efeitos que runas concedem
- Raridade de equipamentos/runas
- Como equipamento é obtido (loot, loja, crafting?)

---

## 5. Mundo

- Mapa mundo com **cidades, reinos e regiões**.
- **Lojas** para compra de itens/equipamentos.
- Sem sistema de exploração livre estilo mundo aberto definido ainda (referência inicial: similar ao projeto anterior djangoquest, a detalhar).

### Em aberto
- Como o mapa é navegado (grid, pontos de viagem, mundo aberto?)
- O que cada loja vende e como varia por região
- Como regiões se desbloqueiam

---

## 6. Narrativa e Quests

- Sem estrutura de capítulos fixos.
- Progressão da lore via **sistema de quests**:
  - **Quests principais**: avançam a história geral do jogo.
  - **Quests de NPC**: pessoais de cada NPC recrutável, aprofundam a relação/afinidade e podem desbloquear conteúdo daquele personagem.

### Em aberto
- Estrutura de uma quest (objetivo, status, recompensa, pré-requisitos)
- Como quests principais e de NPC se cruzam
- Sistema de diálogos

---

## Próximos passos sugeridos

1. Detalhar cada seção "Em aberto" acima, sistema por sistema.
2. Só depois de fechar os detalhes, desenhar os **models Django** de cada sistema (Character, Enemy, Battle, Equipment, Rune, Quest, etc.)
3. Manter este documento atualizado a cada decisão nova.
