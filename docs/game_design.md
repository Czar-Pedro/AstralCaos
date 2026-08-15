# AstralCaos — Documento de Design (GDD)

> Documento vivo. Atualizar sempre que uma decisão nova for tomada ou algo mudar.
> Sugestão: salvar como `docs/game_design.md` dentro do repositório e versionar no git.

Última atualização: 15/08/2026 (Adicionado orçamento de pontos para bônus de atributo racial: 5 pontos líquidos, teto +4/-2 por atributo)

---

## Status geral

| Sistema | Status |
|---|---|
| Personagens (jogador + NPCs) | Direções gerais + fórmulas de afinidade, progressão e bônus racial definidas |
| Inimigos | Direções gerais definidas |
| Combate | Direções gerais definidas |
| Equipamento | Direções gerais + fórmula de raridade definidas (runas aguardam design do Runista) |
| Mundo | Direções gerais definidas |
| Narrativa / Quests | Direções gerais definidas |
| Models (código) | Iniciado — Raça, PassivaRacial, PerfilUsuario criados no repositório (AstralCaos); Personagem/Classe ainda não desenhados |

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

### Diálogos e afinidade — como isso vira código (não if/else por linha)
- Diálogo e afinidade são modelados como **dados**, não como condicionais no código. O padrão já usado em `Raca` → `PassivaRacial` (tabela "pai" + tabela "filha") se repete aqui: um model `Dialogo` (ligado a um NPC/cena) e um model `OpcaoDialogo` (as respostas possíveis, cada uma com `texto` e `ganho_afinidade`).
- Uma única função genérica processa qualquer diálogo/opção: lê o `ganho_afinidade` da opção escolhida, aplica a fórmula de Carisma, salva. Nunca há lógica por texto específico.
- Consequência: escrever diálogo novo vira trabalho de conteúdo (preencher registros no admin), não trabalho de programação.
- Ainda não iniciado — retomar quando formos desenhar os models de Diálogo.

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
- Cada raça é caracterizada principalmente por **passivas de sabor** (até ~5 por raça) — isso mantém as 27 raças viáveis sem explodir o trabalho de balanceamento.
- Exemplos de referência: Tortle tem casca (resistência física aumentada / pode se recolher na concha), Aarakocra voa (mobilidade/esquiva em certos terrenos), Vampiro jogável drena vida em ataques básicos, Esqueleto jogável é imune a Veneno e Sono mas vulnerável a Luz.
- Ainda falta: listar as passivas exatas de cada uma das 27 raças (trabalho de conteúdo, não de sistema).

### Bônus de atributo racial (orçamento de pontos)
- Cada raça tem um **orçamento líquido de 5 pontos** para distribuir entre os 6 atributos.
- Pontos negativos "compram" orçamento extra: o líquido (soma dos positivos menos soma dos negativos) é sempre 5.
- **Teto por atributo**: máximo **+4** em um único atributo, máximo **-2** em um único atributo.
- Exemplos:
  - Orc: +3 Força, +2 Constituição (sem negativo, líquido 5)
  - Tortle: +2 Constituição, +3 Sabedoria, +1 Carisma, -1 Destreza (bruto +6, líquido 6-1=5)
  - Raça "rígida" tipo Construto/Golem: +3 Força, +2 Constituição, +2 extra via negativo, -2 Carisma (bruto +7, líquido 7-2=5)
- Já implementado em código: `Raca` no `core/models.py` tem os 6 campos de bônus (`bonus_for`, `bonus_dex`, `bonus_con`, `bonus_int`, `bonus_sab`, `bonus_car`) — a regra de orçamento/teto acima é uma diretriz de preenchimento de dados, não uma validação obrigatória no model por enquanto.

### Em aberto
- Passivas raciais completas (as ~5 de cada uma das 27 raças)
- Preencher os 6 bônus de atributo de cada uma das 27 raças, respeitando orçamento de 5 líquidos e teto +4/-2
- Teto de nível (level cap)
- Como a segunda classe (multiclasse) do jogador interage com atributos/bônus de classe
- O que cada faixa de Vínculo desbloqueia especificamente por NPC
- Models de Diálogo/OpcaoDialogo

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
- Precisam de tabela de fraqueza/resistência por inimigo.
- Cada inimigo pode ter **até 2 elementos** associados (ex: um inimigo pode ser Água + Gelo, ou Terra + Metal).

**Status/condições** (14, confirmados) — não têm força/fraqueza entre si, apenas uma tabela de 3 graus por inimigo: **Normal / Vulnerável / Imune**.
- **Controle**: Paralisia, Sono, Confusão, Silêncio, Medo, Atordoamento
- **Dano contínuo / debuff**: Veneno, Sangramento, Queimadura, Congelamento, Corrosão, Profanação, Drenagem, Enfraquecimento
- Exemplo: um Golem (Terra) pode ser imune a Paralisia mas vulnerável a Sono — cada inimigo define individualmente, sem depender do elemento.
- Gancho de design futuro: status como Queimadura, Congelamento, Corrosão e Profanação combinam com os elementos correspondentes (Fogo, Gelo, Metal, Escuridão).
- Efeitos positivos: cura específica por status (ex: Antídoto cura Veneno) e buffs genéricos (Regeneração, Escudo, Fortalecimento, Haste) — lista completa fica para quando desenharmos skills de suporte.

### Em aberto
- Lista de inimigos e seus ranges de horda específicos
- Lore dos bosses
- Criar a tabela de fraquezas e resistências elementais (12x12)

