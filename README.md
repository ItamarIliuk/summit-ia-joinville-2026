# 🤖 Workshops de Robótica e IA — Summit de IA Joinville 2026

**Profa. Dra. Itamar Iliuk** | LABRIOT — UTFPR Ponta Grossa | NVIDIA Omniverse Ambassador

---

## Sobre

Material completo dos workshops apresentados no **Summit de IA de Joinville 2026**, cobrindo desde treinamento de robôs com Reinforcement Learning até a construção de gêmeos digitais de chão de fábrica.

---

## Workshops

### 🦿 Workshop 01 — Robótica com IA: Treinamento e Inferência com Isaac Lab e GR00T

Treine três tipos de robôs (quadrúpede, humanoide e braço robótico) usando Reinforcement Learning no NVIDIA Isaac Lab, e experimente inferência com o modelo GR00T N1.7.

**Tópicos:** Comparação de 4 bibliotecas de RL (RSL-RL, SKRL, RL-Games, SB3) · Locomoção de quadrúpede (ANYmal-D) e humanoide (Unitree H1) · Pick & Place com Franka Panda · Foundation Models com GR00T N1.7 · Isaac Lab 2.3.2 vs 3.0-beta

📂 **[Acessar material →](workshop-01-robotica-ia/)**

---

### 🏭 Workshop 02 — Digital Twin: Gêmeo Digital de Chão de Fábrica

Construa passo a passo um digital twin de uma célula de manufatura com linha de produção, esteiras, braço robótico e AMR usando NVIDIA Isaac Sim e Omniverse.

**Tópicos:** Warehouse Creator · Conveyor Track Builder · 800+ SimReady Assets · Pick & Place com Franka na esteira · ROS 2, MQTT, visão computacional · Casos reais: Delta, Foxconn, Toyota, KION

📂 **[Acessar material →](workshop-02-digital-twin/)**

---

## Pré-Requisitos

📂 **[Guia de instalação completo →](docs/guia_instalacao.md)**

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| GPU NVIDIA | RTX 3060 (12 GB) | RTX 4090 (24 GB) |
| RAM | 32 GB | 64 GB |
| Disco | 100 GB livres | SSD NVMe |
| OS | Ubuntu 22.04 / 24.04 | Ubuntu 24.04 |
| Driver NVIDIA | 560+ | 580+ |

---

## Estrutura do Repositório

```
summit-ia-joinville-2026/
├── README.md                            ← Você está aqui
├── LICENSE
├── docs/
│   └── guia_instalacao.md               ← Instalação (compartilhado)
├── workshop-01-robotica-ia/
│   ├── README.md
│   ├── handson.md                       ← Guia hands-on completo
│   └── scripts/                         ← Scripts de treinamento
└── workshop-02-digital-twin/
    ├── README.md
    ├── handson.md                       ← Guia hands-on completo
    ├── scripts/                         ← Scripts Python
    └── scenes/                          ← Cenas USD de referência
```

---

## Como Usar

```bash
git clone https://github.com/ItamarIliuk/summit-ia-joinville-2026.git
cd summit-ia-joinville-2026
```

---

## Contato

**Profa. Dra. Itamar Iliuk** · LABRIOT — UTFPR Ponta Grossa · NVIDIA Omniverse Ambassador

## Licença

[Creative Commons BY-NC-SA 4.0](LICENSE)
