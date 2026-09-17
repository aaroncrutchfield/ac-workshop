#!/usr/bin/env python3
"""Generate one image with Codex and copy only this run's artifact to --out."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid


def select_image(events, codex_home):
    threads = {e.get('thread_id') for e in events if e.get('type') == 'thread.started'}
    if len(threads) != 1:
        raise ValueError('Expected one thread.started event; cannot identify this run safely.')
    thread = threads.pop()
    try:
        uuid.UUID(thread)
    except (ValueError, TypeError, AttributeError):
        raise ValueError('Invalid Codex thread ID.')
    root = (codex_home / 'generated_images').resolve()
    directory = root / thread
    if directory.is_symlink():
        raise ValueError('Refusing a symlinked image directory.')
    candidates = [p for p in directory.glob('*') if p.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'} and p.is_file() and not p.is_symlink() and p.stat().st_size]
    if len(candidates) != 1:
        raise ValueError(f'Expected exactly one image in this run; found {len(candidates)}. No file copied.')
    return candidates[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--ref', action='append', default=[], type=Path)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('prompt')
    args = parser.parse_args()
    out = args.out.expanduser().absolute()
    if out.exists():
        parser.error('Output already exists. Choose a new filename; originals are never overwritten.')
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    refs = [p.expanduser().resolve() for p in args.ref]
    for ref in refs:
        if not ref.is_file():
            parser.error(f'Reference does not exist: {ref}')
    if not shutil.which('codex'):
        parser.error('Install Codex CLI first: npm install -g @openai/codex')
    if subprocess.run(['codex', 'login', 'status'], capture_output=True).returncode:
        parser.error('Run codex login, then retry.')
    home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))).expanduser().resolve()
    instruction = ('Use the built-in image generation tool to produce exactly ONE final image. '
                   'Do not use browser tools, API scripts, or a substitute generator. '
                   'Do not copy files or change project files. Return the generated image path.\n\n' + args.prompt)
    # A fresh working directory avoids reading unrelated project instructions.
    with tempfile.TemporaryDirectory(prefix='codex-images-') as work:
        command = ['codex', 'exec', '--ignore-user-config', '--sandbox', 'read-only',
                   '--skip-git-repo-check', '--enable', 'image_generation', '--json', '-C', work]
        for ref in refs:
            command += ['--image', str(ref)]
        command += ['--', instruction]
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            print('Codex timed out. No file copied. Check usage before retrying.', file=sys.stderr)
            return 1
    events = []
    for line in run.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if run.returncode or any(e.get('type') in {'error', 'turn.failed'} for e in events):
        print('Codex failed. No file copied. Check your login, image access, and CLI version.', file=sys.stderr)
        return 1
    try:
        source = select_image(events, home)
        if out.suffix.lower() != source.suffix.lower():
            raise ValueError(f'Generated {source.suffix}; choose an output with that extension. No conversion performed.')
        out.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as src, out.open('xb') as dest:
            shutil.copyfileobj(src, dest)
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
