"""Export the hub and component sources without Git metadata or ignored outputs."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
config = json.loads((ROOT / 'repositories.json').read_text(encoding='utf-8'))
output = ROOT / 'dist' / f'Nitracord-source-{config["version"]}.zip'
output.parent.mkdir(exist_ok=True)
entries = {}
for component in config['repositories']:
    repo = (ROOT / component['path']).resolve()
    if not (repo / '.git').is_dir():
        raise SystemExit(f'Missing independent Git checkout: {repo}')
    listing = subprocess.check_output(
        ['git', '-C', str(repo), 'ls-files', '--cached', '--others', '--exclude-standard', '-z']
    ).decode('utf-8')
    for name in listing.split('\0'):
        if not name:
            continue
        file = repo / name
        if file.is_symlink() or not file.resolve().is_relative_to(repo):
            raise SystemExit(f'Unsupported source link: {file}')
        if not file.is_file():
            continue
        relative = file.relative_to(ROOT)
        if any(part in {'.git', '.gradle', '.signing', 'build', 'dist', 'node_modules', '.tool-cache'} for part in relative.parts):
            raise SystemExit(f'Generated/private path included in Git sources: {relative}')
        if file.name == 'local.properties' or file.suffix.lower() in {'.apk', '.apkm', '.apks', '.aab', '.jks', '.keystore', '.p12', '.pfx'}:
            raise SystemExit(f'Local artifact included in Git sources: {relative}')
        entries['Nitracord/' + relative.as_posix()] = file
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, file in sorted(entries.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = (0o100755 if file.name == 'gradlew' else 0o100644) << 16
        archive.writestr(info, file.read_bytes())
digest = hashlib.sha256(output.read_bytes()).hexdigest()
output.with_suffix('.zip.sha256').write_text(f'{digest}  {output.name}\n', encoding='utf-8')
print(f'Exported {len(entries)} source files: {output}')
