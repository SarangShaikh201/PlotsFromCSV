import os
import uuid

import matplotlib.pyplot as plt
import seaborn as sns

def get_columns_types(columns):
    temp = {}
    for k,v in columns.items():
        if v[3] == 1:
            temp[k] = "zip"
        elif v[2] == 1:
            temp[k] = "date"
        elif v[1] == 1:
            temp[k] = "category"
        elif v[0] == 1:
            temp[k] = "numeric"
        else:
            temp[k] = "non-numeric/continous"
        if temp[k]:
            if temp[k] is "category" and v[0] == 1:
                temp[k] = "numeric/category"
            elif temp[k] is "category" and v[0] == 0:
                temp[k] = "non-numeric/category"
            elif temp[k] is "numeric" and v[1] == 0:
                temp[k] = "numeric/continous"
        else:
            temp[k] = "non-numeric/continous"
    return temp


def get_valid_combinations(combinations, columns_types):
    rules = [
        [['numeric'], ['numeric'], [plt.plot,plt.scatter,plt.stackplot]],
        [['numeric'], ['numeric/continous'], [plt.plot,plt.scatter,plt.stackplot]],
        [['numeric/category'], ['numeric'], [plt.plot,plt.scatter,plt.bar]],
        [['non-numeric/category'], ['numeric'], [plt.plot,plt.scatter,plt.bar]],
        [['non-numeric'], ['numeric'], [plt.plot,plt.scatter,plt.bar]],
        [['date'], ['numeric'], [plt.plot,plt.scatter]],
        [['zip'], ['numeric'], [plt.plot,plt.scatter]],
        [['zip'], ['non-numeric'], [plt.plot,plt.scatter]],
        [['date'], ['non-numeric'], [plt.plot,plt.scatter]],
        [['date'], ['numeric/continous'], [plt.plot,plt.scatter]],
        [['numeric/continous'], ['numeric/continous'], [plt.plot,plt.scatter,plt.stackplot]],
        [['non-numeric/continous'], ['numeric/continous'], [plt.plot,plt.scatter]],
        [['non-numeric/continous'], ['non-numeric/continous'], [plt.scatter]],
        [['non-numeric/category'], ['numeric/continous'], [plt.plot,plt.scatter,plt.bar]],
        [['non-numeric/category'], ['non-numeric/continous'], [plt.bar]]
    ]
    valid_combination = []
    for combination in combinations:
        temp_x = []
        temp_y = []
        for x in combination[0]:
            temp_x.append(columns_types.get(x))
        for y in combination[1]:
            temp_y.append(columns_types.get(y))
        for rule in rules:
            if set(sorted(temp_x)) == set(sorted(rule[0])) and set(sorted(temp_y)) == set(sorted(rule[1])):
                print("valid",combination)
                combination.append(rule[2])
                valid_combination.append(combination)

    return valid_combination


def plot_charts(csv_data, possible_plots, save_dest):
    # plot_types = [plt.plot,plt.bar,plt.pie,plt.hist,plt.scatter]
    colours = ["brown", "orange","green","olive","black","purple"]
    for myplot in possible_plots:
        print(myplot)
        for var in myplot[2]:
            try:
                plt.clf()
                if len(myplot[0]) > 1 and len(myplot[1]) > 1:
                    for item in myplot[0]:
                        var(csv_data[item], csv_data[myplot[1][0]])
                        for i in range(1,len(myplot[1])):
                            var(csv_data[item], csv_data[myplot[1][i]], color=colours[i])
                    plt.title('Interesting Graph\nCheck it out')
                    plt.xlabel(myplot[0])
                    plt.ylabel(myplot[1])
                    plt.legend()
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                    # plt.show()
                elif len(myplot[1]) > 1:
                    for idx,item in enumerate(myplot[1]):
                        var(csv_data[myplot[0][0]], csv_data[item],color=colours[idx])
                    plt.title('Interesting Graph\nCheck it out')
                    plt.xlabel(myplot[0][0])
                    plt.legend()
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                    # plt.show()
                elif len(myplot[0]) > 1:
                    for idx,item in enumerate(myplot[0]):
                        var(csv_data[item], csv_data[myplot[1][0]], color=colours[idx])
                    plt.title('Interesting Graph\nCheck it out')
                    plt.xlabel(myplot[0])
                    plt.ylabel(myplot[1][0])
                    plt.legend()
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                    # plt.show()
                else:
                    var(csv_data[myplot[0][0]],csv_data[myplot[1][0]])
                    plt.xlabel(myplot[0][0])
                    plt.ylabel(myplot[1][0])
                    plt.title('Interesting Graph\nCheck it out')
                    plt.legend()
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                # plt.show()
            except:
                print("didn't plot",myplot,var)
                pass


