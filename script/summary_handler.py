from datetime import datetime


def write_summary(file, current_date, total_count, total_true_count, run_map, ironclad, silent, defect, watcher):
    def calculate_percentage(part, total):
        return (part / total) * 100 if total > 0 else 0

    # Helper function to get the count of clear and fail for each character
    def get_run_stats(character):
        clear_key = f'{character}_clear'
        fail_key = f'{character}_fail'
        clear_count = len(run_map.get(clear_key, []))
        fail_count = len(run_map.get(fail_key, []))
        total_runs = clear_count + fail_count
        return clear_count, fail_count, total_runs, calculate_percentage(total_runs, total_true_count)

    # Calculate the percentage of total runs for each character
    ironclad_clear, ironclad_fail, ironclad_total, ironclad_true = get_run_stats('ironclad')
    silent_clear, silent_fail, silent_total, silent_true = get_run_stats('silent')
    defect_clear, defect_fail, defect_total, defect_true = get_run_stats('defect')
    watcher_clear, watcher_fail, watcher_total, watcher_true = get_run_stats('watcher')

    # Write the summary to the file
    file.write(f"""
    batch time: start at {current_date} finish in {datetime.now().strftime('%Y%m%d-%H%M%S')}

    **origin data**

    total runs: {total_count}
    ironclad: {ironclad} runs({calculate_percentage(ironclad, total_count):.3f}%)
    silent: {silent} runs({calculate_percentage(silent, total_count):.3f}%)
    defect: {defect} runs({calculate_percentage(defect, total_count):.3f}%)
    watcher: {watcher} runs({calculate_percentage(watcher, total_count):.3f}%) 

    --------------------------------------------------------

    **after filter**

    total true runs: {total_true_count}
    filtered runs: {total_count - total_true_count}

    ironclad: {ironclad_total} runs({ironclad_true:.3f}%) - clear({ironclad_clear}) / fail({ironclad_fail})
    silent: {silent_total} runs({silent_true:.3f}%) - clear({silent_clear}) / fail({silent_fail})
    defect: {defect_total} runs({defect_true:.3f}%) - clear({defect_clear}) / fail({defect_fail})
    watcher: {watcher_total} runs({watcher_true:.3f}%) - clear({watcher_clear}) / fail({watcher_fail})
    """)