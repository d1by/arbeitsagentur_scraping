# slurm_scraping
<details>
  <summary> Problem Statement </summary> 
  
###### Translated from German
The Bundesagentur's (BA) offer is the best structured: https://www.arbeitsagentur.de/kursnet

Here, a distinction is essentially made between initial and continuing training, then between different categories and then subject areas, which are derived from the DKZ (= the BA-internal, but publicly available classification scheme. Unfortunately not a real taxonomy).

If you look at an advertisement here, you can see the structure well: content, duration, information on type of education, form of instruction, degree, provider, access information, ...
This raises the following questions: 
- How can free text information on access be extracted and identified as entities in a taxonomy/ontology? Nice examples are the almost infinite number of school degrees or "work experience in a commercial profession"...
- How can degree titles be mapped to the KldB ("Klassifikation der Berufe" - classification of occupations) or state-recognised continuing education degrees? Can one derive an overview of non-state-regulated continuing education?
- Classification by economic sector.
- Extraction of competences, tools, ...
- Identification of providers.

However, most continuing education portals look more like this:
https://weiterbildungsportal.rlp.de

Steps to reproduce: 
1.	Navigate to the website, https://www.arbeitsagentur.de/kursnet. The website opens in german, use translate the translationtand the translation
2.	Click on ‘Weiterbildungsangebote’/’Oppurtunities 

![image](https://github.com/d1by/slurm_scraping/assets/108338649/82259ed2-fae2-4d5f-96bc-6b30850771da)

3.	Search for any course, for demo purpose I am searching for ‘Computer Science’

![image](https://github.com/d1by/slurm_scraping/assets/108338649/b5f44f8e-590b-43f8-ad86-a6c21f7da6b5)

 
4.	You could see the search results with content ,duration etc. The detailed description can be obtained by clicking on the link ‘Go to details page’


If you study several ads here, you will see that essentially only the ad text and the provider are structured here.

It would be great if you could have a look at these two.

As first step I need you to extract the structure of these advertisement from these two websites. 
Points to remember: 
https://www.arbeitsagentur.de/kursnet this is correct URL, I case if you click or navigate to home page the url changes to ‘https://www.arbeitsagentur.de’ that’s not correct.


</details>
