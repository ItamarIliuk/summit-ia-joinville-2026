#!/bin/bash
# =============================================================================
# Exemplo 2: Treinar Humanoide Unitree H1 — Locomoção
# Summit de IA Joinville 2026
# =============================================================================

TASK="Isaac-Velocity-Flat-H1-v0"
NUM_ENVS=4096
MAX_ITER=500
RL_LIB="rsl_rl"

echo "============================================"
echo " Treinando: $TASK"
echo " Biblioteca: $RL_LIB"
echo " Ambientes: $NUM_ENVS"
echo " Iterações: $MAX_ITER"
echo "============================================"

python scripts/reinforcement_learning/${RL_LIB}/train.py \
    --task ${TASK} \
    --num_envs ${NUM_ENVS} \
    --max_iterations ${MAX_ITER} \
    --headless

echo ""
echo "Para visualizar: python scripts/reinforcement_learning/${RL_LIB}/play.py --task ${TASK} --num_envs 1"
