def main(port, export, css, files):
    """
    \x08
    Examples:
    $ moo README.md                     # live preview README.md
    $ moo -e *.md                       # export all markdown files
    $ moo --no-css -e README.md         # export README.md without CSS
    $ cat README.md | moo -e - | less   # export STDIN to STDOUT
    """
    options = {'css': css, 'port': port}
    try:
        if not export:
            if len(files) != 1:
                error('please specify just one file to preview')
            preview(files[0], options)
        else:
            export_files(files, options)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        die()