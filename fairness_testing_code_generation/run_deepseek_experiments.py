import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
GENERATE_CODE_DIR = ROOT_DIR / "generate_code"
FAIRNESS_TEST_DIR = ROOT_DIR / "fairness_test"
TEST_SUITES_DIR = FAIRNESS_TEST_DIR / "test_suites"
DATASET_DIR = ROOT_DIR / "dataset"


def run_command(args, cwd, env=None):
    print("Running:", " ".join(str(arg) for arg in args))
    subprocess.run(args, cwd=str(cwd), check=True, env=env)


def write_test_config(base_dir, log_dir, report_base_dir):
    config_content = (
        "import os\n\n"
        'BASE_DIR = os.path.abspath(os.environ.get("SOLAR_BASE_DIR", r"' + str(base_dir) + '"))\n\n'
        'LOG_DIR = os.path.abspath(os.environ.get("SOLAR_LOG_DIR", r"' + str(log_dir) + '"))\n\n'
        'REPORT_BASE_DIR = os.path.abspath(os.environ.get("SOLAR_REPORT_BASE_DIR", r"' + str(report_base_dir) + '"))\n'
    )
    config_path = TEST_SUITES_DIR / "config.py"
    config_path.write_text(config_content, encoding="utf-8")
    return config_path


def run_single_experiment(
    sampling,
    temperature,
    prompt_style,
    data_path,
    tasks_file_path,
    model_dir,
    strategy,
    strategy_config_path=None,
    model_name="gemini", # Change this to use different model
):
    model_dir = Path(model_dir).resolve()
    response_dir = model_dir / "response"
    test_result_dir = model_dir / "test_result"
    log_dir = test_result_dir / "log_files"
    inconsistency_dir = test_result_dir / "inconsistency_files"
    bias_info_dir = test_result_dir / "bias_info_files"

    if test_result_dir.exists():
        shutil.rmtree(test_result_dir)
    response_dir.mkdir(parents=True, exist_ok=True)

    generation_command = [
        sys.executable,
        "generate_code.py",
        str(Path(data_path).resolve()),
        str(response_dir),
        str(sampling),
        str(temperature),
        prompt_style,
        model_name,
        strategy,
    ]
    if strategy_config_path:
        generation_command.append(str(Path(strategy_config_path).resolve()))
    run_command(generation_command, GENERATE_CODE_DIR)

    write_test_config(response_dir, log_dir, inconsistency_dir)
    test_env = os.environ.copy()
    test_env["SOLAR_BASE_DIR"] = str(response_dir)
    test_env["SOLAR_LOG_DIR"] = str(log_dir)
    test_env["SOLAR_REPORT_BASE_DIR"] = str(inconsistency_dir)
    run_command([sys.executable, "-m", "pytest"], TEST_SUITES_DIR, env=test_env)

    post_process_commands = [
        [sys.executable, "parse_bias_info.py", str(log_dir), str(bias_info_dir), str(sampling)],
        [sys.executable, "summary_result.py", str(model_dir)],
        [sys.executable, "count_bias.py", str(model_dir)],
        [sys.executable, "count_related.py", str(model_dir)],
        [sys.executable, "pass_at_attribute.py", str(model_dir), str(sampling), str(Path(tasks_file_path).resolve())],
        [sys.executable, "count_bias_leaning.py", str(model_dir)],
    ]
    for command in post_process_commands:
        run_command(command, FAIRNESS_TEST_DIR)

    return load_experiment_summary(model_dir)


