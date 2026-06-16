# Digital Twin Hands-On: Como Criar um Gêmeo Digital de Chão de Fábrica

**Workshop Summit de IA — Joinville**
**Profa. Dra. Itamar Iliuk | LABRIOT — UTFPR Ponta Grossa**

---

## Sumário

1. [Visão Geral e Contexto Industrial](#1-visão-geral-e-contexto-industrial)
2. [Arquitetura e Ferramentas](#2-arquitetura-e-ferramentas)
3. [Parte 1 — Construindo a Estrutura da Fábrica (Warehouse Creator)](#3-parte-1--construindo-a-estrutura-da-fábrica-warehouse-creator)
4. [Parte 2 — Montando a Linha de Produção (Conveyor Track Builder)](#4-parte-2--montando-a-linha-de-produção-conveyor-track-builder)
5. [Parte 3 — Populando o Chão de Fábrica (SimReady Assets)](#5-parte-3--populando-o-chão-de-fábrica-simready-assets)
6. [Parte 4 — Adicionando Física e Simulação](#6-parte-4--adicionando-física-e-simulação)
7. [Parte 5 — Trazendo Robôs Autônomos para o Digital Twin](#7-parte-5--trazendo-robôs-autônomos-para-o-digital-twin)
8. [Parte 6 — Pick & Place com Braço Robótico na Esteira](#8-parte-6--pick--place-com-braço-robótico-na-esteira)
9. [Parte 7 — Conectando ao Mundo Real (Sensores e Dados)](#9-parte-7--conectando-ao-mundo-real-sensores-e-dados)
10. [O Pipeline Completo: Da Realidade ao Digital Twin](#10-o-pipeline-completo-da-realidade-ao-digital-twin)
11. [Casos Reais de Referência](#11-casos-reais-de-referência)
12. [Desafios para os Alunos](#12-desafios-para-os-alunos)
13. [Referências](#13-referências)

---

## 1. Visão Geral e Contexto Industrial

### O que é um Digital Twin de Chão de Fábrica?

Um gêmeo digital (Digital Twin) é uma réplica virtual fisicamente precisa de um ambiente real. No contexto de manufatura, ele permite simular, testar e otimizar operações antes (e durante) a implantação no mundo físico. De acordo com a McKinsey, cerca de 75% das empresas em indústrias avançadas já adotam tecnologias de digital twin.

### Por que isso importa?

Grandes fabricantes como Foxconn, Delta Electronics, Toyota, Caterpillar e Siemens estão usando digital twins da NVIDIA para:

- **Projetar layouts de fábrica** antes de construí-los fisicamente
- **Treinar robôs em simulação** (braços articulados, AMRs, humanoides) antes do deploy
- **Otimizar fluxos logísticos** (rotas de AMRs, posicionamento de estações)
- **Validar programas de robôs** sem parar a produção
- **Gerar dados sintéticos** para treinar modelos de visão computacional

### O que vamos construir neste workshop

Vamos construir, passo a passo, um digital twin simplificado de uma **célula de manufatura** contendo:

```
┌─────────────────────────────────────────────────────────┐
│                    FÁBRICA (Warehouse)                   │
│                                                         │
│  ┌──────────┐     ═══════════════════     ┌──────────┐  │
│  │ Estação  │     Esteira (Conveyor)      │ Estação  │  │
│  │ de       │──→  ═══════════════════ ──→ │ de       │  │
│  │ Entrada  │          │                  │ Saída    │  │
│  └──────────┘     ┌────┴────┐             └──────────┘  │
│                   │  Franka │                            │
│                   │  Panda  │                            │
│                   │(Pick &  │                            │
│                   │ Place)  │                            │
│                   └─────────┘                            │
│                                                         │
│  🤖 AMR (Carter)  ←→  Prateleiras com paletes          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Arquitetura e Ferramentas

### O Pipeline CAD → Digital Twin

```
CAD/3D Scan ──→ Conversão USD ──→ Omniverse ──→ Isaac Sim ──→ Deploy
(SolidWorks,     (Connectors,     (Composição    (Física,      (Robôs
 Blender,         URDF Import,     de cena,       sensores,     reais,
 3D Scan)         OnShape)         iluminação)    RL, Nav)      IoT)
```

### Ferramentas que usaremos no Isaac Sim

| Ferramenta | Função | Menu no Isaac Sim |
|-----------|--------|-------------------|
| **Warehouse Creator** | Criar estrutura (chão, paredes, portas) | Window > Extensions > Warehouse Creator |
| **Conveyor Track Builder** | Montar esteiras de transporte | Tools > Conveyor Track Builder |
| **NVIDIA Assets Browser** | Acessar 800+ assets SimReady | Window > Browsers > NVIDIA Assets |
| **Conveyor Belt Utility** | Configurar física das esteiras | Create > Isaac Sim > Warehouse Items > Conveyor |
| **OmniGraph** | Programar lógica visual | Window > Visual Scripting > Action Graph |
| **Physics Inspector** | Validar colisões e rigid bodies | Window > Physics > Physics Inspector |

### Pré-Requisitos

- Isaac Sim 5.1+ ou 6.0 instalado (workstation ou pip)
- Isaac Sim Assets Pack baixado (contém o Modular Warehouse e Conveyors)
- GPU NVIDIA RTX com 16+ GB VRAM
- Mínimo 32 GB RAM
- Conhecimento básico de navegação 3D (viewport, stage, properties)

### Download dos Assets

O pacote de assets do Isaac Sim precisa ser baixado separadamente:

```bash
# O Isaac Sim mostrará um prompt de download na primeira execução
# Ou acesse: https://developer.nvidia.com/isaac-sim-assets

# Após download, os assets ficam disponíveis em:
# Isaac/Environments/Modular_Warehouse_New/  (warehouse modular)
# Isaac/Props/Conveyors/                      (peças de esteira)
# Isaac/Robots/                               (robôs)
```

---

## 3. Parte 1 — Construindo a Estrutura da Fábrica (Warehouse Creator)

O Warehouse Creator é um editor visual de planta baixa que converte um grid 2D em uma estrutura USD 3D completa com chão, paredes e aberturas.

### Passo 1.1 — Abrir o Isaac Sim e Criar Nova Cena

1. Abra o Isaac Sim
2. Vá em **File > New Stage** para criar uma cena vazia
3. A cena já vem com um ground plane e iluminação padrão

### Passo 1.2 — Habilitar a Extensão Warehouse Creator

1. Vá em **Window > Extensions**
2. Pesquise por **"warehouse creator"**
3. Habilite a extensão `isaacsim.warehouse.creator` (ou nome similar na sua versão)
4. Um novo painel aparecerá na interface

### Passo 1.3 — Configurar os Parâmetros

No painel do Warehouse Creator:

| Parâmetro | Valor Sugerido | Descrição |
|-----------|----------------|-----------|
| **Cell Size** | 5.0 m | Tamanho de cada célula do grid |
| **Wall Height** | 6.0 m | Altura das paredes |
| **Asset Root Path** | `[Isaac Sim Assets]/Isaac/Environments/Modular_Warehouse_New/` | Caminho para os assets modulares |

> **Dica:** Os valores padrão correspondem ao pack de assets do Isaac Sim. Se estiver usando assets customizados, ajuste o Cell Size e Wall Height conforme necessário.

### Passo 1.4 — Desenhar a Planta Baixa

O editor funciona como uma ferramenta de pintura em grid:

1. **Clique nas células** do grid para ocupá-las (criando chão)
2. **Clique novamente** para remover (criando aberturas ou áreas externas)
3. As **paredes são geradas automaticamente** nas bordas expostas (onde uma célula ocupada encontra uma célula vazia)
4. Paredes entre duas células adjacentes ocupadas são **omitidas** automaticamente

**Planta sugerida para o workshop (6×4 células = 30m × 20m):**

```
    1   2   3   4   5   6
  ┌───┬───┬───┬───┬───┬───┐
1 │ X │ X │ X │ X │ X │ X │  ← Área de recebimento
  ├───┼───┼───┼───┼───┼───┤
2 │ X │ X │ X │ X │ X │ X │  ← Linha de produção (esteiras)
  ├───┼───┼───┼───┼───┼───┤
3 │ X │ X │ X │ X │ X │ X │  ← Área do braço robótico
  ├───┼───┼───┼───┼───┼───┤
4 │ X │ X │ X │ X │ X │ X │  ← Expedição / armazém
  └───┴───┴───┴───┴───┴───┘
```

### Passo 1.5 — Gerar o Warehouse

1. Clique no botão **"Generate Warehouse"**
2. Aguarde o popup "Generating Warehouse" finalizar
3. A estrutura USD será criada no stage sob `/Warehouse`
4. Verifique no Stage tree: cada célula tem um prim de chão (center) e as bordas têm prims de parede

### Passo 1.6 — Personalizar as Paredes (Variantes)

Após a geração, cada tile (parede e chão) possui **variantes visuais**:

1. No viewport, mude o **Select Mode** para **Component** (botão direito na toolbar) para selecionar tiles individuais
2. Selecione um tile de parede
3. No painel **Properties**, seção **Warehouse Tiles**, escolha entre as variantes disponíveis: parede sólida, parede com janela, porta de carga (loading dock), painel de acesso, etc.
4. Adicione pelo menos uma **porta de carga (loading dock)** na fileira 1 (recebimento) e uma na fileira 4 (expedição)

> **Resultado esperado:** Uma estrutura retangular de fábrica com chão industrial, paredes de alvenaria, e aberturas para carga/descarga.

---

## 4. Parte 2 — Montando a Linha de Produção (Conveyor Track Builder)

As esteiras de transporte são o coração de uma linha de produção. O Isaac Sim fornece um builder visual e assets prontos.

### Passo 2.1 — Habilitar as Extensões de Conveyor

1. **Window > Extensions**
2. Pesquise por **"conveyor"**
3. Habilite:
   - `isaacsim.asset.gen.conveyor` — funcionalidade base
   - `isaacsim.asset.gen.conveyor.ui` — interface visual e Conveyor Track Builder

### Passo 2.2 — Abrir o Conveyor Track Builder

1. Vá em **Tools > Conveyor Track Builder**
2. O painel mostra uma paleta de peças de esteira disponíveis:
   - **Reta (Straight)** — segmento reto de esteira
   - **Curva (Curve)** — seção curva (90°)
   - **Junção (T / Y)** — divisão de fluxo
   - **Inclinada (Incline/Decline)** — subida ou descida
   - **Roletes (Rollers)** — esteira de roletes

### Passo 2.3 — Montar a Linha de Produção

Monte uma linha em L que vai da estação de entrada até a estação do braço robótico:

**Sequência sugerida:**

1. Posicione o cursor na **fileira 1** (área de recebimento)
2. Adicione 3 segmentos **retos** alinhados (formando ~15m de esteira reta)
3. Adicione 1 **curva de 90°** para virar em direção à fileira 3
4. Adicione 2 segmentos **retos** descendo em direção ao braço robótico
5. Termine com 1 segmento **reto** na posição onde o Franka ficará

**Como conectar as peças:**

- O Track Builder tenta **conectar automaticamente** as peças nos endpoints definidos pela configuração
- Se a peça selecionada no stage é parte do dataset de conveyors, o builder conecta no endpoint mais próximo
- Caso contrário, a peça é inserida como filha da seleção atual

```
Estação Entrada (Loading Dock)
        │
        ▼
  ═══════════════════  (3 segmentos retos)
                    │
                    │  (curva 90°)
                    ▼
                    ║
                    ║  (2 segmentos retos)
                    ║
                    ▼
              [Franka Panda]  ← Ponto de pick & place
                    │
                    ▼
              ═══════════  (2 segmentos retos → saída)
```

### Passo 2.4 — Configurar a Física das Esteiras

Para cada segmento de esteira, é necessário configurar o comportamento de conveyor:

1. **Selecione o prim `Belt` ou `Rollers`** do segmento de esteira (não o prim raiz)
2. Vá em **Create > Isaac Sim > Warehouse Items > Conveyor**
3. Isso cria um nó OmniGraph que controla a esteira
4. No painel Properties, configure:
   - **Velocity:** 0.5 m/s (velocidade da esteira)
   - **Direction:** Ajuste o eixo conforme a orientação do segmento (X, Y ou Z)
   - **Enabled:** True

> **Importante:** Os assets de conveyor do Isaac Sim estão em `Isaac/Props/Conveyors`. Ao selecionar o prim para aplicar a física, escolha sempre o sub-prim `Belt` ou `Rollers`, não o prim raiz do asset.

### Passo 2.5 — Testar a Esteira

1. Adicione um cubo simples acima da esteira: **Create > Shape > Cube**
2. Redimensione para algo realista (ex: 0.3 × 0.2 × 0.15 m)
3. Adicione um **Rigid Body** ao cubo: **selecione o cubo > Properties > Add > Physics > Rigid Body**
4. Adicione um **Collision Mesh**: **Properties > Add > Physics > Collision**
5. Pressione **Play (Space)** para iniciar a simulação
6. O cubo deve ser transportado pela esteira em direção à curva

> **Resultado esperado:** Os cubos colocados na esteira deslizam suavemente na direção configurada, seguem a curva, e param no final da linha.

---

## 5. Parte 3 — Populando o Chão de Fábrica (SimReady Assets)

### Passo 3.1 — Abrir o Browser de Assets

1. Vá em **Window > Browsers > NVIDIA Assets**
2. No browser, clique no **ícone +** ao lado de **Industrial**
3. Categorias disponíveis:
   - **Buildings** — estruturas (já usamos o Warehouse)
   - **Shelving** — prateleiras e racks
   - **Equipment** — máquinas e ferramentas
   - **Containers** — caixas, paletes, bins
   - **Safety** — cones, barreiras, sinalizações
   - **Vehicles** — empilhadeiras, carrinhos

### Passo 3.2 — Adicionar Prateleiras (Racks)

1. No browser, navegue até **Industrial > Shelving**
2. Arraste um **WarehouseRack** para a cena, posicionando na **fileira 4** (armazém)
3. Repita para criar uma fileira de 3-4 racks alinhados
4. Ajuste a posição usando as ferramentas de Move (W) e Rotate (E) no viewport

> **Atenção com escalas:** Alguns assets no NVIDIA Assets estão em **centímetros** enquanto o Isaac Sim trabalha em **metros**. Se um asset parecer gigante, crie um Xform pai com escala `0.01` em todos os eixos e arraste os assets para dentro dele.

### Passo 3.3 — Adicionar Paletes e Caixas

1. Navegue até **Industrial > Containers**
2. Arraste **Pallets** para as prateleiras
3. Adicione **Cardboard Boxes** sobre os paletes
4. Para caixas que serão manipuladas pelo robô, certifique-se de adicionar:
   - **Rigid Body** (Physics > Rigid Body)
   - **Collision Mesh** (Physics > Collision)

### Passo 3.4 — Adicionar Equipamentos de Segurança

1. Navegue até **Industrial > Safety**
2. Adicione **Safety Barriers** ao redor da célula do braço robótico
3. Adicione **Warning Signs** nas áreas de movimentação de AMR
4. Estes elementos são importantes para realismo visual e para treinar modelos de visão computacional

### Passo 3.5 — Organizar a Hierarquia do Stage

Mantenha a cena organizada criando Xforms para agrupar:

```
/World
├── /Warehouse          ← Estrutura (gerada pelo Warehouse Creator)
├── /ConveyorSystem     ← Sistema de esteiras
│   ├── /Straight_01
│   ├── /Curve_01
│   └── /Straight_02
├── /Equipment          ← Equipamentos e mobiliário
│   ├── /Racks
│   ├── /Palettes
│   └── /SafetyBarriers
├── /Robots             ← Robôs (adicionaremos a seguir)
│   ├── /Franka
│   └── /Carter
└── /Props              ← Objetos manipuláveis
    └── /Boxes
```

---

## 6. Parte 4 — Adicionando Física e Simulação

### Passo 4.1 — Configurar o Physics Scene

1. Vá em **Create > Physics > Physics Scene**
2. No painel Properties, verifique:
   - **Gravity:** (0, 0, -9.81) m/s² — direção correta para Z-up
   - **GPU Dynamics:** Habilitado (para performance)

### Passo 4.2 — Configurar Ground Plane com Colisão

1. O ground plane padrão já tem colisão
2. Se não tiver, selecione o chão e adicione: **Properties > Add > Physics > Collision**
3. Configure o material de física: **Create > Physics > Physics Material**
   - **Static Friction:** 0.5
   - **Dynamic Friction:** 0.3
   - **Restitution:** 0.1

### Passo 4.3 — Transformar Caixas em Rigid Bodies

Para cada caixa que será transportada pela esteira ou manipulada pelo robô:

1. Selecione a caixa
2. **Properties > Add > Physics > Rigid Body**
3. **Properties > Add > Physics > Collision** (escolha Mesh ou Box simplificado)
4. Configure a massa: **Mass > ~0.5 kg** (para uma caixa pequena)

### Passo 4.4 — Testar a Simulação Completa

1. Posicione 3-5 caixas no início da esteira
2. Pressione **Play (Space)**
3. Verifique:
   - Caixas devem ser transportadas pela esteira
   - Caixas devem seguir a curva
   - Caixas não devem atravessar paredes ou esteiras
   - Caixas devem parar no final da linha

> **Troubleshooting:** Se caixas atravessam a esteira, verifique se o prim `Belt` tem Collision habilitada. Se caixas voam para longe, reduza a velocidade da esteira ou aumente a massa das caixas.

---

## 7. Parte 5 — Trazendo Robôs Autônomos para o Digital Twin

### Passo 5.1 — Adicionar o Braço Robótico Franka Panda

1. Vá em **Create > Isaac Sim > Robots > Manipulation > Franka**
2. O Franka aparecerá na origem — reposicione-o na posição designada (ao lado da esteira, na curva)
3. O Franka já vem com:
   - Articulações configuradas
   - Controladores de juntas
   - Gripper paralelo funcional

**Posicionamento sugerido:**

- Coloque o Franka em uma base (mesa ou pedestal) adjacente à esteira
- O end-effector deve alcançar as caixas na esteira
- Verifique o alcance (~855mm) para garantir que as caixas estão acessíveis

### Passo 5.2 — Adicionar um AMR (Robô Móvel Autônomo)

O Isaac Sim inclui vários modelos de AMR. O Carter é um bom ponto de partida:

1. Vá em **Create > Isaac Sim > Robots > Navigation > Carter**
2. Ou use o Asset Browser: pesquise por "Carter" nos assets Isaac
3. Posicione o Carter no corredor entre as prateleiras e a linha de produção
4. O Carter inclui sensores LIDAR e câmeras para navegação

### Passo 5.3 — Configurar Navegação do AMR (Opcional Avançado)

Para navegação autônoma do Carter:

1. Ative a extensão de **Navigation Mesh**: **Window > Extensions > "navigation"**
2. Gere um **NavMesh** do ambiente: **Create > Navigation Mesh**
3. Configure waypoints para o AMR patrulhar entre prateleiras

---

## 8. Parte 6 — Pick & Place com Braço Robótico na Esteira

### Passo 6.1 — Abordagem Visual (OmniGraph — sem código)

O Isaac Sim permite programar o pick & place usando programação visual:

1. Vá em **Window > Visual Scripting > Action Graph**
2. Crie um novo Action Graph
3. Adicione os seguintes nós:

```
[On Playback Tick] → [Isaac Read Sim Time]
                   → [Pick and Place Controller]
                        ├── Robot Prim Path: /World/Robots/Franka
                        ├── Robot Model: "Franka"
                        ├── Picking Position: (posição da caixa na esteira)
                        └── Placing Position: (posição do palete destino)
```

4. Conecte:
   - **Picking Position** ← Posição de um cubo de referência na esteira
   - **Placing Position** ← Posição no palete ou mesa de destino
5. Pressione **Play** — o Franka deve executar a sequência: mover → abrir gripper → descer → fechar → levantar → mover → abrir

### Passo 6.2 — Abordagem por Script (Python — mais controle)

Para controle programático com cinemática inversa:

```python
# Arquivo: factory_pick_place.py
# Executar dentro do Isaac Sim Python environment

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import numpy as np
from isaacsim.core import World
from isaacsim.robot.manipulators import SingleManipulator
from isaacsim.robot.manipulators.controllers import PickPlaceController

# Criar o mundo
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# Adicionar o Franka (ou carregar a cena existente)
# Se já tem a cena montada, use: open_stage("sua_cena.usd")

# Inicializar o controlador de pick and place
controller = PickPlaceController(
    name="pick_place_controller",
    gripper=franka.gripper,
    robot_articulation=franka,
)

# Definir posições
pick_position = np.array([0.5, 0.0, 0.3])    # Posição da caixa na esteira
place_position = np.array([0.5, -0.5, 0.3])   # Posição do palete destino

# Loop de simulação
while simulation_app.is_running():
    world.step(render=True)
    
    if world.is_playing():
        actions = controller.forward(
            picking_position=pick_position,
            placing_position=place_position,
            current_joint_positions=franka.get_joint_positions(),
            end_effector_offset=np.array([0, 0, 0.005]),
        )
        franka.apply_action(actions)
        
        if controller.is_done():
            controller.reset()

simulation_app.close()
```

### Passo 6.3 — Abordagem Isaac Lab com RL (Avançado)

Para treinar o pick & place por RL (usando o ambiente de referência do Isaac Lab):

```bash
conda activate isaaclab_prod

# Treinar a tarefa de Lift (pegar e levantar)
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Lift-Cube-Franka-v0 \
    --num_envs 4096 \
    --max_iterations 2000 \
    --headless
```

---

## 9. Parte 7 — Conectando ao Mundo Real (Sensores e Dados)

### 9.1 — Adicionando Câmeras para Visão Computacional

1. Selecione o Franka ou uma posição na fábrica
2. **Create > Camera**
3. Configure:
   - **Resolution:** 1280 × 720
   - **FOV:** 60°
4. A câmera pode gerar: RGB, Depth, Segmentação Semântica, Bounding Boxes

### 9.2 — Semantic Labeling (Rotulagem Semântica)

Os assets SimReady já vêm com labels semânticas para treino de modelos de visão:

- Caixas → `"box"` / `"cardboard"`
- Paletes → `"pallet"`
- Prateleiras → `"rack"` / `"shelf"`
- Robôs → `"robot"`
- Pessoas → `"person"`

Isso permite gerar datasets sintéticos para detecção de objetos sem anotar dados reais.

### 9.3 — Fluxo de Dados para o Mundo Real

O pipeline completo do Digital Twin conecta ao real via:

```
Digital Twin (Isaac Sim)          Mundo Real (Fábrica)
       │                                  │
       ├── ROS 2 Bridge ←──────────────── ├── ROS 2 (robôs)
       ├── OPC-UA ←────────────────────── ├── PLCs / SCADA
       ├── MQTT ←──────────────────────── ├── IoT Sensors
       └── Omniverse Connect ←─────────── └── CAD Updates
```

---

## 10. O Pipeline Completo: Da Realidade ao Digital Twin

### Fluxo Recomendado para Fábricas Reais

```
ETAPA 1: CAPTURA
├── Planta baixa (CAD / DWG / PDF)
├── Scan 3D do ambiente (LiDAR, fotogrametria)
├── Fotos de referência
└── Especificações de equipamentos

ETAPA 2: MODELAGEM
├── Converter CAD para USD (via Connectors: SolidWorks, STEP, FBX)
├── Importar URDF dos robôs
├── Usar SimReady Assets para equipamentos padrão
└── Modelar assets customizados (Blender → USD)

ETAPA 3: COMPOSIÇÃO (O que fizemos neste workshop)
├── Construir estrutura (Warehouse Creator)
├── Montar esteiras (Conveyor Track Builder)
├── Posicionar equipamentos e robôs
└── Configurar iluminação e materiais

ETAPA 4: FÍSICA E SIMULAÇÃO
├── Adicionar rigid bodies e colisões
├── Configurar atuadores e sensores
├── Programar lógica (OmniGraph ou Python)
└── Validar fluxo de materiais

ETAPA 5: INTELIGÊNCIA
├── Treinar navegação de AMRs (Isaac Nav)
├── Treinar manipulação de braços (Isaac Lab / RL)
├── Treinar visão computacional (Replicator / SDG)
└── Otimizar rotas (cuOpt)

ETAPA 6: DEPLOY E SINCRONIZAÇÃO
├── Deploy de políticas para robôs reais
├── Conectar sensores IoT via MQTT / OPC-UA
├── Sincronizar posições via ROS 2
└── Monitoramento em tempo real
```

---

## 11. Casos Reais de Referência

### Delta Electronics

A Delta Electronics, líder em soluções de eletrônicos e IoT, usa o NVIDIA Isaac Sim para simular e otimizar linhas de produção de componentes eletrônicos. O digital twin permite testar layouts de fábrica, validar programas de robôs e treinar AMRs antes da implantação — reduzindo o tempo de ramp-up significativamente.

### Foxconn (Guadalajara)

A Foxconn construiu um digital twin completo da fábrica de Guadalajara (México) usando Omniverse + Siemens Teamcenter para produzir sistemas NVIDIA Blackwell HGX. Engenheiros definem processos e treinam robôs no ambiente virtual antes de qualquer implantação física. O digital twin inclui dezenas de braços robóticos, AMRs e sistemas de visão treinados em simulação.

### KION + Accenture + Siemens (Mega Omniverse Blueprint)

Usando o Mega Omniverse Blueprint, a KION otimiza processos de warehouse e distribuição com digital twins de larga escala que treinam e testam frotas de empilhadeiras autônomas baseadas em NVIDIA Jetson para a GXO, maior operadora logística do mundo.

### Toyota (Georgetown, Kentucky)

A Toyota usa a tecnologia idealworks iw.sim, integrada com o Mega Omniverse Blueprint, para criar digital twins da fábrica de Georgetown e explorar cenários complexos de automação com frotas heterogêneas de robôs.

---

## 12. Desafios para os Alunos

### Desafio 1 — Básico (~20 min)

Use o Warehouse Creator para criar uma fábrica em formato de "L" com pelo menos 2 portas de carga. Adicione variantes visuais (janelas, loading docks) e capture um screenshot do resultado.

### Desafio 2 — Intermediário (~30 min)

Monte uma esteira com pelo menos uma curva de 90° usando o Conveyor Track Builder. Adicione 5 caixas com Rigid Body e teste a simulação — todas as caixas devem percorrer a esteira sem cair ou atravessar.

### Desafio 3 — Avançado (~45 min)

Posicione um Franka Panda ao lado da esteira e configure o OmniGraph de Pick & Place para que ele pegue caixas da esteira e coloque em uma mesa adjacente. O ciclo deve funcionar para pelo menos 3 caixas.

### Desafio 4 — Expert (~60 min)

Crie um cenário completo com:

- Warehouse com pelo menos 3 zonas distintas (recebimento, produção, expedição)
- Linha de produção com esteira em L
- Franka fazendo pick & place
- Pelo menos 1 AMR (Carter) posicionado para transporte
- Prateleiras com paletes na zona de expedição
- Pelo menos 2 câmeras posicionadas para visão computacional

Salve como arquivo `.usd` e apresente para o grupo.

---

## 13. Referências

### Documentação Oficial Isaac Sim — Digital Twin

- [Digital Twin Overview](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/index.html)
- [Warehouse Creator Extension](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/warehouse_logistics/ext_omni_warehouse_creator.html)
- [Static Warehouse Assets](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/warehouse_logistics/tutorial_static_assets.html)
- [Conveyor Belt Utility](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/warehouse_logistics/ext_isaacsim_asset_gen_conveyor.html)
- [Environment Assets (Warehouse, Hospital, Office)](https://docs.isaacsim.omniverse.nvidia.com/latest/assets/usd_assets_environments.html)
- [Bringing in Autonomous Systems](https://docs-prod.omniverse.nvidia.com/digital-twins/latest/auto-sys.html)
- [Building Scenes](https://docs-prod.omniverse.nvidia.com/digital-twins/latest/building-full-fidelity-viz/building-scenes.html)
- [Reference Architecture](https://docs.isaacsim.omniverse.nvidia.com/latest/isaac_sim_reference_architecture.html)

### Franka Pick & Place

- [Franka Pick and Place Example](https://docs.isaacsim.omniverse.nvidia.com/latest/examples/manipulation_franka_pick_place.html)
- [OmniGraph Pick-and-Place Controller Node](https://docs.isaacsim.omniverse.nvidia.com/latest/advanced_tutorials/tutorial_advanced_omnigraph_pickplace_controller.html)
- [Adding a Manipulator Robot](https://docs.isaacsim.omniverse.nvidia.com/latest/core_api_tutorials/tutorial_core_adding_manipulator.html)

### Casos Industriais

- [Delta Electronics, Foxconn, Pegatron, Wistron — Computex 2024](https://investor.nvidia.com/news/press-release-details/2024/Robotic-Factories-Supercharge-Industrial-Digitalization-as-Electronic-Makers-Adopt-NVIDIA-AI-and-Omniverse)
- [Mega Omniverse Blueprint](https://blogs.nvidia.com/blog/how-digital-twins-scale-industrial-ai/)
- [Foxconn Digital Twin — Guadalajara](https://blogs.nvidia.com/blog/foxconn-digital-twin-ai)

### OpenUSD e Omniverse

- [Documentação OpenUSD](https://openusd.org/release/index.html)
- [Omniverse Digital Twins](https://docs-prod.omniverse.nvidia.com/digital-twins/latest/index.html)
- [SimReady Assets](https://developer.nvidia.com/omniverse/simready-assets)

---

*Documento gerado em Junho de 2026 — Workshop Summit de IA Joinville*

*Licença: CC BY-NC-SA 4.0*