---

## 3. Combate

### Formato
- RPG por turnos, estilo Final Fantasy clássico.
- Grupo do jogador: até **4 aliados** em batalha.
- Horda de inimigos: até **10 inimigos** (variando por composição).
- **Ataque mirado**: jogador escolhe o alvo específico dentro da horda.

### Ações disponíveis
Ataque físico, Magia, Habilidade especial, Item usável, Defender, Fugir.

### Ordem de turno
- Round-robin por **Velocidade**, recalculado a cada rodada.
- Empate: inimigos podem ter tag **Rápido**/**Lento** para resolver desempate coerente com a lore.
- Efeitos que alteram ordem: Haste, Slow, Paralisia/Sono (perde a vez).

### Fórmulas de dano
**Físico:**
```
Dano = (ATK do atacante × multiplicador da habilidade) − (DEF do alvo × fator de redução)
Dano final = Dano × variância aleatória (ex: 90%–110%)
```
**Mágico:** mesma lógica, trocando ATK/DEF por Inteligência/Sabedoria vs. Resistência Mágica.

**Crítico:** base pequena vinda de Destreza, maior parte do investimento vem de skills/runas. Teto de chance ~75%. Multiplicador x1.5.

**Defender:** reduz dano recebido em ~50% até o próximo turno.

### Multiplicador elemental
| Relação | Multiplicador |
|---|---|
| Fraqueza | x1.5 (ou x2, a testar) |
| Neutro | x1.0 |
| Resistência | x0.5 |
| Imunidade | x0 |
| Absorção | dano vira cura |

### Em aberto
- Valores exatos de multiplicadores/redução de defesa (via playtest)
- Valor exato do teto de crítico e bônus de Destreza
- Desempate de Velocidade sem tag aplicável

---

## 4. Equipamento

- Vários tipos: armas, armaduras, amuletos, etc. Trocável em combate.
- **Runas**: encaixadas em slots do equipamento.

### Efeitos das runas (categorias — aprofundar com a classe Runista)
- Runas de atributo, elementais, de status, de combate (crítico, roubo de vida, custo de mana).

### Raridade
| Raridade | Multiplicador de stats | Slots de runa |
|---|---|---|
| Comum | x1.0 | 0–1 |
| Incomum | x1.2 | 1–2 |
| Raro | x1.5 | 2–3 |
| Épico | x1.8 | 3 |
| Lendário | x2.2 | 3–4 |

### Como é obtido
Loot (principal, chance maior em bosses), Loja (Comum/Incomum + runas), Crafting (considerar depois).

### Em aberto
- Aprofundar efeitos de runas junto com o design da classe Runista

---

## 5. Mundo

- Mapa mundo com cidades, reinos e regiões. Lojas para compra.

### Navegação
- Mapa em ícones conectados por rotas (estilo JRPG clássico).
- Primeira travessia: combates pelo caminho. Depois de atravessar o suficiente, libera viagem rápida (sem XP/loot).
- Cidades têm área de combates própria (dungeon local).

### Lojas
- Estoque base + regional (temático). Escala com progresso.
- Tipos: Ferreiro, Runista/Arcanista, Boticário, + ponto de aprendizado de magias/skills.

### Desbloqueio de regiões
- Majoritariamente por progresso da quest principal. Regiões opcionais por nível mínimo ou item específico.

### Em aberto
- Número exato de combates/nível para liberar viagem rápida
- Revisitar djangoquest para decisões específicas de mapa
- Lista completa do que cada loja vende, por região

---

## 6. Narrativa e Quests

- Sem capítulos fixos. Progressão via **quests principais** e **quests de NPC**.

### Estrutura de uma quest
Objetivo, Recompensa, Requisito para completar, Requisito para receber/desbloquear.

### Cruzamento main x NPC
- Quest de NPC desbloqueia por: NPC recrutado + afinidade mínima + progresso mínimo da main.
- Pode alterar a main levemente (cena extra, diálogo especial) com afinidade alta, sem ramificar o final.
- Nunca trava a main — sempre opcional/paralela.

### Diálogos
- Árvore simples: NPC fala, jogador escolhe entre 2-4 respostas.
- Cada escolha: sabor, +/- afinidade, ou desbloqueio/flag de quest.
- Sem moralidade global nem múltiplos finais.

### Vocabulário de requisitos
**Desbloqueio (AND combinável)**: progresso de main, nível mínimo, afinidade mínima com NPC, item no inventário, região desbloqueada.
**Completar**: derrotar inimigo/boss, entregar item, chegar em local, falar com NPC.

### Em aberto
- Detalhar exemplos concretos de quests conforme a lore for escrita

---

## 7. Conta / Usuário (infraestrutura)

- `User` padrão do Django para autenticação.
- `PerfilUsuario` estendido via `OneToOneField` — hoje só guarda `data_criacao`.
- Múltiplos personagens por usuário via `ForeignKey` de `Personagem → User`.
- Conquistas: planejado, depois. Configurações: pós-jogo finalizado. Sem monetização (exceto cosméticos, talvez).

---

## Próximos passos sugeridos

1. Detalhar cada seção "Em aberto" acima, sistema por sistema.
2. Continuar os models Django do sistema de Personagens (Classe, Personagem) — Raça, PassivaRacial e PerfilUsuario já feitos.
3. Preencher os 27 registros de Raça no admin, respeitando o orçamento de pontos (5 líquidos, teto +4/-2).
4. Manter este documento atualizado a cada decisão nova.
