# Blender scene skill

## Use when

The request needs 3D geometry, cameras, lights, materials, GLB export or a
rendered image.

## Tool routing

1. Prepare a JSON scene specification.
2. Use `blender.run --operation create-scene` to create a `.blend`.
3. Use `blender.run --operation render` to create a still image.
4. Keep generated files inside the current job output directory.

Never pass arbitrary shell commands to Blender. Only invoke the checked-in
`adapters/blender/agent_blender.py` adapter.
