CURRENT_DIR=$(pwd)

if [ "$#" -le 2 ]; then
    echo "Usage: bash exp_by_iterations.sh [model_name] [iterations] [sampling]"
    exit
fi

STYLE="default"
TEMPERATURE="1.0"
temperature="${TEMPERATURE/./}"
MODEL_NAME=$1
ITERATIONS=$2
SAMPLING=$3
SRC_PATH="$CURRENT_DIR""/../outputs/hyp_variations/""$MODEL_NAME""$temperature""$STYLE"
ITERATIVE_PATH="$CURRENT_DIR""/../outputs/iterative/""$MODEL_NAME""$temperature""$STYLE"

rm -rf "$ITERATIVE_PATH"
mkdir -p "$ITERATIVE_PATH"
cp -r "$SRC_PATH" "$ITERATIVE_PATH""/iteration0"


for i in $(seq 1 "$ITERATIONS")
do
  echo "Iteration $i"
  cd "$CURRENT_DIR""/../generate_code" || exit
  python feed_bias_code.py "$ITERATIVE_PATH""/iteration""$((i-1))""/response" "$ITERATIVE_PATH""/iteration""$((i-1))""/test_result/bias_info_files" "$ITERATIVE_PATH""/iteration""$i""/response" $TEMPERATURE $STYLE $MODEL_NAME

  #run test suits
  cd "$CURRENT_DIR""/../fairness_test/test_suites" || exit

  # prepare config file
  BASE_DIR="$ITERATIVE_PATH""/iteration""$i""/response"
  LOG_DIR="$ITERATIVE_PATH""/iteration""$i""/test_result/log_files"
  REPORT_BASE_DIR="$ITERATIVE_PATH""/iteration""$i""/test_result/inconsistency_files"

  cp config_template.py config.py
  sed -i "s|##PATH##TO##RESPONSE##|$BASE_DIR|g" config.py
  sed -i "s|##PATH##TO##LOG##FILES##|$LOG_DIR|g" config.py
  sed -i "s|##PATH##TO##INCONSISTENCY##FILES##|$REPORT_BASE_DIR|g" config.py

  pytest

  # parse bias summary from log files
  cd .. || exit
  python parse_bias_info.py "$ITERATIVE_PATH""/iteration""$i""/test_result/log_files" "$ITERATIVE_PATH""/iteration""$i""/test_result/bias_info_files" "$SAMPLING"
  python summary_result.py "$ITERATIVE_PATH""/iteration""$i"
  python count_bias.py "$ITERATIVE_PATH""/iteration""$i"
  python count_bias_leaning.py "$ITERATIVE_PATH""/iteration""$i"

done
