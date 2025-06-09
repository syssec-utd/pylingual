from pathlib import Path

def dump_fs(html, target_folder, packlist):
    html.write(f"""PYGBAG_FS={len(packlist)}\n__import__('os').chdir(__import__('tempfile').gettempdir())\ndef fs_decode(fsname, o248):\n    from pathlib import Path\n    filename = Path.cwd() / fsname\n    if not filename.is_file():\n        filename.parent.mkdir(parents=True, exist_ok=True)\n        print("FS:", filename)\n        with open(fsname,"wb") as fs:\n            for input in o248.split("\\n"):\n                if not input: continue\n                fs.write(bytes([ord(c) - 248 for c in input]))\n""")
    for topack in packlist:
        if topack == '/main.py':
            continue
        vfs_name = topack[1:].replace('-pygbag.', '.')
        src_name = target_folder / topack[1:]
        sum = str(src_name.stat().st_size)
        if topack.lower().endswith('.py'):
            html.write(f'''\nwith open("{vfs_name}","w") as fs:fs.write("""\\\n{open(src_name, 'r').read()}""")\n''')
            html.write('\n')
        else:
            html.write(f"\nfs_decode('{vfs_name}','''\n")
            c = 0
            for b in open(src_name, 'rb').read():
                html.write(chr(b + 248))
                c += 1
                if c > 78:
                    html.write('\n')
                    c = 0
            html.write("''')\n")
    html.write('\ndel fs_decode, PYGBAG_FS\n')

def make_header(html, line):
    if line and line[0] == '<':
        pass
    else:
        if line.find('pythons.js') > 0:
            SCRIPT = line[2:].strip()
        else:
            SCRIPT = ' src="https://pygame-web.github.io/archives/0.3.0/pythons.js"'
            SCRIPT += ' data-src="vtx,fs,gui"'
        line = f'\n<html>\n<head>\n<meta charset="utf-8">\n</head>\n<script {SCRIPT} type=module id="__main__"  async defer>\n#<!--\n'.replace('\n', '').replace('  ', ' ').strip()
    print(line, end='\n', file=html)

def html_embed(target_folder, packlist: list, htmlfile: str):
    print('HTML:', htmlfile)
    RUNPY = 'asyncio.run(main())'
    SKIP = False
    with open(htmlfile, 'w+', encoding='utf-8') as html:
        for topack in packlist:
            if topack == '/main.py':
                for lnum, line in enumerate(open(target_folder / topack[1:], 'r', encoding='utf-8').readlines()):
                    if line.startswith('asyncio.run'):
                        RUNPY = line
                        MAX = lnum
                        break
                for lnum, line in enumerate(open(target_folder / topack[1:], 'r', encoding='utf-8').readlines()):
                    if SKIP:
                        if line.endswith('del fs_decode, PYGBAG_FS'):
                            SKIP = False
                    if line.startswith('PYGBAG_FS='):
                        SKIP = True
                    if SKIP:
                        continue
                    line = line.rstrip('\r\n')
                    if not lnum:
                        make_header(html, line)
                        dump_fs(html, target_folder, packlist)
                        continue
                    elif lnum >= MAX:
                        break
                    print(line, end='\n', file=html)
            break
        print(f'\n{RUNPY}\n# --></script></html>\n', file=html)