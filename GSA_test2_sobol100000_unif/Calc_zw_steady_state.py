#Function used ot initialize zw. based on te hypothesis of steady state zf and zm
def Calc_zw_steady_state(zf_steady,zm_steady,zbot_f_,ztube_):
    if (zf_steady>=zbot_f_):
        zw=min(zf_steady,ztube_)
    elif (zm_steady>zbot_f_):
        zw = zbot_f_
    else:
        zw = zm_steady
    return zw
