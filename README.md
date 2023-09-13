# Kelompok Upgrading JBC Generator

A simple python script that generates a list of teams that follows a strict randomized algorithm that ensures each team is meticulously sorted, yielding a  equitable arrangement.


## Run

```bash
python script.py
```

Upon execution, the command will yield a pair of distinct files:

1. `output.csv`, contains each team members in a csv format
2.  `output.json`, a summarized metadata of each teams


## Future Use

In order to make this script recyclable, we first need to include a data source within the root directory. This data source is a JSON file that contains a list of information for each JBC member in which it must follow a strict set of attributes, as illustrated in the following example:

```json
{
  "fullName": "Naufal Rafif Teddyantho",
  "division": "Inti",
  "isMaba": false,
  "isKabinet": true
}
```

In the `script.py` file, the JSON file containing data about the members is referenced via the constant variable `DATA_PATH`, which can be modified to reflect the data source.

```py
DATA_PATH = 'panitia-jbc-2023.json'
```

By default, the total team is set to 6. However, it is possible to adjust this value to your preferred count by modifying the corresponding value within the script file. Simply update the specified value to your desired number under the variable `TOTAL_TEAMS`.

```py
TOTAL_TEAMS = 6
```

To anticipate any changes for the divisions in the future, you can manually rewrite the divisions in a list structure. Any other divisions or members that needs to be excluded can also be include within the top of the script file.

```py
DIVISIONS = ['Inti', 'EO', 'CO', 'LOA', ...]
EXCLUDED_DIVSIONS = ['LOA', ...]
EXCLUDED_DIVSIONS = ['Rakha Putra Pebri Yandra', ...]
```
