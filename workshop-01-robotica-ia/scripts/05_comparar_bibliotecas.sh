#!/bin/bash
# =============================================================================
# Desafio: Comparar as 4 bibliotecas de RL no mesmo ambiente
# Summit de IA Joinville 2026
#
# Execute cada bloco separadamente e compare no TensorBoard
# =============================================================================

TASK="Isaac-Velocity-Flat-Anymal-D-v0"
NUM_ENVS=4096
MAX_ITER=300

echo "============================================"
echo " Comparando bibliotecas de RL"
echo " Task: $TASK"
echo "============================================"
echo ""
echo "Execute cada comando em um terminal separado:"
echo ""
echo "# RSL-RL"
echo "python scripts/reinforcement_learning/rsl_rl/train.py --task ${TASK} --num_envs ${NUM_ENVS} --max_iterations ${MAX_ITER} --headless"
echo ""
echo "# SKRL"
echo "python scripts/reinforcement_learning/skrl/train.py --task ${TASK} --num_envs ${NUM_ENVS} --max_iterations ${MAX_ITER} --headless"
echo ""
echo "# RL-Games"
echo "python scripts/reinforcement_learning/rl_games/train.py --task ${TASK} --num_envs ${NUM_ENVS} --max_iterations ${MAX_ITER} --headless"
echo ""
echo "# Stable-Baselines3"
echo "python scripts/reinforcement_learning/sb3/train.py --task ${TASK} --num_envs ${NUM_ENVS} --max_iterations ${MAX_ITER} --headless"
echo ""
echo "# TensorBoard (depois de rodar todos)"
echo "tensorboard --logdir logs/"
