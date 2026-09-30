import argparse
from pathlib import Path
import yaml

parser = argparse.ArgumentParser(description="Extract CRDs from a rendered chart, or assert none exist")
parser.add_argument("--expect-none", action="store_true")
parser.add_argument("source")
parser.add_argument("destination", nargs="?")
args = parser.parse_args()
docs = [d for d in yaml.safe_load_all(Path(args.source).read_text()) if isinstance(d, dict) and d.get("kind") == "CustomResourceDefinition"]
if args.expect_none:
    if docs:
        raise SystemExit(f"Unexpected CRDs: {len(docs)}")
    print("OK: no CRDs")
else:
    if not docs or not args.destination:
        raise SystemExit("CRDs and destination are required")
    Path(args.destination).write_text(yaml.safe_dump_all(docs, sort_keys=False))
    print(f"Extracted {len(docs)} CRDs")
