import numpy as np
import os
import json
from collections import OrderedDict
from copy import deepcopy


def main():

    data_type = ["interactive", "obstacle"]
    behavior_root = "behavior"

    for _type in data_type:
        
        behavior_path = os.path.join(behavior_root, _type)
        new_json = OrderedDict()

        for file in sorted(os.listdir(behavior_path)):
            basic_variant = file.split('.')[0]
            basic = "_".join(basic_variant.split('_')[:-3])
            variant = "_".join(basic_variant.split('_')[-3:])

            src_json = json.load(open(os.path.join(behavior_path, file)))

            start = int(src_json["start_frame"])
            end = int(src_json["end_frame"])

            if not basic in new_json:
                new_json[basic] = OrderedDict()

            new_json[basic][variant] = [start, end]

        # with open(f"behavior/{_type}.json", "w") as f:
        #     json.dump(new_json, f, indent=4)


def check_scenario():

    data_type = ["interactive", "obstacle"]
    video_root = ""
    cur_root = "./behavior"

    for _type in data_type:

        behavior_path = os.path.join(cur_root, _type+"_behavior.json")
        behavior_dict = json.load(open(behavior_path))

        video_list = sorted(os.listdir(video_root+"/"+_type))

        for video in video_list:
            basic_variant = video.split('.')[0]
            basic = "_".join(basic_variant.split('_')[:-3])
            variant = "_".join(basic_variant.split('_')[-3:])

            if (not basic in behavior_dict) or (not variant in behavior_dict[basic]):
                print("current: ", _type, basic, variant)

        copy_behavior_dict = deepcopy(behavior_dict)
        for basic in copy_behavior_dict:
            for variant in copy_behavior_dict[basic]:

                if not basic+"_"+variant+".mp4" in video_list:
                    print("src: ", _type, basic, variant)
                    del behavior_dict[basic][variant]

                    if len(behavior_dict[basic].keys()) == 0:
                        del behavior_dict[basic]

        # with open(f"behavior/{_type}_behavior_.json", "w") as f:
        #     json.dump(behavior_dict, f, indent=4)

        print("#"*20)


if __name__ == '__main__':

    check_scenario()
    # main()
