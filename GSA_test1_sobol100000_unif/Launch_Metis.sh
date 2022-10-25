rm -f post_proc_metis/champs_piezos_fract.* post_proc_metis/parametres.vtk post_proc_metis/OBSvsSIM.png
rm -f systeme* mac5_* tempo* diag*
rm -f Entrees/temp_*
python3 U_interp_Points_pilotes.py
python3 U_Calc_recharge.py
rm -f Sorties/S_*
STR=$(hostname)
SUB='u-'
if [[ "$STR" == *"$SUB"* ]]; then
  ./metis_old < instructions_Metis0.txt
else
  ./metis_ < instructions_Metis0.txt
fi
fileName="Sorties/S_champ_potentiel_spinup_fract.txt"
size_sortie=$(du --apparent-size --block-size=1  "$fileName" | awk '{ print $1}')
	if [ $size_sortie -lt 30 ]
	then
		echo '******** DIMINUTION DU PAS DE TEMPS, ET NOUVEL ESSAI*********'
		rm Sorties/S_*
		rm -f post_proc_metis/champs_piezos_fract.* post_proc_metis/parametres.vtk post_proc_metis/OBSvsSIM.png
		rm -f systeme* mac5_* tempo* diag*		
		if [[ "$STR" == *"$SUB"* ]]; then
		  ./metis_old < instructions_Metis1.txt
		else
		  ./metis_ < instructions_Metis1.txt
		fi
		fileName="Sorties/S_champ_potentiel_spinup_fract.txt"
        size_sortie=$(du --apparent-size --block-size=1  "$fileName" | awk '{ print $1}')
	    if [ $size_sortie -lt 30 ]
		then
		   echo '******** NOUVELLE DIMINUTION DU PAS DE TEMPS, ET DERNIER ESSAI*********'
		   rm Sorties/S_*
		   rm -f post_proc_metis/champs_piezos_fract.* post_proc_metis/parametres.vtk post_proc_metis/OBSvsSIM.png
		   rm -f systeme* mac5_* tempo* diag*		
		   if [[ "$STR" == *"$SUB"* ]]; then
		    ./metis_old < instructions_Metis2.txt
		   else
			./metis_ < instructions_Metis2.txt
		   fi
		fi
	fi
rm -f Sorties/S_p_piez.txt
python3 U_Model_piezo_from_mat_and_fract.py
	