CURRENT_DIR=$(pwd)

SAMPLING="10"
TEMPERATURE="1.0"
DATA_PATH="$CURRENT_DIR""/../dataset/prompts.jsonl"
MODEL_NAME=$1

#STYLE_PARTIAL="partial"
#DATA_PATH_PARTIAL="../dataset/prompts_32_partial.jsonl"

if [ "$#" -le 0 ]; then
    echo "Usage: bash exp_by_style_batch.sh [model_name]"
    exit
fi

if [ "$#" -ge 2 ]; then
    SAMPLING=$2
fi

if [ "$#" -ge 3 ]; then
    TEMPERATURE=$3
fi

temperature="${TEMPERATURE/./}"

for i in "default" "chain_of_thoughts" "positive_chain_of_thoughts"
do
    bash gen_and_exp.sh "$SAMPLING" "$TEMPERATURE" $i $DATA_PATH "$CURRENT_DIR""/../outputs/styles/""$MODEL_NAME""$temperature"$i "$MODEL_NAME"
done

#bash gen_and_exp.sh "$SAMPLING" "$TEMPERATURE" $STYLE_PARTIAL "$DATA_PATH_PARTIAL" "../outputs/styles/""$MODEL_NAME""$temperature""$STYLE_PARTIAL" "$MODEL_NAME"
