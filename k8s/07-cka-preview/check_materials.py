"""Check k8s links/shell blocks and YAML syntax and lab isolation.

Run from any directory: python3 k8s/07-cka-preview/check_materials.py
Requires PyYAML. This is an offline content check, not a live cluster test.
"""
from pathlib import Path
import json
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
        for section in ('## 먼저 이해할 것', '## 1. 구축하고 관찰하기', '## 2. 직접 바꿔보기', '## 3. 검증하기', '## 4. 정리 및 재실행', '## 스스로 설명할 질문'):
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
            kind = doc['kind']
            if kind in ('Deployment', 'ReplicaSet', 'DaemonSet', 'StatefulSet', 'Job'):
                spec = doc['spec']
                template = spec['template']
            elif kind == 'CronJob':
                spec = doc['spec']['jobTemplate']['spec']
                template = spec['template']
            elif kind == 'Pod':
                spec = {}
                template = doc
            else:
                continue
            labels = template.get('metadata', {}).get('labels', {})
            selector = spec.get('selector', {}).get('matchLabels', {})
            if any(labels.get(k) != v for k, v in selector.items()):
                errors.append(f'{path}: selector does not match Pod')
            pod_spec = template['spec']
            volumes = {v['name'] for v in pod_spec.get('volumes', [])}
            volumes.update(v['metadata']['name'] for v in spec.get('volumeClaimTemplates', []))
            for container in pod_spec.get('containers', []) + pod_spec.get('initContainers', []):
                for mount in container.get('volumeMounts', []):
                    if mount['name'] not in volumes:
                        errors.append(f'{path}: missing volume {mount["name"]}')
    except yaml.YAMLError as e:
        errors.append(f'{path}: {e}')

# Canonical curriculum after the 08/09 consolidation.
# No standalone 8-stage curriculum or duplicate internals directory is required.
groups = ('00-foundation', '01-core-objects', '02-controllers',
          '03-pod-deep-dive', '04-storage-security', '05-advanced',
          '06-architecture')
canonical = [p for group in groups for p in (base.parent / group).glob('*/README.md')]
cka = list(base.glob('[0-9][0-9]-*/README.md'))
admin = list((base.parent / '10-cluster-admin').glob('[0-9][0-9]-*/README.md'))
if len(canonical) != 42 or len(cka) != 16 or len(admin) != 7:
    errors.append(f'Curriculum count mismatch: base={len(canonical)}, CKA={len(cka)}, admin={len(admin)}')
if (base.parent / '08-independent').exists() or (base.parent / '09-internals').exists():
    errors.append('Obsolete independent/internals directories still exist')
for p in canonical + cka + admin:
    if not p.is_file():
        errors.append(f'Missing lab: {p}')

labs = [p for p in base.iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name)]
if len(labs) != 16:
    errors.append(f'Expected 16 labs, got {len(labs)}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'OK: {len(labs)} labs, {docs} documents, {objects} YAML objects, {shells} shell blocks; relative links checked across k8s/')