def load_experiment_summary(model_dir):
    model_dir = Path(model_dir).resolve()
    test_result_dir = model_dir / "test_result"

    pass_summary_path = test_result_dir / "pass_at_attribute_summary.json"
    bias_summary_path = test_result_dir / "aggregated_bias_ratios_after.json"

    pass_summary = json.loads(pass_summary_path.read_text(encoding="utf-8"))
    bias_summary = json.loads(bias_summary_path.read_text(encoding="utf-8"))

    total_objects = 0
    biased_objects = 0
    executable_objects = 0
    for record in bias_summary.values():
        total_objects += record.get("total_objects", 0)
        biased_objects += record.get("objects_with_bias", 0)
        executable_objects += record.get("total_objects", 0)

    has_executable_objects = executable_objects > 0
    num_tasks = pass_summary.get("num_tasks", 0)
    num_samples = pass_summary.get("num_samples", 0)
    attempted_objects = num_tasks * num_samples
    executable_rate = (executable_objects / attempted_objects) if attempted_objects else None
    overall_cbs = (biased_objects / total_objects) if total_objects else None
    average_pass_at_attribute = pass_summary.get("average_pass_at_attribute")
    if not has_executable_objects:
        average_pass_at_attribute = None

    return {
        "model_dir": str(model_dir),
        "average_pass_at_attribute": average_pass_at_attribute,
        "overall_code_bias_score": overall_cbs,
        "biased_objects": biased_objects if has_executable_objects else None,
        "total_executable_objects": executable_objects,
        "attempted_objects": attempted_objects,
        "executable_rate": executable_rate,
        "has_executable_objects": has_executable_objects,
        "pass_at_attribute_summary": str(pass_summary_path),
        "bias_summary": str(bias_summary_path),
    }


def run_all_experiments(
    output_root,
    sampling=5,
    temperature=1.0,
    prompt_style="default",
    data_path=None,
    tasks_file_path=None,
    strategies=None,
    strategy_config_path=None,
    max_workers=1,
):
    if data_path is None:
        data_path = DATASET_DIR / "prompts.jsonl"
    if tasks_file_path is None:
        tasks_file_path = DATASET_DIR / "tasks.json"
    if strategies is None:
        strategies = ["baseline", "pp", "sr", "ip"]

    output_root = Path(output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    def run_one_strategy(strategy):
        experiment_dir = output_root / strategy
        print("\n" + "=" * 80)
        print(f"Running experiment for strategy: {strategy}") # Change this to use different model
        print("=" * 80)
        summary = run_single_experiment(
            sampling=sampling,
            temperature=temperature,
            prompt_style=prompt_style,
            data_path=data_path,
            tasks_file_path=tasks_file_path,
            model_dir=experiment_dir,
            strategy=strategy,
            strategy_config_path=strategy_config_path,
            model_name="gemini", # Change this to use different model
        )
        summary["strategy"] = strategy
        return summary

    summaries = []
    if max_workers <= 1:
        for strategy in strategies:
            summaries.append(run_one_strategy(strategy))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(run_one_strategy, strategy): strategy for strategy in strategies}
            for future in concurrent.futures.as_completed(future_map):
                summaries.append(future.result())

    summary_path = output_root / "gemini_run_all_summary.json" # Change this to use different model
    summary_path.write_text(json.dumps(summaries, indent=4), encoding="utf-8")
    print("\nRun-all summary written to", summary_path)
    return summaries


def main():
    parser = argparse.ArgumentParser(description="Run the full Gemini fairness experiment pipeline.") # Change this to use different model
    parser.add_argument("--output-root", required=True, help="Directory that will contain one subdirectory per strategy.")
    parser.add_argument("--sampling", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--prompt-style", default="default")
    parser.add_argument("--data-path", default=str(DATASET_DIR / "prompts.jsonl"))
    parser.add_argument("--tasks-file", default=str(DATASET_DIR / "tasks.json"))
    parser.add_argument("--strategy-config", default=None)
    parser.add_argument("--max-workers", type=int, default=1)
    parser.add_argument(
        "--strategies",
        nargs="+",
        default=["baseline", "pp", "sr", "ip"],
        choices=["baseline", "pp", "sr", "ip"],
    )
    args = parser.parse_args()

    run_all_experiments(
        output_root=args.output_root,
        sampling=args.sampling,
        temperature=args.temperature,
        prompt_style=args.prompt_style,
        data_path=args.data_path,
        tasks_file_path=args.tasks_file,
        strategies=args.strategies,
        strategy_config_path=args.strategy_config,
        max_workers=args.max_workers,
    )


if __name__ == "__main__":
    main()
