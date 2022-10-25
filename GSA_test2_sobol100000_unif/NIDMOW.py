from corrections_on_zw import *
from def_case import *
from int_z_minus_cst_dz import *
from make_graph import *
from Calc_V import *
from calc_k import *
from Txt_outputs import *
from interp_time_data import *
from Calc_zw_steady_state import *
from calc_k_rect_int___partial_unsat_soil_and_wet_well import *
import numpy as np
import random
import sys

Test_case =sys.argv[1]
#print('NIDMOWR MODEL START : '+Test_case)
#Read NIDMOWR settings
file_settings=np.loadtxt(fname=Test_case+"/Inputs/settings_NIDMOWR.txt", dtype=float, usecols=1)
nbr_Interp_deltaT=int(file_settings[0])
nbr_pts_rect_int_K  =int(file_settings[1])
niter_max =int(file_settings[2])
n_failmax =int(file_settings[3])
epsilon =file_settings[4]
AveragingK=int(file_settings[5])
#Read params_well
ztube,zsurf_,zbot_f,zbot_m,rin_,rout_,rdrill_,wdrill_,deltaE_=np.loadtxt(fname=Test_case+"/Inputs/params_well.txt", dtype=float, usecols=1)
#Physical limits on zbot_f
if (zbot_f<zbot_m):
        zbot_f=zbot_m
elif(zbot_f>zsurf_):
        zbot_f=zsurf_
#Read Time series of zm and zf
file_zm_zf=params_well=np.loadtxt(fname=Test_case+"/Inputs/zm_zf.txt", dtype=float,skiprows=1)
times=file_zm_zf[:,0]
vector_zf=file_zm_zf[:,2]
vector_zm=file_zm_zf[:,1]
nb_simulated_times=len(times)
#Read params_mat and params_fract
param_mat=np.loadtxt(fname=Test_case+"/Inputs/params_matrix.txt", dtype=float, usecols=1)
param_fract=np.loadtxt(fname=Test_case+"/Inputs/params_fractures.txt", dtype=float, usecols=1)
#interpolation of time series for zm and zf
times_interp,nbr_dates_interp,periode_interp,vector_zf_interp,vector_zm_interp=interp_time_data(times,vector_zf,vector_zm,nbr_Interp_deltaT)
#initialisation of zw assuming steady state conditions
zw=Calc_zw_steady_state(zf_steady=vector_zf_interp[0],zm_steady=vector_zm_interp[0],zbot_f_=zbot_f,ztube_=ztube)
#other initilaisations
Zw_final,stockfract,stockmat,fluxmat,fluxfract=np.full((5,nbr_dates_interp),0.0)
stockmat_foo,stockfract_foo,index_time=(0.0,0.0,-1)
#START OF CALCULATIONS
    #time loop
