source .qavenv/bin/activate

bash scripts/sut_up.sh

pytest -m api

pytest -m ui