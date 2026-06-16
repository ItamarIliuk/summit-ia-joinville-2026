# 🏭 Workshop 02 — Digital Twin

## Como Criar um Gêmeo Digital de Chão de Fábrica

**Duração estimada:** 3-4 horas
**Nível:** Iniciante a intermediário
**Pré-requisito:** [Guia de instalação](../docs/guia_instalacao.md) + Isaac Sim Assets Pack

---

## O que você vai aprender

1. Como construir a estrutura de uma fábrica com o Warehouse Creator
2. Como montar linhas de produção com o Conveyor Track Builder
3. Como usar os 800+ SimReady Assets para popular o chão de fábrica
4. Como adicionar física (rigid bodies, colisões, materiais)
5. Como integrar robôs (Franka Panda + AMR Carter)
6. Como configurar pick & place na esteira (OmniGraph + Python)
7. O pipeline completo: do mundo real ao digital twin

---

## Material

| Arquivo | Descrição |
|---------|-----------|
| [handson.md](handson.md) | **Guia hands-on completo** — siga este documento durante o workshop |
| [scripts/](scripts/) | Scripts Python para automação |
| [scenes/](scenes/) | Cenas USD de referência |

---

## Roteiro do Workshop

| Tempo | Atividade |
|-------|-----------|
| 00:00 - 00:30 | Introdução: Digital Twins, OpenUSD, pipeline industrial |
| 00:30 - 01:00 | **Parte 1:** Construir estrutura da fábrica (Warehouse Creator) |
| 01:00 - 01:45 | **Parte 2-3:** Montar esteiras + popular com assets |
| 01:45 - 02:00 | *Intervalo* |
| 02:00 - 02:30 | **Parte 4:** Adicionar física e testar simulação |
| 02:30 - 03:15 | **Parte 5-6:** Robôs autônomos + Pick & Place |
| 03:15 - 03:30 | **Parte 7:** Conexão com o mundo real + casos industriais |
| 03:30 - 04:00 | Desafios práticos + Q&A |

---

## Extensões Necessárias no Isaac Sim

Antes de começar, habilite estas extensões em **Window > Extensions**:

- `isaacsim.warehouse.creator` — Warehouse Creator
- `isaacsim.asset.gen.conveyor` — Conveyor Belt Utility
- `isaacsim.asset.gen.conveyor.ui` — Conveyor Track Builder UI

---

## Links Úteis

- [Isaac Sim Digital Twin Docs](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/index.html)
- [Warehouse Creator](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/warehouse_logistics/ext_omni_warehouse_creator.html)
- [Conveyor Belt Utility](https://docs.isaacsim.omniverse.nvidia.com/latest/digital_twin/warehouse_logistics/ext_isaacsim_asset_gen_conveyor.html)
- [Mega Omniverse Blueprint](https://blogs.nvidia.com/blog/how-digital-twins-scale-industrial-ai/)

---

[← Voltar ao índice](../README.md)
