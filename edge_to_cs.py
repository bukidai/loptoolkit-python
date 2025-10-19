import pandas as pd
import json
from sys import argv


# station_code:[その駅につながる枝のlist]
def edge_to_cs(edge: pd.DataFrame) -> dict:
    cs_dict = {}
    for i, row in edge.iterrows():
        from_station = row["from_station_cd"]
        to_station = row["to_station_cd"]

        if from_station not in cs_dict:
            cs_dict[from_station] = []
        if to_station not in cs_dict:
            cs_dict[to_station] = []

        cs_dict[from_station].append(i)
        cs_dict[to_station].append(i)

    return cs_dict


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: python edge_to_cs.py <input_edge_csv> [output_cs_json]")
        exit(1)

    input_edge_csv = argv[1]

    res = edge_to_cs(pd.read_csv(input_edge_csv, index_col=0))

    if len(argv) == 3:
        # 出力ファイルが指定されている場合はJSONファイルに保存
        output_cs_json = argv[2]
        with open(output_cs_json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=4)
    else:
        # 指定されていない場合は標準出力に表示
        print(json.dumps(res, ensure_ascii=False, indent=4))
