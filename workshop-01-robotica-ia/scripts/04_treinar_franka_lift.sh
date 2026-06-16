#!/bin/bash
# =============================================================================
# Exemplo 3b: Treinar Franka Panda — Lift (pegar e levantar cubo)
# Summit de IA Joinville 2026
# =============================================================================

TASK="Isaac-Lift-Cube-Franka-v0"
NUM_ENVS=4096
MAX_ITER=2000        # Lift precisa de mais iterações que Reach
RL_LIB="rsl_rl"

echo "============================================"
echo " Treinando: $TASK (Lift — tarefa mais complexa)"
echo " NOTA: Requer ~2000 iterações para convergir"
echo "============================================"

python scripts/reinforcement_learning/${RL_LIB}/train.py \
    --task ${TASK} \
    --num_envs ${NUM_ENVS} \
    --max_iterations ${MAX_ITER} \
    --headless

echo ""
echo "Para visualizar: python scripts/reinforcement_learning/${RL_LIB}/play.py --task ${TASK} --num_envs 1"
