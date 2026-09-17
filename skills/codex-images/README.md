# Codex Images

**Stay in Claude Code. Generate and edit images with Codex CLI.**

This self-contained skill lets a shell-based agent call Codex's image tool and save the result to a chosen project path. No browser automation or other toolkit skills required.

## See it work

![Generate an orange mug, then edit it to blue: real Codex CLI outputs side by side.](assets/generate-and-edit.png)

Real outputs from this wrapper, not mockups. The edit request changed the glaze color while asking to preserve the scene. See [prompts and verification](examples/README.md). Results vary; inspect edits for unintended changes.

## Requirements

- Python 3.10 or newer (standard library only).
- Codex CLI installed and signed in with `codex login`.
- Account access to Codex image generation. Account limits and usage apply.
- An agent that can run shell commands, such as Claude Code, or a terminal.

Tested with Codex CLI **0.153.4 on macOS**. CI is configured to test Linux and macOS file handling; live Linux generation has not been verified. Windows is not currently tested. Feature flags and event formats can change between CLI releases.

## Install just this skill

[Download codex-images.zip](https://github.com/aaroncrutchfield/ac-workshop/releases/download/codex-images-v0.1.1/codex-images.zip), unzip it, and put the entire `codex-images` folder inside your project's `.claude/skills/` directory:

```text
my-project/
  .claude/skills/codex-images/
    SKILL.md
    README.md
    scripts/codex_image.py
    references/prompting.md
    examples/
    LICENSE
```

Keep its supporting files together. You do not need to clone the workshop or install another plugin. The README is for you; SKILL.md contains the agent's workflow.

Then ask Claude Code:

> Use codex-images to generate an orange mug on a charcoal desk. Save it to assets/mug.png.

For an edit:

> Use codex-images to edit assets/mug.png. Change only the mug to cobalt blue and save it as assets/mug-blue.png.

Claude Code still needs permission to run the command under your normal settings. This skill does not bypass those settings.

## Use from a terminal

Run from your project root after installation:

```bash
python3 .claude/skills/codex-images/scripts/codex_image.py \
  --out assets/mug.png \
  -- 'An orange ceramic mug on a charcoal desk. Soft window light from the left. No text or logos.'
```

```bash
python3 .claude/skills/codex-images/scripts/codex_image.py \
  --ref assets/mug.png \
  --out assets/mug-blue.png \
  -- 'Keep the scene and mug shape unchanged. Change only the mug glaze to cobalt blue.'
```

## How it works

![How it works: your request in Claude Code goes to the bundled Python wrapper, which calls Codex CLI to generate or edit an image, then copies that run's image into your project.](assets/how-it-works.png)

The wrapper explicitly selects the read-only shell sandbox for the child Codex run. It ignores the user's CLI config to avoid inheriting unrelated settings; authentication remains in place. After the run, Python copies exactly one generated image from the matching thread directory into your chosen output location.

It never scans other runs for a newer image, silently overwrites an output, or automatically retries a generation. The wrapper is a local program with your filesystem permissions; the child's sandbox does not sandbox the wrapper itself.

## Troubleshooting

- **CLI missing or not signed in:** install Codex CLI and run `codex login` first.
- **Image generation unavailable:** check account access and CLI compatibility. Supporting `--enable` alone does not prove image generation is available.
- **No image or multiple images:** the wrapper stops rather than guessing. Review the run before spending usage on another attempt.
- **Output exists:** choose a new filename. There is intentionally no overwrite switch.
- **Wrong extension:** use the extension the error reports; the wrapper does not disguise a JPEG as a PNG.
- **Timeout:** default is 600 seconds; override with `--timeout 900` if needed. Check the prior run before retrying.

## License

[MIT](LICENSE). The downloadable skill includes a copy. Generated images are demonstration artifacts; no claim of exclusivity is made.
