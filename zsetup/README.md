### Analysis variants

All variants use the additive benefit function (ABF) cell removal rule.

Variants increase in data and analysis feature complexity used. 

01_msnfi_w_pe
02_msnfi_w_pe_cmat
03_msnfi_sfc_w_pe
04_msnfi_sfc_w_pe_cmat
05_all_sfc_w_pe
06_all_sfc_w_pe_cmat

----

### Explanation for Zonation-related terms used 

For more detailed explanation and examples, see the [manual](http://www.helsinki.fi/bioscience/consplan/software/Zonation/ZONATION_v3.1_Manual_120416.pdf)

Abbreviation in brackets (e.g. `[cmat]`) are the same abbreviations used in file/folder names in this repo.

`msnfi` = Variant uses data from multi-source National Forest Inventory (MSNFI) only.
`sfc` = Data (index features) are further divided into separate rasters using soil fertility classification.
`all` = 
`penalty [pe]` = Penalty imposed on areas that have seen active forestry operation lately. Implemented as a condition layer.  
`weights [w]` = Weighting scheme for analysis features in use  
`connectivity matrix [cmat]` =  Connectivity between different forest types is accounted for. Implemented using Zonation's matrix connectivity feature.