while (index_time<nbr_dates_interp-1):
         index_time=index_time+1
         zw_old_=zw
         zf=0.5*vector_zf_interp[min(index_time+1,nbr_dates_interp-1)]+0.5*vector_zf_interp[index_time]
         zm=0.5*vector_zm_interp[min(index_time+1,nbr_dates_interp-1)]+0.5*vector_zm_interp[index_time]
         convergence=False
         index_iterations=-1
         zw_it=[-999999.0]*(niter_max+2)
         Delta=[-999999.0]*(niter_max+2)
         F=[-999999.0]*(niter_max+2)
         J=[-999999.0]*(niter_max+2)
         fail=0
         #convergence loop
         while (convergence==False):
             index_iterations=index_iterations+1
             #1st iteration : assume zw(n+1)=zw(n)
             if (index_iterations==0):
                     zw_it[index_iterations]=zw_old_
             #following iterations : update the approximation of zw(n+1)
             else:                 
                 zw_it[index_iterations]=random.uniform(0.1, 1.0)*Delta[index_iterations-1]+zw_it[index_iterations-1] # random relaxation factor to help convegrence
             #CALCULATION OF F
             #find in what situation we are in for the matrix
             case_m=def_case(zbot_m_=zbot_m,surface=zsurf_,zw__=zw_it[index_iterations],zi=zm)
             #Calc Vm and its derivative
             t4=calc_V(R_IN=rin_,R_OUT=rout_,R_DRILL=rdrill_,W_DRILL=wdrill_,flux_bottom=False,case=case_m,
                   parameters_medium=param_mat,_zi_=zm,z_bot_i=zbot_m,zsurf=zsurf_,deltaE=deltaE_,
                   nbr_points_interpolation_K=nbr_pts_rect_int_K ,zw_=zw_it[index_iterations],AveragingK_=AveragingK)
             V_mat=t4[0]
             dV_mat=t4[1]
             #find in what situation we are in for the fractures
             case_f=def_case(zbot_m_=zbot_f,surface=zsurf_,zw__=zw_it[index_iterations],zi=zf)
             #Calc Vf and its derivative
             t5=calc_V(R_IN=rin_,R_OUT=rout_,R_DRILL=rdrill_,W_DRILL=wdrill_,flux_bottom=False,case=case_f,parameters_medium=param_fract,_zi_=zf,z_bot_i=zbot_f,
                   zsurf=zsurf_,deltaE=deltaE_,nbr_points_interpolation_K=nbr_pts_rect_int_K ,
                   zw_=zw_it[index_iterations],AveragingK_=AveragingK)
             Vfract=t5[0]
             dVfract=t5[1]
             #V is the sum of Vm and Vf
             V_total=V_mat+Vfract
             dV_total=dV_mat+dVfract
             #conclude to calulate F
             F[index_iterations]=zw_it[index_iterations]-zw_old_+periode_interp*V_total
             #Is F a suitable approximation of 0 (i.e did we find a suitable approximation of zw(n+1) ?
             #if yes :
             if (abs(F[index_iterations])<epsilon):
                 convergence=True
                 #get value of zw
                 zw_apriori=zw_it[index_iterations]
                 zw=corrections_on_zw(zw_initial=zw_apriori,ztube_=ztube,zbot_m_=zbot_m)           
                 Zw_final[index_time]=zw
                 #Calc fluxes and sum of fluxes
                 area=3.14159265359*rin_*rin_+wdrill_*3.14159265359*(rdrill_*rdrill_-rout_*rout_)
                 fluxfract[index_time]=Vfract*area
                 fluxmat[index_time]=V_mat*area
                 stockfract_foo=stockfract_foo+fluxfract[index_time]*periode_interp
                 stockfract[index_time]=stockfract_foo
                 stockmat_foo=stockmat_foo+fluxmat[index_time]*periode_interp
                 stockmat[index_time]=stockmat_foo   
             #if no :
             else:
                #State that the simulation failed if too many iterations have already occured  
                if (index_iterations>niter_max):
                      index_iterations=-1
                      zw_it=[-999999.0]*(niter_max+2)
                      Delta=[-999999.0]*(niter_max+2)
                      F=[-999999.0]*(niter_max+2)
                      J=[-999999.0]*(niter_max+2)
                      fail=fail+1
                      #Possibility to start again from t=0 with a reduced time step if too many fails
                      if (fail>n_failmax):
                         print("Simulation failed")
                         nbr_Interp_deltaT=nbr_Interp_deltaT*2
                         #interpolation of time series
                         times_interp,nbr_dates_interp,periode_interp,vector_zf_interp,vector_zm_interp=interp_time_data(times,vector_zf,vector_zm,nbr_Interp_deltaT)
                         print(str(f'Retry with a reduced time step deltaT={periode_interp}\n'))
                         #initialisation of zw
                         zw=Calc_zw_steady_state(zf_steady=vector_zf_interp[0],zm_steady=vector_zm_interp[0],zbot_f_=zbot_f,ztube_=ztube)
                         #other initilaisations
                         Zw_final,stockfract,stockmat,fluxmat,fluxfract=np.full((5,nbr_dates_interp),0.0)
                         stockmat_foo,stockfract_foo,index_time=(0.0,0.0,-1)
                         break #This makes the whole simulation start again with a reduced time step
                else:
                      #Find a new approximation of zw
                      J[index_iterations]=1+periode_interp*dV_total
                      Delta[index_iterations]=-F[index_iterations]/J[index_iterations]

#WRITE OUTPUTS
Txt_outputs(path=Test_case+'/Outputs',Zw_final_=Zw_final,stockmat_=stockmat,
            stockfract_=stockfract,fluxmat_=fluxmat,fluxfract_=fluxfract,times_interp_=times_interp)                      
make_graph(outputfile=Test_case+"/Outputs/Output_graph.png",
           zm=vector_zm_interp,zf=vector_zf_interp,zw=Zw_final,
           time=times_interp,flux_m=3600*fluxmat,flux_f=-3600*fluxfract,zbot_f_=zbot_f)
#print("NIDMOWR MODEL RAN SUCCESSFULY FOR "+Test_case)   
