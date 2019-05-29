import numpy as np
import csv, os, cv2, glob, argparse

# Parser for Command Line Instructions
#######################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--collection', help='path to collection for logo recognition')
args = parser.parse_args()

if args.collection and os.path.isdir(args.collection):
    path = args.collection

path = os.path.abspath(path)
files = os.listdir(path)
image_paths = [os.path.join(path, file) for file in files if file.endswith(('.jpg', '.jpeg', '.tif'))]
#######################################################################################################

# Body of Script
########################################################################################################################################

# template_list1 = ['central_info_harbin.jpg', 'comitato_assistenza.jpg', 'comite_emigrants_juifs.jpg', 'comite_national.jpg', 'comite_tot_verdediging1.jpg',
#                   'comite_tot_verdediging2.jpg', 'comite_voor_joodsche.jpg', 'ezra.jpg', 'hias_ica_lithuania.jpg', 'hias_america.jpg', 'isr_cultusgemeinde_zurich.jpg',
#                   'jew_ref_com.jpg', 'jewish_colonization_association1.jpg', 'jewish_colonization_association2.jpg', 'jewish_refugees_committee1.jpg',
#                   'jewish_refugees_committee2.jpg', 'mjesni_odbor_zagreb.jpg', 'odbor_zagreb.jpg', 'sociedad_de_proteccion.jpg', 'zentralstelle.jpg',
#                   'fuersorge-zentrale-ikg-wien.jpg', 'hicem_prague.jpg', 'hicem_prague2.jpg', 'hilfsverein_deutschland.jpg', 'hilfsverein_deutschland2.jpg', 'hilfsverein3.jpg',
#                   'jeas_w_polsce.jpg', 'palaestina_amt_wien.jpg', 'palaestina_amt_berlin.jpg']

template_list2 = ['beratungsstelle1.jpg', 'beratungsstelle2.jpg', 'bureau_voor_bero.jpg', 'comitato_milano.jpg', 'comitato_trieste1.jpg', 'comite_allemagne.jpg',
                  'comite_voor_joodsche_amsterdam.jpg', 'council_for_german_jewry.jpg', 'esra_luxembourg.jpg', 'ezra_barcelona.jpg',
                  'gmina_zydowska.jpg', 'haut_commissaire_allemagne.jpg', 'hias_bucarest.jpg', 'hias_bucarest2.jpg', 'hias_cernauti.jpg',
                  'hias_emigdirect1.jpg', 'hias_emigdirect2.jpg', 'hias_kaunas.jpg', 'hias_riga.jpg', 'hias_rio_de_janeiro.jpg', 'hicem_barcelona.jpg',
                  'jewish_col_assoc_moscow.jpg', 'jewish_women_of_australia.jpg', 'judische_gemeinde.jpg', 
                  'magyarorszagi_budapest.jpg', 'oratorio_israelita.jpg', 'palastina_amt_kaunas.jpg',
                  'sociedad_de_proteccion_uruguay.jpg']

with open('HICEMlogofind.csv', mode='w') as csv_file:
    fieldnames = ['Filename', 'Logo', 'Confidence']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    for image in image_paths:
        # for template in template_list1:
        for template in template_list2:
            templ = cv2.imread(template,0)
            match = cv2.imread(image,0)
            
            h, w = match.shape
            if w < 235:
                continue
        
            result = cv2.matchTemplate(match, templ, cv2.TM_CCOEFF_NORMED)
        
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print("File: {}, Max Value: {}".format(os.path.basename(image), max_val))
        
            if max_val > (0.69):
                # c.execute("INSERT INTO logofindr VALUES (%s,%s,%s,%s)",('USHMM_RG-11.001M_HICEM_Paris', os.path.basename(image), template, float(max_val)))
                # mysqlconn.commit()
                writer.writerow({'Filename': os.path.basename(image), 'Logo': template, 'Confidence': max_val})

########################################################################################################################################