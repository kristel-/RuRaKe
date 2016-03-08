# Overview

RuRaKe is a project that aims to add geographical information to the existing corpus of Estonian dialects (CED) and to digitize dialect maps of the „Väike Eesti murdeatlas” („Small atlas of Estonian dialects) by Andrus Saareste.


# Corpus correction documentation
The subfolder *Corpus-correction-documentation* contains an attribute tabel and a log file. *CED-header-info* includes entries of CED that have geographical information (the longitude and latitude of informants residence) already attached to them. *CED-header-geoinfo-correction- log* records the changes made to the CED attribute table.

# Small dialect atlas
The subfolder *Saareste-vaike-murdeatlas* contains the documentation and a few examples of the process of digitizing the „Väike Eesti murdeatlas” (VMA). Atlase-geoinfo contains among others the attribute table that was the basis for creating the base layer Shapefile *kogumispunktid_utf8_97*. The Shapefile includes all the data collection points of VMA joined with the attribute table of nowadays settlements and parish information. The subfolder also contains the log file (*Saareste-VMA- logifail*) and the data insertion scheme (*Saareste-VMA-sisestusskeem*). The examples of the digitized maps as well as the base layer Shapefile are at the moment presented as jpeg-s.

# Scripts
The third subfolder contains Python scripts for CED data manipulation and collection as well as the scripts for (semi)automatic task to correct CED mistakes and insconsistencies. Some example data is added to test the scripts.