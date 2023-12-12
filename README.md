# octans

## Record data with the Prophesee Gen4

https://github.com/neuromorphicsystems/gen4

## Record data with the DAVIS 346

https://inivation.gitlab.io/dv/dv-docs/docs/getting-started.html

## Load recordings

- Convert to frames: https://github.com/neuromorphicsystems/charidotella

- Read .es (Prophesee Gen 4) with Python: https://github.com/neuromorphicsystems/event_stream

- Read .aedat (DAVIS recordings) with Python: https://github.com/neuromorphicsystems/aedat

## Control the motor

https://www.pololu.com/docs/0J73

## Generate the star map

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python star_map.py
```
