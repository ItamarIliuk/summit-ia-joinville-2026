#!/bin/bash
# =============================================================================
# Exemplo 3a: Treinar Franka Panda — Reach (alcançar posição alvo)
# Summit de IA Joinville 2026
# =============================================================================

TASK="Isaac-Reach-Franka-v0"
NUM_ENVS=4096
MAX_ITER=500
RL_LIB="rsl_rl"

echo "============================================"
echo " Treinando: $TASK (Reach — tarefa mais simples)"
echo "============================================"

python scripts/reinforcement_learning/${RL_LIB}/train.py \
    --task ${TASK} \
    --num_envs ${NUM_ENVS} \
    --max_iterations ${MAX_ITER} \
    --headless

echo ""
echo "Para visualizar: python scripts/reinforcement_learning/${RL_LIB}/play.py --task ${TASK} --num_envs 1"
