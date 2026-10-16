"""Protect password fields in the confirmed 1080p demo; never overwrite the source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ffmpeg', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    args = parser.parse_args()
    source, target = args.input.resolve(), args.output.resolve()
    if not source.is_file() or source == target or target.exists():
        parser.error('Source must exist; output must be a different, new file.')
    probe = subprocess.run([str(args.ffmpeg), '-hide_banner', '-i', str(source)],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
    if '1920x1080' not in probe.stderr:
        parser.error('These reviewed redaction coordinates require the confirmed 1920x1080 source.')
    before = digest(source)
    enable = "between(t,922,936)"
    # Coordinates cover the three password fields and the password-manager popup.
    boxes = [(320, 580, 630, 70), (950, 580, 650, 70),
             (320, 686, 630, 70), (1080, 646, 630, 240), (330, 115, 1250, 48)]
    filters = [f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black:t=fill:enable='{enable}'"
               for x, y, w, h in boxes]
    filters.append("drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':"
                   "text='Credenciales ocultas por seguridad (edicion del video)':"
                   "x=345:y=125:fontsize=25:fontcolor=white:enable='" + enable + "'")
    target.parent.mkdir(parents=True, exist_ok=True)
    command = [str(args.ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-n',
               '-i', str(source), '-map', '0:v:0', '-map', '0:a:0?',
               '-vf', ','.join(filters), '-c:v', 'libx264', '-preset', 'ultrafast',
               '-crf', '20', '-pix_fmt', 'yuv420p', '-threads', '4',
               '-r', '30', '-fps_mode', 'cfr', '-c:a', 'copy',
               '-map_metadata', '-1', '-movflags', '+faststart', str(target)]
    subprocess.run(command, check=True)
    unchanged = digest(source) == before
    if not unchanged:
        raise RuntimeError('Original file integrity check failed.')
    result = {'source_file': source.name, 'output_file': target.name,
              'source_sha256': before, 'output_sha256': digest(target),
              'source_unchanged': unchanged, 'audio': 'Copied without re-encoding',
              'output_fps': 30, 'redaction_seconds': [922, 936],
              'redaction_label': 'Credenciales ocultas por seguridad (edicion del video)',
              'purpose': 'Protect visible credentials; no cuts or changes to test results.',
              'visual_output_reviewed': False, 'full_content_and_audio_reviewed': False,
              'limit': 'Protects reviewed screen coordinates, not an automatic secret detector.'}
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
