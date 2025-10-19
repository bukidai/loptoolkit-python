import pandas as pd
from sys import argv


def cd_to_edge(cd: pd.DataFrame, sd: pd.DataFrame) -> pd.DataFrame:
    # sdは路線名と駅名が混じってるので、分離
    lines = {}
    stations = {}
    line_finished = False
    for row in sd.itertuples():
        if row[1] == 0 and row[2] == 0:
            continue
        if not line_finished and row[1] != 0:
            # 路線名
            line_cd = row[1]
            line_name = row[3]
            lines[line_cd] = line_name
        if row[1] == 0 and row[2] != 0:
            line_finished = True
            # 駅名
            station_cd = row[2]
            station_name = row[3]
            stations[station_cd] = station_name
    line_df = pd.DataFrame.from_dict(lines, orient="index", columns=["line_name"])
    station_df = pd.DataFrame.from_dict(
        stations, orient="index", columns=["station_name"]
    )

    # ここから本番
    edges = []
    for i in range(1, len(cd)):
        prev_row = cd.iloc[i - 1]
        curr_row = cd.iloc[i]
        if prev_row["line_cd"] != curr_row["line_cd"]:
            # 路線が変わったらスキップ
            continue
        # 運賃計算キロが0の場合営業キロで埋める
        prev_row["keisan_kiro_rel"] = (
            prev_row["eigyo_kiro_rel"]
            if prev_row["keisan_kiro_rel"] == 0
            else prev_row["keisan_kiro_rel"]
        )
        curr_row["keisan_kiro_rel"] = (
            curr_row["eigyo_kiro_rel"]
            if curr_row["keisan_kiro_rel"] == 0
            else curr_row["keisan_kiro_rel"]
        )
        eigyo_kiro = abs(curr_row["keisan_kiro_rel"] - prev_row["keisan_kiro_rel"])
        keisan_kiro = abs(curr_row["keisan_kiro_rel"] - prev_row["keisan_kiro_rel"])
        edge = {
            "edge_cd": i,
            "line_cd": curr_row["line_cd"],
            "from_station_cd": min(prev_row["station_cd"], curr_row["station_cd"]),
            "to_station_cd": max(prev_row["station_cd"], curr_row["station_cd"]),
            "eigyo_kiro": eigyo_kiro,
            "keisan_kiro": keisan_kiro,
            "comment": f"{line_df.loc[curr_row['line_cd'], 'line_name']}：{station_df.loc[prev_row['station_cd'], 'station_name']} - {station_df.loc[curr_row['station_cd'], 'station_name']}",
        }
        edges.append(edge)
    edge_df = pd.DataFrame(edges)
    return edge_df


if __name__ == "__main__":
    if len(argv) < 3:
        print("Usage: python cd_to_edge.py <cd_csv_path> <sd_csv_path> [output_path]")
        exit(1)
    cd_csv_path = argv[1]
    sd_csv_path = argv[2]
    cd = pd.read_csv(cd_csv_path)
    sd = pd.read_csv(sd_csv_path, header=None)
    edge_df = cd_to_edge(cd, sd)
    # 結果を保存orSTDOUTに出力
    if len(argv) == 4:
        output_path = argv[3]
        edge_df.to_csv(output_path, index=False)
    else:
        print(edge_df.to_csv(index=False))
