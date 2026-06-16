"""
Configuração Programática de Conveyor Belt — Digital Twin Workshop
Summit de IA Joinville 2026

Demonstra como criar e configurar esteiras de transporte
programaticamente via Python API do Isaac Sim.

Uso:
    ./python.sh setup_conveyor.py
"""

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

import numpy as np
import omni.usd
from pxr import UsdGeom, Gf

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

# Parâmetros da esteira
CONVEYOR_LENGTH = 3.0       # metros
CONVEYOR_WIDTH = 0.6        # metros
CONVEYOR_HEIGHT = 0.8       # metros (altura do chão)
CONVEYOR_SPEED = 0.5        # m/s
NUM_BOXES = 5               # caixas para teste

# ============================================================================
# FUNÇÕES
# ============================================================================

def create_simple_conveyor(stage, position, direction="x"):
    """
    Cria uma esteira simplificada usando um cubo com propriedades de conveyor.

    Em um cenário real, use os assets de conveyor do Isaac Sim:
    Isaac/Props/Conveyors/

    Args:
        stage: USD stage
        position: (x, y, z) posição da esteira
        direction: eixo de movimento ("x", "y", ou "z")
    """
    # Criar o mesh da esteira
    conveyor_path = "/World/ConveyorSystem/Belt_01"
    conveyor_prim = UsdGeom.Cube.Define(stage, conveyor_path)

    # Dimensões
    conveyor_prim.GetSizeAttr().Set(1.0)
    xform = UsdGeom.Xformable(conveyor_prim)
    xform.AddTranslateOp().Set(Gf.Vec3d(*position))
    xform.AddScaleOp().Set(Gf.Vec3d(
        CONVEYOR_LENGTH,
        CONVEYOR_WIDTH,
        0.05  # espessura da esteira
    ))

    print(f"Esteira criada em {position}")
    print(f"Direção: {direction} | Velocidade: {CONVEYOR_SPEED} m/s")

    return conveyor_path


def create_test_boxes(stage, start_position, count=5):
    """Cria caixas de teste sobre a esteira."""
    boxes = []
    for i in range(count):
        box_path = f"/World/Boxes/test_box_{i:02d}"
        box = UsdGeom.Cube.Define(stage, box_path)
        box.GetSizeAttr().Set(1.0)

        xform = UsdGeom.Xformable(box)
        pos = Gf.Vec3d(
            start_position[0] - i * 0.4,  # espaçamento entre caixas
            start_position[1],
            start_position[2] + 0.15       # acima da esteira
        )
        xform.AddTranslateOp().Set(pos)
        xform.AddScaleOp().Set(Gf.Vec3d(0.2, 0.15, 0.1))

        boxes.append(box_path)
        print(f"  Caixa {i+1}/{count} criada em {pos}")

    return boxes


def main():
    """Configura a cena com esteira e caixas."""
    stage = omni.usd.get_context().get_stage()

    print("\n" + "=" * 60)
    print("  Setup de Conveyor Belt — Digital Twin Workshop")
    print("=" * 60 + "\n")

    # Criar esteira
    conveyor_pos = (0.0, 0.0, CONVEYOR_HEIGHT)
    belt_path = create_simple_conveyor(stage, conveyor_pos)

    # Criar caixas de teste
    print("\nCriando caixas de teste...")
    box_start = (CONVEYOR_LENGTH / 2 - 0.3, 0.0, CONVEYOR_HEIGHT)
    boxes = create_test_boxes(stage, box_start, NUM_BOXES)

    print(f"\n  Total: {len(boxes)} caixas criadas")
    print("\n  NOTA: Para conveyor belts com física completa,")
    print("  use o Conveyor Track Builder (Tools > Conveyor Track Builder)")
    print("  com os assets de Isaac/Props/Conveyors/")
    print("\n  Pressione PLAY para iniciar a simulação\n")

    while simulation_app.is_running():
        simulation_app.update()

    simulation_app.close()


if __name__ == "__main__":
    main()
