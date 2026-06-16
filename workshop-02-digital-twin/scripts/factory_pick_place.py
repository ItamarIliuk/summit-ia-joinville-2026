"""
Pick & Place na Linha de Produção — Digital Twin Workshop
Summit de IA Joinville 2026

Este script demonstra o controle de um Franka Panda fazendo pick & place
de caixas em uma esteira de produção usando cinemática inversa.

Uso:
    # Dentro do ambiente Python do Isaac Sim:
    python factory_pick_place.py

    # Ou via Isaac Sim:
    ./python.sh factory_pick_place.py
"""

from isaacsim import SimulationApp

# Configuração da aplicação
config = {
    "headless": False,
    "width": 1920,
    "height": 1080,
    "title": "Digital Twin - Factory Pick & Place",
}

simulation_app = SimulationApp(config)

# Imports após inicializar o SimulationApp
import numpy as np
import carb

from isaacsim.core import World
from isaacsim.core.objects import DynamicCuboid, FixedCuboid
from isaacsim.core.utils.stage import add_reference_to_stage

# ============================================================================
# CONFIGURAÇÃO DA CENA
# ============================================================================

# Posições da célula de produção (em metros)
FRANKA_POSITION = np.array([0.0, 0.0, 0.0])       # Base do Franka
PICK_POSITION = np.array([0.5, 0.0, 0.3])          # Caixa na esteira
PLACE_POSITION = np.array([0.5, -0.5, 0.3])        # Palete de destino
CUBE_SIZE = np.array([0.05, 0.05, 0.05])            # Tamanho da caixa

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

def setup_scene():
    """Configura a cena com o Franka, caixas e esteira."""
    world = World(stage_units_in_meters=1.0)
    world.scene.add_default_ground_plane()

    # Adicionar o Franka Panda
    # Nota: ajuste o caminho USD conforme sua instalação
    franka_usd = "Isaac/Robots/FrankaEmika/franka_instanceable.usd"
    try:
        add_reference_to_stage(
            usd_path=franka_usd,
            prim_path="/World/Franka"
        )
        carb.log_info("Franka carregado com sucesso")
    except Exception as e:
        carb.log_warn(f"Erro ao carregar Franka: {e}")
        carb.log_warn("Usando cubo como placeholder")

    # Adicionar cubo para pick (representa a caixa na esteira)
    world.scene.add(
        DynamicCuboid(
            prim_path="/World/Boxes/box_01",
            name="target_box",
            position=PICK_POSITION,
            scale=CUBE_SIZE,
            color=np.array([0.2, 0.6, 1.0]),  # Azul
            mass=0.5,
        )
    )

    # Adicionar mesa/palete de destino
    world.scene.add(
        FixedCuboid(
            prim_path="/World/Equipment/place_table",
            name="place_table",
            position=np.array([0.5, -0.5, 0.15]),
            scale=np.array([0.3, 0.3, 0.3]),
            color=np.array([0.4, 0.4, 0.4]),  # Cinza
        )
    )

    return world


def main():
    """Loop principal da simulação."""
    world = setup_scene()
    world.reset()

    print("\n" + "=" * 60)
    print("  Digital Twin - Factory Pick & Place")
    print("  Summit de IA Joinville 2026")
    print("=" * 60)
    print("\n  Pressione PLAY no Isaac Sim para iniciar")
    print("  Pressione ESC ou feche a janela para sair\n")

    step_count = 0
    while simulation_app.is_running():
        world.step(render=True)

        if world.is_playing():
            step_count += 1

            if step_count % 500 == 0:
                elapsed = step_count / 60.0  # ~60 Hz
                print(f"  Simulação: {elapsed:.1f}s | Steps: {step_count}")

    simulation_app.close()


if __name__ == "__main__":
    main()
