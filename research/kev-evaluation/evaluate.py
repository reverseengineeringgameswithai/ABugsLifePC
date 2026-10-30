#!/usr/bin/env python3
"""Small local-only Kev evidence probe; freeze labels before making requests.

python3 research/kev-evaluation/evaluate.py freeze --out reports/kev/EXP-20261007-001
python3 research/kev-evaluation/evaluate.py run --out reports/kev/EXP-20261007-001

No game execution, writes, model training, or automatic claim promotion.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
KEV = Path('/home/dev/AI/kev')
URL = 'http://127.0.0.1:8021'
LABELS = ['supported', 'contradicted', 'insufficient']
CRITERIA = {
    'supported': 'The supplied evidence establishes the claim, within the exact stated scope.',
    'contradicted': 'The supplied evidence establishes that the claim is false or overstates what was demonstrated.',
    'insufficient': 'The supplied evidence does not settle whether the claim is true. Plausibility, inference and missing tests are not confirmation.',
}
INSTRUCTION = ('Classify this claim using ONLY the evidence in the state. '
               'Respect static versus runtime evidence, tested scope, historical changes, '
               'and explicitly unresolved questions. If the state has no evidence, choose '
               'insufficient. Do not use outside knowledge. Claim: ')
VARIANTS = {
    'primary': LABELS,
    'rotated': ['contradicted', 'insufficient', 'supported'],
    'reversed': list(reversed(LABELS)),
    'no_evidence': LABELS,
}


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def save(path, data):
    with path.open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git_rev(path):
    return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()


def extract(path, headings, preamble):
    data = path.read_bytes()
    lines = data.decode().splitlines(keepends=True)
    starts = [(i, line[3:].strip()) for i, line in enumerate(lines) if line.startswith('## ')]
    chunks = []
    if preamble:
        start = next(i for i, line in enumerate(lines) if line.startswith('# '))
        end = starts[0][0]
        chunks.append({'heading': lines[start][2:].strip(), 'start_line': start + 1,
                       'end_line': end, 'text': ''.join(lines[start:end])})
    for heading in headings:
        matches = [j for j, (_, name) in enumerate(starts) if name == heading]
        if len(matches) != 1:
            raise ValueError(f'{path}: expected one heading {heading!r}')
        j = matches[0]
        start = starts[j][0]
        end = starts[j + 1][0] if j + 1 < len(starts) else len(lines)
        chunks.append({'heading': heading, 'start_line': start + 1, 'end_line': end,
                       'text': ''.join(lines[start:end])})
    return sha(data), chunks


def freeze(out):
    spec_path = Path(__file__).with_name('claims.json')
    spec = read(spec_path)
    out.mkdir(parents=True, exist_ok=False)
    packets = []
    count = 0
    for group in spec['groups']:
        digest, chunks = extract(ROOT / group['source'], group['sections'], group.get('preamble', False))
        claims = []
        for claim, expected, heading, reason in group['claims']:
            if expected not in LABELS or heading not in [c['heading'] for c in chunks]:
                raise ValueError('Invalid label or evidence heading')
            count += 1
            claims.append({'id': f'q{count:02}', 'claim': claim, 'expected': expected,
                           'evidence_heading': heading, 'label_rationale': reason})
        packets.append({'id': group['id'], 'source': group['source'], 'source_sha256': digest,
                        'excerpts': chunks, 'claims': claims})
    assert Counter(c['expected'] for p in packets for c in p['claims']) == dict.fromkeys(LABELS, 12)
    binaries = ['work/copies/BUGS_PC-full-disc/PC/BUGS/bugs.exe',
                'work/copies/studio-1791244451538294368/bugs.exe']
    data = {'experiment': spec['experiment'], 'frozen_at': now(), 'description': spec['description'],
            'ablpc_commit': git_rev(ROOT), 'kev_commit': git_rev(KEV),
            'runner_sha256': sha(Path(__file__).read_bytes()), 'claims_sha256': sha(spec_path.read_bytes()),
            'installation': read(KEV / 'local/provenance.json'),
            'binary_hashes': {p: sha((ROOT / p).read_bytes()) for p in binaries},
            'endpoint': URL, 'instruction': INSTRUCTION, 'criteria': CRITERIA, 'variants': VARIANTS,
            'high_probability_threshold': 0.9, 'packets': packets}
    save(out / 'frozen.json', data)
    print(f'Frozen {count} labels; SHA256 {sha((out / "frozen.json").read_bytes())}', flush=True)


def http(path, payload=None):
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    req = Request(URL + path, data=data, headers={'Content-Type': 'application/json'})
    start = time.perf_counter()
    with urlopen(req, timeout=120) as response:
        result = json.load(response)
        headers = {k: v for k, v in response.headers.items()
                   if k.lower() in ('server-timing', 'x-typesafe-request-id')}
    return result, (time.perf_counter() - start) * 1000, headers


def run(out):
    frozen_path = out / 'frozen.json'
    frozen = read(frozen_path)
    if frozen['runner_sha256'] != sha(Path(__file__).read_bytes()):
        raise ValueError('Runner differs from frozen source')
    save(out / 'run-start.json', {'started_at': now(), 'frozen_sha256': sha(frozen_path.read_bytes())})
    before, _, _ = http('/v1/models')
    save(out / 'models-before.json', before)
    rows, calls = [], []
    for packet in frozen['packets']:
        for variant, order in frozen['variants'].items():
            state = ('No evidence has been supplied.' if variant == 'no_evidence' else
                     'Evidence source: ' + packet['source'] + '\n\n' +
                     '\n'.join(c['text'] for c in packet['excerpts']))
            payload = {'model': 'kev-latest', 'state': state, 'questions': {
                c['id']: {'type': 'choice', 'instructions': frozen['instruction'] + c['claim'],
                          'criteria': {k: frozen['criteria'][k] for k in order}}
                for c in packet['claims']}}
            stem = f'{packet["id"]}-{variant}'
            # Save exact request before sending; expected labels/rationales are never included.
            save(out / f'{stem}-request.json', payload)
            result, elapsed, headers = http('/v1/systemone', payload)
            save(out / f'{stem}-response.json', {'response': result, 'wall_ms': elapsed, 'headers': headers})
            if set(result['answers']) != set(payload['questions']):
                raise ValueError('Missing or extra answer')
            correct = 0
            for claim in packet['claims']:
                answer = result['answers'][claim['id']]
                probs = answer['probabilities']
                if (set(probs) != set(LABELS) or
                    any(not math.isfinite(p) or not 0 <= p <= 1 for p in probs.values()) or
                    abs(sum(probs.values()) - 1) > 0.002 or answer['choice'] not in LABELS):
                    raise ValueError('Invalid probability distribution')
                expected = 'insufficient' if variant == 'no_evidence' else claim['expected']
                matched = answer['choice'] == expected
                correct += matched
                rows.append({'group': packet['id'], 'variant': variant, 'id': claim['id'],
                             'claim': claim['claim'], 'expected': expected, 'predicted': answer['choice'],
                             'correct': matched, 'probabilities': probs, 'top_probability': max(probs.values())})
            calls.append({'group': packet['id'], 'variant': variant, 'wall_ms': elapsed,
                          'usage': result.get('usage'), 'server_latency_ms': result.get('latency_ms')})
            print(f'{stem}: {correct}/6, {elapsed:.0f} ms', flush=True)
    metrics = {}
    for variant in frozen['variants']:
        subset = [r for r in rows if r['variant'] == variant]
        high = [r for r in subset if r['top_probability'] >= frozen['high_probability_threshold']]
        metrics[variant] = {'correct': sum(r['correct'] for r in subset), 'total': len(subset),
                            'confusion': {label: dict(Counter(r['predicted'] for r in subset if r['expected'] == label)) for label in LABELS},
                            'brier_multiclass_sum': statistics.mean(sum((r['probabilities'][k] - (k == r['expected'])) ** 2 for k in LABELS) for r in subset),
                            'high_probability_count': len(high), 'high_probability_errors': sum(not r['correct'] for r in high),
                            'errors': [r for r in subset if not r['correct']]}
    base = {r['id']: r for r in rows if r['variant'] == 'primary'}
    stability = {}
    for variant in ('rotated', 'reversed'):
        subset = [r for r in rows if r['variant'] == variant]
        stability[variant] = {'choice_flips': [r['id'] for r in subset if r['predicted'] != base[r['id']]['predicted']],
                              'max_probability_delta': max(abs(r['probabilities'][k] - base[r['id']]['probabilities'][k]) for r in subset for k in LABELS)}
    after, _, _ = http('/v1/models')
    save(out / 'models-after.json', after)
    save(out / 'results.json', {'finished_at': now(), 'frozen_sha256': sha(frozen_path.read_bytes()),
                               'metrics': metrics, 'stability': stability, 'calls': calls, 'rows': rows})
    print(json.dumps({'metrics': {v: {k: x[k] for k in ('correct', 'total', 'high_probability_errors')} for v, x in metrics.items()}, 'stability': stability}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['freeze', 'run'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    (freeze if args.action == 'freeze' else run)(args.out)
