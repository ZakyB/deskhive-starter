"""Run DeskHive unit and acceptance tests from the repository root."""
import argparse
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
IS_STARTER = (ROOT / 'M6-EXERCISES.md').exists()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    flags = ('smoke', 'all', 'web', 'core', 'rules', 'm4', 'm5',
             'm6-lab1', 'm6', 'm7-lab1', 'm7-lab2', 'm7')
    group = parser.add_mutually_exclusive_group()
    for flag in flags:
        group.add_argument('--'+flag, action='store_true')
    args = parser.parse_args()
    selected = next((flag for flag in flags if getattr(args,flag.replace('-','_'))),
                    'm6' if IS_STARTER else 'all')
    jobs = {
        'smoke': [('deskhive-web', ['manage.py','test','spaces.smoke_tests','-v','2']),
                  ('deskhive-core',['-m','unittest','-v','smoke_tests'])],
        'web': [('deskhive-web',['manage.py','test','spaces','bookings','-v','2'])],
        'core':[('deskhive-core',['-m','unittest','discover','-s','tests','-v'])],
        'rules':[('deskhive-core',['-m','unittest','-v','tests.test_booking'])],
        'm4':[('deskhive-web',['manage.py','test','spaces.tests','spaces.test_m4','bookings.tests','-v','2'])],
        'm5':[('deskhive-web',['manage.py','test','spaces','bookings','-v','2'])],
        'm6-lab1':[('deskhive-web',['manage.py','test','api_m6.tests.SerializerBasicsTests','-v','2'])],
        'm6':[('deskhive-web',['manage.py','test','api_m6.tests','-v','2'])],
        'm7-lab1':[('deskhive-web',['manage.py','test','partner_m7.tests.PartnerXmlRpcTests','-v','2'])],
        'm7-lab2':[('deskhive-web',['manage.py','test','partner_m7.tests.CorporateImportExportTests','-v','2'])],
        'm7':[('deskhive-web',['manage.py','test','partner_m7.tests','-v','2'])],
    }
    jobs['all'] = jobs['web'] + jobs['m6'] + jobs['m7'] + jobs['core']
    failed=False
    for folder,cmd in jobs[selected]:
        print(f'Checking {folder}: {" ".join(cmd)}',flush=True)
        result=subprocess.run([sys.executable,*cmd], cwd=ROOT/folder)
        failed= failed or result.returncode != 0
    if failed and IS_STARTER:
        print('M7 exercises intentionally fail before completing TODOs.',flush=True)
    return int(failed)

if __name__ == '__main__':
    raise SystemExit(main())
