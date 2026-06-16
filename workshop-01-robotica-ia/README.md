# 🦿 Workshop 01 — Robótica com IA

## Treinamento e Inferência com NVIDIA Isaac Lab e GR00T

**Duração estimada:** 3-4 horas
**Nível:** Intermediário a avançado
**Pré-requisito:** [Guia de instalação](../docs/guia_instalacao.md)

---

## O que você vai aprender

1. Como treinar robôs com Reinforcement Learning usando 4 bibliotecas diferentes
2. As diferenças práticas entre RSL-RL, SKRL, RL-Games e Stable-Baselines3
3. Como treinar locomoção de quadrúpede (ANYmal-D) e humanoide (Unitree H1)
4. Como treinar pick & place com braço robótico (Franka Panda)
5. Como usar o modelo GR00T N1.7 para inferência Vision-Language-Action
6. As diferenças entre Isaac Lab 2.3.2 (produção) e 3.0-beta (experimental)

---

## Material

| Arquivo | Descrição |
|---------|-----------|
| [handson.md](handson.md) | **Guia hands-on completo** — siga este documento durante o workshop |
| [scripts/](scripts/) | Scripts prontos para treinamento e avaliação |

---

## Roteiro do Workshop

| Tempo | Atividade |
|-------|-----------|
| 00:00 - 00:30 | Introdução: RL para robótica, bibliotecas, arquitetura Isaac Lab |
| 00:30 - 01:15 | **Exemplo 1:** Quadrúpede ANYmal-D — treinar e visualizar |
| 01:15 - 02:00 | **Exemplo 2:** Humanoide H1 — treinar e comparar bibliotecas |
| 02:00 - 02:15 | *Intervalo* |
| 02:15 - 03:00 | **Exemplo 3:** Franka Panda — Reach, Lift, Pick & Place |
| 03:00 - 03:30 | **GR00T N1.7** — Inferência VLA + discussão RL vs Foundation Models |
| 03:30 - 04:00 | Desafios práticos + Q&A |

---

## Scripts Rápidos

```bash
# Ativar ambiente
conda activate isaaclab_prod

# Treinar quadrúpede (ANYmal-D) — ~10 min na RTX 4090
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-Anymal-D-v0 --num_envs 4096 --headless

# Treinar humanoide (H1) — ~20 min
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Velocity-Flat-H1-v0 --num_envs 4096 --headless

# Treinar braço (Franka Reach) — ~5 min
python scripts/reinforcement_learning/rsl_rl/train.py \
    --task Isaac-Reach-Franka-v0 --num_envs 4096 --headless
```

---

## Links Úteis

- [Isaac Lab Docs](https://isaac-sim.github.io/IsaacLab)
- [RSL-RL](https://github.com/leggedrobotics/rsl_rl)
- [SKRL](https://skrl.readthedocs.io)
- [GR00T N1.7](https://github.com/NVIDIA/Isaac-GR00T)

---

[← Voltar ao índice](../README.md)
