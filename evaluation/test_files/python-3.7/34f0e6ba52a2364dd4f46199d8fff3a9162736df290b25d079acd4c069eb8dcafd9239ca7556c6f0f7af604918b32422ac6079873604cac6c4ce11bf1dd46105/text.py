from typing import List
from pathlib import Path
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as date_parse
from guten.backend import Backend
from guten.press import FetchedSourceGroup
METADATA_FILE = '.metadata'

def underline(s: str, c='-') -> str:
    return f'{s}\n{c * len(s)}\n\n'

class TextBackend(Backend):

    async def run(self, groups: List[FetchedSourceGroup], output_dir: Path) -> Path:
        today = datetime.now(timezone.utc)
        output_file = output_dir / f'{today.year}-{today.month}-{today.day}.txt'
        metadata_file = output_dir / METADATA_FILE
        previous_run_date = today - timedelta(days=5)
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = f.read()
            temp = date_parse(data)
            if temp.date() != today.date():
                previous_run_date = temp
            else:
                previous_run_date = today - timedelta(days=1)
        with open(output_file, 'w') as f:
            localdate = datetime.now()
            f.write(underline(f'Feed - {localdate.year}/{localdate.month}/{localdate.day}', c='='))
            f.write(f'Generated at: {today.isoformat()}\n\n')

            def process_source(item):
                (source, df) = item
                if df.empty:
                    return (source, [])
                data = df
                if 'published' in df:
                    df['date'] = df['published'].apply(lambda x: date_parse(x))
                    data = df[df['date'] > previous_run_date]
                data = data[['title', 'link']]
                data = data.apply(lambda x: f"- [{x['title']}]({x['link']})", axis=1)
                data = list(data)
                return (source, data)
            for (group, sources) in groups:
                sources = [process_source(source) for source in sources]
                sources = [(source, data) for (source, data) in sources if len(data) > 0]
                if len(sources) == 0:
                    continue
                f.write(underline(group.name.title(), c='~'))
                for (source, data) in sources:
                    f.write(underline(source.name, c='-'))
                    f.write('\n'.join(data))
                f.write('\n\n')
        with open(metadata_file, 'w') as f:
            f.write(today.isoformat())
        return output_file
__backend__ = TextBackend