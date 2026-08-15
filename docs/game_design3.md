# AstralCaos — Documento de Design (GDD)

> Documento vivo. Atualizar sempre que uma decisão nova for tomada ou algo mudar.
> Sugestão: salvar como `docs/game_design.md` dentro do repositório e versionar no git.

Última atualização: 15/08/2026 (Adicionadas fórmulas de afinidade, distribuição de pontos por level up, XP necessário por nível, e multiplicadores de raridade de equipamento)

---

## Status geral

| Sistema | Status |
|---|---|
| Personagens (jogador + NPCs) | Direções gerais + fórmulas de afinidade e progressão definidas |
| Inimigos | Direções gerais definidas |
| Combate | Direções gerais definidas |
| Equipamento | Direções gerais + fórmula de raridade definidas (runas aguardam design do Runista) |
| Mundo | Direções gerais definidas |
| Narrativa / Quests | Direções gerais definidas |
| Models (código) | Iniciado — Raça, PassivaRacial, PerfilUsuario criados no repositório novo (AstralCaos); Personagem/Classe ainda não desenhados |

---

## 1. Personagens

### Jogador
- Existe apenas **1 personagem do jogador**.
- Customizável na criação, incluindo escolha de **classe e raça**.
- Status distribuíveis (pontos para investir em atributos ao subir de nível).
- A partir de um certo nível, pode escolher uma **segunda classe** (multiclasse).

### Distribuição de pontos de status
- **5 pontos livres por nível**, mais **+1 automático no atributo principal da classe** a cada nível (ex: Guerreiro sempre +1 Força, Mago sempre +1 Inteligência) — separado dos 5 livres.
- Objetivo: manter liberdade de build sem a classe perder identidade (evita, por ex., um Mago virar tanque puro só de distribuição).
- **Atributos finais confirmados (6, estilo D&D)**: Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma.
- **Velocidade deriva de Destreza** (não é atributo próprio) — resolve a ordem de turno em Combate.
- **Sorte não existe como atributo dedicado** — decisão consciente para evitar builds de crítico que empilham atributo + skill + runa e ficam quebradas (o problema clássico do "dobro de dano garantido"). Chance de crítico vem de uma parcela pequena de Destreza, mas a build de crítico "de verdade" mora em skills e runas — investimento ativo e visível, não um atributo que qualquer build maximiza.
- Freios estruturais para crítico, para manter isso saudável mesmo com skills/runas somando: **teto de chance de crítico** (hard cap, ex: 75% — nunca garantido) e **multiplicador de crítico moderado** (x1.5, não x2).
- Ainda falta: o **teto de nível** (level cap) do jogo.

### XP necessário por nível
Fórmula reaproveitada do Django Quest (já testada):
```
XP necessário = nível × 100 + (nível − 1) × 50
```
Exemplos: nível 2 = 200 XP, nível 3 = 400 XP, nível 4 = 650 XP...

*Ponto de partida para playtest, não valor final.*

### NPCs recrutáveis
- Todos os demais personagens jogáveis são **NPCs recrutáveis**.
- Cada NPC tem **classe fixa** (definida previamente, não escolhida pelo jogador). NPCs não-recrutáveis (figurantes, vendedores, etc.) não têm classe.
- Cada NPC tem **skills próprias** — e pode aprender mais skills ao evoluir, mas a **escolha de quais skills aprender/equipar é feita pelo jogador**.
- Sobem de nível como o jogador, com status distribuíveis — **também distribuídos pelo jogador** (não automático).

### Sistema de relação/afinidade
- Pontos de afinidade por NPC, de 0 a 100, em faixas:

| Faixa | Intervalo |
|---|---|
| Estranho | 0–19 |
| Conhecido | 20–39 |
| Confiante | 40–64 |
| Aliado | 65–89 |
| Vínculo | 90–100 |

**Ganho de pontos por ação:**
- Presença em batalha junto (passivo, por batalha vencida): **+1**
- Diálogo positivo: **+3 a +5** (varia por escolha)
- Diálogo negativo: **−3 a −8**
- Presente que o NPC gosta: **+8** / presente neutro: **+2** / presente que odeia: **−10**
- Quest pessoal do NPC concluída: **+20** (salto grande)

