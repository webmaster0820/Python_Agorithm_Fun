# Name : Sebastian Corradini
# Email: sebastiancor7218@gmail.com

# all possible x axis -- ex: start_day = 5, possible x axis = [5, 10, 35]
xpoints = []
# min sellers list in (xpoints[n] ~ xpoints[n - 1])
min_sellers = []

"""

Algorithm
Type: Dynamic programming & Greedy algorithm

we can think of all sellers as a segment.
start_day ----------- start_day + 30
-----------
|   -----------
|   |  -----------
|   |  |   |   |  |
1   2  3   4   5  6 -- xpoints (! we need to add 10 and total_days in xpoints, and last point should be total_days)

min_sellers[3] is list of min sellers in (xpoints[3] ~ xpoints[4])

if min_sellers[i] is None, there is not a solution
----------
|        |   -----------
|        |   |         |
!         None

min_cost[point] = min_cost[point - 1] + min_sellers[point-1] * (xpoints[point] - xpoint[point - 1])

"""

def get_min_list(sellers: []):
    """
        A function to get min sellers list from sellers
    Arguments:
        sellers {list} -- sellers

    Returns:
        {list} -- min sellers
    """
    res = []
    if not len(sellers):
        return None
    sorted_sellers = sorted(sellers, key=lambda seller: seller[2])
    for seller in sorted_sellers:
        if seller[2] > sorted_sellers[0][2]:
            break
        res.append(seller)
    sorted_res = sorted(res, key=lambda seller: seller[1])
    return sorted_res


def find_minimum_cost_and_plan(point: int, selected_sellers: {}):
    """
        A function to get minimum cost and sellers
    Arguments:
        point {int} -- Where to get the minimum cost.
        selected_sellers {list} -- sellected sellers in (point ~ total_days)
    Returns:
        (min_cost, selected_sellers) -- min cost and sellected sellers in (0 ~ total_days)
    """
    global xpoints
    global min_sellers
    if xpoints[point] == 10:
        # if the point's value is 10, minimum cost is 0
        return [0, selected_sellers]

    selected_seller = min_sellers[point - 1][0]
    for seller in min_sellers[point - 1]:
        if seller[0] in selected_sellers:
            # if the seller was already selected, we need to use the seller
            selected_seller = seller
            break

    if selected_seller[0] in selected_sellers:
        selected_sellers[selected_seller[0]] = selected_sellers[selected_seller[0]] + xpoints[point] - xpoints[point - 1]
    else:
        selected_sellers[selected_seller[0]] = xpoints[point] - xpoints[point - 1]
    res = find_minimum_cost_and_plan(point - 1, selected_sellers)
    res[0] = res[0] + selected_seller[2] * (xpoints[point] - xpoints[point - 1])
    return res


def calculate_purchasing_plan(total_days, sellers: []):
    """
        Calculate puchasing plan for bread
    Arguments:
        total_days {int}
        sellers {list}

    Returns:
        {list} -- calculated plan
    """
    global xpoints
    global min_sellers
    # all x axis
    xpoints = sorted(
        list(
            set([point for seller in sellers for point in (seller[0], seller[0] + 30)])
        ) + [10, total_days]
    )
    # add index for sellers
    sellers = [(idx,) + ele for idx, ele in enumerate(sellers)]
    # sort sellers by start_day
    sorted_seller = sorted(sellers, key=lambda seller: seller[1])
    count_seller = len(sorted_seller)
    now_seller_point = 0
    valid_sellers = []
    for point in xpoints:
        if point == total_days:
            break

        # remove outdated sellers
        if len(valid_sellers):
            valid_sellers = list(
                filter(
                    lambda item: item[1] + 30 > point,
                    valid_sellers
                )
            )
        # add new sellers
        while now_seller_point < count_seller and sorted_seller[now_seller_point][1] == point:
            valid_sellers.append(sorted_seller[now_seller_point])
            now_seller_point = now_seller_point + 1

        # add min sellers in (point ~ )
        min_list = get_min_list(valid_sellers)
        if min_list is None:
            return None
        min_sellers.append(get_min_list(valid_sellers))
    end_point = xpoints.index(total_days)
    min_cost_and_plan = find_minimum_cost_and_plan(end_point, {})
    # get only plan
    plan = []
    for index in range(count_seller):
        if index in min_cost_and_plan[1]:
            plan.append(min_cost_and_plan[1][index])
        else:
            plan.append(0)
    return plan


if __name__ == '__main__':
    res = calculate_purchasing_plan(
        100, [(86, 383), (15, 777), (35, 793), (92, 386), (21, 649), (27, 362), (59, 690), (26, 763), (26, 540), (36, 172), (68, 211), (29, 567), (30, 782), (23, 862), (35, 67), (2, 929), (58, 22), (67, 69), (56, 393), (42, 11), (73, 229), (19, 421), (37, 784), (24, 198), (70, 315), (26, 413), (80, 91), (73, 956), (70, 862), (81, 996), (25, 305), (27, 84), (5, 336), (29, 846), (57, 313), (95, 124), (45, 582), (67, 814), (64, 434), (50, 43), (8, 87), (78, 276), (84, 788), (51, 403), (99, 754), (60, 932), (68, 676), (12, 739), (86, 226), (39, 94)])
    print(res)
