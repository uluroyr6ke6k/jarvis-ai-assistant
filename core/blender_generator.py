from __future__ import annotations

import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class BlenderAsset:
    scene_name: str
    prompt: str
    setup_script: str
    render_settings: dict
    output_dir: str
    created_at: str


class BlenderGenerator:
    """Creates Blender scene prompts and setup scripts for 3D generation workflows."""

    def __init__(self, output_dir: str = "blender_assets"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_prompt(self, subject: str, style: str = "futuristic industrial") -> str:
        return (
            f"{subject}, {style}, highly detailed, cinematic lighting, realistic materials, "
            "clean geometry, premium product design, dramatic perspective"
        )

    def build_setup_script(self, subject: str) -> str:
        return f'''
import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 1))
obj = bpy.context.active_object
obj.name = "{subject.replace(' ', '_')}_asset"

mat = bpy.data.materials.new(name="Material")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.1, 0.7, 1.0, 1.0)
obj.data.materials.append(mat)

bpy.context.scene.render.filepath = "//renders/{subject.replace(' ', '_')}_render.png"
'''

    def create_asset(self, subject: str, style: str = "futuristic industrial") -> BlenderAsset:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scene_name = f"scene_{timestamp}_{subject.replace(' ', '_')}"
        output_dir = os.path.join(self.output_dir, scene_name)
        os.makedirs(output_dir, exist_ok=True)

        return BlenderAsset(
            scene_name=scene_name,
            prompt=self.create_prompt(subject, style),
            setup_script=self.build_setup_script(subject),
            render_settings={
                "engine": "CYCLES",
                "samples": 128,
                "resolution_x": 1920,
                "resolution_y": 1080,
            },
            output_dir=output_dir,
            created_at=datetime.now().isoformat(),
        )

    def create_batch(self, subjects: List[str]) -> List[BlenderAsset]:
        return [self.create_asset(subject) for subject in subjects]

    def export_summary(self, assets: List[BlenderAsset]) -> List[dict]:
        return [asdict(asset) for asset in assets]
