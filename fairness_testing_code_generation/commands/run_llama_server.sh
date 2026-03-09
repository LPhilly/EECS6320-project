#!/encs/bin/bash
#SBATCH -J llama_job --partition=pa --mem=16GB --gpus=1  --account=jinqiuy
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=l_ling20@encs.concordia.ca
# Specify the output file name
#SBATCH -o llama.log

conda init bash
source ~/.bashrc

conda activate /speed-scratch/l_ling20/FairT

bash exp_by_hyp_batch.sh llama 5 default
bash exp_by_style_batch.sh llama 5 1.0
bash exp_by_iterations.sh llama 3 5
