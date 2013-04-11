## Zonation conservation prioritization analysis for the regional forest center of Etelä-Savo (FIN)

* Corresponding author: Joona Lehtomäki <joona.lehtomaki@gmail.com>
* License: [Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
](http://creativecommons.org/licenses/by-sa/3.0/)
* Data used in this particular analysis and the results produced *cannot be shared* because of terms of use 
of the Finnish Forest Centre (data manager). 
* For description of the data used, analysis, and results see [manuscript in preparation](https://github.com/jlehtoma/validityms)

### Analysis variants

Variants 1-13 done with 6 soil fertility classes.

1. ABF
2. ABF + penalty
3. ABF + penalty + weights
4. ABF + penalty + weights + connectivity matrix
5. CAZ + penalty + weights + connectivity matrix 
6. ABF + penalty + weights + connectivity matrix + edge correction
7. ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity)
8. ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
9. ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
10. ABF + penalty + weights + connectivity matrix
11. ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity)
12. ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
13. ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
     
----

Variants 14-20 done with 5 soil fertility classes.
        
14. ABF(5kp)
15. ABF(5kp) + penalty
16. ABF(5kp) + penalty + weights
17. ABF(5kp) + penalty + weights + connectivity matrix
18. ABF(5kp) + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity)
19. ABF(5kp) + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
20. ABF(5kp) + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
        
  ABF/CAZ       = Zonationin kהyttהmה analyysimetodi. Additive Benefit Function suosii alueita, joilla on runsaasti piirteitה, Core Area Zonation puolestaan alueita, joissa on harvinaisia piirteitה
    
  penalty       = Metsהkהsittelyilmoituksiin perustuva sakkorastesti, jolla alennetaan kהsitetlyjen metsהalueiden arvoa

  weights        = analyysiversiossa on weights mukana kaikille piirteille (lצytyy tiedostosta configure.xlsx)
 
  connectivity matrix = kytkeytyvyysmatriisi mukana. Kaikkien piirteiden (n=28, pההpuulaji x kasvupaikka) vהlille on laskettu kytkeytyvyysvasteet (1.0 = tהysin kytkeytynyt, 0.0 = ei ollenkaan kytkeytynyt). 
                  Esimerkiksi jos mlp_lehto ja mlp_lehtomainen vהlinen kytkeyvyys on 1.0, on kyseessה kytkeytyvyyden nהkצkulmasta sama habitaatti. 0.0 taas tarkoittaisi, ettה kyseisessה habitaatissa
                  elהvה lajisto ei esiinny lainkaan toisessa habitaatissa. Arvot lצytyvהt tiedostosta configure.xlsx.
 
  edge correction  = kytketyvyyden kannalta habitaatit voidaan jakaa haitallisiin (estהה lajiston liikkumista) sekה haitattomaan habitaattiin (ei haittaa mutta ei edistהkההn). Tהssה analyysivariantissa
                  vesistצt sekה metsהkeskuksen rajojen ulkopuolinen alue on laskettu kytkeytyvyydelle haitattomaksi habitaatiksi. Nהin ollen vesistצjen rannat sekה lהhellה MK:n reunaa olevat alueet
                  eivהt saa sakkoa ainakaan kytkeytyvyyden takia. 

  suojelualueiden lהheisyys = interaktio (vuorovaikutus) suojelualueilla sekה niiden ulkopuolella olevan habitaatin vהlillה. Toisin sanoen kytkeytyvyys suojelualueilta ulos pהin. Vaikutuksen voimakkuus
                  riippuu siitה, millaista habitaattia suojelualueella on, eli pelkkה suojelualue sellaisenaan ei riitה voimakkaan vaikutuksen aiheuttajaksi. Vaikutuksen voimakkuuden mההrittelyssה 
                  on kהytetty lajiston keskimההrהistה 5 km:n dispersaalikykyה.
 
  protected areas masked in = Zonation on pakotettu kהsittelemההn ensin kaikki muut alueet ja vasta viimeiseksi suojelualueet. Ts. huippuprioriteetit osuvat varmasti suojelualueille. 
                  Analyysivariantin merkitys on tarkastella suojelualueiden laatua suhteessa muuhun maisemaan, mutta myצs mikה olisi optimaalinen tapaa laajentaa suojelualueita.
 
  mete-kohteiden lהheisyys = samanlainen vuorovaikutus kuin suojelualueisiin, mutta tהllה kertaa METE-kohteisiin. Vaikutuksen etהisyys on lyhyempi (500 m) kuin suojelualueiden tapauksessa.
        
* Tiedoston nimi:
        9_60_abf_pe_w_cmat_ec_cres_cmete_mask_spp.dat
        | |  |   |  | |    |  |    |     |    |_lajitietoja mukana
        | |  |   |  | |    |  |    |     |_maski kהytצssה
        | |  |   |  | |    |  |    |_"connectivity mete", kytkeytyvyys mete-kohteisiin
        | |  |   |  | |    |  |_"connectivity reserves", kytkeytyvyys suojelualueisiin
        | |  |   |  | |    |_"edge correction" edge correction      
        | |  |   |  | |_"connectivity matrix", kytkeytyvyys metsהtyyppien vהlillה
        | |  |   |  |_weightsukset kהytצssה
        | |  |   |_sakkorasteri mukana
        | |  |_kהytetty Z-metodi, voi olla caz (core area zonation) tai abf (additive benefit function)
        | |_resoluutio
        |_ID numero