**Carisma do jogador impacta o ganho de afinidade — para o bem e para o mal:**
```
Ganho final = ganho_base × (1 + (Carisma − 10) × 0.03)
```
Carisma 10 = neutro (sem bônus, padrão D&D). Cada ponto acima de 10 amplifica ganho **e** perda em 3% — Carisma alto acelera afinidade positiva, mas também intensifica a perda em interações negativas (suas palavras têm mais peso, positivo ou negativo).

*Todos os valores acima são ponto de partida para playtest, não finais — vale simular cenários de Carisma extremo antes de considerar fechado.*

- Cada faixa desbloqueia: diálogos extras, uma quest pessoal, e no topo (Vínculo) possivelmente uma skill exclusiva ou combo especial em batalha com o jogador. **Considerar também um item especial exclusivo desbloqueado em Vínculo**, além da skill/combo.
- Ainda falta: o que cada faixa de Vínculo desbloqueia especificamente por NPC (conteúdo, não sistema).

### Classes (7 grupos, 25 classes confirmadas)
- **Corpo-a-corpo**: Guerreiro, Bárbaro, Domador, Guardião, Duelista
- **Suporte corpo-a-corpo**: Monge, Ladino
- **À distância**: Arqueiro, Atirador, Pirata
- **Conjurador ofensivo**: Mago, Feiticeiro, Bruxo, Necromante, Invocador
- **Suportes defensivo**: Clérigo, Bardo, Alquimista, Runista
- **Suportes ofensivos**: Ilusionista, Artífice, Xamã
- **Coringas**: Druida, Cartomante, Manipulador

Ainda falta decidir se todas as 25 já entram na v1 do jogo ou se algumas ficam para depois.

### Raças (27, confirmadas)
Humano, Elfo, Anão, Halfling, Orc, Gnomo, Drow, Duergar, Dragonborn, Felino humanoide, Lobo humanoide, Fauno, Minotauro, Centauro, Construto/Golem, Genasi, Fada, Goblin, Kobold, Tiefling, Aasimar, Changeling, Vampiro jogável, Esqueleto jogável, Golias, Aarakocra, Tortle

### Bônus/passivas raciais
- Cada raça é caracterizada principalmente por **passivas de sabor** (até ~5 por raça), não por peso numérico em atributos — isso mantém as 27 raças viáveis sem explodir o trabalho de balanceamento.
- Exemplos de referência: Tortle tem casca (resistência física aumentada / pode se recolher na concha), Aarakocra voa (mobilidade/esquiva em certos terrenos), Vampiro jogável drena vida em ataques básicos, Esqueleto jogável é imune a Veneno e Sono mas vulnerável a Luz.
- Ajustes de atributo, quando existirem, devem ser pequenos (ex: +1/-1) e secundários às passivas — quem define a build é a classe; a raça é tempero e identidade visual/narrativa.
- Ainda falta: listar as passivas exatas de cada uma das 27 raças (trabalho de conteúdo, não de sistema).

### Em aberto
- Passivas raciais completas (as ~5 de cada uma das 27 raças)
- Teto de nível (level cap)
- Como a segunda classe (multiclasse) do jogador interage com atributos/bônus de classe
- O que cada faixa de Vínculo desbloqueia especificamente por NPC

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
Dois sistemas separados, porque têm complexidade diferente:

**Elementos de dano** (12, confirmados): Físico, Fogo, Água, Gelo, Ar/Vento, Terra, Grama, Metal, Raio, Luz, Escuridão, Etéreo.
- Precisam de tabela de fraqueza/resistência por inimigo — 12 elementos é mais trabalho de balanceamento que a proposta original de 8, mas é uma escolha consciente por mais profundidade de build.
- Cada inimigo pode ter **até 2 elementos** associados (ex: um inimigo pode ser Água + Gelo, ou Terra + Metal).

