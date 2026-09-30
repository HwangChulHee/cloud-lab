#!/usr/bin/env python3
"""Wait for a named Pod to exist and be Ready, optionally with a new UID.

Run from the repository root. Uses the current kubectl context; never changes it.
Only absence (--ignore-not-found) is retried. API/authentication errors fail early.
"""
import argparse
import json
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('namespace')
    parser.add_argument('name')
    parser.add_argument('--different-uid', default=None)
    parser.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args()
    if args.timeout <= 0 or args.different_uid == '':
        parser.error('timeout must be positive; different-uid must not be empty')
    deadline = time.monotonic() + args.timeout
    state = 'not observed'
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        try:
            result = subprocess.run(
                ['kubectl', '-n', args.namespace, 'get', 'pod', args.name,
                 '--ignore-not-found', '-o', 'json', '--request-timeout=10s'],
                capture_output=True, text=True, timeout=min(12, remaining),
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            print(f'kubectl failed: {error}', file=sys.stderr)
            return 1
        if result.returncode:
            print(result.stderr.strip() or 'kubectl failed', file=sys.stderr)
            return 1
        if not result.stdout.strip():
            state = 'Pod not created yet'
        else:
            try:
                pod = json.loads(result.stdout)
            except json.JSONDecodeError as error:
                print(f'Invalid kubectl JSON: {error}', file=sys.stderr)
                return 1
            metadata = pod.get('metadata', {})
            uid = metadata.get('uid')
            ready = any(c.get('type') == 'Ready' and c.get('status') == 'True'
                        for c in pod.get('status', {}).get('conditions', []))
            state = f'uid={uid}, Ready={ready}, deleting={bool(metadata.get("deletionTimestamp"))}'
            if uid and ready and not metadata.get('deletionTimestamp') and (
                args.different_uid is None or uid != args.different_uid
            ):
                print(f'{args.namespace}/{args.name}: {state}')
                return 0
        time.sleep(min(1, max(0, deadline - time.monotonic())))
    print(f'Timed out waiting for {args.namespace}/{args.name}: {state}. '
          'Check kubectl describe pod and PVC Events before continuing.', file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
