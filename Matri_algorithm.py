

import gird_algorithm

def girdincell(gird_list,gird_cell):
    eci_list = []
    for cur_girdid in gird_list:
        for d_eci in gird_cell[cur_girdid]:
            if d_eci in eci_list:
                pass
            else:
                eci_list.append(d_eci)
    return eci_list
def gird_dict_create(cur_girdid,gird_dict,cur_rsrp,cur_rsrq):
    r_lon, r_lat = gird_algorithm.gird_parser(cur_girdid)
    if cur_girdid in gird_dict:
        gird_dict[cur_girdid]['rsrp'] = (gird_dict[cur_girdid]['rsrp'] * gird_dict[cur_girdid][
            'samples'] + cur_rsrp) / (gird_dict[cur_girdid]['samples'] + 1)
        gird_dict[cur_girdid]['rsrq'] = (gird_dict[cur_girdid]['rsrq'] * gird_dict[cur_girdid][
            'samples'] + cur_rsrq) / (gird_dict[cur_girdid]['samples'] + 1)
        gird_dict[cur_girdid]['samples'] = gird_dict[cur_girdid]['samples'] + 1
    else:
        gird_dict[cur_girdid] = {}
        gird_dict[cur_girdid] = {'rsrp': cur_rsrp, 'rsrq': cur_rsrq, 'samples': 1, 'lon': r_lon, 'lat': r_lat}
    return gird_dict
def cell_dict_create(cur_girdid,cur_eci,cell_dict,cur_rsrp,cur_rsrq):
    r_lon, r_lat = gird_algorithm.gird_parser(cur_girdid)
    if cur_eci in cell_dict:
        if cur_girdid in cell_dict[cur_eci]:
            cell_dict[cur_eci][cur_girdid]['rsrp'] = (cell_dict[cur_eci][cur_girdid]['rsrp'] *
                                                      cell_dict[cur_eci][cur_girdid]['samples'] + cur_rsrp) / (
                                                             cell_dict[cur_eci][cur_girdid]['samples'] + 1)
            cell_dict[cur_eci][cur_girdid]['rsrq'] = (cell_dict[cur_eci][cur_girdid]['rsrq'] *
                                                      cell_dict[cur_eci][cur_girdid]['samples'] + cur_rsrq) / (
                                                             cell_dict[cur_eci][cur_girdid]['samples'] + 1)
            cell_dict[cur_eci][cur_girdid]['samples'] = cell_dict[cur_eci][cur_girdid]['samples'] + 1
        else:
            cell_dict[cur_eci][cur_girdid] = {'rsrp': cur_rsrp, 'rsrq': cur_rsrq, 'samples': 1, 'lon': r_lon,
                                              'lat': r_lat}
    else:
        cell_dict[cur_eci] = {}
        cell_dict[cur_eci][cur_girdid] = {'rsrp': cur_rsrp, 'rsrq': cur_rsrq, 'samples': 1, 'lon': r_lon,
                                          'lat': r_lat}
    return cell_dict
def cell_gird_create(cur_eci,cur_girdid,cell_gird,gird_cell):
    if cur_girdid in gird_cell:
        if cur_eci in gird_cell[cur_girdid]:
            pass
        else:
            gird_cell[cur_girdid].append(cur_eci)
    else:
        gird_cell[cur_girdid] = []
        gird_cell[cur_girdid] = [cur_eci]

    if cur_eci in cell_gird:
        if cur_girdid in cell_gird[cur_eci]:
            pass
        else:
            cell_gird[cur_eci].append(cur_girdid)
    else:
        cell_gird[cur_eci] = []
        cell_gird[cur_eci] = [cur_girdid]


    return cell_gird,gird_cell