**Status/condições** (14, confirmados) — não têm força/fraqueza entre si (diferente dos elementos), apenas uma tabela de 3 graus por inimigo: **Normal / Vulnerável / Imune**. Isso permite variedade sem precisar de uma matriz cruzada como a dos elementos.
- **Controle** (impede ou limita ações): Paralisia, Sono, Confusão, Silêncio, Medo, Atordoamento
- **Dano contínuo / debuff** (dano ou penalidade ao longo do tempo): Veneno, Sangramento, Queimadura, Congelamento, Corrosão, Profanação, Drenagem, Enfraquecimento
- Exemplo de uso: um Golem (Terra) pode ser imune a Paralisia mas vulnerável a Sono — cada inimigo define individualmente, sem depender do elemento.
- Gancho de design futuro: status como Queimadura, Congelamento, Corrosão e Profanação combinam naturalmente com os elementos correspondentes (Fogo, Gelo, Metal, Escuridão) — habilidades elementais podem ter chance de aplicar o status combinado.
- Efeitos positivos (contrapartida): cura específica por status (ex: Antídoto cura Veneno) e buffs genéricos de suporte (Regeneração, Escudo, Fortalecimento, Haste) — lista completa fica para quando desenharmos as skills de suporte (Clérigo, Bardo, Alquimista).

Inimigos têm **fraquezas e resistências elementais** (multiplicador, ver seção 3), e resistência/imunidade/vulnerabilidade a status específicos (tabela de 3 graus).

### Em aberto
- Lista de inimigos e seus ranges de horda específicos
- Lore dos bosses
- **Criar a tabela de fraquezas e resistências elementais** (12x12) — próxima tarefa concreta de conteúdo/sistema para Inimigos

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

### Ordem de turno
- Round-robin por **Velocidade**, recalculado a cada rodada (não é ATB em tempo real).
- No início de cada rodada, todos os participantes (aliados + inimigos) são ordenados pelo valor de Velocidade.
- **Empate**: inimigos podem ter uma tag opcional **Rápido** ou **Lento**, que resolve o empate contra um personagem da party de forma coerente com a lore do inimigo (ex: um javali rápido vence o empate contra um guerreiro pesado; um golem lento perde). Inimigo sem tag (neutro) cai em desempate aleatório.
- Ainda em aberto: como resolver empate entre dois inimigos ou entre dois personagens da party (sem tag aplicável) — provavelmente aleatório nesses casos.
- Efeitos que alteram a ordem: Haste (aumenta Velocidade temporariamente), Slow (reduz), Paralisia/Sono (perde a vez).

### Fórmulas de dano
Direção definida, baseada no padrão clássico de JRPG (ataque vs defesa, com variância). Números exatos (multiplicadores, % de redução) ficam para o playtest/balanceamento — o que importa fechar agora é a fórmula em si:

**Dano físico:**
```
Dano = (ATK do atacante × multiplicador da habilidade) − (DEF do alvo × fator de redução)
Dano final = Dano × variância aleatória (ex: 90%–110%)
```

**Dano mágico:** mesma lógica, trocando ATK/DEF por Inteligência (ou Sabedoria, dependendo da classe) do atacante vs. Resistência Mágica do alvo.

**Crítico:**
- Chance de crítico vem de uma parcela pequena de Destreza como base, mas a maior parte do investimento em crítico vem de **skills e runas** (não existe atributo Sorte dedicado — ver seção 1).
- **Teto de chance de crítico**: hard cap (ex: 75%) — nunca 100% garantido.
- **Multiplicador de crítico moderado**: x1.5 (não x2) — crítico ignora uma parte da defesa do alvo.

**Defender:** reduz dano recebido em ~50% até o próximo turno do personagem.

### Como fraquezas elementais afetam o dano
Multiplicador direto sobre o dano final, com 5 níveis:

| Relação | Multiplicador |
|---|---|
| Fraqueza | x1.5 (ou x2, a testar) |
| Neutro | x1.0 |
| Resistência | x0.5 |
| Imunidade | x0 |
| Absorção | dano vira cura |

