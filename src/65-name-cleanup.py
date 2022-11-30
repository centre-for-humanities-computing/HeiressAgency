import csv
import os
from tqdm import tqdm

name_dict = { "Anna": ["Anna","Miss_Anna","Anna_Murray", "Lady_Anna", "Anna_Thwaite"],
              "Betty": ["Lady_Betty", "Lady_Lawrence"],
              "William": ["William Mainwaring", "Mainwaring",
                              		"Mr_William", "William_Guppy", "Mr_Guppy"],
              "Roger": ["Roger_Solmes", "Mr_Solmes"],
              "John": ["Mr_John", "John_Eyre", "John", "Mr_Eyre",
                            "John_Jarndyce","Mr_Jarndyce","Jarndyce",
                           		"Colonel_Herncastle", "John_Herncastle",
                                    "John_Harmon", "Harmon"],
              "Arabella": ["Arabella", "Bella", "Lady_Bella"],
              "Clementina": ["Signorina_Clementina", "Clementina"],
              "Charles": ["Sir_Charles", "Mr_Vernon","Charley", "Charles_Vernon"],
              "Rowland": ["Sir_Rowland", "Rowland_Meredith", "Sir_Rowland_Meredith"],
              "Hargrave": ["Sir_Hargreve", "Sir_Hargrave_Pollexfen", "Pollexfen", "Sir_Pollexfen", "Hargrave"],
              "Evelina": ["Evelina", "Evelina_Anville"],
              "Maria": ["Miss_Maria", "Miss_Mirvan"],
              "Madame_Duval": ["Madame_Duval", "Mme_Duval"],
              "Arthur": ["Reverend_Arthur", "Arthur_Villars", "Mr_Villars"],
              "Clement": ["Sir_Clement", "Clement_Willoughby", "Clement"],
              "McCartney": ["Mr_McCartney", "McCartney"],
              "Cecilia": ["Cecilia", "Cecilia_Beverley", "Miss_Beverley"],
              "Henrietta": ["Miss_Henrietta", "Henrietta", "Henrietta_Belfield", "Miss_Belfield", "Mrs_Arnott"],
              "Honoria": ["Lady_Honoria", "Honoria"],
              "Margaret": ["Lady_Margaret", "Margaret"],
              "Augusta": ["Augusta", "Augusta_Delvile", "Mrs_Augusta", "Mrs_Delvile"],
              "Mortimer": ["Mortimer_Delvile", "Delvile", "Mr_Mortimer", "Domino", "Mr_Beverley"],
              "Harrel": ["Mr_Harrel", "Harrel"],
              "Briggs": ["Mr_Briggs", "Briggs", "chimneysweeper"],
              "Albany": ["Albany", "Mr_Albany"],
              "Emmeline": ["Emmeline_Mowbary", "Emmeline", "Miss_Mowbary"],
              "Adelina": ["Lady_Adelina","Adelina"],
              "Maloney": ["Maloney", "Mr_Maloney"],
              "Delamere": ["Mr_Delamare", "Delamare","Frederic"],
              "Emily": ["Emily_st", "Emily_st_Aubert", "Emily", "Aubert", "St_Aubert",
                            "Emily_Hotspur", "Miss_Hotspur"],
              "Madame_Montoni": ["Madame_Monotoni", "Madame_Cheron"],
              "Agnes": ["Agnes", "Agnes_Maynard", "Signora_Laurentina"],
              "Count_Montoni": ["Count_Montoni", "Montoni"],
              "Darnford": ["Henry", "Darnford"],
              "George": ["George_Venables", "Venables",
                            "Sir_George", "Captain_Ardworth",
                                "George_Hotspur", "Captain_George", "Cousin_George",
                                    "Lord_George", "George_de_Bruce_Carruthers", "George_Carruthers"],
              "Emma":["Emma", "Emma_Woodhouse","Miss_Woodhouse",
                       		 "Emma_Vine", "Miss_Vine"],
	      "Henry_Woodhouse": ["Henry_Woodhouse", "Mr_Woodhouse"],
              "Jane": ["Jane", "Jane_Fairfax", "Miss_Fairfax", "Fairfax", "Mrs_Fairfax",
                        		"Jane_Eyre", "Miss_Eyre", "Jane_Elliott", "Miss_Jane"],
              "Harriet": ["Harriet", "Harriet_Smith"],
              "Weston": ["Weston", "Mr_Weston"],
              "Knightley": ["Knightley", "Mr_Knightley"],
              "Elton": ["Mr_Elton", "Elton"],
              "Adèle": ["Adèle", "Adèle_Varnes"],
              "Blanche": ["Blanche", "Blanche_Ingram", "Miss_Ingram"],
              "Bertha": ["Mrs_Rochester", "Bertha", "Bertha_Mason"],
              "Mrs_Reed": ["Mrs_Reed", "Aunt_Reed"],
              "Diana": ["Diana_Rivers", "Diana"],
              "Mary": ["Mary_Rivers", "Mary", "Mary_Garth", "Miss_Garth", "Mary_Clayton"],
              "Edward": ["Mr_Rochester","Edward", "Edward_Rochester", "Edward_Fairfax",
                        "Edward_Clayton"],
              "St_John": ["St_John", "St_John_Rivers", "John_Rivers"],
              "Richard": ["Richard_Mason", "Mr_Mason", "Richard",
                            	"Carstone", "Richard_Carstone", "Mr. Carstone", "Richard",
                                		"Richard_Mutimer", "Mr_Mutimer", "Mutimer", "Richard", "Dick"],
              "Lucretia": ["Lucretia_Clavering", "Miss_Clavering","Lucretia", "Lucretia_Dalibard"],
              "Susan": ["Miss_Mivers", "Susan_Mivers"],
              "Olivier": ["Olivier_Dalibard","Dalibard", "provencal", "Frenchman"],
              "Vincent": ["Vincent_Braddell", "Beck", "Mr_Braddell"],
              "Ada": ["Ada Clare","Ada", "Miss_Clare", "Mrs_Carstone"],
              "Esther": ["Esther","Esther_Summerson","Miss_Summerson"],
              "Charlotte": ["Charlotte_Neckett", "Miss_Neckett"],
              "Leicester": ["Sir_Leicester", "Leicester_Dedlock"],
              "Hawdwen": ["Captain_Hawden", "Nemo", "Hawden"],
              "Laura": ["Laura", "Miss_Fairlie","Laura_Fairlie", "Lady_Glyde", "Laura_Edmonstone"],
              "Marian": ["Marian_Halcombe", "Marian","Miss_Halcombe", "Halcombe"],
              "Percival": ["Percival_Glyde", "Percival", "Glyde", "Sir_Percival"],
              "Walter": ["Walter", "Walter_Hartright", "Mr_Hartright"],
              "Fosco": ["Count_Fosco", "Fosco", "The_Count"],
              "Frederick": ["Frederick_Fairlie", "Mr_Fairlie", "Laura’s_uncle", "Uncle", "Mr Frederick",
                            "Frederick_Lovel", "Frederick", "Frederick Tilney", "Mr_Frederick_Tilney"],
              "Josephine": ["Josephine_Murray", "Countess_Love", "Lady_Love", "Mrs_Murray"],
              "Daniel": ["Daniel", "Daniel_Thwaite", "Daniel_Dabbs"],
              "Rachel": ["Rachel_Verinder","Rachel","Miss_Rachel","Miss_Verinder"],
              "Drusila": ["Drusila_Clack", "Miss_Clack", "Drusila"],
              "Franklin": ["Franklin_Blake", "Mr_Blake"],
              "Godfrey": ["Godfrey_Ablewhite", "Mr_Godfrey","Godfrey"],
              "Sergeant_Cuff": ["Sergeant_Cuff", "Sergeant"],
              "Dorothea": ["Dorothea_Brooke", "Dorothea", "Miss_Brooke"],
              "Rosamond": ["Rosamond_Vincy", "Miss_Vincy","Rosamond"],
	            "Casaubon": ["Casaubon", "Mr_Casaubon"],
	            "Bulstrode": ["Bulstrode", "Mr_Bulstrode"],
	            "James": ["James", "Sir_James", "James_Morland", "Mr_Morland"],
	            "Farebrother": ["Farebrother", "Mr_Farebrother"],
	            "Garth": ["Garth", "Mr_Garth", "Caleb"],
	            "Vincy": ["Fred", "Fred_Vincy", "Vincy"],
                "Will": ["Will_Ladislow", "Ladislow"],
                "Joshua": ["Joshua_Rigg", "Mr_Rigg"],
                "Thomas": ["Thomas_Eowling", "Thomas_Bowling", "Mr_Bowling", "Tom_Bowling",
                            	"Thomas", "Thomas_Underwood", "Sir_Thomas"],
              "Hugh": ["Hugh_Strap", "Strap", "Sir_Hugh", "Sir_Hugh_Tyrold", "Sir_Tyrold", "Hugh"],
              "Sophia": ["Sophia_Weston", "Sophia"],
              "Tom": ["Tom_Jones", "Tom", "Mr_Jones", "Jones",
                        "Tom_Brice", ],
	            "Allworthy": ["Allworthy", "Mr_Allworthy"],
              "Partridge": ["Partridge", "Mr_Partridge"],
	        "Deborah": ["Deborah", "Mrs_Deborah"],
              "Camilla": ["Camilla", "Camilla_Spondi", "Camilla_Tyrold", "Miss_Tyrold", "Signorina_Spondi"],
              "Maud": ["Maud", "Maud_Ruthyn", "Miss_Ruthyn"],
              "Lavinia": ["Lavinia", "Miss_Lavinia"],
              "Isabella": ["Lady_Isabella", "Isabella",
                            	"Isabella_Linton", "Isabella_Thorpe", "Miss_Thorpe",
                                    "Isabella_Somerive"],
	        "Selina": ["Selina", "Selina_Somerive"],
	        "Eugenia": ["Eugenia", "Eugenia_Tyrold", "Miss_Eugenia"],
                "Indiana": ["Indiana_Lynmere", "Miss_Lynmere", "Miss_Indiana"],
                "Ann-Jane-Eliza": ["Ann-Jane-Eliza_Hollybourn", "Miss_Hollybourn"],
              "Eliza": ["Miss_Wildmam", "Eliza", "Eliza_Wildman"],
              "Biddy": ["Biddy_Slash'em", "Biddy", "Mrs_Slash'em"],
              "Gabriel": ["Gabriel_Outcast", "Gabriel"],
              "Woodford": ["Mr_Woodford", "Woodford"],
            "Grace": ["Grace_Nugent","Miss_Nugent","Grace", "Mrs_Rayland", "Mrs_Grace",	"Grace_Rayland"],
              "Clonbrony": ["Lord_Clonbrony", "Lord_Clombrony", "Clonbrony", "Clombrony"],
              "Colambre": ["Lord_Colambre", "Colambre"],
              "Nicholas": ["Nicholas_Gerraghty", "Gerraghty", "Mr_Gerraghty", "Nicholas",
                            "Nicholas_Gwigg", "Alphonso_Bellamy"],
              "Catherine": ["Catherine","Catherine_Morland","Miss_Morland"],
              "Pip": ["Pip", "Pirrip", "Handel"],
              "Abel": ["Abel_Magwitch", "Magwitch"],
              "Herbert": ["Herbert_Pocket", "Pocket"],
              "Jaggers": ["Jaggers", "Mr_Jaggers"],
              "Wemnick": ["Wemnick", "Mr_Wemnick"],
              "Patience": ["Patience_Underwood","Patience","Patty"],
              "Lizzie": ["Lizzie_Greystock", "Lady_Eustace", "Lizzie"],
              "Glencora": ["Lady_Glencora", "Lady_Glencora_Palliser", "Lady_Palliser"],
              "Lucinda": ["Lucinda_Roanoke", "Lucinda"],
              "Florian": ["Sir_Florian", "Sir_Florian_Eustace", "Florian_Eustace"],
              "Griffin": ["Sir_Griffin", "Sir_Griffin_Tewett", "Griffin_Tewett"],
              "Adela": ["Adela_Waltham", "Miss_Waltham", "Adela", "Adela_Mutimer", "Mrs_Mutimer"],
              "Stella": ["Stella_Westlake","Miss_Westlake"],
              "Hubert": ["Hubert_Eldon", "Eldon", "Hubert", "Mr_Eldon"],
	            "Skimpole":["Skimpole", "Mr_Skimpole"],
             "Chadband":["Chadband," "Mr_Chadband"],
	        "Perry": ["Perry", "Mr_Perry"],
            "Mrs_Allen": ["Allen", "Mrs_Allen"],
            ";Mrs_Tilney": ["Tilney", "Mrs_Tilney"],
	"Miles": ["Miles", "Sir_Miles"],
	"Havisham": ["Havisham", "Miss_Havisham"],
	"Boffin": ["Boffin", "Mr_Boffin"],
	"Lammle": ["Lammle", "Mr_Lammle"],
	"Wilfer": ["Wilfer", "Mr_Wilfer"],
	"Wegg": ["Wegg", "Mr_Wegg", "Silas"],
	"Veneering": ["Veneering", "Mrs_Veneering"],
        "Roderick": ["Roderick", "Roderick_Random", "Rory", "Rory_Random"]
}


dirs = []
for folder in os.listdir('corpus'):
    if folder.endswith('-chapters'):
        dirs.append('corpus/' + folder + '/')


for path in tqdm(dirs):
    final_edge_tuples = []
    with open(path + 'actor-benefactor-edge-list.csv', 'r') as csvfile:
        srlreader = csv.reader(csvfile, delimiter=',')
        for row in srlreader:
            final_edge_tuples.append(row)

    name1 = [pair[0] for pair in final_edge_tuples]
    name2 = [pair[1] for pair in final_edge_tuples]

    for idx,character in enumerate(name1):
        for name, aliases in name_dict.items():
            if character in aliases:
                name1[idx] = name
            else:
                pass

    for idx,character in enumerate(name2):
        for name, aliases in name_dict.items():
            if character in aliases:
                name2[idx] = name
            else:
                pass

    corrected = list(zip(name1, name2))

    with open(path + 'CORRECTED.actor-benefactor-edge-list.csv', 'w') as write_file:
        csvwriter = csv.writer(write_file, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        for t in corrected:
            csvwriter.writerow(t)
