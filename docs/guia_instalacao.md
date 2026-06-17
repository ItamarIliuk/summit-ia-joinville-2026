# Guia de Instalação — NVIDIA Isaac Sim + Isaac Lab

**Workshop de Robótica com IA | Summit de IA — Joinville**
**Profa. Dra. Itamar Iliuk | LABRIOT — UTFPR Ponta Grossa**

---

## Visão Geral

Este guia cobre a instalação de **duas stacks paralelas** dos frameworks de robótica da NVIDIA, permitindo que você trabalhe com a versão estável para projetos de produção e experimente a versão mais recente para futuras implementações.

| Stack | Isaac Sim | Isaac Lab | Python | Status |
|-------|-----------|-----------|--------|--------|
| **Produção** | 5.1 | 2.3.2 | 3.11 | Estável (GA) |
| **Experimentação** | 6.0 | 3.0-beta | 3.12 | Beta / Early Access |

Ambas as stacks coexistem na mesma máquina usando **ambientes virtuais isolados** (conda), sem conflitos.

---

## Pré-Requisitos

### Sistema Operacional

- Ubuntu 22.04 LTS ou 24.04 LTS

### Hardware

- GPU NVIDIA com suporte RTX (série 20xx ou superior)
- Mínimo 16 GB de VRAM (recomendado: RTX 3090, RTX 4090 ou superior)
- Mínimo 32 GB de RAM
- 100 GB de espaço livre em disco (para ambas as stacks)

> **Atenção — GPUs de notebook (RTX 4050/4060 Laptop etc.):** Essas GPUs têm tipicamente 6–8 GB de VRAM, abaixo do mínimo recomendado. O Isaac Sim pode carregar, mas o renderer RTX pode falhar com `Segmentation fault` ao inicializar o scenedb. Use sempre o modo headless e defina `renderer: RayTracedLighting` para reduzir uso de VRAM.

### Driver NVIDIA

O driver NVIDIA deve ser **versão 560+** (recomendado: **580.65.06 ou superior**). Um único driver atende ambas as stacks.

```bash
# Verificar o driver instalado
nvidia-smi

# Se precisar atualizar
sudo apt update
sudo apt install nvidia-driver-580
sudo reboot
```

### Conda (Miniconda)

Usaremos conda para isolar os ambientes. Se não tiver instalado:

```bash
# Download do Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Instalar
bash Miniconda3-latest-Linux-x86_64.sh

# Reiniciar o terminal e verificar
conda --version
```

### Dependências do sistema

```bash
sudo apt update
sudo apt install -y cmake build-essential git curl vulkan-tools
```

Após instalar, verifique se o Vulkan enxerga a GPU:
```bash
vulkaninfo 2>&1 | grep -E 'GPU|deviceName|driverVersion'
```

---

## Stack 1 — Produção (Isaac Sim 5.1 + Isaac Lab 2.3.2)

Esta é a stack recomendada para projetos em andamento e uso em produção.

### Passo 1: Criar o ambiente conda

```bash
conda create -n isaaclab_prod python=3.11 -y
conda activate isaaclab_prod
```

### Passo 2: Instalar PyTorch com CUDA

Instale o PyTorch **antes** do Isaac Lab. Isso evita que o pip tente baixar o torch (arquivo de vários GB) durante a etapa seguinte, o que pode causar `BrokenPipeError` em conexões instáveis:

```bash
pip install torch==2.7.0 torchvision==0.22.0 \
    --index-url https://download.pytorch.org/whl/cu128 \
    --timeout 300 --retries 5
```

### Passo 3: Instalar Isaac Sim + Isaac Lab

Um único comando instala **ambos** — o Isaac Sim é puxado automaticamente como dependência. Como o PyTorch já está instalado, o pip não precisará baixá-lo novamente:

```bash
pip install "isaaclab[isaacsim,all]==2.3.2.post1" \
    --extra-index-url https://pypi.nvidia.com \
    --timeout 300 --retries 5
```

Os extras significam:

- `isaacsim` → instala o Isaac Sim via pip
- `all` → instala todos os sub-pacotes do Isaac Lab (assets, rl, tasks, sensors, etc.)

### Passo 4: Verificar a instalação

