#!/bin/bash
# =============================================================================
# Exemplo 1: Treinar Quadrúpede ANYmal-D — Locomoção em terreno plano
# Summit de IA Joinville 2026
# =============================================================================

# Configuração
TASK="Isaac-Velocity-Flat-Anymal-D-v0"
NUM_ENVS=4096        # Reduzir para 1024 se GPU < 16GB VRAM
MAX_ITER=500         # ~10 min na RTX 4090
RL_LIB="rsl_rl"     # Opções: rsl_rl, skrl, rl_games, sb3

echo "============================================"
echo " Treinando: $TASK"
echo " Biblioteca: $RL_LIB"
echo " Ambientes: $NUM_ENVS"
echo " Iterações: $MAX_ITER"
echo "============================================"

# Treinar
python scripts/reinforcement_learning/${RL_LIB}/train.py \
    --task ${TASK} \
    --num_envs ${NUM_ENVS} \
    --max_iterations ${MAX_ITER} \
    --headless

echo ""
echo "Treinamento finalizado!"
echo "Para visualizar: python scripts/reinforcement_learning/${RL_LIB}/play.py --task ${TASK} --num_envs 1"
echo "Para TensorBoard: tensorboard --logdir logs/${RL_LIB}/"
