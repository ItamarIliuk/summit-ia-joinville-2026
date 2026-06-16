# Hands-On: Robótica com IA — Treinamento e Inferência com NVIDIA Isaac Lab e GR00T

**Workshop de Robótica com IA | Summit de IA — Joinville**
**Profa. Dra. Itamar Iliuk | LABRIOT — UTFPR Ponta Grossa**

---

## Sumário

1. [Visão Geral do Workshop](#1-visão-geral-do-workshop)
2. [Entendendo as Bibliotecas de RL](#2-entendendo-as-bibliotecas-de-rl)
3. [Exemplo 1 — Quadrúpede: ANYmal-D (Locomoção)](#3-exemplo-1--quadrúpede-anymal-d-locomoção)
4. [Exemplo 2 — Humanoide: Unitree H1 (Locomoção)](#4-exemplo-2--humanoide-unitree-h1-locomoção)
5. [Exemplo 3 — Braço Robótico: Franka Panda (Pick & Place)](#5-exemplo-3--braço-robótico-franka-panda-pick--place)
6. [Comparando as Stacks: Isaac Lab 2.3.2 vs 3.0-beta](#6-comparando-as-stacks-isaac-lab-232-vs-30-beta)
7. [GR00T N1.7 — Modelo Vision-Language-Action](#7-groot-n17--modelo-vision-language-action)
8. [Guia de Decisão: Qual Framework de RL Escolher?](#8-guia-de-decisão-qual-framework-de-rl-escolher)
9. [Desafios para os Alunos](#9-desafios-para-os-alunos)
10. [Referências](#10-referências)

---

## 1. Visão Geral do Workshop

Neste hands-on, você vai treinar três tipos de robôs usando Reinforcement Learning (RL) no NVIDIA Isaac Lab e experimentar inferência com o GR00T N1.7:

| Exemplo | Robô | Tarefa | Tipo |
|---------|------|--------|------|
| 1 | ANYmal-D (quadrúpede) | Locomoção em terreno plano | Locomotion |
| 2 | Unitree H1 (humanoide) | Locomoção com rastreamento de velocidade | Locomotion |
| 3 | Franka Panda (braço 7-DOF) | Pick & Place de cubo | Manipulation |
| 4 | GR00T N1.7 (VLA) | Inferência de ações a partir de linguagem + visão | Foundation Model |

Todos os exemplos usam ambientes que já vêm incluídos no Isaac Lab — não é necessário criar nada do zero.

---

## 2. Entendendo as Bibliotecas de RL

O Isaac Lab não implementa seus próprios algoritmos de RL. Em vez disso, ele se integra com **quatro bibliotecas externas** através de wrappers padronizados. Cada uma tem filosofia, algoritmos e performance diferentes.

### 2.1 As Quatro Bibliotecas Suportadas

#### RSL-RL (Robotic Systems Lab — ETH Zurich)

É a biblioteca **mais usada na comunidade de robótica legged** (quadrúpedes e humanoides). Foi criada especificamente para robótica, não para RL genérico.

- **Algoritmos:** PPO + Behavior Cloning (estilo DAgger)
- **Arquiteturas:** MLP e LSTM (redes recorrentes para estimação de estado)
- **Diferenciais:** Simetria de dados (explorar que um quadrúpede tem simetria bilateral), exploração por curiosidade, pipeline 100% GPU, multi-GPU/multi-node nativo
- **Quando usar:** Locomoção de robôs legged (quadrúpedes, humanoides), projetos de pesquisa onde sim-to-real é o objetivo, quando você quer seguir a literatura publicada (a maioria dos papers usa RSL-RL)
- **Pontos fortes:** Simples, focado, rápido, bem documentado na comunidade legged
- **Limitação:** Apenas PPO — se você precisa de SAC, TD3 ou outros algoritmos, não está disponível

```bash
# Instalação
./isaaclab.sh --install rsl_rl
```

#### SKRL (Modular RL Library)

É a biblioteca **mais versátil e modular** das quatro. Suporta a maior variedade de algoritmos e é a única com suporte nativo a multi-agente (MAPPO, IPPO).

- **Algoritmos:** PPO, SAC, TD3, DDPG, A2C, RPO, AMP, CEM, MAPPO, IPPO
- **Arquiteturas:** MLP, CNN, RNN, GNN, transformers
- **Diferenciais:** Suporte JAX e PyTorch, multi-agente (MARL), modular (fácil trocar componentes), documentação excelente
- **Quando usar:** Pesquisa com múltiplos algoritmos (comparação SAC vs PPO), tarefas multi-agente (mãos dextras cooperando), quando você quer flexibilidade máxima para experimentar
- **Pontos fortes:** Versatilidade, MARL, boa documentação, ativamente mantido
- **Limitação:** Performance ligeiramente inferior ao RSL-RL em tarefas de locomoção pura

```bash
# Instalação
./isaaclab.sh --install skrl
```

#### RL-Games (High-Performance RL)

Focada em **performance máxima**. Originária da comunidade IsaacGym, é otimizada para treinamento massivamente paralelo em GPU.

- **Algoritmos:** PPO (altamente otimizado), A2C, SAC
- **Arquiteturas:** MLP, LSTM, resnet-like
- **Diferenciais:** A mais rápida das quatro para treinamento bruto, otimizada para milhares de ambientes paralelos, suporte a AMP (Adversarial Motion Priors)
- **Quando usar:** Quando velocidade de treinamento é a prioridade #1, projetos legados migrados do IsaacGym, tarefas que precisam de AMP para geração de movimentos naturais
- **Pontos fortes:** Velocidade, maturidade, herança do ecossistema IsaacGym
- **Limitação:** Menos modular, configuração via YAML pode ser menos intuitiva

```bash
# Instalação
./isaaclab.sh --install rl_games
```

#### Stable-Baselines3 (SB3)

A biblioteca **mais popular e acessível** do ecossistema RL em Python. Ideal para quem está aprendendo.

- **Algoritmos:** PPO, SAC, TD3, A2C, DQN, HER
- **Arquiteturas:** MLP (CNN para imagens)
- **Diferenciais:** Documentação impecável, grande comunidade, fácil de entender e modificar, boas práticas de engenharia de software
- **Quando usar:** Aprendizado e ensino de RL, prototipagem rápida, quando você quer entender o que está acontecendo internamente, benchmarking contra a literatura não-robótica
- **Pontos fortes:** Acessibilidade, documentação, comunidade, estabilidade
- **Limitação:** Significativamente mais lenta que as outras (usa CPU para parte do pipeline), não é ideal para produção com milhares de ambientes

```bash
# Instalação
./isaaclab.sh --install sb3
```

### 2.2 Comparação de Performance (Benchmark Oficial)

Benchmark realizado pela equipe do Isaac Lab no ambiente `Isaac-Humanoid-v0`, treinando 65.5M steps (4096 ambientes × 32 rollout steps × 500 iterações) em uma única RTX 4090:

| Biblioteca | Algoritmo | Tempo Total | Velocidade Relativa | Reward Final |
|-----------|-----------|-------------|---------------------|--------------|
| **RL-Games** | PPO | ~15 min | ⭐ Mais rápida | Alto |
| **RSL-RL** | PPO | ~18 min | Muito rápida | Alto |
| **SKRL** | PPO | ~20 min | Rápida | Alto |
| **SB3** | PPO | ~90 min | Lenta | Comparável |

> **Nota:** Os tempos são aproximados e baseados nos benchmarks oficiais. A reward final converge para valores similares em todas as bibliotecas — a diferença está no tempo de treinamento, não na qualidade da política.

### 2.3 O Algoritmo PPO (Proximal Policy Optimization)

Todos os exemplos deste workshop usam **PPO**, que é o algoritmo dominante em robótica simulada. Entenda o porquê:

**O que é PPO?** É um algoritmo de RL on-policy que otimiza uma política (rede neural) para maximizar a recompensa acumulada, usando uma restrição de "clip" para evitar atualizações muito grandes que desestabilizem o treinamento.

**Por que PPO domina em robótica?**

- **Estabilidade:** A restrição de clip evita colapsos durante o treinamento — essencial quando cada simulação é custosa
- **Paralelização massiva:** Como é on-policy, escala perfeitamente com milhares de ambientes paralelos em GPU
- **Sim-to-real:** Políticas PPO se transferem bem para o mundo real quando combinadas com domain randomization
- **Simplicidade:** Poucos hiperparâmetros para ajustar comparado com SAC ou TD3

**Quando considerar SAC em vez de PPO?**

- Tarefas de manipulação fina com espaço de ações contínuo de alta dimensão
- Quando sample efficiency é mais importante que wall-clock time
- Tarefas onde exploração é difícil (SAC maximiza entropia automaticamente)

---

## 3. Exemplo 1 — Quadrúpede: ANYmal-D (Locomoção)

O ANYmal-D é um robô quadrúpede desenvolvido pela ANYbotics (ETH Zurich). Neste exemplo, treinamos uma política de locomoção para rastrear comandos de velocidade em terreno plano.

### 3.1 Sobre o Ambiente

| Propriedade | Valor |
|-------------|-------|
| **Task ID** | `Isaac-Velocity-Flat-Anymal-D-v0` |
| **Espaço de Observação** | 48 dimensões (posição das juntas, velocidades, orientação do corpo, comandos de velocidade, ações anteriores) |
| **Espaço de Ação** | 12 dimensões (posições-alvo para as 12 juntas — 3 por pata) |
| **Frequência de Controle** | 50 Hz (simulação a 200 Hz, decimation = 4) |
| **Recompensa** | Rastreamento de velocidade linear/angular + penalizações por torque excessivo, velocidade das juntas, colisões do corpo |
| **Tipo de Workflow** | Manager-Based |

### 3.2 Treinamento — Stack Produção (Isaac Lab 2.3.2)

```bash
# Ativar o ambiente
conda activate isaaclab_prod

# ===== OPÇÃO A: RSL-RL (recomendado para locomoção) =====
# Treinar em modo headless (sem janela gráfica) para máxima performance
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --headless

# ===== OPÇÃO B: SKRL =====
python scripts/reinforcement_learning/skrl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --headless

# ===== OPÇÃO C: RL-Games =====
python scripts/reinforcement_learning/rl_games/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --headless

# ===== OPÇÃO D: Stable-Baselines3 =====
python scripts/reinforcement_learning/sb3/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --headless
```

> **Dica:** Comece com `--num_envs 1024` se sua GPU tem menos de 16 GB de VRAM.

### 3.3 Monitoramento com TensorBoard

Em um terminal separado, monitore o treinamento:

```bash
conda activate isaaclab_prod
tensorboard --logdir logs/rsl_rl/
```

Abra `http://localhost:6006` no navegador. As métricas mais importantes:

- **`Episode/Reward/mean`** — Recompensa média por episódio (deve subir)
- **`Episode/Episode_length/mean`** — Duração média do episódio (deve subir, o robô fica de pé por mais tempo)
- **`Loss/value_loss`** — Perda do critic (deve estabilizar)

### 3.4 Visualizando a Política Treinada

```bash
# Reproduzir com visualização (1 ambiente para melhor visualização)
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 1

# Usando um checkpoint pré-treinado (se disponível)
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 1 \
    --use_pretrained_checkpoint

# Gravando vídeo do resultado (requer ffmpeg)
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 1 \
    --headless \
    --video \
    --video_length 300
```

### 3.5 Variação: Terreno Rugoso

Para aumentar a dificuldade e treinar uma política mais robusta:

```bash
# Terreno rugoso com currículo de dificuldade progressiva
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Rough-Anymal-D-v0 \
    --num_envs 4096 \
    --headless
```

O terreno rugoso inclui escadas, inclinações, obstáculos e superfícies irregulares. O currículo começa com terreno fácil e progride automaticamente conforme o robô aprende.

### 3.6 O Que Observar

- O robô deve aprender um andar natural em ~300–500 iterações (~10 min na RTX 4090)
- As 4 patas devem coordenar-se em um padrão de marcha (trot, walk, ou pace)
- Comandos de velocidade aleatórios fazem o robô virar, andar para frente/trás
- No terreno rugoso, o robô aprende a levantar mais as patas para evitar tropeçar

---

## 4. Exemplo 2 — Humanoide: Unitree H1 (Locomoção)

O Unitree H1 é um humanoide de corpo inteiro com 19 graus de liberdade. A tarefa de locomoção é significativamente mais complexa que a do quadrúpede por causa do equilíbrio bípede.

### 4.1 Sobre o Ambiente

| Propriedade | Valor |
|-------------|-------|
| **Task ID** | `Isaac-Velocity-Flat-H1-v0` |
| **Espaço de Observação** | 69 dimensões (orientação do torso, posições/velocidades das juntas, velocidade base, comandos, ações anteriores) |
| **Espaço de Ação** | 19 dimensões (posições-alvo para todas as juntas — pernas, cintura, braços) |
| **Frequência de Controle** | 50 Hz |
| **Recompensa** | Rastreamento de velocidade + penalizações por queda, torque, energia, movimentos bruscos |
| **Tipo de Workflow** | Manager-Based |

### 4.2 Treinamento

```bash
conda activate isaaclab_prod

# ===== RSL-RL (recomendado) =====
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --num_envs 4096 \
    --headless

# ===== Comparar as 4 bibliotecas no mesmo ambiente =====
# (Executar cada uma separadamente, em terminais diferentes)

# RSL-RL
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --max_iterations 500 --headless

# SKRL
python scripts/reinforcement_learning/skrl/train.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --max_iterations 500 --headless

# RL-Games
python scripts/reinforcement_learning/rl_games/train.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --max_iterations 500 --headless

# SB3
python scripts/reinforcement_learning/sb3/train.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --max_iterations 500 --headless
```

### 4.3 Visualização

```bash
# Reproduzir a política treinada
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --num_envs 1

# Gravar vídeo
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Velocity-Flat-H1-v0 \
    --num_envs 1 \
    --headless --video --video_length 300
```

### 4.4 Variações Disponíveis

```bash
# Terreno rugoso (mais difícil — requer mais iterações)
--task Isaac-Velocity-Rough-H1-v0

# Unitree G1 (humanoide menor, mais ágil)
--task Isaac-Velocity-Flat-G1-v0
--task Isaac-Velocity-Rough-G1-v0
```

### 4.5 O Que Observar

- O humanoide leva mais tempo para aprender que o quadrúpede (~500–1000 iterações)
- O equilíbrio bípede é o maior desafio — o robô aprende primeiro a ficar de pé, depois a andar
- Observe como a política coordena braços e pernas para manter o equilíbrio
- No terreno rugoso, o robô aprende movimentos compensatórios com os braços

### 4.6 Diferenças do Quadrúpede

| Aspecto | Quadrúpede (ANYmal) | Humanoide (H1) |
|---------|---------------------|----------------|
| Estabilidade base | Alta (4 pontos de apoio) | Baixa (2 pontos) |
| DOF | 12 | 19 |
| Tempo de treino | ~300 iterações | ~500–1000 iterações |
| Dificuldade da reward | Mais fácil de projetar | Precisa de muitas penalizações |
| Sim-to-real | Bem estabelecido | Ainda área de pesquisa ativa |

---

## 5. Exemplo 3 — Braço Robótico: Franka Panda (Pick & Place)

O Franka Emika Panda é um braço robótico de 7 graus de liberdade com gripper paralelo, amplamente usado em pesquisa de manipulação.

### 5.1 Abordagens de Pick & Place

O Isaac Lab oferece **três caminhos diferentes** para pick & place, cada um com nível de complexidade diferente:

#### Abordagem A — RL Puro (aprender do zero via recompensa)

O robô aprende toda a tarefa (alcançar, pegar, mover, soltar) exclusivamente por reinforcement learning.

| Propriedade | Valor |
|-------------|-------|
| **Task ID** | `Isaac-Lift-Cube-Franka-v0` |
| **Espaço de Observação** | 36 dimensões (posições das juntas, posição do cubo, posição-alvo, estado do gripper) |
| **Espaço de Ação** | 8 dimensões (7 juntas + 1 gripper) |
| **Recompensa** | Distância end-effector→cubo + distância cubo→alvo + bônus por segurar + bônus por alcançar o alvo |

#### Abordagem B — Controlador Clássico (IK + máquina de estados)

Usa cinemática inversa (IK) e um controlador pré-programado. Sem RL — tudo é determinístico.

#### Abordagem C — Imitation Learning (Isaac Lab Mimic)

Coleta demonstrações humanas via teleoperação e treina uma política por comportamento clonado (BC).

### 5.2 Treinamento — Abordagem A: RL Puro

```bash
conda activate isaaclab_prod

# ===== Passo 1: Treinar a tarefa de REACH (alcançar) — mais simples =====
# Recomendado como aquecimento antes do Lift
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Reach-Franka-v0 \
    --num_envs 4096 \
    --headless

# Visualizar o Reach treinado
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Reach-Franka-v0 \
    --num_envs 1

# ===== Passo 2: Treinar a tarefa de LIFT (pegar e levantar) =====
# IMPORTANTE: Requer mais iterações que o Reach (~1000-2000)
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Lift-Cube-Franka-v0 \
    --num_envs 4096 \
    --max_iterations 2000 \
    --headless

# Visualizar o Lift treinado
python scripts/reinforcement_learning/rsl_rl/play.py \
    --task Isaac-Lift-Cube-Franka-v0 \
    --num_envs 1
```

> **Atenção:** A tarefa de Lift é mais difícil que a de Reach. Se o robô não estiver pegando o cubo, aumente `--max_iterations` para 3000+.

### 5.3 Treinamento — Comparando SKRL vs RSL-RL para manipulação

```bash
# SKRL com SAC (off-policy — potencialmente mais sample-efficient para manipulação)
python scripts/reinforcement_learning/skrl/train.py \
    --task Isaac-Lift-Cube-Franka-v0 \
    --num_envs 4096 \
    --algorithm SAC \
    --headless

# RSL-RL com PPO (on-policy — mais rápido em wall-clock time)
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Lift-Cube-Franka-v0 \
    --num_envs 4096 \
    --headless
```

### 5.4 Abordagem B — Controlador Clássico (Pick & Place via IK)

Esta abordagem não usa RL. O Isaac Sim traz um exemplo standalone com controlador de cinemática inversa:

```bash
conda activate isaaclab_prod

# Exemplo interativo — abrir Isaac Sim GUI
# Window > Examples > Robotics Examples > Manipulation > Franka Pick Place
# Clicar em LOAD, depois START PICK PLACE

# Ou via script standalone (Isaac Sim 5.1+)
python standalone_examples/api/isaacsim.robot.manipulators/franka/pick_place.py
```

### 5.5 Abordagem C — Imitation Learning com Isaac Lab Mimic

O Isaac Lab Mimic permite gerar grandes datasets de demonstrações a partir de poucas demonstrações humanas, usando augmentação automática:

```bash
# Gerar dataset a partir de demonstrações pré-gravadas
# (O Isaac Lab inclui datasets de exemplo para o Franka)

# Treinar política de BC (Behavior Cloning)
python scripts/imitation_learning/train.py \
    --task Isaac-Lift-Cube-Franka-IK-Abs-v0 \
    --algo bc \
    --headless
```

### 5.6 Quando Usar Cada Abordagem

| Abordagem | Prós | Contras | Melhor Para |
|-----------|------|---------|-------------|
| **RL Puro** | Generaliza bem, descobre estratégias inesperadas | Lento para convergir, reward shaping difícil | Pesquisa, tarefas onde o comportamento ótimo é desconhecido |
| **Controlador IK** | Rápido, determinístico, previsível | Não generaliza, frágil a variações | Produção industrial, tarefas repetitivas e bem definidas |
| **Imitation Learning** | Aprende de demonstrações naturais, bom para tarefas complexas | Precisa de teleoperação hardware, limitado pelas demos | Tarefas onde o comportamento humano é o objetivo |

### 5.7 O Que Observar

- No **Reach**, o braço converge rápido (~200 iterações) para alcançar pontos aleatórios
- No **Lift**, o robô precisa descobrir uma sequência: aproximar → abrir gripper → descer → fechar → levantar → mover para o alvo
- Com **IK**, observe como o movimento é suave mas rígido (sempre a mesma trajetória)
- Compare o tempo de treinamento entre RSL-RL (PPO) e SKRL (SAC) — PPO é mais rápido em wall-clock, mas SAC pode precisar de menos amostras

---

## 6. Comparando as Stacks: Isaac Lab 2.3.2 vs 3.0-beta

Se você instalou ambas as stacks, pode rodar os mesmos exemplos na stack beta para comparar:

### 6.1 Mesmo Exemplo, Stacks Diferentes

```bash
# ===== Stack Produção (Isaac Lab 2.3.2 + Isaac Sim 5.1) =====
conda activate isaaclab_prod
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --max_iterations 300 \
    --headless

# ===== Stack Beta (Isaac Lab 3.0 + Isaac Sim 6.0) =====
conda activate isaaclab_beta
cd ~/IsaacLab3
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 \
    --num_envs 4096 \
    --max_iterations 300 \
    --headless
```

### 6.2 Novidade da 3.0: Backend Newton (Kit-less)

A grande novidade do Isaac Lab 3.0 é o backend Newton, que usa MuJoCo-Warp e **não precisa do Isaac Sim**:

```bash
conda activate isaaclab_beta
cd ~/IsaacLab3

# Treinar usando o backend Newton (sem Isaac Sim!)
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-Newton-v0 \
    --num_envs 4096 \
    --headless
```

Vantagens do Newton para treino:

- **Mais rápido** (menos overhead sem Kit/Omniverse)
- **Menos VRAM** (não carrega renderer RTX)
- **CUDA Graphs** para stepping acelerado
- Ideal para RL massivo onde renderização não é necessária

Limitações do Newton:

- Sem câmeras RTX (sem imagens fotorrealísticas)
- Sem objetos deformáveis (por enquanto)
- Beta — pode ter bugs

### 6.3 O Que Comparar

| Aspecto | Isaac Lab 2.3.2 | Isaac Lab 3.0-beta |
|---------|-----------------|---------------------|
| Estabilidade | GA (produção) | Beta (experimentos) |
| Performance de treino | Excelente | Potencialmente superior com Newton |
| Renderização | RTX (Isaac Sim) | RTX ou Newton Warp ou OVRTX |
| Backend de física | PhysX apenas | PhysX **ou** Newton (MuJoCo-Warp) |
| Modo kit-less | Não disponível | Disponível (sem Isaac Sim) |

---

## 7. GR00T N1.7 — Modelo Vision-Language-Action

O GR00T N1.7 é completamente diferente das abordagens anteriores. Em vez de treinar via RL, ele é um **foundation model** pré-treinado que recebe linguagem + imagens e gera ações do robô diretamente.

### 7.1 Arquitetura

```
Câmera(s) do robô ─┐
                    ├─→ [ Vision Encoder (Cosmos-Reason2-2B / Qwen3-VL) ]
Comando de texto ───┘             │
                           [ Diffusion Transformer Head ]
                                  │
                           [ Ações contínuas ] → juntas do robô
```

O GR00T é um modelo VLA (Vision-Language-Action) que combina um backbone de visão-linguagem com uma cabeça de difusão que gera ações contínuas. Ele foi treinado em dados de múltiplos robôs (cross-embodiment) incluindo bimanuais, semi-humanoides e humanoides.

### 7.2 Diferença Fundamental: RL vs Foundation Model

| Aspecto | RL (RSL-RL, SKRL, etc.) | Foundation Model (GR00T) |
|---------|-------------------------|--------------------------|
| **Paradigma** | Aprender por tentativa e erro | Aprender de dados (pré-treinado + fine-tune) |
| **Entrada** | Estado do robô (números) | Linguagem + Imagens |
| **Treino** | Horas em simulação | Pré-treinado em 20K+ horas de vídeo |
| **Generalização** | Específico para uma tarefa | Cross-task, cross-embodiment |
| **Sim-to-real** | Domain randomization | Dados reais no pré-treino |
| **Custo computacional (treino)** | 1 GPU por horas | Clusters de H100 por semanas |
| **Custo computacional (inferência)** | Muito leve (~ms) | Moderado (requer GPU 16GB+) |
| **Melhor para** | Locomoção, controle preciso | Manipulação generalizada, seguir instruções |

### 7.3 Inferência com GR00T N1.7

```bash
conda activate groot
cd ~/Isaac-GR00T

# Exemplo de inferência com um embodiment pré-definido
python scripts/inference.py \
    --model_path nvidia/GR00T-N1.7-3B \
    --embodiment_tag new_embodiment \
    --input_image path/to/camera_image.jpg \
    --instruction "pick up the red cup"
```

### 7.4 Fine-tuning com Dados Customizados

O fluxo típico para adaptar o GR00T a um robô específico:

```bash
# Passo 1: Preparar dataset no formato LeRobot
# (gravações de demonstrações com câmera + ações do robô)

# Passo 2: Fine-tuning
python scripts/train.py \
    --model_path nvidia/GR00T-N1.7-3B \
    --dataset_path path/to/your/dataset \
    --embodiment_tag your_robot \
    --batch_size 32 \
    --num_epochs 100

# Passo 3: Avaliar
python scripts/eval.py \
    --model_path output/your_finetuned_model \
    --embodiment_tag your_robot
```

### 7.5 Quando Usar GR00T vs RL Puro

| Cenário | Use GR00T | Use RL |
|---------|-----------|--------|
| Manipulação guiada por linguagem | ✅ | ❌ |
| Locomoção precisa (velocidade, terreno) | ❌ | ✅ |
| Tarefa nova sem dados | ❌ (precisa de fine-tuning) | ✅ (aprende em simulação) |
| Múltiplas tarefas com um único modelo | ✅ | ❌ (1 modelo por tarefa) |
| Deploy em hardware limitado (Jetson) | ⚠️ (16GB+ VRAM) | ✅ (~ms em CPU) |
| Comportamento que segue instruções humanas | ✅ | ❌ |

---

## 8. Guia de Decisão: Qual Framework de RL Escolher?

### 8.1 Fluxograma de Decisão

```
Sua tarefa é locomoção de robô legged?
├─ SIM → RSL-RL (PPO)
│        └─ Precisa de LSTM para estimação de estado? → RSL-RL com ActorCriticRecurrent
│
├─ NÃO → É manipulação?
│        ├─ SIM → Quer comparar algoritmos (PPO vs SAC)?
│        │        ├─ SIM → SKRL (suporta ambos)
│        │        └─ NÃO → RSL-RL (PPO) ou SKRL (PPO)
│        │
│        └─ NÃO → É multi-agente?
│                 ├─ SIM → SKRL (MAPPO/IPPO)
│                 └─ NÃO → Velocidade é prioridade?
│                          ├─ SIM → RL-Games
│                          └─ NÃO → Está aprendendo RL?
│                                   ├─ SIM → SB3
│                                   └─ NÃO → RSL-RL ou SKRL
```

### 8.2 Resumo por Caso de Uso

| Caso de Uso | Biblioteca Recomendada | Algoritmo | Justificativa |
|-------------|------------------------|-----------|---------------|
| Quadrúpede (locomoção) | RSL-RL | PPO | Padrão da comunidade, sim-to-real comprovado |
| Humanoide (locomoção) | RSL-RL | PPO + LSTM | Estimação de estado com redes recorrentes |
| Braço robótico (reach) | RSL-RL ou SKRL | PPO | Converge rápido em tarefas simples |
| Braço robótico (pick & place) | SKRL | SAC ou PPO | SAC pode ser mais sample-efficient |
| Mãos dextras (reorientação) | RL-Games ou SKRL | PPO + AMP | AMP para movimentos naturais |
| Aprendizado/ensino | SB3 | PPO | Documentação e transparência |
| Benchmark de performance | RL-Games | PPO | Mais rápido em wall-clock |
| Multi-agente | SKRL | MAPPO | Único com suporte MARL nativo |
| Pesquisa acadêmica | RSL-RL | PPO | Mais citado em papers |

---

## 9. Desafios para os Alunos

### Desafio 1 — Fácil (~15 min)

Treine o ANYmal-D em terreno plano e depois em terreno rugoso. Compare as curvas de recompensa no TensorBoard e anote: quantas iterações cada um leva para convergir? A reward final é diferente?

```bash
# Terreno plano
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 --num_envs 2048 --headless

# Terreno rugoso
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Rough-Anymal-D-v0 --num_envs 2048 --headless
```

### Desafio 2 — Médio (~30 min)

Compare o treinamento do Humanoid H1 usando RSL-RL vs SKRL vs RL-Games. Use `--max_iterations 500` para todas. Abra 3 TensorBoards (um para cada) e compare: qual converge mais rápido? Qual atinge a maior recompensa?

### Desafio 3 — Avançado (~45 min)

Treine primeiro o `Isaac-Reach-Franka-v0` e depois o `Isaac-Lift-Cube-Franka-v0`. Documente em formato de mini-relatório:

1. Quantas iterações cada tarefa precisou?
2. Qual é a diferença no espaço de ação/observação?
3. Por que o Lift é mais difícil?
4. Tente treinar o Lift com SKRL usando SAC — é melhor ou pior que PPO?

### Desafio 4 — Expert (~60 min)

Se a stack beta estiver instalada: treine o ANYmal-D no backend Newton (sem Isaac Sim) e compare a velocidade de treinamento com o backend PhysX na stack de produção. Documente a diferença em FPS (frames por segundo) e tempo total.

---

## 10. Referências

### Documentação Oficial

- [Isaac Lab — Documentação](https://isaac-sim.github.io/IsaacLab)
- [Isaac Lab — Ambientes Disponíveis](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)
- [Isaac Lab — Comparação de Bibliotecas de RL](https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_frameworks.html)
- [Isaac Lab — Scripts de RL](https://isaac-sim.github.io/IsaacLab/main/source/overview/reinforcement-learning/rl_existing_scripts.html)
- [Isaac Lab — Imitation Learning com Mimic](https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html)

### Bibliotecas de RL

- [RSL-RL (GitHub)](https://github.com/leggedrobotics/rsl_rl) — ETH Zurich, focada em robótica
- [SKRL (Docs)](https://skrl.readthedocs.io) — Modular, multi-agente, multi-framework
- [RL-Games (GitHub)](https://github.com/Denys88/rl_games) — Alta performance, herança IsaacGym
- [Stable-Baselines3 (Docs)](https://stable-baselines3.readthedocs.io) — Acessível, bem documentada

### GR00T

- [GR00T N1.7 (GitHub)](https://github.com/NVIDIA/Isaac-GR00T)
- [GR00T no HuggingFace](https://huggingface.co/collections/nvidia/gr00t-n17)
- [Paper: GR00T N1](https://arxiv.org/abs/2503.14734)

### Papers Fundamentais

- [PPO: Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — Schulman et al., 2017
- [Isaac Lab: A GPU-Accelerated Simulation Framework](https://arxiv.org/abs/2511.04831) — Mittal et al., 2025
- [RSL-RL: A Learning Library for Robotics Research](https://arxiv.org/abs/2509.10771) — Serrano-Muñoz et al., 2025

---

*Documento gerado em Junho de 2026 — Workshop Summit de IA Joinville*

*Licença: CC BY-NC-SA 4.0*
