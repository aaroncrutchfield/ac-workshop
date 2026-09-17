# Generation and editing example

Verified on September 17, 2026 using Codex CLI 0.153.4 on macOS, through the bundled Python wrapper. These images were produced by two real CLI runs, not the desktop image-generation tool. This verifies the wrapper's generation and reference-image paths; it is not a separate end-to-end test of Claude Code's skill discovery.

## Generate

Output: `mug-orange.png`

Prompt:

> Generate exactly one square image: a simple orange ceramic mug on a charcoal desk, soft window light from the left, eye-level view, uncluttered composition. No lettering, no logos. Editorial product photograph.

The wrapper added its instruction to use the built-in image tool, produce one image, and leave file placement to Python.

## Edit

Reference: `mug-orange.png`. Output: `mug-blue.png`.

Prompt:

> Edit this image. Preserve the mug shape, handle, camera angle, lighting, shadow, and charcoal desk background. Change only the mug glaze from orange to cobalt blue. Produce one image.

## Reproduce

Run the terminal commands from the parent README with these prompts, using fresh output paths. Generation is nondeterministic; do not expect byte-identical results.

## Observed result

Both runs returned an image at the requested path. Visual inspection confirmed an orange mug followed by a cobalt-blue mug with consistent framing and scene. Glaze texture and reflections vary; this is not a pixel-identical color replacement. Both PNGs are 1254 x 1254 pixels.
