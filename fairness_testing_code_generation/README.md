# Bias Unveiled: Investigating Social Bias in LLM-Generated Code

## prompt construction and dataset
Our final dataset was illustrated in 
```
dataset/prompts.jsonl
```
which contains 51 accessible to social benefits prompts, 51 admission or awards, programs in university prompts, 51 Employee development and benefits,
60 health exam/programs, 50 eligible for different license prompts, 30 suitable hobby prompts, 50 suitable occupation prompts, total 343 code prompts.

The dataset could be extendable by using script 

```
generate_task_dsl.py
```

## Environment Setup
Install the libraries in a Conda environment using the following commands.
```
cd commands
./setup.sh
```

## Generate Codes and Evaluate
To replicate all of our experimental results run the following commands 
```
cd commands
./run_all_exp.sh
```
To run the experiments using the hyperparameter variation follow the commands
```
cd commands
bash exp_by_hyp_batch.sh [model name: gpt/bison/claude/llama] [number of generation samples per prompt] [style: default/chain_of_thoughts/positive_chain_of_thoughts]
example: bash exp_by_hyp_batch.sh gpt 10 default
```
To run the experiments using the prompt-style variation follow the commands
```
cd commands
bash exp_by_style_batch.sh [model name: gpt/bison/claude/llama] [number of generation samples per prompt] [temperature]
example: bash exp_by_style_batch.sh gpt 10 1.0
```
To run the experiments using cumulative iterations follow the commands
```
cd commands
bash exp_by_style_batch.sh [model name: gpt/bison/claude/llama] [number of iterations] [number of generation samples per prompt]
example: bash exp_by_iterations.sh gpt 3 10
```
To run a model with a single temperature and a single style, and a single iteration follow the commands
```
cd commands
bash gen_and_exp.sh [sampling] [temperature] [prompt_style] [data_path] [model_dir] [model_name] [strategy: baseline/pp/sr/ip]
Example: bash gen_and_exp.sh 10 1.0 default "../dataset/prompts.jsonl" "../outputs/hyp_variations/gpt10default" gpt baseline
```

For prompt-based debiasing experiments, use the `strategy` argument:
```
bash gen_and_exp.sh 10 1.0 default "../dataset/prompts.jsonl" "../outputs/debiasing/gpt_pp" gpt pp
bash gen_and_exp.sh 10 1.0 default "../dataset/prompts.jsonl" "../outputs/debiasing/gpt_sr" gpt sr
bash gen_and_exp.sh 10 1.0 default "../dataset/prompts.jsonl" "../outputs/debiasing/gpt_ip" gpt ip
```

Each run now also writes `test_result/pass_at_attribute_summary.json`, which contains the per-task
and average `Pass@attribute` score derived from the generated bias and related-attribute summaries.

## DeepSeek Run-All Notebook
For the student-project workflow using `deepseek-chat` only, open
`DeepSeek_Run_All.ipynb`, set `DEEPSEEK_API_KEY`, adjust the configuration cell,
and run the notebook to execute `baseline`, `pp`, `sr`, and `ip` end-to-end.
The notebook also exposes an editable `STRATEGY_CONFIG` block so you can directly
modify how Prefix Prompting, Self-Refinement, and Implication Prompting are worded.
