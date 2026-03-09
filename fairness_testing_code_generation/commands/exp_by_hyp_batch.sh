CURRENT_DIR=$(pwd)

SAMPLING="10"
STYLE="default"
DATA_PATH="$CURRENT_DIR""/../dataset/prompts.jsonl"
MODEL_NAME=$1

if [ "$#" -le 0 ]; then
    echo "Usage: bash exp_by_hyp_batch.sh [model_name]"
    exit
fi

if [ "$#" -ge 2 ]; then
    SAMPLING=$2
fi

if [ "$#" -ge 3 ]; then
    STYLE=$3
fi

for i in 1.0 0.2 0.4 0.6 0.8
do
    temperature="${i/./}"
    bash gen_and_exp.sh "$SAMPLING" $i "$STYLE" $DATA_PATH "$CURRENT_DIR""/../outputs/hyp_variations/""$MODEL_NAME""$temperature""$STYLE" "$MODEL_NAME"
done
