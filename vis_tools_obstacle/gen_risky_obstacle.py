import numpy as np
import json
import os
from collections import OrderedDict


def cal_dis(a, b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5


TYPE = {0: "trafficcone", 1: "streetbarrier",
        2: "trafficwarning", 3: "vehicle"}


def main():

    dataset_root = "./RiskBench_Dataset/obstacle"
    src_obstacle_path = "./obstacle_points"
    risk_dict = OrderedDict()

    for src_file in sorted(os.listdir(src_obstacle_path)):

        basic = src_file.split('.')[0].split('#')[1]
        basic_path = os.path.join(dataset_root, basic, "variant_scenario")

        src_loc = json.load(open(os.path.join(src_obstacle_path, src_file)))
        src_obstacle_type = TYPE[int(basic.split('_')[2])]

        for variant in os.listdir(basic_path):

            variant_path = os.path.join(basic_path, variant)
            obstacle_info_path = os.path.join(
                variant_path, "obstacle_info.json")

            obstacle_info = json.load(open(obstacle_info_path))
            risk_ids = []

            for loc in src_loc:
                ref_x, ref_y = loc[0]

                min_dis = float('inf')
                min_id = -1
                obstacle_type = None

                for actor_id in obstacle_info:
                    actor_loc = obstacle_info[actor_id]["location"]

                    dis = cal_dis([ref_x, ref_y], [actor_loc["x"], actor_loc["y"]])

                    if dis < min_dis:
                        min_dis = dis
                        min_id = actor_id
                        obstacle_type = obstacle_info[actor_id]["obstacle_type"]

                if not src_obstacle_type in obstacle_type:
                    print(basic, variant, src_obstacle_type, obstacle_type)

                risk_ids.append(min_id)

            
            assert len(risk_ids) == len(set(risk_ids)), print(risk_ids, variant_path)

            # list of string
            risk_dict[basic+"_"+variant] = risk_ids

    with open('./obstacle.json', 'w') as f:
        json.dump(risk_dict, f, indent=4)


if __name__ == '__main__':
    main()
