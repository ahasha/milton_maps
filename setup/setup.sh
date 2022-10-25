#Determine absolute path of environment.yml file
cd "$(dirname "$0")"
SETUP_DIR=$PWD
ROOT_DIR=${BASE_DIR}/..

if [ -e "${SETUP_DIR}/environment.yml"] && [ ! -e "$HOME/.conda/envs/milton_maps"]; then

  # Create a conda envirnoment for the project
  echo "Creating conda environment"
  conda env create -f ${SETUP_DIR}/environment.yml

fi

conda activate milton_maps
