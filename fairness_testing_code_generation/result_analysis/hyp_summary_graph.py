import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import sys
import os
from os.path import join

models = {"gpt": 2, "bison": 4, "llama": 1, "claude": 3}
id_to_model = {v: k for k, v in models.items()}
temperatures = [0.2, 0.4, 0.6, 0.8, 1.0]
style = "default"
result_path = "../outputs/hyp_variations"
BIAS_THRESHOLD = 0.5
BIAS_PERCENTAGE_THRESHOLD = 0.3
colors = ["red", "blue", "green", "purple", "orange", "brown", "cyan"]

def read_models():
    x_axis = [] # Models
    y_axis = [] # Temperatures
    points_info = []
    bias_unique_attributes = []
    for model_name in models.keys():
        for temperature in temperatures:
            x_axis.append(models[model_name])
            y_axis.append(temperature)
            temp = str(temperature).replace(".", "")
            summary_path = join(result_path, f"{model_name}{temp}{style}", "test_result", "aggregated_bias_ratios_after.json")
            with open(summary_path, "r") as f:
                data = json.load(f)
                attr_percentage = {}
                attr_occurrence = {}
                attr_count = {}
                for index, attribute_info in sorted(data.items()):
                    for attr, count in sorted(attribute_info["attribute_counts"].items()):
                        if attr not in attr_percentage.keys():
                            attr_percentage[attr] = []
                        attr_percentage[attr].append(count/max(attribute_info["total_objects"], 0.1))
                        bias_unique_attributes.append(attr)
                for k, v in sorted(attr_percentage.items()):
                    attr_count[k] = len([num for num in v if num >= BIAS_PERCENTAGE_THRESHOLD])
                points_info.append({"model": models[model_name], "temperature": temperature, "bias_count": attr_count})
    return x_axis, y_axis, points_info, sorted(list(set(bias_unique_attributes)))

def show_graph(x_axis, y_axis, points_info, colors_dict):
    plt.figure(figsize=(20, 10))

    plt.scatter(x_axis, y_axis, marker='o', alpha=0.5, color='gray')  # Adjust marker and transparency

    for point in points_info:
        x = point["model"]
        y = point["temperature"]
        bias_count = point["bias_count"]
        shifted = -0.15
        for attr, count in sorted(bias_count.items()):
            plt.scatter(x + shifted, y, s=count*70, color=colors_dict[attr])
            shifted += 0.05

    # Plot highlighted points with categories
    # plt.scatter(x_axis[1], y_axis[1], s=point_size, color=point_color1)
    # plt.scatter(x_axis[1] + 0.1, y_axis[1], s=point_size * 2, color=point_color2)

    # Customize plot elements
    plt.xlabel('Models', fontsize=20)  # Rename x-axis label
    plt.ylabel('Temperature', fontsize=20)  # Rename y-axis label
    plt.title('Frequency of Biases with Different Temperatures', fontsize=25)
    plt.xticks([v for k,v in sorted(models.items())], [k for k in models.keys()], fontsize=15)
    plt.yticks(temperatures, fontsize=15)
    plt.grid(axis='y', linestyle='--', linewidth=0.5, color='gray')


    # plt.legend(title='Categories', handles=[red_patch, blue_patch])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Categories', handles=[mpatches.Patch(color=v, label=k) for k,v in sorted(colors_dict.items())], fontsize=15)
    plt.tight_layout()
    plt.savefig('temp.png')
    plt.show()



x_axis, y_axis, points_info, bias_unique_attributes = read_models()
colors_dict = {attr: colors[i] for i, attr in enumerate(bias_unique_attributes)}
# print(x_axis)
# print(y_axis)
# print(points_info)
# print(colors_dict)

show_graph(x_axis, y_axis, points_info, colors_dict)

# print(points_info)