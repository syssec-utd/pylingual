import pathlib
import tqdm
import click
import csv

from datetime import datetime

import signal

from pylingual.decompiler import decompile

@click.command(help= "Evaluation script for pylingual")
@click.argument("pyc_list")
@click.argument("out_dir")
def main(pyc_list, out_dir):
    start_time = datetime.now()
    
    def timeout_handler(signum, frame):
        raise TimeoutError()
    signal.signal(signal.SIGALRM, timeout_handler)

    pyc_list = pathlib.Path(pyc_list)
    out_dir = pathlib.Path(out_dir) / f"pylingual-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    
    pyc_files = [pathlib.Path(pyc_path_line.strip()) for pyc_path_line in pyc_list.read_text().splitlines()]

    out_dir.mkdir(parents=True, exist_ok=True)
    evaluation_results_file = out_dir / 'evaluation_results.csv'
    evaluation_results_stream = evaluation_results_file.open('w', newline='')
    evaluation_writer = csv.DictWriter(evaluation_results_stream, fieldnames=['pyc_file', 'py_file', 'identifier', 'success', 'category', 'notes'])
    evaluation_writer.writeheader()

    # decompile all the pyc files
    total_files_succeeded = 0
    total_files_attempted = 0 
    for pyc_file in (evaluation_progress := tqdm.tqdm(pyc_files)):
        decompiler_results_dir = out_dir / 'decompilation_results'
        decompiler_results_dir.mkdir(parents=True, exist_ok=True)
        target_out_dir =  decompiler_results_dir / pyc_file.parent.name
        identifier = str(pyc_file).split("/")[-2]
        # update progress bar
        if total_files_attempted > 0:
            evaluation_progress.set_postfix({
                'file_success': f'{total_files_succeeded}/{total_files_attempted} ({total_files_succeeded / total_files_attempted:.2%})', 
                })

        total_files_attempted += 1

        # decompile the file
        try:
            signal.alarm(300) # 5-minute timeout for decompiling one file
            py_file = decompile(pyc_file, target_out_dir)
            signal.alarm(0) # success; disable timer
        except Exception as err:
            signal.alarm(0) 
            evaluation_writer.writerow({'pyc_file': pyc_file, 'py_file': '', 'identifier': 'FILE', 'success': False, 'category': 'DECOMPILER ERROR', 'notes': repr(err)})
            continue

        if all([result.success for result in py_file.equivalence_results]):
            evaluation_writer.writerow({'pyc_file': pyc_file, 'py_file': py_file, 'identifier': 'FILE', 'success': True, 'category': 'Equal', 'notes': ''})
            total_files_succeeded += 1
        else:
            evaluation_writer.writerow({'pyc_file': pyc_file, 'py_file': py_file, 'identifier': 'FILE', 'success': False, 'category': 'Different', 'notes': ''})
        
        evaluation_writer.writerows({'pyc_file': pyc_file, 'py_file': py_file, 'identifier': identifier, 'success': result.success,  'notes': ''} for result in py_file.equivalence_results)
    
    evaluation_results_stream.close()
    elapsed_time = datetime.now() - start_time
    
    with open(out_dir / 'elapsed_time.txt', 'w') as time_file:
        time_file.write(f"Elapsed Time: {str(elapsed_time)}\n")
        time_file.write(f"File success: {total_files_succeeded}/{total_files_attempted} {total_files_succeeded/total_files_attempted :.2%}")

if __name__ == "__main__":
    main()