```bash
conda activate isaaclab_prod

# Verificar versão instalada
# Nota: o wheel não expõe __version__; use pip show para confirmar
pip show isaaclab | grep Version

# Teste de simulação headless (sem janela gráfica)
# IMPORTANTE: isaaclab.sim e outros módulos do Isaac Sim só podem ser importados
# APÓS a instanciação de SimulationApp (requisito do framework Carbonite).
# Nunca use `import isaaclab.sim` diretamente sem antes criar o SimulationApp.
# CUDA_VISIBLE_DEVICES=0 garante uso da GPU NVIDIA em máquinas com Intel + NVIDIA
CUDA_VISIBLE_DEVICES=0 python -c '
from isaacsim import SimulationApp
app = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})
import isaaclab
import isaaclab.sim
print("Isaac Sim + Isaac Lab OK -", isaaclab.__file__)
app.close()
'

# Para rodar tutoriais gráficos, é necessário clonar o repositório:
# git clone -b v2.3.2 https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab
# cd ~/IsaacLab && python scripts/tutorials/00_sim/create_empty.py
```

> **Nota:** O comando `python -m isaaclab.tutorials.*` **não funciona** na instalação via pip — as tutoriais são scripts avulsos, não módulos Python. Para executá-las sem clonar o repo, localize os scripts com: `python -c 'import isaaclab, os; print(os.path.dirname(isaaclab.__file__))'`

Se o import não gerar erros, a instalação está completa.

---

## Stack 2 — Experimentação (Isaac Sim 6.0 + Isaac Lab 3.0-beta)

Esta stack traz as novidades: multi-backend physics (PhysX + Newton/MuJoCo-Warp), modo kit-less e renderer plugável.

### Passo 1: Criar o ambiente conda

Note que o Isaac Sim 6.0 exige **Python 3.12** (diferente da stack anterior):

```bash
conda create -n isaaclab_beta python=3.12 -y
conda activate isaaclab_beta
```

### Passo 2: Instalar PyTorch com CUDA

Instale o PyTorch **antes** do Isaac Lab. Isso evita que o pip tente baixar o torch (arquivo de vários GB) durante a etapa seguinte, o que pode causar `BrokenPipeError` em conexões instáveis:

```bash
pip install torch==2.7.0 torchvision==0.22.0 \
    --index-url https://download.pytorch.org/whl/cu128 \
    --timeout 300 --retries 5
```

### Passo 3 — Opção A: Instalar tudo via pip

Como o PyTorch já está instalado, o pip não precisará baixá-lo novamente:

```bash
pip install "isaaclab[isaacsim,all]" \
    --extra-index-url https://pypi.nvidia.com \
    --timeout 300 --retries 5
```

Os extras significam:

- `isaacsim` → instala o Isaac Sim via pip
- `all` → instala todos os sub-pacotes do Isaac Lab (assets, rl, tasks, sensors, etc.)

### Passo 3 — Opção B: Instalar do source (recomendado para beta)

Essa opção dá mais controle e facilita atualizar com `git pull`:

```bash
# Instalar o Isaac Sim via pip
pip install isaacsim --extra-index-url https://pypi.nvidia.com

# Clonar o Isaac Lab (branch beta)
git clone -b release/3.0.0-beta2 \
    https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab3
cd ~/IsaacLab3

# Instalar o Isaac Lab e todas as extensões
./isaaclab.sh --install all
```

### Passo 4: Verificar a instalação

```bash
conda activate isaaclab_beta

# Verificar versão instalada
pip show isaaclab | grep Version

# Teste de simulação headless (sem janela gráfica)
# IMPORTANTE: isaaclab.sim e outros módulos do Isaac Sim só podem ser importados
# APÓS a instanciação de SimulationApp (requisito do framework Carbonite).
# CUDA_VISIBLE_DEVICES=0 garante uso da GPU NVIDIA em máquinas com Intel + NVIDIA

# Se instalou via pip (Opção A)
CUDA_VISIBLE_DEVICES=0 python -c '
from isaacsim import SimulationApp
app = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})
import isaaclab
import isaaclab.sim
print("Isaac Sim 6.0 + Isaac Lab OK -", isaaclab.__file__)
app.close()
'

# Se instalou do source (Opção B)
cd ~/IsaacLab3
CUDA_VISIBLE_DEVICES=0 python scripts/tutorials/00_sim/create_empty.py
```

Se o import não gerar erros, a instalação está completa.

---

## GR00T N1.7 (Opcional — Modelo VLA para Humanoides)

O GR00T N1.7 é um modelo Vision-Language-Action para robôs humanoides. Ele é **independente** do Isaac Sim/Lab e pode ser instalado em um terceiro ambiente.

### Instalação

```bash
conda create -n groot python=3.11 -y
conda activate groot

# Clonar o repositório
git clone https://github.com/NVIDIA/Isaac-GR00T.git ~/Isaac-GR00T
cd ~/Isaac-GR00T

# Instalar dependências
pip install -e .
```

### Requisitos de hardware para GR00T

- **Inferência:** 1 GPU com 16 GB+ de VRAM (ex: RTX 4090)
- **Fine-tuning:** 1+ GPU com 40 GB+ de VRAM (ex: H100, L40)