def dual_axis_chart(csv_data, possible_plots, columns_types,save_dest):
    dual_axis_rules = [
        [['non-numeric/category'], ['numeric/continous']],
        [['numeric/category'], ['numeric/continous']]
    ]

    valid_combination = []
    for combination in possible_plots:
        if len(combination[1]) < 2 and len(set(combination[0])) > 1:
            temp_x = []
            temp_y = []
            for x in combination[1]:
                temp_x.append(columns_types.get(x))
            for y in combination[0]:
                temp_y.append(columns_types.get(y))
            for rule in dual_axis_rules:
                if set(sorted(temp_x)) == set(sorted(rule[0])) and set(sorted(temp_y)) == set(sorted(rule[1])):
                    print("dual chart",combination)
                    # combination.append(rule[2])
                    valid_combination.append(combination)

    for myplot in valid_combination:

        try:
            fig, ax1 = plt.subplots()
            color = 'tab:red'
            ax1.set_xlabel(myplot[1][0])
            ax1.set_ylabel(myplot[0][0], color=color)
            ax1.bar(csv_data[myplot[1][0]], csv_data[myplot[0][0]], color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            color = 'tab:blue'
            ax2.set_ylabel(myplot[0][1], color=color)  # we already handled the x-label with ax1
            ax2.scatter(csv_data[myplot[1][0]], csv_data[myplot[0][1]], color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            plt.legend()
            filename = str(uuid.uuid4())
            image_path = os.path.join(save_dest, filename)
            plt.savefig(image_path)
        except:
            print("dual chart didn't plot")
            pass


def plot_aggregate_data(csv_data,possible_plots,save_dest):
    print("Aggregate Plots",possible_plots)
    aggregates = ['sum','mean','count']
    for plot in possible_plots:
        for item in aggregates:
            if len(plot[0]) < 2 and len(set(plot[1])) < 2:
                try:
                    df = csv_data.groupby(plot[0][0]).agg([item]).reset_index()
                    plt.clf()
                    plt.plot(df[plot[0][0]], df[plot[1][0]], label=item + " of " + plot[1][0])
                    plt.xlabel(plot[0][0])
                    plt.ylabel(plot[1][0])
                    plt.title('Interesting Graph\nCheck it out')
                    plt.legend()
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                except:
                    print("didn't plot")


def plot_single_column_charts(csv_data,columns_types,possible_plots,save_dest):
    single_column_rules = [
        [['numeric/category'], False, [plt.pie]],
        [['non-numeric/category'], True, [plt.pie]],
    ]
    possible_plots = [[plot] for plot in possible_plots]
    valid_combination = []
    for plot in possible_plots:
        temp_x = columns_types.get(plot[0])
        for rule in single_column_rules:
            if temp_x == rule[0][0]:
                plot.append(rule[1])
                plot.append(rule[2])
                valid_combination.append(plot)

    for myplot in valid_combination:
        print(myplot)
        for var in myplot[2]:
            try:
                plt.clf()
                if myplot[1]:
                    labels = csv_data[myplot[0]].astype('category').cat.categories.tolist()
                    counts = csv_data[myplot[0]].value_counts()
                    sizes = [counts[var_cat] for var_cat in labels]
                    var(sizes, labels=labels, autopct='%1.1f%%')
                    plt.axis('equal')
                    plt.xlabel(myplot[0])
                    plt.title('Interesting Graph\nCheck it out')
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                    # plt.show()
                else:
                    var(csv_data[myplot[0]])
                    plt.title('Interesting Graph\nCheck it out')
                    filename = str(uuid.uuid4())
                    image_path = os.path.join(save_dest, filename)
                    plt.savefig(image_path)
                    # plt.show()
            except:
                print("didn't plot")