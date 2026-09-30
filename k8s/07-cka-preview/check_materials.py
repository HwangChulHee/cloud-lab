"""Check k8s links/shell blocks and YAML syntax and lab isolation.

Run from any directory: python3 k8s/07-cka-preview/check_materials.py
Requires PyYAML. This is an offline content check, not a live cluster test.
"""
from pathlib import Path
import re
import subprocess
import yaml

base = Path(__file__).resolve().parent
errors = []
docs = shells = objects = 0
for path in base.parent.rglob('*.md'):
    text = path.read_text()
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text):
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        target = target.split('#')[0]
        if target and not (path.parent / target).exists():
            errors.append(f'{path.relative_to(base.parent)}: broken link {target}')
    docs += 1
    for script in re.findall(r'```bash\n(.*?)\n```', text, re.S):
        shells += 1
        result = subprocess.run(['bash', '-n'], input=script, text=True, capture_output=True)
        if result.returncode:
            errors.append(f'{path.relative_to(base.parent)}: shell syntax: {result.stderr.strip()}')
    if base in path.parents and path.name == 'README.md' and path.parent != base:
        for section in ('## 먼저 이해할 것', '## 1. 구축하고 관찰하기', '## 2. 직접 바꿔보기', '## 3. 검증하기', '## 4. 정리 및 재실행', '## 강의에서 확인할 질문'):
            if section not in text:
                errors.append(f'{path.parent.name}: missing {section}')

for path in base.parent.rglob('*.yaml'):
    try:
        for doc in yaml.safe_load_all(path.read_text()):
            if not isinstance(doc, dict) or not all(k in doc for k in ('apiVersion', 'kind', 'metadata')):
                errors.append(f'{path}: malformed object')
                continue
            objects += 1
            namespace = doc['metadata'].get('namespace')
            if namespace and not namespace.startswith(('preview-', 'lab-')):
                errors.append(f'{path}: non-lab namespace {namespace}')
            if doc['kind'] == 'Deployment':
                spec = doc['spec']
                labels = spec['template']['metadata']['labels']
                if any(labels.get(k) != v for k, v in spec['selector']['matchLabels'].items()):
                    errors.append(f'{path}: selector does not match Pod')
                pod = spec['template']['spec']
                volumes = {v['name'] for v in pod.get('volumes', [])}
                for container in pod.get('containers', []) + pod.get('initContainers', []):
                    for mount in container.get('volumeMounts', []):
                        if mount['name'] not in volumes:
                            errors.append(f'{path}: missing volume {mount["name"]}')
    except yaml.YAMLError as e:
        errors.append(f'{path}: {e}')

labs = [p for p in base.iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name)]
if len(labs) != 16:
    errors.append(f'Expected 16 labs, got {len(labs)}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'OK: {len(labs)} labs, {docs} documents, {objects} YAML objects, {shells} shell blocks; relative links checked across k8s/')
