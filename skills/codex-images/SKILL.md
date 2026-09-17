---
name: codex-images
description: Generate or edit an image through the Codex CLI and save it to a chosen project path. Use when the user wants image creation or a targeted image edit from a shell-based agent such as Claude Code.
---

# Codex Images

Use the bundled Python wrapper to generate one image per request. No other skills or plugins are required. Requires Python 3.10+, Codex CLI, and a signed-in account with access to Codex image generation. This uses the user's Codex account and usage allowance; it is not a free image API.

## Prepare

Clarify the desired result and destination only when missing details matter. For edits, inspect the source image and identify what must stay unchanged. Read [prompting.md](references/prompting.md) when composing the prompt.

The user requesting generation authorizes the ordinary generation run. Do not generate unrelated variants or repeatedly retry without considering usage. Never install tools or change login/configuration silently.

## Run

Resolve the script relative to this SKILL.md, not the current working directory:

```bash
python3 /path/to/codex-images/scripts/codex_image.py \
  --out /absolute/project/assets/hero.png \
  -- 'Generate one image: a warm desk scene, simple composition, space on the left for a headline.'
```

For edits, pass an absolute reference path; multiple --ref arguments are supported:

```bash
python3 /path/to/codex-images/scripts/codex_image.py \
  --ref /absolute/project/assets/hero.png \
  --out /absolute/project/assets/hero-blue.png \
  -- 'Keep the composition and objects unchanged. Change only the orange mug to cobalt blue.'
```

The wrapper runs Codex with an explicit read-only shell sandbox in a temporary directory. It ignores user CLI configuration while retaining authentication. It finds the generated image only in the thread identified by this run's JSON events, then copies it to --out. The copy is performed by Python outside the child agent's sandbox. Existing outputs are never overwritten.

## Verify and report

Open the output and check it against the request. File creation proves generation completed, not visual accuracy. For edits, compare the source and result. Report the actual path and any visible limitation; do not claim perfect identity preservation.

On failure, explain the error. Do not choose the newest file from the global generated_images directory, substitute a different backend, or claim completion. Automatic retries are deliberately omitted.

## Compatibility

Developed against Codex CLI 0.153.4. The image_generation feature and output/event formats can change. See the README's verification record for the tested environment. If the wrapper cannot identify exactly one image, it stops rather than guessing.