- Absorção é reservada para inimigos/status especiais, não para todo mundo — senão complica demais o balanceamento.
- O multiplicador entra depois do cálculo de dano base: `Dano final = (fórmula base) × multiplicador elemental`.

### Em aberto
- Valores exatos de multiplicadores/fator de redução de defesa nas fórmulas de dano (via playtest)
- Valor exato do teto de crítico e do bônus de Destreza na chance base (dentro dos limites já definidos: cap ~75%, multiplicador x1.5)
- Desempate de Velocidade quando não há tag aplicável (inimigo x inimigo, aliado x aliado)

---

## 4. Equipamento

- Sistema de inventário com **vários tipos de equipamento**: armas, armaduras, amuletos, etc.
- Equipamento pode ser **trocado durante o combate**.
- **Sistema de runas**: equipamentos têm slots onde runas podem ser encaixadas/removidas.

### Efeitos das runas
Direção geral definida (categorias abaixo) — mas o aprofundamento fica para quando desenharmos a classe **Runista**, já que ela tem envolvimento direto e provavelmente vai expandir/especializar esse sistema.

- **Runas de atributo**: bônus flat ou percentual em um atributo (ex: +5 Força, +3% Inteligência).
- **Runas elementais**: adicionam dano de um elemento ao ataque, ou dão resistência/imunidade a um elemento (conecta com os 12 elementos de Inimigos).
- **Runas de status**: chance de aplicar um status ao acertar, ou resistência/imunidade a um status específico (conecta com os 14 status de Inimigos).
- **Runas de combate**: efeitos situacionais — chance de crítico, roubo de vida, redução de custo de mana, etc.

### Raridade de equipamentos e runas
5 níveis, com multiplicador sobre os stats base do item:

| Raridade | Cor sugerida | Multiplicador de stats | Slots de runa |
|---|---|---|---|
| Comum | Branco/Cinza | x1.0 | 0–1 |
| Incomum | Verde | x1.2 | 1–2 |
| Raro | Azul | x1.5 | 2–3 |
| Épico | Roxo | x1.8 | 3 |
| Lendário | Dourado/Laranja | x2.2 | 3–4 |

*Ponto de partida para playtest — o salto de Épico para Lendário pode ser ampliado (ex: x2.5) se a intenção for Lendário parecer mais excepcional.*

- Runas têm raridade própria, independente da raridade do equipamento em que são encaixadas (uma runa Lendária dá efeito mais forte que uma Comum).

### Como equipamento é obtido
- **Loot**: principal fonte de equipamento aleatório/raro — inimigos e bosses dropam, com chance maior de raridade alta em bosses.
- **Loja**: fonte confiável de Comum/Incomum, e principal fonte de compra de runas.
- **Crafting**: considerar para depois — sistema grande por si só (materiais, receitas), não é pendência bloqueante para a v1.

### Em aberto
- Aprofundar efeitos de runas junto com o design da classe Runista

---

## 5. Mundo

- Mapa mundo com **cidades, reinos e regiões**.
- **Lojas** para compra de itens/equipamentos.

### Navegação do mapa
- Mapa mundo em **ícones conectados por rotas** (estilo JRPG clássico), não mundo aberto livre — combina melhor com o combate por turnos.
- Para ir de uma região a outra pela primeira vez, é necessário **atravessar a rota**, com um número de combates pelo caminho.
- Depois de já ter atravessado (por número de vezes, ou nível mínimo — a definir), a rota libera **viagem rápida** direto entre os pontos, sem combates — só que sem ganhos (sem XP/loot) nessa viagem rápida, já que ela é conveniência, não farm.
- Dentro de cada cidade, uma opção separada leva a uma **área de combates daquela cidade** (masmorra/dungeon local), fora do mapa mundo.

### Lojas
- Estoque base (consumíveis comuns) + estoque regional (equipamento/runas temáticos da região, ex: região gélida vende itens de elemento Gelo com mais frequência).
- Estoque escala com progresso: regiões desbloqueadas mais tarde vendem raridade mais alta.
- Tipos de loja especializados: Ferreiro (armas/armaduras), Runista/Arcanista (runas), Boticário (consumíveis) — além de **pontos para aprender novas magias/skills**, que também entram nesse sistema de "loja"/estabelecimento.

