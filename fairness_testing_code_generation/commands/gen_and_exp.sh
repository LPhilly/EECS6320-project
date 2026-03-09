if [ "$#" -le 5 ]; then
    echo "Usage: bash gen_and_exp.sh [sampling] [temperature] [prompt_style] [data_path] [model_dir] [model_name]"
    exit
fi

CURRENT_DIR=$(pwd)

SAMPLING=$1
TEMPERATURE=$2
PROMPT_STYLE=$3
DATA_PATH=$4
MODEL_DIR=$5
MODEL_NAME=$6

echo "SAMPLING:" "$SAMPLING"
echo "TEMPERATURE:" "$TEMPERATURE"
echo "PROMPT_STYLE:" "$PROMPT_STYLE"
echo "DATA_PATH:" "$DATA_PATH"
echo "MODEL_DIR:" "$MODEL_DIR"
echo "MODEL_NAME:" "$MODEL_NAME"
echo "-------------------"

echo generate_code.py "$DATA_PATH" "$MODEL_DIR"/response "$SAMPLING" "$TEMPERATURE" "$PROMPT_STYLE" "$MODEL_NAME"
echo parse_bias_info.py "$MODEL_DIR"/test_result/log_files "$MODEL_DIR"/test_result/bias_info_files "$SAMPLING"
echo summary_result.py "$MODEL_DIR"
echo count_bias.py "$MODEL_DIR"
echo count_bias_leaning.py "$MODEL_DIR"
echo "===================="


# Delete the previous result files
rm -rf "$MODEL_DIR""/test_result"

#generate and save responses from model
cd "$CURRENT_DIR""/../generate_code" || exit
python generate_code.py "$DATA_PATH" "$MODEL_DIR"/response "$SAMPLING" "$TEMPERATURE" "$PROMPT_STYLE" "$MODEL_NAME"

#run test suits
cd "$CURRENT_DIR""/../fairness_test/test_suites/" || exit

BASE_DIR="$MODEL_DIR""/response"
LOG_DIR="$MODEL_DIR""/test_result/log_files"
REPORT_BASE_DIR="$MODEL_DIR""/test_result/inconsistency_files"

cp config_template.py config.py
sed -i "s|##PATH##TO##RESPONSE##|$BASE_DIR|g" config.py
sed -i "s|##PATH##TO##LOG##FILES##|$LOG_DIR|g" config.py
sed -i "s|##PATH##TO##INCONSISTENCY##FILES##|$REPORT_BASE_DIR|g" config.py

pytest

#parse bias summary from log files
cd .. || exit
python parse_bias_info.py "$MODEL_DIR""/test_result/log_files" "$MODEL_DIR""/test_result/bias_info_files" "$SAMPLING"
python summary_result.py "$MODEL_DIR"
python count_bias.py "$MODEL_DIR"
python count_related.py "$MODEL_DIR"
python count_bias_leaning.py "$MODEL_DIR"