---

## Alternando Entre as Stacks

Para alternar, basta ativar o ambiente correspondente:

```bash
# Trabalhar com a stack estável
conda activate isaaclab_prod

# Alternar para a stack experimental
conda activate isaaclab_beta

# Trabalhar com o GR00T
conda activate groot

# Ver todos os ambientes disponíveis
conda env list
```

Apenas **um ambiente deve estar ativo por vez**. Não rode as duas stacks simultaneamente na mesma GPU.

---

## Resolução de Problemas

### Falha de segmentação em `librtx.scenedb.plugin.so`

O renderer RTX (`carbOnPluginStartup`) travou ao inicializar. Causas comuns:

**1. Driver muito novo — incompatibilidade de ABI** (causa mais freqüente)

O Isaac Sim 5.1 foi validado com drivers até a série **575**. Driver 590+ pode causar crash determinístico no `librtx.scenedb`. Verifique e, se necessário, faça downgrade:
```bash
nvidia-smi  # se mostrar 590+ e o crash for consistente, faça downgrade
sudo apt install nvidia-driver-570
sudo reboot
```

**2. Máquina com duas GPUs (NVIDIA + Intel)** — Isaac Sim pode tentar inicializar na Intel. Force a GPU NVIDIA:
```bash
CUDA_VISIBLE_DEVICES=0 python -c '
from isaacsim import SimulationApp
app = SimulationApp({"headless": True, "renderer": "RayTracedLighting"})
print("OK")
app.close()
'
```

**3. Sem display** — o Isaac Sim inicializa Vulkan mesmo em modo headless:
```bash
echo $DISPLAY          # deve retornar algo como :1 ou :0
sudo apt install vulkan-tools
vulkaninfo 2>&1 | grep -E 'GPU|deviceName'  # GPU NVIDIA deve aparecer
```

**4. Se o crash persistir**, verifique se a `libnvidia-egl-wayland` está instalada:
```bash
sudo apt install libnvidia-egl-wayland1
```

> **Nota sobre aspas no bash:** Ao usar `python -c` no terminal, prefira aspas simples no exterior: `python -c '...'`. Aspas duplas com `!` dentro causam `bash: !: event not found`.

---

### Erro: `ModuleNotFoundError: No module named 'isaacsim'`

Verifique se o ambiente conda correto está ativado e se o Isaac Sim foi instalado:

```bash
conda activate isaaclab_prod  # ou isaaclab_beta
pip list | grep isaacsim
```

### Erro de compatibilidade com `libgomp`

Conflito entre a biblioteca OpenMP do sistema e a do PyTorch. Solução:

```bash
export LD_PRELOAD=""
```

### Erro de driver / GPU não encontrada

```bash
# Verificar se o driver está funcionando
nvidia-smi

# Verificar a versão do CUDA
nvcc --version
```

### Lentidão na primeira execução

O Isaac Sim compila shaders e baixa assets na primeira execução. Isso é normal e pode levar vários minutos. As execuções seguintes serão mais rápidas.

### Cache de assets

Para evitar downloads repetidos entre as stacks, configure um cache compartilhado:

```bash
# Adicionar ao seu ~/.bashrc
export ISAAC_CACHE_PATH=~/isaac_cache
mkdir -p $ISAAC_CACHE_PATH
```

---

## Matriz de Compatibilidade — Referência Rápida

| Isaac Lab | Isaac Sim | Python | PyTorch | CUDA |
|-----------|-----------|--------|---------|------|
| 3.0-beta | 6.0 | 3.12 | 2.7.0 | 12.8 |
| 2.3.x | 4.5 / 5.0 / 5.1 | 3.11 | 2.7.0 | 12.8 |
| 2.2.x | 4.5 / 5.0 | 3.11 | 2.5.1 | 12.4 |
| 2.1.x | 4.5 | 3.10 | 2.4.0 | 12.1 |

---

## Links Úteis

- [Documentação do Isaac Lab](https://isaac-sim.github.io/IsaacLab)
- [Documentação do Isaac Sim](https://docs.isaacsim.omniverse.nvidia.com)
- [Repositório Isaac Lab (GitHub)](https://github.com/isaac-sim/IsaacLab)
- [Repositório GR00T N1.7 (GitHub)](https://github.com/NVIDIA/Isaac-GR00T)
- [Fórum NVIDIA Developer](https://forums.developer.nvidia.com/c/agx-autonomous-machines/isaac/67)
- [Isaac Lab — Ambientes Disponíveis](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)

---

*Documento gerado em Junho de 2026 — As versões e links podem mudar. Consulte sempre a documentação oficial para atualizações.*

*Licença: CC BY-NC-SA 4.0*