### Como regiões se desbloqueiam
- Majoritariamente por **progresso da quest principal** (avançar a história libera a próxima região).
- Regiões opcionais/secretas podem ter gate adicional por **nível mínimo** ou **item específico** (chave, mapa) — bom para conteúdo end-game ou side content.
- Nível não deve ser o gate primário de história, só filtro de dificuldade/conteúdo opcional.

### Em aberto
- Definir o número exato de combates/nível necessário para uma rota liberar viagem rápida
- Revisitar o projeto djangoquest (referência inicial) para puxar decisões específicas de mapa/exploração
- Lista completa do que cada tipo de loja vende, região por região (conteúdo)

---

## 6. Narrativa e Quests

- Sem estrutura de capítulos fixos.
- Progressão da lore via **sistema de quests**:
  - **Quests principais**: avançam a história geral do jogo.
  - **Quests de NPC**: pessoais de cada NPC recrutável, aprofundam a relação/afinidade e podem desbloquear conteúdo daquele personagem.

### Estrutura de uma quest
- **Objetivo**: o que precisa ser feito
- **Recompensa**: o que o jogador ganha ao completar
- **Requisito para completar**: condição de conclusão
- **Requisito para receber/desbloquear**: condição para a quest ficar disponível para o jogador

### Como quests principais e de NPC se cruzam
- Quest de NPC desbloqueia por combinação de: NPC recrutado + afinidade mínima (faixa Confiante/Aliado) + progresso mínimo da main.
- Quests de NPC podem alterar a main de forma leve (cena extra, diálogo especial, aliado presente num momento-chave) se a afinidade estiver alta — sem ramificar o final ou o rumo geral da história.
- Quests de NPC nunca travam a progressão da main — são sempre opcionais/paralelas.

### Sistema de diálogos
- Direção enxuta para a v1: árvore simples, NPC fala e jogador escolhe entre 2-4 respostas.
- Cada escolha pode ter um destes efeitos: puramente de sabor, +/- afinidade com o NPC presente, ou desbloqueio/flag de quest.
- Sem moralidade global nem múltiplos finais por escolha — impacto fica contido em afinidade e quests, não ramifica a narrativa principal.

### Requisitos de quest (vocabulário base)
**Requisito para receber/desbloquear** (combinável via AND):
- Progresso de main (quest X completa ou capítulo/ponto Y)
- Nível mínimo do jogador
- Afinidade mínima com um NPC específico
- Item no inventário (chave, carta, objeto de quest anterior)
- Região desbloqueada

**Requisito para completar**: derrotar inimigo/boss específico, entregar item, chegar em local, ou falar com NPC (trigger de diálogo).

### Em aberto
- Detalhar exemplos concretos de quests (principais e de NPC) usando esse vocabulário, conforme a lore for sendo escrita

---

## 7. Conta / Usuário (fora do escopo de lore — infraestrutura)

- Usa o `User` padrão do Django para autenticação (username, senha, email).
- `PerfilUsuario` como perfil estendido, ligado via `OneToOneField` — hoje só guarda `data_criacao`.
- Suporta **múltiplos personagens por usuário** (resolvido pela relação `Personagem → User` via `ForeignKey`, não por campo especial no perfil).
- Conquistas/achievements: planejado, mas só depois.
- Configurações (idioma, notificação): só pós-jogo finalizado.
- Sem moeda real/monetização — exceto, possivelmente, venda de cosméticos no futuro.

---

## Próximos passos sugeridos

1. Detalhar cada seção "Em aberto" acima, sistema por sistema.
2. Continuar os models Django do sistema de Personagens (Classe, Personagem) no repositório novo (AstralCaos) — Raça, PassivaRacial e PerfilUsuario já estão feitos.
3. Manter este documento atualizado a cada decisão nova.
