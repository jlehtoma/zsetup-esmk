### Analysis variants

Variants 1-13 done with 6 soil fertility classes. **These are legacy version and not included in this repo**. They are
kept here to retain the original variant numbering scheme.

```
1 ABF
2 ABF + penalty
3 ABF + penalty + weights
4 ABF + penalty + weights + connectivity matrix
5 CAZ + penalty + weights + connectivity matrix
6 ABF + penalty + weights + connectivity matrix + edge correction
7 ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity)
8 ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
9 ABF + penalty + weights + connectivity matrix + edge correction + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
10 ABF + penalty + weights + connectivity matrix
11 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity)
12 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
13 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
```

Variants 14-20 done with 5 soil fertility classes. Groups based on tree spp groups.
        
```
14 ABF
15 ABF + penalty
16 ABF + penalty + weights
17 ABF + penalty + weights + connectivity matrix
18 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity)
19 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)
20 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas (interaction connectivity)  + protected areas masked in
```

Variants 21-27 are the same as 14-20, but with different groups (grouping based on soil feritility classes).
     
```
28 ABF + penalty + weights + connectivity matrix + woodland key habitats (interaction connectivity) + protected areas masked in
```

Variant `29` is the same as `28`, but with different groups (grouping based on soil feritility classes).

----
### Explanation for Zonation-related terms used 
For more detailed explanation and examples, see the [manual](http://www.helsinki.fi/bioscience/consplan/software/Zonation/ZONATION_v3.1_Manual_120416.pdf)

Abbreviation in brackets (e.g. `[cmat]`) are the same abbreviations used in file/folder names in this repo.

`ABF/CAZ [abf/caz]` = Zonation cell removal rule (Additive benefit function / Core-area Zonation)   
`penalty [pe]` = Penalty imposed on areas that have seen active forestry operation lately. Implemented as a condition layer.  
`weights [w]` = Weighting scheme for analysis features in use  
`connectivity matrix [cmat]` =  
`edge correction [ec]` =  
`protected areas (interaction connectivity) [cres]` =  
`protected areas masked in [mask]` =  
`woodland key habitats (interaction connectivity) [cmete]` =  
