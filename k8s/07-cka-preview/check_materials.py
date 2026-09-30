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

# Every old lab must have an explicit place in the standalone curriculum.
mapping_path = base.parent / '08-independent' / 'curriculum.json'
if mapping_path.exists():
    mapping = json.loads(mapping_path.read_text())
    expected_core = {
        str(p.relative_to(base.parent))
        for group in ('00-foundation', '01-core-objects', '02-controllers',
                      '03-pod-deep-dive', '04-storage-security', '05-advanced', '06-architecture')
        for p in (base.parent / group).glob('*/README.md')
    }
    expected_extensions = {str(p.relative_to(base.parent)) for p in base.glob('[0-9][0-9]-*/README.md')}
    for key, expected in (('foundation_labs', expected_core), ('extension_labs', expected_extensions)):
        rows = mapping[key]
        actual = [row['lab'] for row in rows]
        if len(actual) != len(set(actual)) or set(actual) != expected:
            errors.append(f'{key}: missing/duplicate curriculum mappings')
        for row in rows:
            guide = base.parent / row['guide']
            if not guide.is_file():
                errors.append(f'{row["lab"]}: missing standalone guide')
    completed_guides = set()
    for stage in mapping['stages']:
        if not (base.parent / stage['guide']).is_file():
            errors.append(f'{stage["guide"]}: missing stage')
        if not set(stage['requires']).issubset(completed_guides):
            errors.append(f'{stage["guide"]}: prerequisite appears after stage')
        completed_guides.add(stage['guide'])
    if len(completed_guides) != 8 or len(expected_core) != 42 or len(expected_extensions) != 16:
        errors.append('Expected 8 standalone stages, 42 foundation labs and 16 extension labs')

labs = [p for p in base.iterdir() if p.is_dir() and re.match(r'^\d\d-', p.name)]
if len(labs) != 16:
    errors.append(f'Expected 16 labs, got {len(labs)}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'OK: {len(labs)} labs, {docs} documents, {objects} YAML objects, {shells} shell blocks; relative links checked across k8s/')
